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
import numpy

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
        if problem.problemType == '3x3':
            print
            return -1

        print ('Beginning to solve problem {} of type {}'.format(problem.name, problem.problemType))
        problem_images = {}
        problem_figures = {}
        for name in problem.figures:
            figure = problem.figures[name]
            image = Image.open(figure.visualFilename)
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
        return answer

    @staticmethod
    def get_difference(image_a, image_b):
        return ImageChops.difference(image_a, image_b).getbbox() is None

    def transformation_unchanged(self, image_a, image_b, image_c, problem_images):
        is_same_ab = self.get_difference(image_a, image_b)
        is_same_ac = self.get_difference(image_a, image_c)
        #both A to B and A to C are unchanged
        if is_same_ab and is_same_ac:
            for choice in range(1, 7):
                image_choice = problem_images[str(choice)]
                if self.get_difference(image_c, image_choice):
                    return choice
        return -1

    def transformation_y_axis_reflection(self, image_a, image_b, image_c, problem_images):
        image_a_vertical_reflected = image_a.transpose(Image.FLIP_LEFT_RIGHT)
        is_same = self.get_difference(image_b, image_a_vertical_reflected)
        if is_same:
            image_c_vertical_reflected = image_c.transpose(Image.FLIP_LEFT_RIGHT)
            for choice in range(1, 7):
                image_choice = problem_images[str(choice)]
                if self.get_difference(image_c_vertical_reflected, image_choice):
                    return choice
        return -1
