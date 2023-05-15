import tkinter as tk
from PIL import Image
import matplotlib.pyplot as plt
from gaussian_blur import gaussian_blur_background
from fft_blur import blur_background

import os
IMAGES_FOLDER = "Images"
BLURRED_FOLDER = "Blurred-Images"

def get_file_names(folder_path = IMAGES_FOLDER ):
    file_names = []

    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_names.append(filename)

    return file_names     

def plot_img_comparison(input_image, imagem_fundo_borrado):
    try:
        
        plt.figure(figsize = (8,5))
        plt.subplot(1,2,1)
        plt.imshow(input_image)
        plt.subplot(1,2,2)
        plt.imshow(imagem_fundo_borrado)
        plt.show()          
    except:
        print("problemas com esta imagem, verifique a extensao e a escrita do arquivo")

def read_img_file(image_path = IMAGES_FOLDER + "/author.jpeg"):
    try: 
        input_image = Image.open(image_path)   
    except:
        image_path = os.path.join(IMAGES_FOLDER,image_path) 
        input_image = Image.open(image_path)   
    return input_image  


def make_background_blurr(image_path, blurr_type = "gaussian", save_img= True):
    input_image = read_img_file(image_path)

    if blurr_type == "gaussian":
        blurred_image = gaussian_blur_background(input_image= input_image)
    elif blurr_type == "low-freq":
        blurred_image = blur_background(input_image= input_image)
    

    plot_img_comparison(input_image, blurred_image)

    if save_img:
        
        image_path = os.path.join(BLURRED_FOLDER, blurr_type , image_path)
    
        plt.imshow(blurred_image)
        plt.savefig(image_path)
        plt.title("Image saved at " +  image_path)
        plt.show()


# Define a function to update the dropdown menu
def update_dropdown(folder_path = IMAGES_FOLDER ):

    file_names = []

    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_names.append(filename)

    dropdown["menu"].delete(0, tk.END)  # Clear the current dropdown menu

    # Add the file names to the dropdown menu
    for filename in file_names:
        dropdown["menu"].add_command(label=filename, command=tk._setit(var, filename))



def update_radio_button():     

    filter_names = ["low-freq", "gaussian"]

    # Create a StringVar to store the selected file name
    selected_filter = tk.StringVar()

    # Create a list of Radiobutton widgets to display the radio_button
    # Create a list of Radiobutton widgets to display th               e file names
    radio_buttons = [tk.Radiobutton(root, text=filtername, variable=selected_filter, value=filtername) 
                        for filtername in filter_names]

    # Pack the Radiobutton widgets
    for checkbox in radio_buttons:
        checkbox.pack()

    # Save the checkbox states for later use
    update_radio_button.radio_buttons = radio_buttons #???
    return selected_filter




if  __name__ == "__main__":
        
    # Create the tkinter window
    root = tk.Tk()

    # Create a canvas to display the image
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()


    # Create a variable to store the selected file name
    var = tk.StringVar(root)
    # Create the dropdown menu
    dropdown = tk.OptionMenu(root, var,"" )
    dropdown.pack()



    # Update the dropdown menu with the file names
    update_dropdown()

    # Create a button to update the dropdown menu
    update_button = tk.Button(root, text="Update Images Folder", command=update_dropdown)
    update_button.pack()


    # Update the radio_button with the file names
    selected_filter = update_radio_button()


    savefig_flag = tk.BooleanVar(root,value = True)
    save_button = tk.Checkbutton(                               
                                    root,      
                                    text= "save-images",
                                    variable= savefig_flag,
                                )   
    save_button.pack()

    blurr_button = tk.Button(
                            root,
                            text = "blur",
                            command = lambda: make_background_blurr(
                                                                    image_path= var.get(),
                                                                    blurr_type = selected_filter.get(),
                                                                    save_img = savefig_flag.get()
                                                                    )
                            )  
    blurr_button.pack()


    # Start the main loop
    root.mainloop()
