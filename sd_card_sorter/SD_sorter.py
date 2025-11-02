import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time

from PIL import Image, ImageTk

import file_extractor


def choose_folder():
    global FILE_LIST, IMAGE_INDEX
    folder = filedialog.askdirectory()
    if folder:
        FILE_LIST = file_extractor.categorize_folder(folder)
    update_image(FILE_LIST["Images"][IMAGE_INDEX])



def fit_image_with_padding(img, target_width, target_height, padding_color=(0, 0, 0)):
    """
    Resize an image to fit inside target_width x target_height,
    keeping aspect ratio and adding padding.

    Parameters:
        img: PIL.Image or path to image
        target_width: desired width
        target_height: desired height
        padding_color: RGB tuple for padding (default black)

    Returns:
        PIL.Image object with padded and resized image
    """
    # Load image if a path is given
    if isinstance(img, str):
        img = Image.open(img)

    # Compute aspect ratios
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height

    # Determine new size
    if target_ratio > img_ratio:
        # Window is wider → fit by height
        new_height = target_height
        new_width = int(img_ratio * new_height)
    else:
        # Window is taller → fit by width
        new_width = target_width
        new_height = int(new_width / img_ratio)

    # Resize the image
    resized = img.resize((new_width, new_height), Image.LANCZOS)

    # Create a new image with padding
    padded_image = Image.new("RGB", (target_width, target_height), padding_color)
    x = (target_width - new_width) // 2
    y = (target_height - new_height) // 2
    padded_image.paste(resized, (x, y))

    return padded_image

def add_button():
    global FILE_LIST
    folder = filedialog.askdirectory()
    btn = tk.Button(button_frame, text=folder, command= lambda: save_image(folder))
    row = button_frame.grid_size()[1]
    btn.grid(row=row, column=0)
    add_remover()


def add_remover():
    b = tk.Button(button_frame, text="X", command=lambda : remove_button_row(b))
    row = button_frame.grid_size()[1] - 1
    b.grid(row=row, column=1)


def remove_button_row(button):
    info = button.grid_info()
    destroy_at(info['row'], info['column'] - 1)
    destroy_at(info['row'], info['column'])


def save_image(button_text):
    global IMAGE, IMAGE_NAME, FILE_LIST, IMAGE_INDEX
    folder = button_text
    filename = f"{folder}/{IMAGE_NAME}"

    IMAGE.save(filename)
    os.remove(FILE_LIST["Images"][IMAGE_INDEX])
    IMAGE_INDEX += 1
    try:
        update_image(FILE_LIST["Images"][IMAGE_INDEX])
    except IndexError:
        set_image_init_state()
        messagebox.showinfo("Info", f"Keine neuen Bilder verfügbar")


def destroy_at(row, column):
    for widget in button_frame.grid_slaves():  # returns all widgets in the frame
        info = widget.grid_info()
        if info['row'] == row and info['column'] == column:
            widget.destroy()
            break


def update_image(image_path):
    global IMAGE, IMAGE_NAME, IMAGE_PHOTO, PhotoLabel, label_text
    IMAGE_NAME = image_path.split("\\")[-1]
    IMAGE_NAME = f"{int(time.time())}_{IMAGE_NAME}"
    image = Image.open(image_path)
    image = fit_image_with_padding(image, 600, 400)
    IMAGE = image
    IMAGE_PHOTO = ImageTk.PhotoImage(image)
    PhotoLabel.config(image= IMAGE_PHOTO)
    PhotoLabel.image = IMAGE_PHOTO
    label_text.config(text= IMAGE_NAME)


def set_image_init_state():
    global IMAGE, IMAGE_NAME, IMAGE_PHOTO, PhotoLabel, label_text, IMAGE_INDEX
    IMAGE_NAME = ""
    image = Image.new("RGB", (600, 400), (0, 0, 0))
    image = fit_image_with_padding(image, 600, 400)
    IMAGE = image
    IMAGE_PHOTO = ImageTk.PhotoImage(image)
    PhotoLabel.config(image=IMAGE_PHOTO)
    PhotoLabel.image = IMAGE_PHOTO
    label_text.config(text=IMAGE_NAME)
    IMAGE_INDEX = 0


def skip_image():
    global IMAGE_INDEX, FILE_LIST
    IMAGE_INDEX += 1
    try:
        update_image(FILE_LIST["Images"][IMAGE_INDEX])
    except IndexError:
        set_image_init_state()
        messagebox.showinfo("Info", f"Keine neuen Bilder verfügbar")


def delete_and_continue():
    global IMAGE_INDEX, FILE_LIST
    os.remove(FILE_LIST["Images"][IMAGE_INDEX])
    IMAGE_INDEX += 1
    try:
        update_image(FILE_LIST["Images"][IMAGE_INDEX])
    except IndexError:
        set_image_init_state()
        messagebox.showinfo("Info", f"Keine neuen Bilder verfügbar")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Sorter")
    root.geometry("1200x800")

    # Global Vars
    FILE_LIST = {}
    IMAGE = Image.new("RGB", (600, 400), (0, 0, 0))
    IMAGE_PHOTO = ImageTk.PhotoImage(IMAGE)
    IMAGE_NAME = ""
    IMAGE_INDEX = 0

    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0)

    tk.Label(main_frame, text="Select a folder to sort:").grid(row=0, column=0, columnspan=2)
    tk.Button(main_frame, text="Browse...", command=choose_folder).grid(row=1, column=0, columnspan=2)

    image_frame = tk.Frame(main_frame)
    image_frame.grid(row=2, column=0)

    label_text = tk.Label(image_frame, text=IMAGE_NAME, font=("Arial", 20), fg="white", bg="gray")
    label_text.grid(row=0, column=0, columnspan=2)
    PhotoLabel = tk.Label(image_frame, image=IMAGE_PHOTO, bg="#222")
    PhotoLabel.grid(row=1, column=0, columnspan=2)
    delete_button = tk.Button(image_frame, text="Löschen", command= delete_and_continue)
    skip_button = tk.Button(image_frame, text="Überspringen", command= skip_image)
    delete_button.grid(row=2, column=0)
    skip_button.grid(row=2, column=1)

    button_frame = tk.Frame(main_frame)
    button_frame.grid(row=2, column=1)
    add_btn = tk.Button(button_frame, text="Add", command= add_button)
    add_btn.grid(row=0, column=0, sticky="n")

    root.mainloop()