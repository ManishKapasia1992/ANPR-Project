# Import the needed libraries
import cv2
import pytesseract
import imutils
pytesseract.pytesseract.tesseract_cmd  = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = cv2.imread(r'C:\Users\admin\Desktop\C.jpg')

# image = cv2.resize(img, (750, 640))
# image = imutils.resize(img, width=800, height=200)

# Convert image to gray image
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray_image", gray_img)
cv2.waitKey(0)

# Now we will reduce the noise from the image and make it smooth
gray_img = cv2.bilateralFilter(gray_img, 11, 17, 17)
# # cv2.namedWindow("Smoother Image")
cv2.imshow("Smoother Image", gray_img)
cv2.waitKey(0)

# So now we will find the edges of images
edged = cv2.Canny(gray_img, 170, 200)
cv2.imshow("Canny edge", edged)
cv2.waitKey(0)

# Now we will find the contour based on the images
cntrs, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

image1 = image.copy()
cv2.drawContours(image1, cntrs, -1, (0, 255, 0), 3)
cv2.imshow("Canny after contouring", image1)
cv2.waitKey(0)

# Now find the contours for number plate
cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:30]
NumberPlateCount = None
#
image2 = image.copy()
cv2.drawContours(image2, cntrs, -1, (0, 255, 0), 3)
cv2.imshow("Top 30 Contours", image2)
cv2.waitKey(0)
#
# # Now we will run a loop on contours to find the best possible contour we are expecting
count = 0
name = 1
#
for i in cntrs:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.01*perimeter, True)
    if len(approx) == 4:
        NumberPlateCount = approx
        x, y, w, h = cv2.boundingRect(i)
        crp_img = image[y:y+h, x:x+w]
        cv2.imwrite(str(name)+ '.png', crp_img)
        name +=1
#
        break

# now draw contour in our main image that we have identified as a number plate
cv2.drawContours(image, [NumberPlateCount], -1, (0, 255, 0), 3)
cv2.imshow("Final Image", image)
cv2.waitKey(0)

# # Now we will crop only the part of number plate
crop_img_loc = '1.png'
cv2.imshow("Cropped Image", cv2.imread(crop_img_loc))
cv2.waitKey(0)

# Further remove noise from the image
# crop_img = cv2.imread(crop_img_loc)
# crop_img = cv2.bilateralFilter(crop_img, 11, 17, 17)
# cv2.imshow("Final Image", crop_img)
# cv2.waitKey(0)

text = pytesseract.image_to_string(crop_img_loc)
print("Number is: ", text)
# cv2.waitKey(0)
