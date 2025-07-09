import cv2
import numpy as np

# Path to the image you want to draw on (use red or green image as background)
image_path = r"C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\IF-images\WebImages\redMem.png"
output_path = r"C:\Users\Ifeanyi Enekwa\Web dev projects\ciliasync\IF-images\WebImages\manual_mask.png"

drawing = False
thickness = 2
points = []

def draw(event, x, y, flags, param):
    global drawing, points
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points.append((x, y))
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# Load base image to draw on
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"Could not load {image_path}")

# Create blank canvas for mask (black background)
mask = np.zeros(img.shape[:2], dtype=np.uint8)

cv2.namedWindow("Draw Membrane")
cv2.setMouseCallback("Draw Membrane", draw)

while True:
    temp = img.copy()
    for i in range(1, len(points)):
        cv2.line(temp, points[i - 1], points[i], (0, 255, 0), thickness)
        cv2.line(mask, points[i - 1], points[i], 255, thickness)
    cv2.imshow("Draw Membrane", temp)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        points = []
        mask[:] = 0
    elif key == ord('s'):
        cv2.imwrite(output_path, mask)
        print(f"Mask saved to: {output_path}")
        break
    elif key == 27:  # ESC
        break

cv2.destroyAllWindows()
