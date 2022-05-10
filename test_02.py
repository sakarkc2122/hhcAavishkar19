
### error code:

### maybe only for linux system

from PIL import Image
from pytesseract import image_to_string

img = Image.open('C:\\Users\\User\\Desktop\\name.png')

text = image_to_string(img, lang='eng  ')

print(text)