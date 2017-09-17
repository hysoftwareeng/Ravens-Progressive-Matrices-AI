from PIL import Image, ImageChops
import numpy as np
import math, operator, functools


def check_if_same(image_a, image_b):
    if ImageChops.difference(image_a, image_b).getbbox() is None or calc_rms(image_a, image_b) <= 45:
        return True
    return False


def get_answer_by_image(image_template, problem_images):
    answer_choice = -1
    for choice in range(1, 7):
        image_choice = problem_images[str(choice)]
        if check_if_same(image_template, image_choice):
            answer_choice = choice
            break
    return answer_choice


def calc_rms(source, compare):
    # http://effbot.org/zone/pil-comparing-images.htm#rms
    # calculate the root-mean-square difference between two images

    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(source, compare)
    h = diff.histogram()
    sq = (value * (idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(source.size[0] * source.size[1]))
    return round(rms, 0)


def count_black_pixels(img):
    """
    Return the number of pixels in img that ARE black.
    img must be a PIL.Image object in mode L.
    """
    bbox = img.getbbox()
    if not bbox: return 0
    # logger.info("Count Black Pixels in: %r" % bbox)
    return sum(img.crop(bbox)
               .point(lambda x: 0 if x else 255)
               .convert("L")
               .point(bool)
               .getdata())


def count_white_pixels(image):
    """Return the number of pixels in img that are not black.
    img must be a PIL.Image object in mode RGB.

    """
    bbox = image.getbbox()
    if not bbox: return 0
    return sum(image.crop(bbox)
               .point(lambda x: 255 if x else 0)
               .convert("L")
               .point(bool)
               .getdata())


def count_total_pixels(img):
    width, height = img.size
    return width*height