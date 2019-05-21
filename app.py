import random
import lib
import math
import numpy
from PIL import ImageDraw, Image, ImageOps

#lib.generate_pattern_set("city.jpg",5,8,512)

#lib.blured_image("city.jpg")

temp_image = Image.open("city.jpg")
draw = ImageDraw.Draw(temp_image)
lib.draw_pattern(draw,45,5,512)
temp_image.save("lined.jpg")


f_image = Image.open("lined.jpg")
pixels = numpy.array(f_image)

fr = numpy.fft.fftn(pixels)

size = fr.shape

fr_real = numpy.empty(size)
fr_imag = numpy.empty(size)

for i in range(size[0]-1):
    for j in range(size[1]-1):
        for k in range(size[2]-1):
            fr_real[i][j][k] = fr[i][j][k].real
            fr_imag[i][j][k] = fr[i][j][k].imag


un_fr = numpy.fft.ifftn(fr_real)

print(fr_real[100][100])