from PIL import ImageDraw, Image, ImageOps
import random
import math
import numpy as np
import os, shutil


def draw_line(ang, offset, width, draw, w=256):
    base = {
        'x': w/2,
        'y': w/2
    }
    d = ang/180*math.pi
    r = w

    x1 = math.cos(d - math.pi * offset) * r + base['x']
    y1 = math.sin(d - math.pi * offset) * r + base['y']

    x2 = math.cos(d + math.pi + math.pi * offset) * r + base['x']
    y2 = math.sin(d + math.pi + math.pi * offset) * r + base['y']

    p1 = (x1, y1)
    p2 = (x2, y2)

    draw.line([p1, p2], (0, 0, 0), width)


def draw_pattern(draw, ang, width=5, w=256):
    count = round(w/width)
    for i in range(round(-count/2), round(count/2)):
        draw_line(ang, i*width/w/1.5, width, draw, w)


def generate_pattern_set(path, width, count= 6, w=256, fftmult=1):
    clear_dir('patterns')
    clear_dir('ff')

    step = 360/count

    for i in range(round(-count/2), round(count/2)):
        ang = i*step
        temp_image = Image.open(path)
        temp_image = blured_image(temp_image)
        draw = ImageDraw.Draw(temp_image)
        draw_pattern(draw, ang, width, w)
        temp_image.save("patterns/img_%s.jpg" % ang)
        generate_fft("patterns/img_%s.jpg" % ang, fftmult)


def blured_image(image):
    width, height = image.size

    n = 5

    count = int(n // 2)
    new_image = Image.new("RGB", (width + count * 2, height + count * 2), (0, 0, 0))
    draw = ImageDraw.Draw(new_image)
    pixel = new_image.load()
    area = (count, count, width + count, height + count)
    new_image.paste(image, area)
    matrix = [[1] * n] * n

    for i in range(count + 1, width + count + 1):
        print(i, " / ", width + count + 1)
        for j in range(count + 1, height + count + 1):
            r, g, b = 0, 0, 0
            for k in range(n):
                for x in range(n):
                    r += pixel[i + k - (count + 1), j + x - (count + 1)][0] * matrix[k][x]
                    g += pixel[i + k - (count + 1), j + x - (count + 1)][1] * matrix[k][x]
                    b += pixel[i + k - (count + 1), j + x - (count + 1)][2] * matrix[k][x]
            draw.point((i - (count), j - (count)), (int(r / n ** 2), int(g / n ** 2), int(b / n ** 2)))
    return new_image


def generate_fft(name, mult):
    input_image = Image.open(name)
    channels = input_image.split()  # splits an image into R, G, B channels
    result_array = np.zeros_like(input_image)  # make sure data types,
    # sizes and numbers of channels of input and output numpy arrays are the save

    if len(channels) > 1:  # grayscale images have only one channel
        for i, channel in enumerate(channels):
            result_array[..., i] = fft(channel) * mult
    else:
        result_array[...] = fft(channels[0]) * mult

    result_image = Image.fromarray(result_array)
    result_image.save('ff/ff_%s' % name.split('/')[1])


def fft(channel):
    fft = np.fft.fft2(channel)
    fft *= 255.0 / fft.max()  # proper scaling into 0..255 range
    return np.absolute(fft)



def clear_dir(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)