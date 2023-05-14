from PIL import Image
from matplotlib import pyplot as plt
from gaussian_blur  import gaussian_blur_background
from fft_blur import blur_background

if __name__ == '__main__':  

    # definir tamanho das imagens
    plt.rcParams["figure.figsize"] = (8,5)

    print("################################ IMAGE BLUR ################################")
    while True: 
        print("Press Q to quit, or any other key to continue...")
        k = input("press enter after typing to confirm...")
        if k == 'q' or k == 'Q':
            break
        
        input_files = []
        print("press enter after the LAST image you wanto to blur")
        while True:
            input_file = input("name of a file (with extension jpg or jpeg):")
            if input_file == "":
                break
            
            input_files.append(input_file)


        for input_file in input_files:
            
            
            try:
                
                input_image = Image.open(input_file)
                print("read image ok")

                print("blurring image with gaussian kernel filter",end = " ")
                imagem_fundo_borrado_gauss = gaussian_blur_background(input_image= input_image)
                print(" | done")
                print("blurring image with low frequency filter",end= " ")
                imagem_fundo_borrado_lff = blur_background(input_image= input_image)
                print(" | done\n")

                print("ploting images")
                plt.figure(figsize = (8,5))
                
                plt.title("original image")
                plt.subplot(1,3,1)
                plt.imshow(input_image)

                plt.title("low-freq-filter")
                plt.subplot(1,3,2)
                plt.imshow(imagem_fundo_borrado_lff)

                plt.title("gaussian-filter")
                plt.subplot(1,3,3)
                plt.imshow(imagem_fundo_borrado_gauss)  
                plt.show()
            except:
                print(f"problems with {input_file}, verify the extension and if the name is correct\n")
                