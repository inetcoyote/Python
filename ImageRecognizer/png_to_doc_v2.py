from PIL import Image
import pytesseract

# Укажи путь к tesseract, если нужно
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Путь к изображению
image_path = 'name.png'

# Путь к выходному текстовому файлу
output_path = 'recognized_name.txt'
# Открываем изображение
try:
    img = Image.open(image_path)
    print(f"✅ Изображение {image_path} загружено.")
except FileNotFoundError:
    print(f"❌ Ошибка: файл {image_path} не найден.")
    exit()

# Распознаём текст (только русский)
try:
    text = pytesseract.image_to_string(img, lang='rus')
    print("✅ Текст успешно распознан.")
except Exception as e:
    print(f"❌ Ошибка при распознавании текста: {e}")
    exit()

# Сохраняем текст в .txt файл
try:
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"✅ Текст сохранён в файл: {output_path}")
except Exception as e:
    print(f"❌ Ошибка при сохранении файла: {e}")