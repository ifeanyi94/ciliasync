import cv2
import numpy as np
import os

def detect_cilia(image_path, save_path=None):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found or invalid format.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY)

    # Morphology (clean up)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Detect contours (cilia)
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cilia_count = len(contours)

    # Draw bounding boxes
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

    if save_path:
        cv2.imwrite(save_path, image)

    return {
        "cilia_count": cilia_count,
        "output_image": save_path
    }
