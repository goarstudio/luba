from psd_tools import PSDImage
import os

psd_file = 'Lyuba.psd'  # Название твоего PSD-файла (проверь имя!)
output_folder = 'output_layers'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

psd = PSDImage.open(psd_file)

for i, layer in enumerate(psd):
    if layer.is_group():
        continue

    if layer.visible:
        layer_image = layer.composite()
        layer_image.save(os.path.join(output_folder, f'layer_{i}_{layer.name}.png'))

print("Готово! Все слои сохранены в папке:", output_folder)