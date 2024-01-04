import cv2

# Load the image
image = cv2.imread('./cheques/1.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Edge detection
edged = cv2.Canny(blurred, 30, 150)

# Dilation
dilated = cv2.dilate(edged, None, iterations=2)

# Find contours
contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize micr_strip variable
micr_strip = None

# Filter contours based on aspect ratio, location and area
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / float(h)
    # print(aspect_ratio)
    if aspect_ratio > 5 and y > image.shape[0] * 0.8 and w > 0 and h > 0:  # add check for w and h
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        micr_strip = image[y:y+h, x:x+w]
        print(micr_strip)

# If micr_strip was found and has valid size, display it
if micr_strip is not None and micr_strip.shape[0] > 0 and micr_strip.shape[1] > 0:
    cv2.imshow("MICR strip", micr_strip)
    cv2.waitKey(0)
else:
    print("No valid MICR strip found")