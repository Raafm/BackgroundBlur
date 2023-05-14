"""# Usar este conjunto de celulas para apresentacao

## definir funcoes
"""

import cv2
import numpy as np
import torch
from torchvision import transforms


from urllib.request import urlretrieve
from PIL import Image
from matplotlib import pyplot as plt
from normalizar import  normalizar
from remove_background import remove_background, load_model
from gaussian_blurr  import gaussian_blurr_background
from fft_blurr import blurr_background

if __name__ == '__main__':  

    """## definir tamanho das imagens"""

    plt.rcParams["figure.figsize"] = (8,5)

    """## celulas para demosntracao

    ### celula exemplo
    """

    input_files = []
    print("pressione enter para terminar")
    while True:
        input_file = input("nome de um arquivo (com extensao jpg ou jpeg):")
        if input_file == "":
            break
        
        input_files.append(input_file)


    for input_file in input_files:
        
        
        try:
            
            input_image = Image.open(input_file)
            print("could open input image")
            imagem_fundo_borrado = gaussian_blurr_background(input_file= input_file)
            
            plt.figure(figsize = (8,5))
            plt.subplot(1,2,1)
            plt.imshow(input_image)
            plt.subplot(1,2,2)
            plt.imshow(imagem_fundo_borrado)
            plt.show()
        except:
            print("problemas com esta imagem, verifique a extensao e a escrita do arquivo")



    input_files = []
    print("pressione enter para terminar")
    while True:
        input_file = input("nome de um arquivo (com extensao jpg ou jpeg):")
        if input_file == "":
            break
        
        input_files.append(input_file)


    for input_file in input_files:
        plt.figure(figsize = (8,5))
        
        try:
            input_image = Image.open(input_file)
            imagem_fundo_borrado = blurr_background(input_file= input_file)

            plt.subplot(1,2,1)
            plt.imshow(input_image)
            plt.subplot(1,2,2)
            plt.imshow(imagem_fundo_borrado)
            plt.show()
        except:
            print("problemas com esta imagem, verifique a extensao e a escrita do arquivo")