
import os
from rembg import remove, new_session
from PIL import Image

input_folder = r'C:\Users\k1lla\Downloads\datasetK\test'  # Замените на путь к папке с изображениями
output_folder = r'C:\Users\k1lla\Downloads\datasetK\test_processed'  # Замените на путь к папке для обработанных изображений

# Создаем выходную папку, если она не существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Создаем сессию с моделью u2netp
model_name = "u2netp"
session = new_session(model_name)

for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Проверяем расширение файла
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            input_image = Image.open(input_path)
            output_image = remove(input_image, session=session)

            # Преобразуем изображение в RGB перед сохранением в JPEG
            if output_image.mode in ('RGBA', 'P'):
                output_image = output_image.convert('RGB')

            # Если исходное изображение было PNG, сохраняем как PNG, чтобы сохранить прозрачность
            if filename.endswith('.png'):
                output_image.save(output_path)
            else:
                output_image.save(output_path, 'JPEG')

            print(f"Обработано: {filename}")
        except Exception as e:
            print(f"Ошибка обработки {filename}: {e}")

print("Обработка завершена.")
