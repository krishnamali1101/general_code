import glob
import os
import shutil 

import cv2
import numpy as np

from collections import OrderedDict 

# inDir = "../data/forms/*.*"
# out_dir = "../output/"


# call this function to process all the forms and extract lines out of all and save it to out_dir,
# it will call get_lines() function for each form
'''
- input:
    - in_dir: input directory, where all forms are available
    - out_dir: output directory, save all extracted lines at this location
- Output: 
    - if out_dir is provided, it will save all segmented lines at that location
    - else: return a dict <fileName: (marked_image,lines)>
'''
def process_all_forms(in_dir, out_dir=''):
    files = glob.glob(in_dir)
    
    # del outDir if exists
    if out_dir and os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    
    file_markedimage_lines_dict = {}
    for file in files:
        # marked_image, lines = getLines(file)
        file_markedimage_lines_dict[file] = getLines(file) # it returns marked_image & lines
    
    if out_dir:
        for file, (markedImage, lines) in file_markedimage_lines_dict.items():
            # save lines
            file_outdir = out_dir+str(os.path.basename(file)).split('.')[0]
            os.makedirs(file_outdir)

            # save original image with marked areas
            cv2.imwrite(file_outdir+'/marked_areas.png',markedImage)

            # save ROI/ lines
            for i, roi in enumerate(lines):
                cv2.imwrite(file_outdir+'/segment_no_'+str(i)+'.png',roi)
        
    else:
        # return lines
        return file_markedimage_lines_dict
        

# Call this function to extract the lines out of input form, It returns marked_image & list of lines/roi
'''
- input:
    - in_dir: input file/form path(.jpg, .jpeg,.png)
- Output: 
    - returns marked_image & list of lines/roi
'''
def get_lines(file):
    image = cv2.imread(file)

    # grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # binary
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

    # dilation
    kernel = np.ones((5,100), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=2)

    # find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    y_axis_roi_dict = OrderedDict()
    # ctrs are sorted in descending order by default, so traverse the ctrs list in reverse order to get required order
    for i, ctr in enumerate(ctrs[::-1]):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y+h, x:x+w]

        # remove noise/unwanted images based on some hardcoded values of h&w
        if w > 150 and h > 25:
            y_axis_roi_dict[y] = roi

        cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)

    # sort contours, uncomment this line if lines are not sorted
    # y_axis_roi_dict = sorted(y_axis_roi_dict.items(), key=lambda x: x[0])

    # return marked_image & lines/roi
    return image, y_axis_roi_dict.values()


# Call this function to extract and save all segmented lines and return list of lines path
'''
- input:
    - in_dir: input file/form path(.jpg, .jpeg,.png)
    - out_dir: output directory, save all extracted lines at this location
- Output: 
    - returns list of segmented lines path
'''
def save_lines(file, out_dir = "../output/"):

    image = cv2.imread(file)

    # grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # binary
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # dilation
    kernel = np.ones((5, 100), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=2)

    # find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # del outDir if exists
    if out_dir and os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    # create outdir
    file_outdir = out_dir + str(os.path.basename(file)).split('.')[0]
    os.makedirs(file_outdir)

    y_axis_roi_dict = OrderedDict()

    # list of lines path
    lines = []
    # ctrs are sorted in descending order by default, so traverse the ctrs list in reverse order to get required order
    for i, ctr in enumerate(ctrs[::-1]):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y + h, x:x + w]

        # remove noise/unwanted images based on some hardcoded values of h&w
        if w > 200 and h > 40:
            y_axis_roi_dict[y] = roi

        # save ROI/ lines
        path = file_outdir + '/segment_no_' + str(i) + '.png'
        lines.append(path)
        cv2.imwrite(path, roi)

        # mark bounding box on original image
        cv2.rectangle(image, (x, y), (x + w, y + h), (90, 0, 255), 2)

    # save original image with marked areas
    cv2.imwrite(file_outdir + '/marked_areas.png', image)

    # return lines path
    return lines


# process_all_forms(indir,outdir)
# process_all_forms(indir)
