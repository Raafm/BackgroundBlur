import cv2

import numpy as np
import torch
from torchvision import transforms
from normalizar import normalizar   
from remove_background import load_model

normalization_term = 2*np.pi
sigma_square = 10
r_norm = lambda x,y: ((x)**2 +(y)**2)/(2*sigma_square)
gaussian2D = lambda x,y: np.exp(-r_norm(x,y))/normalization_term
def gaussian_filter_generator (x_size,y_size) :
    x_center = x_size/2 + 1
    y_center = y_size/2 + 1
    return np.array([[ gaussian2D(x-x_center,y-y_center) for y in range(y_size)] for x in range(x_size)])




def fft_gauss_blur_gray(gray_img, nitidez = 10):
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

    # apply gaussian filter
    gauss_filter = gaussian_filter_generator(fshift.shape[0], fshift.shape[1])
    fshift_gauss = gauss_filter*fshift



    # Inverse FFT
    f_ishift_gauss = np.fft.ifftshift(fshift_gauss)
    img_back_gauss = np.fft.ifft2(f_ishift_gauss)
    img_back_gauss = np.abs(img_back_gauss)

    return img_back_gauss



def gaussian_blur_background(model = None, input_image = None):
    if model is None:
        model = load_model()
    if input_image is None:
        print( "No input image was passed to the function gaussian_blur_background")
        return
    
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

    #move the input and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        output = model(input_batch)['out'][0]
    output_predictions = output.argmax(0)

    # create a binary (black and white) mask of the profile foreground
    mask = output_predictions.byte().cpu().numpy()

    bin_mask = mask > 0
    # plt.imshow(mask.astype('float'))
    # plt.show()

    # apply mask for all 3 channels
    bin_mask3channels = np.stack((bin_mask, bin_mask, bin_mask), axis = -1)
    
    # get image to apply blur
    input_image = np.array(input_image)

    # get 3 channels to apply fft
    red   = input_image[:,:,0] 
    green = input_image[:,:,1] 
    blue  = input_image[:,:,2] 

    # aplly blurr to all 3 channels
    red_blurred   = fft_gauss_blur_gray(red  , nitidez = 10 )
    green_blurred = fft_gauss_blur_gray(green, nitidez = 10 )
    blue_blurred  = fft_gauss_blur_gray(blue , nitidez = 10 )

    # juntar 3 channels borrados em uma so imagem
    background_blurred = np.stack((red_blurred, green_blurred, blue_blurred), axis = -1)
    # colocar pixels entre 0 e 255
    background_blurred = normalizar(background_blurred)*255

    #normalizar imagem inicial para colocar seus pixels entre 0 e 255
    input_image = normalizar(input_image)*255

    # onde a mask indicar foreground colocar imagem original (input_image), 
    # onde indicar background colocar background_blurred
    imagem_fundo_borrado = np.where(bin_mask3channels, input_image, background_blurred).astype(np.uint8)


    return imagem_fundo_borrado
