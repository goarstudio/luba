import imageio
import numpy as np
from PIL import Image
import math
import os

folder = 'output_layers'  # имя папки с PNG
output = 'animation.mp4'

files = [f for f in os.listdir(folder) if f.endswith('.png') and not f.startswith('.')]
files.sort()
layers = [Image.open(os.path.join(folder, f)).convert('RGBA') for f in files]

girl = next((l for l, n in zip(layers, files) if 'Lyuba_layer_1' in n), None)
circles = [l for l, n in zip(layers, files) if 'text' in n]
base_size = girl.size

# Сделать размеры чётными
new_width = base_size[0] if base_size[0] % 2 == 0 else base_size[0] + 1
new_height = base_size[1] if base_size[1] % 2 == 0 else base_size[1] + 1
base_size = (new_width, new_height)

girl = girl.resize(base_size)
circles = [c.resize(base_size) for c in circles]

num_frames = 300  # медленнее вращение = больше кадров
frames = []

print("Начинаю создавать кадры...")

# Задаём индивидуальные скорости для каждого круга (в градусах на кадр)
circle_speeds = [0.3, -0.2, 0.15, -0.1, 0.4, -0.25, 0.35, -0.3, 0.18][:len(circles)]

for i in range(num_frames):
    frame = Image.new('RGBA', base_size, (255, 255, 255, 0))

    # Вращение кругов
    for idx, c in enumerate(circles):
        angle = i * circle_speeds[idx]
        rotated = c.rotate(angle, resample=Image.Resampling.BICUBIC)
        frame = Image.alpha_composite(frame, rotated)

    # Пульсация девушки
    pulse = (math.sin(2 * math.pi * i / num_frames) + 1) / 2  # от 0 до 1
    scale_factor = 1 + (pulse * 0.1)  # до 10% масштаб
    new_size = (int(base_size[0] * scale_factor), int(base_size[1] * scale_factor))
    girl_scaled = girl.resize(new_size, resample=Image.Resampling.BICUBIC)

    # Вставляем по центру
    offset = ((base_size[0] - new_size[0]) // 2, (base_size[1] - new_size[1]) // 2)
    temp_frame = Image.new('RGBA', base_size, (0, 0, 0, 0))
    temp_frame.paste(girl_scaled, offset, girl_scaled)
    frame = Image.alpha_composite(frame, temp_frame)

    frames.append(frame.convert('RGB'))
    print(f"Кадр {i + 1}/{num_frames}")

# Сохраняем кадры как PNG
for i, frame in enumerate(frames):
    filename = f"frame_{i:03d}.png"
    frame.save(filename)
    print(f"Сохранён кадр {filename}")

print("✅ Все кадры сохранены! Чтобы собрать видео, запусти в Terminal:")
print("ffmpeg -framerate 20 -i frame_%03d.png -c:v libx264 -pix_fmt yuv420p output_final.mp4")