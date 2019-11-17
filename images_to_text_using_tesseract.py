# Read images from folder and ocr it


import cv2
import sys
import pytesseract
import os
import shutil


def img_preprocess(imPath, thresh=False, blur=True):
    # load the example image and convert it to grayscale
    image = cv2.imread(imPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # check to see if we should apply thresholding to preprocess the image
    if thresh:
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove noise
    elif blur:
        gray = cv2.medianBlur(gray, 3)

    # write the grayscale image to disk as a temporary file so we can apply OCR to it
    # filename = "{}.png".format(os.getpid())
    # cv2.imwrite(filename, gray)

    return gray


def image_to_text(imPath, lang='eng', oem=1, psm=3):
    # Uncomment the line below to provide path to tesseract manually
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'

    # Define config parameters.
    # '-l eng'  for using the English language
    # '--oem 1' for using LSTM OCR Engine
    # https://github.com/tesseract-ocr/tesseract/wiki/ImproveQuality#page-segmentation-method
    # config = ('-l eng --oem 1 --psm 3')
    config = '-l {0} --oem {1} --psm {2}'.format(lang, oem, psm)

    # preprocess the input image
    img = img_preprocess(imPath)

    # Read image from disk (uncomment the line in case of reading image from path)
    img = cv2.imread(imPath, cv2.IMREAD_COLOR)

    # Run tesseract OCR on image
    text = pytesseract.image_to_string(img, config=config)

    # return recognized text
    return text


def run_ocr(inDir, outDir='', supported_ext=['.png', '.jpg', '.jpeg']):
    outDir += "/tesseract_ocr_outout/"

    print("OutDir: ", outDir)
    print('-' * 80)

    # delete existing folder
    if os.path.exists(outDir) and os.path.isdir(outDir):
        shutil.rmtree(outDir)

    # traverse root dir
    for dirName, subdirList, fileList in os.walk(inDir):

        print('Found directory: %s' % dirName)
        for fname in fileList:

            # check for supported extensions
            file_name, ext = os.path.splitext(fname)
            if ext in supported_ext:
                print('\t%s' % file_name)

                relative_path = dirName.replace(inDir, '')
                file_name1 = os.path.split(os.path.dirname(dirName + '/'))

                out_file_path = outDir + '/' + dirName.replace(inDir, '')

                if not os.path.exists(out_file_path):
                    os.makedirs(out_file_path)

                with open(out_file_path + '/' + file_name + '.txt', 'w') as fp:
                    fp.write(image_to_text(dirName + '/' + fname))

        print('-' * 80)


if len(sys.argv) > 2:
    run_ocr(sys.argv[1], sys.argv[2])
elif len(sys.argv) > 1:
    run_ocr(sys.argv[1])
else:
    print("This script excepts 2 arguments inDir & outDir...")
