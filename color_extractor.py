# -*- coding: utf-8 -*-
# Imports
import cv2 as cv
from PIL import Image
import time
import numpy as np
import matplotlib.pyplot as plt

"""## Step 2: Upload your image(s)"""
def extract_colors(image_path, n_colors=6):
    img_max_dim = 256
    final_palettes = []
    quanticized_images = []
    resized_imgs = []
    accuracy_aimed = 1.0
    max_iter = 45

    start_time = time.time()
    img = Image.open(image_path).convert('RGB')

    resized_width = int((img_max_dim * min(img.size)) / max(img.size))
    resized_img = img.copy()
    resized_img.thumbnail((img_max_dim, img_max_dim), Image.Resampling.LANCZOS)

    resized_img_np = np.array(resized_img, np.float32)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, max_iter, accuracy_aimed)

    _, labels, centers = cv.kmeans(resized_img_np.reshape(-1,3), n_colors, None,
                                    criteria, 10, flags=cv.KMEANS_PP_CENTERS)

    unique, counts = np.unique(labels, return_counts=True)
    labels_ordered = unique[counts.argsort()[::-1]]
    ordered_palette = centers[labels_ordered].astype(int)

    final_palettes.append(ordered_palette)
    quanticized_images.append(np.uint8(centers)[labels.flatten()].reshape((resized_img_np.shape)))
    resized_imgs.append(resized_img_np)

    hex_colors = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in ordered_palette]

    end_time = time.time() - start_time

    return {
        "original_image": img,
        "resized_image": resized_img,
        "palette": ordered_palette,
        "quanticized_image": quanticized_images[0],
        "duration": end_time,
        "hex_color":hex_colors,
    }