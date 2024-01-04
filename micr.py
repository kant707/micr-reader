import cv2
import numpy as np
import tensorflow as tf

def load_model(model_path):
    # Load the saved model
    model = tf.saved_model.load(model_path)
    return model

def detect_micr_strip(image, model):
    # Preprocess the image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_expanded = np.expand_dims(image_rgb, axis=0)

    # Run object detection
    detections = model(image_expanded)

    # Convert detection results to numpy arrays
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # Get the class IDs and scores
    class_ids = detections['detection_classes'].astype(np.int64)
    scores = detections['detection_scores']

    # Find the MICR strip region
    micr_strip_index = np.where(class_ids == 1)  # Assuming class ID 1 represents the MICR strip
    micr_strip_score = scores[micr_strip_index]
    micr_strip_box = detections['detection_boxes'][micr_strip_index]

    return micr_strip_box, micr_strip_score

def draw_boxes(image, boxes, scores):
    for box, score in zip(boxes, scores):
        ymin, xmin, ymax, xmax = box
        xmin = int(xmin * image.shape[1])
        xmax = int(xmax * image.shape[1])
        ymin = int(ymin * image.shape[0])
        ymax = int(ymax * image.shape[0])

        # Draw bounding box
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        # Display class and score
        label = 'MICR Strip: {:.2f}'.format(score)
        cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return image

# Load the model
# model_path = 'path/to/your/model_directory/saved_model'
model_path = './model_directory/saved_model/'
model = load_model(model_path)

# Load the image
# image_path = 'path/to/your/check_image.jpg'
image_path = './cheques/2_1.jpg'
image = cv2.imread(image_path)

# Perform MICR strip detection
micr_boxes, micr_scores = detect_micr_strip(image, model)

#
