from PIL import Image, ImageOps
import cv2
import os
import imgkit
import shutil


def video_to_images(path):
    if os.path.exists('Images'):
        shutil.rmtree('Images')
    os.mkdir('Images')
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    success, image = video.read()
    counter = 1
    while success:
        cv2.imwrite("Images/Image{0}.jpg".format(str(counter)), image)
        success, image = video.read()
        counter += 1
    return fps, (counter-1)

def get_image(image_path):
    initial_image = Image.open(image_path)
    width, height = initial_image.size
    initial_image = initial_image.resize((round(width * 1.05), height))
    return initial_image

def pixelate_image(image, final_width=200):
    width, height = image.size
    final_height = int((height * final_width) / width)
    image = image.resize((final_width, final_height))
    return image

def grayscale_image(image):
    image_bw = ImageOps.grayscale(image)
    return image_bw

def ascii_conversion(bw_image, ascii_string=[".", ",", ":", ";", "+", "*", "?", "%", "$", "#", "@"]):
    pixels = bw_image.getdata()
    ascii_image_list = []
    for pixel in pixels:
        ascii_converted = int((pixel * len(ascii_string)) / 256)
        ascii_image_list.append(ascii_string[ascii_converted])
    return ascii_image_list

def get_color(image):
    pixels = image.getdata()  # Creates a list with the RGB value for each pixel
    return pixels

def print_ascii(ascii_list, image, color, image_pos):
    if not os.path.exists('HtmlImages'):
        os.mkdir('HtmlImages')
    file_path = 'HtmlImages/Html{0}.html'.format(str(image_pos))
    with open(file_path, "w") as file:
        file.write("""
            <!DOCTYPE html>
            <html>
                <body style='background-color:black'>
                    <pre style='display: inline-block; border-width: 4px 6px; border-color: black; border-style: solid; background-color:black; font-size: 32px ;font-face: Montserrat;font-weight: bold;line-height:60%'>
            """)

        width, height = image.size
        counter = 0
        for j in ascii_list:
            color_hex = '%02x%02x%02x' % color[counter]
            counter += 1
            if (counter % width) != 0:
                file.write("<span style=\"color: #{0}\">{1}</span>".format(color_hex, j))
            else:
                file.write("<br />")
        file.write("""
                    </pre>
                </body>
            </html>
        """)

def show_result(videoName):
    video = cv2.VideoCapture(videoName)
    if video.isOpened():
        print('Video Succefully opened')
    else:
        print('Something went wrong when playing the video')

    #define a scale lvl for visualization
    scaleLevel = 3 #it means reduce the size to 2**(scaleLevel-1)

    windowName = 'Video Player'
    cv2.namedWindow(windowName)

    while True:
        ret, frame = video.read() 
        if not ret:
            print("Could not read the frame")   
            cv2.destroyWindow(windowName)
            break

        rescaled_frame  = frame
        for i in range(scaleLevel-1):
            rescaled_frame = cv2.pyrDown(rescaled_frame)

        cv2.imshow(windowName, rescaled_frame)

        waitKey = (cv2.waitKey(1) & 0xFF)
        if  waitKey == ord('q'):
            print("closing video and exiting")
            cv2.destroyWindow(windowName)
            video.release()
            break

def convert(args):
    config = imgkit.config(wkhtmltoimage=r'wkhtmltoimage.exe')

    ascii_string = [".", ",", ":", ";", "+", "*", "?", "%", "$", "#", "@"]
    if args.inversion:
        ascii_string.reverse()

    fps, number_images = video_to_images(args.path)

    if os.path.exists('HtmlImages'):
        shutil.rmtree('HtmlImages')
    os.mkdir('HtmlImages')
    if os.path.exists('TextImages'):
        shutil.rmtree('TextImages')
    os.mkdir('TextImages')

    for i in range(1, number_images + 1):
        try:
            image = get_image('Images/Image{0}.jpg'.format(str(i)))
            right_size_image = pixelate_image(image)
            bw_image = grayscale_image(right_size_image)
            converted_list = ascii_conversion(bw_image, ascii_string)
            color_list = get_color(right_size_image)
            print_ascii(converted_list, right_size_image, color_list, i)
            imgkit.from_file('HtmlImages/Html{0}.html'.format(str(i)), 'TextImages/Image{0}.jpg'.format(str(i)), config=config)
        except MemoryError:
            print('You ran out of memory\nClosing program...')
            exit()

    res = Image.open('TextImages/Image1.jpg').size
    video = cv2.VideoWriter(args.outdir + args.filename + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), int(fps), res)

    for j in range(1, number_images + 1):
        video.write(cv2.imread('TextImages/Image{0}.jpg'.format(str(j))))
    video.release()

    if args.show_result:
        show_result(args.outdir + args.filename + '.mp4')