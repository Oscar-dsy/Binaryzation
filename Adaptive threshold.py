import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image

# ===================== 路径设置 =====================
original_folder = ""
output_folder = ""

os.makedirs(output_folder, exist_ok=True)

def find_best_adaptive_threshold(gray_img):

    best_binary_img = None
    min_diff = float('inf')
    best_block_size = None
    best_C = None

    for block_size in range(3, 30, 2):
        for C in range(-5, 15):

            binary_img = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,block_size,C)
            num_white = np.sum(binary_img == 255)
            num_black = np.sum(binary_img == 0)
            diff = abs(num_white - num_black)
            if diff < min_diff:
                min_diff = diff
                best_block_size = block_size
                best_C = C
                best_binary_img = binary_img.copy()
            if diff == 0:
                return best_binary_img, best_block_size, best_C
    return best_binary_img, best_block_size, best_C

for filename in os.listdir(original_folder):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
        continue
    image_path = os.path.join(original_folder, filename)
    try:
        img = Image.open(image_path).convert('RGB')
        if img.size != (50, 50):
            print(f"false：{filename}，not 50×50")
            continue
        img_array = np.array(img)
        gray_img = cv2.cvtColor(img_array,cv2.COLOR_RGB2GRAY)
        binary_img, block_size, C = find_best_adaptive_threshold(gray_img)
        if binary_img is None:
            print(f"false：{filename}")
            continue
        binary_array = np.where(binary_img == 255, 1, 0)
        output_name = os.path.splitext(filename)[0] + '.xlsx'
        excel_path = os.path.join(output_folder, output_name)
        df = pd.DataFrame(binary_array)
        df.to_excel(excel_path, index=False, header=False)
    except Exception as e:
        print(f"false：{filename}，原因：{e}")