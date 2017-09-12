from PIL import Image, ImageChops
import numpy as np
import math, operator, functools

def get_difference(image_a, image_b):
    if ImageChops.difference(image_a, image_b).getbbox() is None or calc_rms(image_a, image_b) <= 45:
        return True
    return False


def get_answer_by_image(image_template, problem_images):
    answer_choice = -1
    for choice in range(1, 7):
        image_choice = problem_images[str(choice)]
        if get_difference(image_template, image_choice):
            answer_choice = choice
            break
    return answer_choice

def histogram_compare(image_a, image_b):
    histogram_1 = image_a.histogram()
    histogram_2 = image_b.histogram()
    sum_image_a = 0.0
    sum_image_b = 0.0
    diff = 0.0
    for i in range(len(histogram_1)):
        sum_image_a += histogram_1[i]
        sum_image_b += histogram_2[i]
        diff += abs(histogram_1[i] - histogram_2[i])
        max_sum = max(sum_image_a, sum_image_b)
        return diff/(2*max_sum)

def PixelCompare(im1, im2, alpha = .005):
    if im1.size == im2.size and im1.mode == im2.mode:
        randPix = im1.getpixel((0,0))
        maxSum = []
        diff = []
        for channel in range(len(randPix)):
            diff += [0.0]
            maxSum += [0.0]
        width = im1.size[0]
        height = im1.size[1]
        for i in range(width):
            for j in range(height):
                pixel1 = im1.getpixel((i,j))
                pixel2 = im2.getpixel((i,j))
                for channel in range(len(randPix)):
                    maxSum[channel] += 255
                    diff[channel] += abs(pixel1[channel] - pixel2[channel])
        for channel in range(len(randPix)):
            if diff[channel] > alpha*maxSum[channel]:
                return False
        return True
    return False

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

def countBlackPixels(img):
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

def countWhitePixels(image):
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

def countTotalPixels(img):
    width, height = img.size
    return width*height