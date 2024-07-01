import os
import datetime

# Define the root directory
root_dir = '.'  # Change this to your root directory if it's not the current one

# Function to process each folder
def process_folder(folder_name):
    # Define the new file and folder names
    new_md_name = folder_name + '.md'
    new_img_folder_name = folder_name

    # Paths
    readme_path = os.path.join(folder_name, 'README.md')
    new_md_path = os.path.join(folder_name, new_md_name)
    img_folder_path = os.path.join(folder_name, 'img')
    new_img_folder_path = os.path.join(folder_name, new_img_folder_name)

    # Rename README.md to the new name
    if os.path.exists(readme_path):
        os.rename(readme_path, new_md_path)

        # Modify the content of the markdown file
        with open(new_md_path, 'r') as file:
            lines = file.readlines()

        # Find the first occurrence of "---"
        try:
            index = lines.index('---\n') + 1
        except ValueError:
            index = 0

        # Prepare the new content to be added
        date_str = folder_name.split('-')[0:3]
        date_str = '-'.join(date_str)
        new_content = f"""---
title:
description:
author: seungki1011
date: {date_str} 12:30:00 +0900
categories: [Java]
tags: [java]
pin: true
math: true
mermaid: true
---

---
"""
        # Write the new content and the remaining old content
        with open(new_md_path, 'w') as file:
            file.write(new_content)
            file.writelines(lines[index:])

    # Rename img folder to the new name
    if os.path.exists(img_folder_path):
        os.rename(img_folder_path, new_img_folder_path)

# Traverse through the root directory and process each folder
for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)
    if os.path.isdir(folder_path):
        process_folder(folder)