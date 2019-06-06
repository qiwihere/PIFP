import random
import lib
import math
import numpy as np
from PIL import ImageDraw, Image, ImageOps


#lib.generate_pattern_set("city64.jpg", width=3, count=12, w=64, fftmult=10)
lib.crop_image('city.jpg', 2, 512)