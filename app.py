import random
import lib
import math
import numpy as np
from PIL import ImageDraw, Image, ImageOps


lib.generate_pattern_set("city.jpg", width=10, count=3, w=512, fftmult=300)
'''
Влияние малого количества пикселей на спектр изображения - Волков
'''