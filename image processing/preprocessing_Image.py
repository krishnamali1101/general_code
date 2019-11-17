import cv2
import numpy as np


# call---> flow(Any image path)

def blur_image(img):
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    # Apply blur to smooth out the edges
    img = cv2.GaussianBlur(img, (5, 5), 0)
    #cv2.imwrite('form4.png',img)
    return img


def increase_contrast(img):
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imghsv[:, :, 2] = [[max(pixel - 19, 0) if pixel < 190 else min(pixel + 25, 255) for pixel in row] for row in
                       imghsv[:, :, 2]]

    # imghsv[:,:,2] = [[max(pixel - 25, 0) if pixel < 190 else min(pixel + 25, 255) for pixel in row] for row in imghsv[:,:,2]]
    im2 = cv2.cvtColor(imghsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite('inc_contrast.png', img)
    return im2



def flow(img_path):
    img = cv2.imread(img_path)
    contrast = increase_contrast(img)
    result = contrast.copy()
    gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('grayscale_img.png', gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imwrite('thresholded_img.png', thresh)

    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=3)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

    # Remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255, 255, 255), 7)

    cv2.imwrite('removed_lines.png', result)
    blurring_img1 = blur_image(result)
    cv2.imwrite('blurring.png',blurring_img1)

flow('sf1.png')