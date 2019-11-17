import cv2
import pytesseract


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
    # img = cv2.imread(imPath, cv2.IMREAD_COLOR)

    # Run tesseract OCR on image
    text = pytesseract.image_to_string(img, config=config)

    # return recognized text
    return text
