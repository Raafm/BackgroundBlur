from fft_blur_gray import fft_blur
import numpy as np
import torch
from torchvision import transforms
from remove_background import load_model
from normalizar import normalizar

def blur_background(model = None, input_image= None):
    if model is None:                                                                    
        model = load_model()                                                    

        if input_image  is None:
            print( "No input image was passed to the function blur_background")
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

    # apply mask for all 3 channels
    bin_mask3channels = np.stack((bin_mask, bin_mask, bin_mask), axis = -1)
    
    # get image to apply blurr
    input_image = np.array(input_image)

    # get 3 channels to apply fft
    red   = input_image[:,:,0] 
    green = input_image[:,:,1] 
    blue  = input_image[:,:,2] 

    # aplly blurr to all 3 channels
    red_blurred   = fft_blur(red  , nitidez = 10 )
    green_blurred = fft_blur(green, nitidez = 10 )
    blue_blurred  = fft_blur(blue , nitidez = 10 )

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

