# import cv2
import json
import numpy as np
from flask import Blueprint, request

# from flask_api import status
bp = Blueprint('videotagging', __name__, url_prefix='/tags')

# Define the input video file path and JSON file path
video_path = "input_video.mp4"
json_path = "input_tags.json"

#
# def create_video(txt, timestamp_from, timestamp_to, filename, file_storage_url):
#     # Load the JSON file
#     with open(json_path, "r") as f:
#         tags_dict = json.load(f)
#
#     # Load the YOLOv4 object detection model
#     model = cv2.dnn.readNetFromDarknet("yolov4.cfg", "yolov4.weights")
#     model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
#     model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
#
#     # Define a list of object classes to detect
#     classes = ["person", "car", "bus", "truck", "motorbike"]
#
#     # Create a video capture object
#     cap = cv2.VideoCapture(video_path)
#
#     # Create a window to display the video
#     cv2.namedWindow("Video player")
#
#     # Initialize a dictionary to store the tags currently displayed on the frame
#     current_tags = {}
#
#     while cap.isOpened():
#         # Read a frame from the video
#         ret, frame = cap.read()
#         if ret:
#             # Get the current frame timestamp
#             timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
#
#             # Run object detection on the frame
#             blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)
#             model.setInput(blob)
#             detections = model.forward()
#
#             # Process the detections and display tags for recognized objects
#             for i in range(detections.shape[0]):
#                 class_id = int(detections[i, 1])
#                 if classes[class_id] in tags_dict:
#                     confidence = detections[i, 2]
#                     if confidence > 0.5:
#                         box = detections[i, 3:7] * np.array(
#                             [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
#                         (x, y, w, h) = box.astype("int")
#                         object_name = classes[class_id]
#                         if object_name not in current_tags:
#                             current_tags[object_name] = timestamp
#                         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                         cv2.putText(frame, object_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#
#             # Remove tags for objects that are no longer visible
#             for object_name, display_timestamp in list(current_tags.items()):
#                 if display_timestamp != timestamp or object_name not in tags_dict:
#                     del current_tags[object_name]
#
#             # Display the frame
#             cv2.imshow("Video player", frame)
#
#             # Exit if 'q' key is pressed
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         else:
#             break
#
#     # Release the video capture object and close the window
#     cap.release()
#     cv2.destroyAllWindows()


@bp.route('/create_video', methods=('GET', 'POST'))
def create_video_call():
    # Get the JSON payload from the request
    json_data = request.get_json()

    # Extract the 4 arguments from the JSON payload
    inputs = json_data.get('inputs', {})
    timestamp_from = json_data.get('timestamp_from')
    timestamp_to = json_data.get('timestamp_to')
    file_name = json_data.get('file_name')
    file_storage_url = json_data.get('file_storage_url')

    # Create video clip
    # create_video(inputs, timestamp_from, timestamp_to, file_name, file_storage_url)

    # Save video file
    # video_clip.write_videofile("output.mp4", codec='libx264', audio_codec='aac')
    content = {'FILE STATUS': 'VIDEO SAVED', 'STATUS': 200}
    return content
