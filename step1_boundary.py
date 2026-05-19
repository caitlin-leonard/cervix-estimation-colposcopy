import cv2
import numpy as np

image = cv2.imread('cervix2.png')
clone = image.copy()
points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        cv2.circle(image, (x, y), 4, (0, 255, 0), -1)
        cv2.putText(image, str(len(points)), (x+5, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        cv2.imshow('Step 1: Click cervix boundary - press Q to finish', image)
        print(f"Point {len(points)}: ({x}, {y})")

cv2.imshow('Step 1: Click cervix boundary - press Q to finish', image)
cv2.setMouseCallback('Step 1: Click cervix boundary - press Q to finish', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

np.save('boundary_points.npy', np.array(points))
print(f"Saved {len(points)} points to boundary_points.npy")