import os
import pandas as pd
import shutil

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths (update these as per your file structure)
labels_csv_file = os.path.join(script_dir, 'scin_labels.csv')
cases_csv_file = os.path.join(script_dir, 'scin_cases.csv')
images_folder = os.path.join(script_dir, 'images')
output_folder = os.path.join(script_dir, 'output_folder')

# Create the output folders if they don't exist
eczema_folder = os.path.join(output_folder, 'eczema')
healthy_folder = os.path.join(output_folder, 'healthy')
os.makedirs(eczema_folder, exist_ok=True)
os.makedirs(healthy_folder, exist_ok=True)

# Read the CSV files
df_labels = pd.read_csv(labels_csv_file)
df_cases = pd.read_csv(cases_csv_file)

# Filter rows where monk_skin_tone_label_us >= 5
df_filtered = df_labels[df_labels['monk_skin_tone_label_us'] >= 5]

# Iterate over each row in the filtered DataFrame
for index, row in df_filtered.iterrows():
    case_id = row['case_id']
    
    # Find the row in scin_cases.csv with the matching case_id
    case_row = df_cases[df_cases['case_id'] == case_id]
    if case_row.empty:
        print(f"No matching case found for case ID: {case_id}")
        continue

    # Get image paths, stripping 'dataset/' prefix
    image_paths = []
    for column in ['image_1_path', 'image_2_path', 'image_3_path']:
        image_path = case_row[column].values[0]  # Access the path value
        if pd.notnull(image_path):  # Check if the path is not null
            image_path = image_path.replace('dataset/images/', '')  # Remove the 'dataset/' prefix
            image_paths.append(image_path)
    
    # Process each image path
    for image_path in image_paths:
        full_image_path = os.path.join(images_folder, image_path)
        
        print(f"Processing case ID: {case_id} with image: {image_path}")
        # Check if the image file exists
        if os.path.isfile(full_image_path):
            # Split the 'dermatologist_skin_condition_on_label_name' column
            print(row['dermatologist_skin_condition_on_label_name'])
            
            conditions = row['dermatologist_skin_condition_on_label_name']

            # Check if 'eczema' is in the list of conditions
            if 'eczema' in conditions:
                # Copy the image to the eczema folder
                shutil.copy(full_image_path, eczema_folder)
            elif conditions == '[]':
                # Copy the image to the healthy folder
                shutil.copy(full_image_path, healthy_folder)
        else:
            print(f"Image not found: {full_image_path}")

print("Images have been filtered and copied successfully!")
