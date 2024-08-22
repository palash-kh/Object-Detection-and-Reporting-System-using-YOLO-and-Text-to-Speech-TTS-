import cv2
import numpy as np
import os
import time
from gtts import gTTS

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

def generate_audio(text):
    tts = gTTS(text=text, lang='en', tld='co.uk', slow=False, xargs=['-ss', '0', '-ac', '1', '-ar', '22050'])
    tts.save("output.wav")
    os.system("aplay output.wav")
    
def detect_and_report(detected_objects):
    print("Detected objects:", detected_objects)

    if detected_objects:
        width = detected_objects[0][-1]  # Assuming width is the last element of each detected object
    else:
        print("No objects detected.")
        return

    image_center = width // 2

    for obj in detected_objects:
        class_name, x, y, w, h, confidence, _ = obj

        object_center = x + (w // 2)

        if object_center < image_center - (width // 4):
            location_text = "left"
        elif object_center > image_center + (width // 4):
            location_text = "right"
        else:
            location_text = "center"

        generate_audio("A {} is detected in the {} side.".format(class_name, location_text))

def capture_detect_and_report():
    os.system("libcamera-still -o captured_photo.jpg")

    # Detect objects
    detected_objects = detect_objects("captured_photo.jpg")

    # Report detected objects
    detect_and_report(detected_objects)

    # Delete captured photo
    os.remove("captured_photo.jpg")

if __name__ == "__main__":
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    while True:
        capture_detect_and_report()
        time.sleep(10)  # Wait for 10 seconds before capturing the next photo
