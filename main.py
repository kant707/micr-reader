import pytesseract
from PIL import Image
import requests
from io import BytesIO
import cv2
import numpy as np

# !ls -alrt /usr/bin/tesseract
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.1_1/bin/tesseract'

image = Image.open('./cheques/micr_1.jpg')
# print(pytesseract.image_to_string(image, lang='eng'))

# cp mcr.traineddata /usr/share/tesseract-ocr/4.00/tessdata/

check_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
# micr_img = check_img[625:717, 0:1630]
# micr_img = check_img[950:1190, 420:1830]
# Size: 1214w X 146h (x:548, y:942)
# micr_img = check_img[942:1214, 548:1762]
# micr_img = check_img[942:1214, 548:1762]

# micr_img = check_img[0:objWidth,0:objWidth+objHeight]
micr_img = check_img[0:1186,0:1344]
check_img.shape

window_name = 'image'
cv2.imshow(window_name, micr_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# import google.colab.patches
# google.colab.patches.cv2_imshow(micr_img)

tessdata_dir_config = r'--tessdata-dir "/usr/local/Cellar/tesseract-lang/4.1.0/share/tessdata"'
# /usr/local/Cellar/tesseract/5.3.1_1/share/tessdata

print(pytesseract.image_to_string(micr_img, lang='mcr', config=tessdata_dir_config))

# https://i0.wp.com/unitedrudrafoundation.com/wp-content/uploads/2019/02/personal_check_single_preprinted_blank.jpg