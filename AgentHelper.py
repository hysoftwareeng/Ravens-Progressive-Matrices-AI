from PIL import Image, ImageChops, ImageOps
import numpy as np
import math

def check_if_same(image_a, image_b):
    if ImageChops.difference(image_a, image_b).getbbox() is None or calc_rms(image_a, image_b) <= 45:
        return True
    return False

def check_if_same_xor(image_a, image_b):
    if ImageChops.difference(image_a, image_b).getbbox() is None or calc_rms(image_a, image_b) <= 50:
        return True
    return False

def check_exactly_same(image_a, image_b):
    if ImageChops.difference(image_a, image_b).getbbox() is None:
        return True
    return False

def get_cropped_image(image_a):
    pixels = np.asarray(image_a)
    #retrieve top x coordinate
    coordinates = np.argwhere(pixels == False)
    try:
        top = min(coordinates[:,0])
        bottom = max(coordinates[:,0])
        left =  min(coordinates[:,1])
        right = max(coordinates[:,1])
        width = right - left + 1
        height = bottom - top + 1
        return image_a.crop((left, top, right, bottom))
    except:
        return image_a



def get_answer_by_image(image_template, problem_images, problem_type):
    answer_choice = []
    if problem_type == '2x2':
        choices = 7
    elif problem_type == '3x3':
        choices = 9
    for choice in range(1, choices):
        image_choice = problem_images[str(choice)]
        if check_if_same(image_template, image_choice):
            answer_choice.append(choice)
    return answer_choice

#retrieves exact answer only, other returns -1
def get_exact_answer_by_image(image_template, problem_images, problem_type):
    answer_choice = []
    if problem_type == '2x2':
        choices = 7
    elif problem_type == '3x3':
        choices = 9
    for choice in range(1, choices):
        image_choice = problem_images[str(choice)]
        if check_exactly_same(image_template, image_choice):
            answer_choice.append(choice)
    return answer_choice

#REFERENCED METHOD: http://effbot.org/zone/pil-comparing-images.htm#rms
def calc_rms(source, compare):
    # calculate the root-mean-square difference between two images

    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(source, compare)
    h = diff.histogram()
    sq = (value * (idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(source.size[0] * source.size[1]))
    return round(rms, 0)
#REFERENCE END


#REFERENCED METHOD: https://codereview.stackexchange.com/questions/55902/fastest-way-to-count-non-zero-pixels-using-python-and-pillow
def count_black_pixels(img):
    """
    Return the number of pixels in img that ARE black.
    img must be a PIL.Image object in mode L.
    """
    bbox = img.getbbox()
    if not bbox: return 0
    return sum(img.crop(bbox)
               .point(lambda x: 0 if x else 255)
               .convert("L")
               .point(bool)
               .getdata())
#REFERENCE END


def count_total_pixels(img):
    width, height = img.size
    return width*height
