import cv2
import numpy as np
import math

# Standard anatomical reference: cervix ~4 cm long and ~3 cm in diameter
# Source basis: NCBI/IARC anatomy references
STANDARD_MAJOR_MM = 40.0
STANDARD_MINOR_MM = 30.0
STANDARD_AREA_MM2 = math.pi * (STANDARD_MAJOR_MM / 2) * (STANDARD_MINOR_MM / 2)

image = cv2.imread('cervix2.png')
if image is None:
    raise FileNotFoundError("cervix.jpg not found.")

clone = image.copy()
h, w = image.shape[:2]
boundary_points = np.load('boundary_points.npy')

# Fit visible cervix ellipse from clicked boundary points
ellipse = cv2.fitEllipse(boundary_points.astype(np.int32))
center_px, axes_px, angle = ellipse
major_px = max(axes_px)
minor_px = min(axes_px)

# Anchor fitted major axis to 40 mm standard cervix length
px_per_mm = major_px / STANDARD_MAJOR_MM
patient_minor_mm = minor_px / px_per_mm
patient_area_mm2 = math.pi * (STANDARD_MAJOR_MM / 2) * (patient_minor_mm / 2)

# Visibility percentage, capped to 100
coverage_pct = (patient_area_mm2 / STANDARD_AREA_MM2) * 100.0
coverage_pct = max(0.0, min(coverage_pct, 100.0))

print("=" * 40)
print(f"Cervix visibility: {coverage_pct:.1f}%")
print("=" * 40)

# Optional result image
result = clone.copy()
os_center = (int(center_px[0]), int(center_px[1]))

# Standard reference ellipse
std_ellipse = (
    (float(os_center[0]), float(os_center[1])),
    (float(STANDARD_MINOR_MM * px_per_mm), float(major_px)),
    angle
)

cv2.ellipse(result, std_ellipse, (255, 120, 0), 2)   # orange = standard reference
cv2.ellipse(result, ellipse, (0, 255, 80), 2)        # green = visible cervix

for pt in boundary_points:
    cv2.circle(result, tuple(pt.astype(int)), 4, (100, 255, 100), -1)

cv2.drawMarker(result, os_center, (0, 255, 255), cv2.MARKER_CROSS, 20, 2)
cv2.putText(result, "OS", (os_center[0] + 8, os_center[1] - 8),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

cv2.rectangle(result, (0, 0), (w, 45), (0, 0, 0), -1)
cv2.putText(result, f"Cervix visibility: {coverage_pct:.1f}%", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

cv2.imwrite('cervix_coverage_result.jpg', result)
print("Saved: cervix_coverage_result.jpg")

cv2.imshow('Cervix Coverage', result)
cv2.waitKey(0)
cv2.destroyAllWindows()