## Object Detection and Reporting System using YOLO and Text-to-Speech (TTS)



This Python script utilizes the YOLOv3 model for object detection and text-to-speech (TTS) conversion to report the detected objects. The script captures an image from the webcam, detects objects in the image using YOLOv3, determines their location relative to the center of the image, and then reports the detected objects using TTS.

### Requirements

- Python 3.x
- See `requirements.txt` for the required Python packages.
- YOLOv3 model files (`yolov3.weights`, `yolov3.cfg`)
- COCO class names file (`coco.names`)

### Installation

1. Install Python 3.x if you haven't already.
2. Install the required Python packages using pip:

    ```
    pip install -r requirements.txt
    ```

3. Download the YOLOv3 model files (`yolov3.weights`, `yolov3.cfg`) and the COCO class names file (`coco.names`) and place them in the same directory as the script.

### Usage

1. Run the Python script using the command:

    ```
    python detect_main.py
    ```

2. The script will continuously capture images from the webcam, detect objects in the images, and report the detected objects using TTS.
3. Detected objects will be reported as either on the left, right, or center of the image based on their position relative to the center of the image.

### Files

- `object_detection.py`: The main Python script implementing object detection and reporting.
- `yolov3.weights`: Pre-trained weights for the YOLOv3 model.
- `yolov3.cfg`: Configuration file for the YOLOv3 model.
- `coco.names`: List of COCO class names.
- `output.mp3`: Temporary file to save the generated audio.
- `requirements.txt`: Text file listing the required Python packages and their versions.

### Customization

- You can modify the confidence threshold for object detection by changing the value `0.5` in the `detect_objects` function.
- Adjust the waiting time between image captures by changing the value in `time.sleep(10)` at the end of the main loop.

### Notes

- Ensure that your webcam is properly connected and configured before running the script.
- The script assumes a webcam index of `0` for capturing images. Modify the code if your webcam has a different index.

---



for weights file refer to :
https://pjreddie.com/media/files/yolov3.weights
