from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
# ml
from flask import Flask, render_template, Response
import torch
import numpy as np
import cv2
import time
from threading import Thread, Event
from queue import Queue
# from playsound import playsound
from pygame import mixer
from threading import Thread, Event


app = Flask(__name__)
CORS(app,)


# Configure the Flask app to use MongoDB Atlas
app.config['MONGO_URI'] = 'mongodb+srv://balasravatsal:vqzafUykYGO4sv3H@cluster0.gh4ppln.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database('safety_first')
owner_db = db.owners
driver_db = db.drivers


# Route for adding a driver
@app.route('/api/drivers', methods=['POST'])
def add_driver():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        # Insert the new driver into the 'drivers' collection
        result = driver_db.insert_one(data)
        # Return the ID of the newly added driver
        return jsonify({'message': 'Driver added successfully', 'driver_id': str(result.inserted_id)}), 201
    except Exception as e:
        print(f"Error adding driver: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# -------------------------------------------------------------------------------------------

# Route for getting all drivers
@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    try:
        # Call the find method of the collection object to retrieve all documents from the collection
        driver_list = list(driver_db.find())
        # Serialize ObjectId to string using json_util
        driver_json = json_util.dumps(driver_list)
        # Return the serialized JSON
        return driver_json, 200
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Route for getting all owners
@app.route('/api/owners', methods=['GET'])
def get_owners():
    try:
        # Call the find method of the collection object to retrieve all documents from the collection
        owners_list = list(owner_db.find())
        # Serialize ObjectId to string using json_util
        owners_json = json_util.dumps(owners_list)
        # Return the serialized JSON
        return owners_json, 200
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


# -------------------------------------------------------------------------------------------
# Route for adding an owner
@app.route('/api/owners', methods=['POST'])
def add_owner():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Insert the new owner into the 'owners' collection
        result = owner_db.insert_one(data)

        # Return the ID of the newly added owner
        return jsonify({'message': 'Owner added successfully', 'owner_id': str(result.inserted_id)}), 201
    except Exception as e:
        print(f"Error adding owner: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


# -------------------------------------------------------------------------------------------

# Starting the mixer
mixer.init()

# Loading the song
mixer.music.load("beep-warning-6387.mp3")

# Setting the volume
mixer.music.set_volume(0.7)

# Start playing the song

app = Flask(__name__)
model = torch.hub.load('ultralytics/yolov5', 'custom', path="D:/SIH/auHack/auHack/server/mlModel/yolov5/runs/train/exp7/weights/last.pt", force_reload=True)
cap = None  # Initialize the camera object
is_on = Event()  # Event to signal start of detection thread
is_paused = Event()  # Event to signal pause/resume of detection thread
no_of_mins_drowsy = 0
frame_queue = Queue()

def initialize_camera():
    global cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False
    return True

def release_camera():
    global cap
    if cap is not None:
        cap.release()

def detect_drowsiness():
    global is_on, is_paused, no_of_mins_drowsy, cap
    trip_start_time = time.localtime()
    prev_time = time.localtime()
    no_sleep = 0

    if not initialize_camera():
        is_on.clear()
        return

    try:
        while is_on.is_set():
            if not is_paused.is_set():
                ret, frame = cap.read()

                if not ret:
                    print("Error reading frame from video capture.")
                    break

                results = model(frame)

                if str(results).__contains__("drowsy"):
                    no_sleep += 1
                    print("detected")
                else:
                    no_sleep -= 1

                rendered_img = np.squeeze(results.render())

                # Encode image as JPEG
                ret, jpeg = cv2.imencode('.jpg', rendered_img)
                frame_bytes = jpeg.tobytes()

                frame_queue.put(frame_bytes)

                if time.localtime().tm_sec - prev_time.tm_sec >= 5:
                    prev_time = time.localtime()
                    if no_sleep > 0:
                        no_of_mins_drowsy += 1
                        mixer.music.play()
                        no_sleep = 0
    finally:
        release_camera()

def generate_frames():
    while is_on.is_set():
        frame_bytes = frame_queue.get()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# -------------------------------------------------------------------------------------------

@app.route('/api/driver/journey-time', methods=['POST', 'OPTIONS'])
def addTime():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        call_function_one()
        data = request.get_json()
        print(data)
        return jsonify({'message': 'Success'}), 200
    except Exception as e:
        print(f"errrrrrror: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/api/driver/start-journey', methods=['POST', 'OPTIONS'])
def getTime():
    print("start journey")
    if request.method == 'OPTIONS':
        return '', 200
    try:
        call_function_three()  # Add parentheses to call the function
        data = request.get_json()
        print(data)
        return jsonify({'message': 'Success'}), 200
    except Exception as e:
        print(f"errrrrrror: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/call_function_one')
def call_function_one():
    global is_on, is_paused
    is_on.set()  # Set the event to start the detection thread
    is_paused.clear()  # Ensure the detection thread is not paused
    return "Function One Called!"


# @app.route('/call_function_three')
def call_function_three():
    global is_on, no_of_mins_drowsy
    is_on.clear()
    result = no_of_mins_drowsy

    # Start the detection thread again
    detection_thread = Thread(target=detect_drowsiness)
    detection_thread.start()

    return f"Total seconds drowsy: {result*5}"

if __name__ == '__main__':
    # Start the detection thread after the app is running
    detection_thread = Thread(target=detect_drowsiness)
    detection_thread.start()

    # Run the Flask app on the main thread
    app.run(debug=True, threaded=True)


# if __name__ == '__main__':
#     app.run(debug=True)