import cv2
import numpy as np

def calculate_colocalization(image_path):
    img = cv2.imread(image_path)
    if img is None or img.shape[2] < 2:
        raise ValueError("Image must be RGB with at least 2 channels.")

    red = img[:, :, 2].astype(float)
    green = img[:, :, 1].astype(float)

    # Normalize
    red = (red - np.mean(red)) / np.std(red)
    green = (green - np.mean(green)) / np.std(green)

    # Pearson Correlation
    pearson = np.corrcoef(red.flatten(), green.flatten())[0, 1]

    # Jaccard Index (simple threshold)
    _, red_bin = cv2.threshold(red, 0.5, 1, cv2.THRESH_BINARY)
    _, green_bin = cv2.threshold(green, 0.5, 1, cv2.THRESH_BINARY)

    overlap = np.logical_and(red_bin, green_bin).sum()
    union = np.logical_or(red_bin, green_bin).sum()

    jaccard = overlap / union if union > 0 else 0

    percent_overlap = 100 * overlap / (red_bin.sum() + 1e-5)

    

    return {
        "pearson_correlation": round(pearson, 3),
        "jaccard_index": round(jaccard, 3),
        "percent_overlap": round(percent_overlap, 2)
    }

def save_overlay(image_path, save_path):
    img = cv2.imread(image_path)

    # Separate channels
    red = img[:, :, 2]
    green = img[:, :, 1]

    # Simple binary threshold to detect "on" pixels
    _, red_bin = cv2.threshold(red, 50, 255, cv2.THRESH_BINARY)
    _, green_bin = cv2.threshold(green, 50, 255, cv2.THRESH_BINARY)

    # Overlap: where both red and green are high
    overlap_mask = cv2.bitwise_and(red_bin, green_bin)

    # Create overlay image
    overlay = img.copy()
    
    # Set overlap areas to yellow [B=0, G=255, R=255]
    overlay[overlap_mask > 0] = [0, 255, 255]  # Yellow

    cv2.imwrite(save_path, overlay)
