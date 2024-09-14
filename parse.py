import os
import json
from PIL import Image

image_folder = 'train'
json_file = os.path.join(image_folder, '_annotations.createml.json')
output_folder = os.path.join(image_folder, 'cropped_images')

os.makedirs(output_folder, exist_ok=True)

with open(json_file, 'r') as file:
    data = json.load(file)

for item in data:
    image_name = item['image']
    annotations = item['annotations']
    
    image_path = os.path.join(image_folder, image_name)
    image = Image.open(image_path)

    for i, annotation in enumerate(annotations):
        label = annotation['label']
        coords = annotation['coordinates']
        x, y, width, height = coords['x'], coords['y'], coords['width'], coords['height']
        
        left = x - width / 2
        upper = y - height / 2
        right = x + width / 2
        lower = y + height / 2
        crop_box = (left, upper, right, lower)
        
        cropped_image = image.crop(crop_box)
        cropped_image_name = f"{os.path.splitext(image_name)[0]}_crop_{i}.jpg"
        cropped_image_path = os.path.join(output_folder, cropped_image_name)
        
        if cropped_image.getbbox():
            print(f"Saving cropped image: {cropped_image_name}")
            cropped_image.save(cropped_image_path)
        else:
            print(f"Skipping empty cropped image: {cropped_image_name}")

print("Cropping completed successfully!")
