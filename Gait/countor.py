import cv2
from PIL import Image
image = cv2.imread('Images/leaf.jpg')
image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(image_gray, 150, 255, cv2.THRESH_BINARY)
Image.fromarray(thresh).show()
# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
# print(contours)
# draw contours on the original image
image_copy = image.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                
image_copy = Image.fromarray(image_copy)
image_copy.show()