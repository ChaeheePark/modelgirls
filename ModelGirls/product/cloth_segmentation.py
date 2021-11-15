# !pip install iglovikov_helper_functions
# !pip install cloths_segmentation

import numpy as np
import os
import cv2
import torch
import albumentations as albu
from iglovikov_helper_functions.utils.image_utils import load_rgb, pad, unpad
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image
from cloths_segmentation.pre_trained_models import create_model


def cloth_segmetation(img_name, cloth_path, mask_path):
    model = create_model("Unet_2020-10-30")
    model.eval()

    image = load_rgb(cloth_path+img_name)
    transform = albu.Compose([albu.Normalize(p=1)], p=1)
    padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)
    x = transform(image=padded_image)["image"]
    x = torch.unsqueeze(tensor_from_rgb_image(x), 0)
    with torch.no_grad():
        prediction = model(x)[0][0]
    mask = (prediction > 0).cpu().numpy().astype(np.uint8)
    mask = unpad(mask, pads)

    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i][j] != 0:
                mask[i][j] = 255

    # mask = cv2.resize(mask, (768, 1024), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(mask_path+img_name, mask)

    image = cv2.imread(cloth_path+img_name)
    # image = cv2.resize(image, (768, 1024), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(cloth_path+img_name, image)