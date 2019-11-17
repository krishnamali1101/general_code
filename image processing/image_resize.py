# Image resize code

import PIL
from PIL import Image
import glob
import os
import shutil

inDir = "/Users/gopalmali/Documents/pics/WhatsApp Zip 2019-10-15 at 3.02.07 PM/green/*.*"
outDir = "/Users/gopalmali/Documents/pics/WhatsApp Zip 2019-10-15 at 3.02.07 PM/green/output/"


#del outDir if exists
if outDir and os.path.exists(outDir):
    shutil.rmtree(outDir)

basewidth = 450

files = glob.glob(inDir)

os.makedirs(outDir)
for file in files:
    img = Image.open(file)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

    file_out = outDir+os.path.basename(file)

    img.save(file_out)
