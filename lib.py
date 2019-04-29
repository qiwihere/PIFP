from PIL import ImageDraw, Image, ImageOps
import random

def draw_line(k, offset, width, draw, w=512):
    for x in range(w):
        p1 = (-10, offset)
        p2 = (w+10, offset+k)
        draw.line([p1, p2], (0, 0, 0), width)

def draw_pattern(draw, w=512):
    count = random.randint(5, 20)
    k = random.randint(-w, w)
    width = random.randint(20, 70)
    for i in range(count):
        offset = i*w/count*2
        draw_line(k, offset, width, draw, w)


def generate_pattern_set(path, count= 50, w=512):
    for i in range(count):
        temp_image = Image.open(path)
        draw = ImageDraw.Draw(temp_image)
        draw_pattern(draw)
        temp_image.save("patterns/img_%s.jpg" % i)

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