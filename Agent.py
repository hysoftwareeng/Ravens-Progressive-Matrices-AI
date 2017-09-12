# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops
import numpy as np
from AgentHelper import get_difference, get_answer_by_image, countBlackPixels, countWhitePixels, countTotalPixels, calc_rms

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass


    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        #Skip 3x3 problems for the first Project
        if problem.problemType == '3x3':# or problem.name != 'Basic Problem B-06':
            return -1

        print ('Beginning to solve problem {} of type {}'.format(problem.name, problem.problemType))
        problem_images = {}
        problem_figures = {}
        for name in problem.figures:
            figure = problem.figures[name]
            image = Image.open(figure.visualFilename).convert('1')
            problem_images[name] = image    #dict of images to open for visual approach
            problem_figures[name] = figure.objects          #dict of all attributes by frame
        answer = self.build_semantic_network_and_solve(problem_images)
        return answer

    def build_semantic_network_and_solve(self, problem_images):
        answer = -1
        image_a = problem_images['A']
        image_b = problem_images['B']
        image_c = problem_images['C']

        if answer == -1:
            answer = self.transformation_unchanged(image_a, image_b, image_c, problem_images)
        if answer == -1:
            answer = self.transformation_y_axis_reflection(image_a, image_b, image_c, problem_images)
        if answer == -1:
            answer = self.transformation_x_axis_reflection(image_a, image_b, image_c, problem_images)
        if answer == -1:
            answer = self.transformation_and(image_a, image_b, image_c, problem_images)
        if answer == -1:
            answer = self.transformation_pixel_ratio_frame(image_a, image_b, image_c, problem_images)
        if answer == -1:
            answer = self.transformation_pixel_ratio_half_frame_vertical(image_a, image_b, image_c, problem_images)
        return answer


    def transformation_and(self, image_a, image_b, image_c, problem_images):
        #A to B is add fill
        image_ab_and = ImageChops.logical_and(image_a, image_b)
        is_same_ab_and = get_difference(image_ab_and, image_b)
        black_pixel_inc = (countBlackPixels(image_b)-countBlackPixels(image_a))/countBlackPixels(image_a)
        potential_choices = {}
        if is_same_ab_and:
            for choice in range(1, 7):
                image_choice = problem_images[str(choice)]
                image_cd_and = ImageChops.logical_and(image_c, image_choice)
                is_same_cd_and = get_difference(image_cd_and, image_choice)
                if is_same_cd_and:
                    black_pixel_inc_cd = (countBlackPixels(image_choice) - countBlackPixels(image_c)) / countBlackPixels(
                        image_c)
                    potential_choices[black_pixel_inc_cd] = choice
            key = min(potential_choices.keys(), key=lambda x: abs(x - black_pixel_inc))
            return potential_choices[key]
        return -1

    def transformation_pixel_ratio_frame(self, image_a, image_b, image_c, problem_images):

        black_pixel_ratio_a = countBlackPixels(image_a)/countTotalPixels(image_a)
        black_pixel_ratio_b = countBlackPixels(image_b) / countTotalPixels(image_b)
        black_pixel_ratio_c = countBlackPixels(image_c) / countTotalPixels(image_c)

        black_pixels_ratio_diff_ab = black_pixel_ratio_b - black_pixel_ratio_a
        black_pixels_ratio_diff_ac = black_pixel_ratio_c - black_pixel_ratio_a

        potential_solutions = []
        for choice in range(1, 7):
            image_choice = problem_images[str(choice)]
            black_pixel_ratio_image_choice = countBlackPixels(image_choice)/countTotalPixels(image_choice)
            if black_pixel_ratio_image_choice - black_pixel_ratio_c == black_pixels_ratio_diff_ab:
                potential_solutions.append(choice)

        if len(potential_solutions) == 1:
            return potential_solutions[0]
        return -1

    #chop square frame into two halves vertically and compare, left, upper, right, lower
    def transformation_pixel_ratio_half_frame_vertical(self, image_a, image_b, image_c, problem_images):
        width, height = image_a.size
        image_a_first_half = image_a.crop((0,0,width/2, height))
        image_a_second_half = image_a.crop((width/2, 0, width, height))
        image_b_first_half = image_b.crop((0,0,width/2, height))
        image_b_second_half = image_b.crop((width/2, 0, width, height))
        image_c_first_half = image_c.crop((0,0,width/2, height))
        image_c_second_half = image_c.crop((width/2, 0, width, height))

        black_pixel_ratio_a_first_half = countBlackPixels(image_a_first_half) / countTotalPixels(image_a_first_half)
        black_pixel_ratio_b_first_half = countBlackPixels(image_b_first_half) / countTotalPixels(image_b_first_half)
        black_pixel_ratio_c_first_half = countBlackPixels(image_c_first_half) / countTotalPixels(image_c_first_half)

        black_pixel_ratio_a_second_half = countBlackPixels(image_a_second_half) / countTotalPixels(image_a_second_half)
        black_pixel_ratio_b_second_half = countBlackPixels(image_b_second_half) / countTotalPixels(image_b_second_half)
        black_pixel_ratio_c_second_half = countBlackPixels(image_c_second_half) / countTotalPixels(image_c_second_half)

        ratio_diff_first_ab = black_pixel_ratio_b_first_half - black_pixel_ratio_a_first_half
        ratio_diff_second_ab = black_pixel_ratio_b_second_half - black_pixel_ratio_a_second_half

        potential_solutions = []
        for choice in range(1, 7):
            image_choice = problem_images[str(choice)]
            image_choice_first_half = image_choice.crop((0, 0, width / 2, height))
            image_choice_second_half = image_choice.crop((width / 2, 0, width, height))
            black_pixel_ratio_choice_first_half = countBlackPixels(image_choice_first_half) / countTotalPixels(image_choice_first_half)
            black_pixel_ratio_choice_second_half = countBlackPixels(image_choice_second_half) / countTotalPixels(image_choice_second_half)

            ratio_diff_first_choicec = black_pixel_ratio_choice_first_half - black_pixel_ratio_c_first_half
            ratio_diff_second_choicec = black_pixel_ratio_choice_second_half - black_pixel_ratio_c_second_half

            if np.abs(ratio_diff_first_choicec - ratio_diff_first_ab) <= 0.005 and abs(ratio_diff_second_choicec - ratio_diff_second_ab) <= 0.005:
                potential_solutions.append(choice)

        if len(potential_solutions) == 1:
            return potential_solutions[0]

        return -1


    def transformation_unchanged(self, image_a, image_b, image_c, problem_images):
        is_same_ab = get_difference(image_a, image_b)
        is_same_ac = get_difference(image_a, image_c)
        #both A to B and A to C are unchanged
        if is_same_ab and is_same_ac:
            return get_answer_by_image(image_c, problem_images)
        #A and C are unchanged
        if is_same_ac:
            return get_answer_by_image(image_b, problem_images)
        return -1

    def transformation_y_axis_reflection(self, image_a, image_b, image_c, problem_images):
        #Compare A to B transformation by Y reflection
        image_a_vertical_reflected = image_a.transpose(Image.FLIP_LEFT_RIGHT)
        is_same = get_difference(image_b, image_a_vertical_reflected)
        if is_same:
            image_c_vertical_reflected = image_c.transpose(Image.FLIP_LEFT_RIGHT)
            return get_answer_by_image(image_c_vertical_reflected, problem_images)
        return -1

    def transformation_x_axis_reflection(self, image_a, image_b, image_c, problem_images):
        image_a_vertical_reflected = image_a.transpose(Image.FLIP_TOP_BOTTOM)
        is_same = get_difference(image_c, image_a_vertical_reflected)
        if is_same:
            image_b_vertical_reflected = image_b.transpose(Image.FLIP_TOP_BOTTOM)
            return get_answer_by_image(image_b_vertical_reflected, problem_images)
        return -1
