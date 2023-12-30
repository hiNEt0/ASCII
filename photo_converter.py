import numpy as np
import ascii_window as aw
from PIL import Image

ASCII_CHARS = [".", ",", ":", ";", "+", "*", "?", "%", "$", "#", "@"]


def image_to_grey(image):
    pixels = np.array(image)
    grey_img = np.zeros((pixels.shape[0], pixels.shape[1]), dtype=np.uint8)

    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            r, g, b = pixels[i, j]
            grey_img[i, j] = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    return grey_img


def change_resolution(image_array, new_width, new_height):
    width, height = image_array.shape[1], image_array.shape[0]  # получаем текущие размеры изображения
    x_ratio = width / new_width
    y_ratio = height / new_height

    new_image_array = np.zeros((new_height, new_width), dtype=np.uint8)  # создаем пустое изображение нового размера

    for y in range(new_height):
        for x in range(new_width):
            orig_x = int(x * x_ratio)  # пересчитываем координаты пикселей в новом разрешении
            orig_y = int(y * y_ratio)
            new_image_array[y, x] = image_array[orig_y, orig_x]  # копируем пиксели из оригинального изображения в новое

    return new_image_array


def size_input(image):
    is_sized = False
    while not is_sized:
        new_size = input('\nEnter the expected width and height of the image in'
                         ' characters separated by a space. If the original '
                         'size is required, press "Enter".\n').strip().split()

        if not new_size:
            new_width, new_height = image.size
            is_sized = True
        elif len(new_size) != 2:
            print('Incorrect input. Enter two numbers.')
            continue
        else:
            try:
                new_width, new_height = map(int, new_size)
                if new_width <= 0 or new_height <= 0:
                    print('Size must be greater than zero. Try again.')
                    continue
                else:
                    is_sized = True
            except ValueError:
                print('Size must be integer.')
                continue
    return int(new_width), int(new_height)


def save_ascii(ascii_image, path):
    try:
        with open(path, "w") as f:
            f.write(ascii_image)
    except NotADirectoryError:
        print('Output direction is not exist\nClosing program...')
        exit()
    except MemoryError:
        print('You ran out of memory\nClosing program...')
        exit()
    except SyntaxError:
        print('File name is incorrect\nClosing program...')
        exit()
    except Exception:
        print('An unknown error has occurred.\nTry run the program again.')
        exit()


def preview_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                print(line)

    except FileNotFoundError:
        print(f"File '{file_path}' not found. File preview is not possible")


def convert(args):
    try:
        image = Image.open(args.path)
    except FileNotFoundError:
        print(args.path, ": Unable to find image")
        exit()

    # Input for new picture size
    new_width, new_height = size_input(image)

    grey_img = image_to_grey(image)

    resized_image = change_resolution(grey_img, new_width, new_height)

    if args.inversion:
        ASCII_CHARS.reverse()

    # replace each pixel with a character from array
    ascii_pixels = [ASCII_CHARS[pixel // 25] for line in resized_image for pixel in line]
    ascii_pixels = ''.join(ascii_pixels)

    # split string of chars into multiple strings of length
    # equal to new width and create a list
    ascii_image = [ascii_pixels[index:index + new_width]
                   for index in range(0, len(ascii_pixels), new_width)]
    ascii_image = "\n".join(ascii_image)

    save_ascii(ascii_image, args.outdir + args.filename + '.txt')

    if args.show_result:
        ascii_window = aw.TextFileViewer()
        ascii_window.text_widget.config(wrap="none")
        ascii_window.print_text(ascii_image)
        ascii_window.mainloop()
