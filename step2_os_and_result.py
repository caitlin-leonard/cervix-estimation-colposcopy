
import cv2
import numpy as np

image = cv2.imread('cervix2.png')
clone = image.copy()
os_points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(os_points) < 2:
        os_points.append([x, y])
        cv2.circle(image, (x, y), 4, (0, 0, 255), -1)
        if len(os_points) == 2:
            cv2.line(image, tuple(os_points[0]), tuple(os_points[1]), (0,0,255), 2)
        cv2.imshow('Step 2: Click 2 points on OS - press Q to finish', image)
        print(f"OS point {len(os_points)}: ({x}, {y})")

cv2.imshow('Step 2: Click 2 points on OS - press Q to finish', image)
cv2.setMouseCallback('Step 2: Click 2 points on OS - press Q to finish', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

boundary_points = np.load('boundary_points.npy')
print(f"Loaded {len(boundary_points)} boundary points")

ellipse = cv2.fitEllipse(boundary_points.astype(np.int32))
center, axes, angle = ellipse
major_px = max(axes)
minor_px = min(axes)

if len(os_points) == 2:
    os_px = np.linalg.norm(np.array(os_points[0]) - np.array(os_points[1]))
    px_per_mm = os_px / 4.0
    print(f"OS: {os_px:.1f} px = 4mm")
else:
    px_per_mm = major_px / 35.0
    print("OS not measured - using assumed 35mm (LIMITATION)")

major_mm = major_px / px_per_mm
minor_mm = minor_px / px_per_mm
import math
area_mm2 = math.pi * (major_mm/2) * (minor_mm/2)

print("=" * 50)
print("  CERVIX SIZE RESULT")
print("=" * 50)
print(f"  Major : {major_mm:.1f} mm")
print(f"  Minor : {minor_mm:.1f} mm")
print(f"  Area  : {area_mm2:.1f} mm2")
print(f"  Range : 25-40mm normal (IARC 2024)")
print("=" * 50)

result = clone.copy()
for pt in boundary_points:
    cv2.circle(result, tuple(pt.astype(int)), 4, (0,255,0), -1)
cv2.ellipse(result, ellipse, (255,50,50), 2)
cv2.drawMarker(result, (int(center[0]),int(center[1])),
               (0,255,255), cv2.MARKER_CROSS, 15, 2)
label = f"Major:{major_mm:.1f}mm Minor:{minor_mm:.1f}mm Area:{area_mm2:.0f}mm2"
cv2.putText(result, label, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
cv2.imwrite('cervix_result.jpg', result)
print("Saved: cervix_result.jpg")
cv2.imshow('RESULT', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
