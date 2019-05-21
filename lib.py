from PIL import ImageDraw, Image, ImageOps
import random
import math


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


def generate_pattern_set(path, width, count= 6, w=256):
    step = 360/count

    for i in range(round(-count/2), round(count/2)):
        ang = i*step
        temp_image = Image.open(path)
        draw = ImageDraw.Draw(temp_image)
        draw_pattern(draw, ang, width, w)
        temp_image.save("patterns/img_%s.jpg" % ang)

def blured_image(path):
    image = Image.open(path)
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

    new_image.save("img_blured.jpg")