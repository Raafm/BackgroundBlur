import numpy as np
import torch
from torchvision import transforms

from PIL import Image
from matplotlib import pyplot as plt
import cv2


def fft_blurr(gray_img, nitidez = 10):
    # Apply 2D FFT
    f = np.fft.fft2(gray_img)
    fshift = np.fft.fftshift(f)

    # Create a circular gradient mask
    rows, cols = gray_img.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols), np.uint8)
    cv2.circle(mask, (ccol, crow), nitidez, 255, -1)

    # Apply the mask to the FFT image
    fshift = fshift * mask

    # Inverse FFT
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    return img_back
