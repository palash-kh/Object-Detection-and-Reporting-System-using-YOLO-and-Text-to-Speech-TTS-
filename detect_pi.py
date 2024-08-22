import cv2
import numpy as np
import os
import time
from gtts import gTTS

# Load YOLOv3 model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Perform object detection on the image
def detect_objects(image_path):
    img = cv2.imread(image_path)
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())
    detected_objects = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                detected_objects.append((classes[class_id], x, y, w, h, confidence, width))
    return detected_objects

# Generate audio from text
def generate_audio(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")

# Detect and report
def detect_and_report(detected_objects):
    print("Detected objects:", detected_objects)

    # Get the width of the image
    if detected_objects:
        width = detected_objects[0][-1]  # Assuming width is the last element of each detected object
    else:
        print("No objects detected.")
        return

    # Calculate the center of the image
    image_center = width // 2

    # Determine the location of the objects
    for obj in detected_objects:
        class_name, x, y, w, h, confidence, _ = obj

        # Calculate the center of the detected object
        object_center = x + (w // 2)

        # Determine the location based on the object's center relative to the image center
        if object_center < image_center - (width // 4):
            location_text = "left"
        elif object_center > image_center + (width // 4):
            location_text = "right"
        else:
            location_text = "center"

        # Generate audio
        generate_audio("A {} is detected in the {} side.".format(class_name, location_text))

def capture_detect_and_report():
    # Capture photo
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't capture photo")
        return
    cv2.imwrite("captured_photo.jpg", frame)
    cap.release()

    # Detect objects
    detected_objects = detect_objects("captured_photo.jpg")

    # Report detected objects
    detect_and_report(detected_objects)

    # Delete captured photo
    os.remove("captured_photo.jpg")

# Main loop
while True:
    capture_detect_and_report()
    time.sleep(10)  #Wait for 10 seconds before capturing the next photos