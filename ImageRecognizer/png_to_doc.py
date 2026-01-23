from PIL import Image
import pytesseract

# Открываем изображение
img = Image.open('example/name.png')
# Распознаём текст
text = pytesseract.image_to_string(img, lang='rus')  # для русского и английского
print(text)