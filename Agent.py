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
from AgentHelper import check_if_same, get_answer_by_image, count_black_pixels, count_total_pixels, calc_rms, get_cropped_image

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
        #Skip 2x2 problems for testing Project 2
        # if problem.problemType == '2x2': #or problem.name != 'Basic Problem C-10':
        #     return -1
        print('-----------------------------------------------------------------------------------')
        print ('Beginning to solve problem {} of type {}'.format(problem.name, problem.problemType))
        problem_images = {}
        problem_figures = {}
        for name in problem.figures:
            figure = problem.figures[name]
            image = Image.open(figure.visualFilename).convert('1')
            problem_images[name] = image    #dict of images to open for visual approach
            problem_figures[name] = figure.objects          #dict of all attributes by frame
        answer = self.build_semantic_network_and_solve(problem_images, problem.problemType)
        return answer

    def build_semantic_network_and_solve(self, problem_images, problem_type):
        answer = -1
        if problem_type == '2x2':
            if answer == -1:
                answer = self.transformation_unchanged(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_y_axis_reflection(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_x_axis_reflection(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_rotation(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_pixel_diff(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_pixel_ratio_frame(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_and(problem_images, problem_type)
        elif problem_type == '3x3':
            if answer == -1:
                answer = self.transformation_unchanged(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_y_axis_reflection(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_pixel_ratio_frame(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_vertical_intersection(problem_images, problem_type)
            if answer == -1:
                answer = self.transformation_half_reflection(problem_images, problem_type)
        return answer

    def transformation_half_reflection(self, problem_images, problem_type):
        print('Solve by HORIZONTAL INTERSECTION transformation')
        image_a = problem_images['A']
        image_b = problem_images['B']
        image_c = problem_images['C']
        image_d = problem_images['D']
        image_e = problem_images['E']
        image_f = problem_images['F']
        image_g = problem_images['G']
        image_h = problem_images['H']


        image_a = get_cropped_image(image_a)
        img_a_width, img_a_height = image_a.size
        image_a_first_half = image_a.crop((0,0,img_a_width/2, img_a_height))
        image_a_second_half = image_a.crop((img_a_width/2, 0, img_a_width, img_a_height))


        image_c = get_cropped_image(image_c)
        img_c_width, img_c_height = image_c.size
        image_c_first_half = get_cropped_image(image_c.crop((0,0,img_c_width/2, img_c_height)))
        image_c_second_half = get_cropped_image(image_c.crop((img_c_width/2, 0, img_c_width, img_c_height)))


        image_ac_first_half_intersect = check_if_same(image_a_first_half, image_c_second_half)


        image_g = get_cropped_image(image_g)
        img_g_width, img_g_height = image_g.size
        image_g_first_half = get_cropped_image(image_g.crop((0,0,img_g_width/2, img_g_height)))
        image_g_second_half = get_cropped_image(image_g.crop((img_g_width/2, 0, img_g_width, img_g_height)))

        if image_ac_first_half_intersect:
            for choice in range(1, 9):
                image_choice = get_cropped_image(problem_images[str(choice)])
                image_choice_width, image_choice_height = image_choice.size
                image_choice_second_half = get_cropped_image(image_choice.crop((img_g_width / 2, 0, img_g_width, img_g_height)))
                image_g_answer_half_intersect = check_if_same(image_g_first_half, image_choice_second_half)
                if image_g_answer_half_intersect:
                    return choice
        return -1

    def transformation_vertical_intersection(self, problem_images, problem_type):
        print('Solve by VERTICAL INTERSECTION transformation')
        image_a = problem_images['A']
        image_b = problem_images['B']
        image_c = problem_images['C']
        image_d = problem_images['D']
        image_e = problem_images['E']
        image_f = problem_images['F']
        image_g = problem_images['G']
        image_h = problem_images['H']

        image_ag_intersect = ImageChops.logical_or(image_a, image_g)
        image_bh_intersect = ImageChops.logical_or(image_b, image_h)
        is_same_ag_intersect = check_if_same(image_a, image_ag_intersect)
        is_same_bh_intersect = check_if_same(image_b, image_bh_intersect)

        image_ad_intersect = ImageChops.logical_or(image_a, image_d)
        image_dg_intersect = ImageChops.logical_or(image_d, image_g)

        is_same_ad_intersect = check_if_same(image_d, image_ad_intersect)
        is_same_dg_intersect = check_if_same(image_g, image_dg_intersect)

        potential_solutions = {}
        #gradual intersect vertically
        if is_same_ad_intersect and is_same_dg_intersect:
            for choice in range(1, 9):
                image_choice = problem_images[str(choice)]
                image_f_ans_intersect = ImageChops.logical_or(image_f, image_choice)
                is_same_f_ans_intersect = check_if_same(image_choice, image_f_ans_intersect)
                rmse = calc_rms(image_choice, image_f_ans_intersect)
                if is_same_f_ans_intersect:
                    potential_solutions[rmse] = choice
            if potential_solutions:
                return potential_solutions[min(potential_solutions.keys())]

        #If vertical intersection is true for AG BH, etc
        potential_solutions = {}
        if is_same_ag_intersect and is_same_bh_intersect:
            black_pixels_a_ratio = count_black_pixels(image_a)/count_total_pixels(image_a)
            black_pixels_g_ratio = count_black_pixels(image_g)/count_total_pixels(image_g)
            black_pixel_inc_ag = black_pixels_g_ratio - black_pixels_a_ratio
            for choice in range(1, 9):
                image_choice = problem_images[str(choice)]
                image_c_ans_intersect = ImageChops.logical_or(image_c, image_choice)
                is_same_c_ans_intersect = check_if_same(image_c, image_c_ans_intersect)
                rmse = calc_rms(image_c, image_c_ans_intersect)
                black_pixels_c_ratio = count_black_pixels(image_c)/count_total_pixels(image_c)
                black_pixels_choice_ratio = count_black_pixels(image_choice)/count_total_pixels(image_choice)
                black_pixels_inc_cchoice = black_pixels_choice_ratio - black_pixels_c_ratio
                if is_same_c_ans_intersect and not abs(black_pixels_inc_cchoice - black_pixel_inc_ag) > 0.1:
                    potential_solutions[rmse] = choice
            if potential_solutions:
                return potential_solutions[min(potential_solutions.keys())]
        return -1



    #chop square frame into two halves vertically and compare, left, upper, right, lower
    def transformation_pixel_ratio_half_frame_vertical(self, image_a, image_b, image_c, problem_images):
        print('Solve by PIXEL RATIO HALF FRAME VERTICAL transformation')
        width, height = image_a.size
        image_a_first_half = image_a.crop((0,0,width/2, height))
        image_a_second_half = image_a.crop((width/2, 0, width, height))
        image_b_first_half = image_b.crop((0,0,width/2, height))
        image_b_second_half = image_b.crop((width/2, 0, width, height))
        image_c_first_half = image_c.crop((0,0,width/2, height))
        image_c_second_half = image_c.crop((width/2, 0, width, height))

        black_pixel_ratio_a_first_half = count_black_pixels(image_a_first_half) / count_total_pixels(image_a_first_half)
        black_pixel_ratio_b_first_half = count_black_pixels(image_b_first_half) / count_total_pixels(image_b_first_half)
        black_pixel_ratio_c_first_half = count_black_pixels(image_c_first_half) / count_total_pixels(image_c_first_half)

        black_pixel_ratio_a_second_half = count_black_pixels(image_a_second_half) / count_total_pixels(image_a_second_half)
        black_pixel_ratio_b_second_half = count_black_pixels(image_b_second_half) / count_total_pixels(image_b_second_half)
        black_pixel_ratio_c_second_half = count_black_pixels(image_c_second_half) / count_total_pixels(image_c_second_half)

        ratio_diff_first_ab = black_pixel_ratio_b_first_half - black_pixel_ratio_a_first_half
        ratio_diff_second_ab = black_pixel_ratio_b_second_half - black_pixel_ratio_a_second_half

        potential_solutions = []
        for choice in range(1, 7):
            image_choice = problem_images[str(choice)]
            image_choice_first_half = image_choice.crop((0, 0, width / 2, height))
            image_choice_second_half = image_choice.crop((width / 2, 0, width, height))
            black_pixel_ratio_choice_first_half = count_black_pixels(image_choice_first_half) / count_total_pixels(image_choice_first_half)
            black_pixel_ratio_choice_second_half = count_black_pixels(image_choice_second_half) / count_total_pixels(image_choice_second_half)

            ratio_diff_first_choicec = black_pixel_ratio_choice_first_half - black_pixel_ratio_c_first_half
            ratio_diff_second_choicec = black_pixel_ratio_choice_second_half - black_pixel_ratio_c_second_half

            if np.abs(ratio_diff_first_choicec - ratio_diff_first_ab) <= 0.005 and abs(ratio_diff_second_choicec - ratio_diff_second_ab) <= 0.005:
                potential_solutions.append(choice)

        if len(potential_solutions) == 1:
            return potential_solutions[0]

        return -1

    def transformation_and(self, problem_images, problem_type):
        print('Solve by AND transformation')
        image_a = problem_images['A']
        image_b = problem_images['B']
        image_c = problem_images['C']

        image_ab_and = ImageChops.logical_and(image_a, image_b)
        image_ac_and = ImageChops.logical_and(image_a, image_c)
        potential_choices = {}

        #A to B is add fill
        is_same_ab_and_add = check_if_same(image_ab_and, image_b)
        black_pixel_inc = count_black_pixels(image_b) - count_black_pixels(image_a)
        if is_same_ab_and_add:
            for choice in range(1, 7):
                image_choice = problem_images[str(choice)]
                image_cd_and = ImageChops.logical_and(image_c, image_choice)
                is_same_cd_and = check_if_same(image_cd_and, image_choice)
                if is_same_cd_and:
                    black_pixel_inc_cd = count_black_pixels(image_choice) - count_black_pixels(image_c)
                    potential_choices[black_pixel_inc_cd] = choice
            if potential_choices:
                key = min(potential_choices.keys(), key=lambda x: abs(x - black_pixel_inc))
                return potential_choices[key]

        #A to C is add fill
        is_same_ac_and_add = check_if_same(image_ac_and, image_c)
        black_pixel_inc = count_black_pixels(image_c) - count_black_pixels(image_a)
        if is_same_ac_and_add:
            for choice in range(1, 7):
                image_choice = problem_images[str(choice)]
                image_bd_and = ImageChops.logical_and(image_b, image_choice)
                is_same_bd_and = check_if_same(image_bd_and, image_choice)
                if is_same_bd_and:
                    black_pixel_inc_bd = count_black_pixels(image_choice) - count_black_pixels(image_b)
                    potential_choices[black_pixel_inc_bd] = choice
            if potential_choices:
                key = min(potential_choices.keys(), key=lambda x: abs(x - black_pixel_inc))
                return potential_choices[key]

        #A to B is remove fill
        is_same_ab_and_add = check_if_same(image_ab_and, image_a)
        black_pixel_dec = count_black_pixels(image_b) - count_black_pixels(image_a)
        if is_same_ab_and_add:
            for choice in range(1, 7):
                image_choice = problem_images[str(choice)]
                image_cd_and = ImageChops.logical_and(image_c, image_choice)
                is_same_cd_and = check_if_same(image_cd_and, image_c)
                if is_same_cd_and:
                    black_pixel_dec_cd = count_black_pixels(image_choice) - count_black_pixels(image_c)
                    potential_choices[black_pixel_dec_cd] = choice
            if potential_choices:
                key = min(potential_choices.keys(), key=lambda x: abs(x - black_pixel_dec))
                return potential_choices[key]

        #A to C is remove fill
        is_same_ac_and_add = check_if_same(image_ac_and, image_a)
        black_pixel_dec = count_black_pixels(image_c) - count_black_pixels(image_a)
        if is_same_ac_and_add:
            for choice in range(1, 7):
                image_choice = problem_images[str(choice)]
                image_bd_and = ImageChops.logical_and(image_b, image_choice)
                is_same_bd_and = check_if_same(image_bd_and, image_b)
                if is_same_bd_and:
                    black_pixel_dec_bd = count_black_pixels(image_choice) - count_black_pixels(image_b)
                    potential_choices[black_pixel_dec_bd] = choice
            if potential_choices:
                key = min(potential_choices.keys(), key=lambda x: abs(x - black_pixel_dec))
                return potential_choices[key]
        return -1


    def transformation_pixel_ratio_frame(self, problem_images, problem_type):
        print('Solve by PIXEL RATIO FRAME transformation')
        if problem_type == '2x2':
            image_a = problem_images['A']
            image_b = problem_images['B']
            image_c = problem_images['C']

            black_pixel_ratio_a = count_black_pixels(image_a) / count_total_pixels(image_a)
            black_pixel_ratio_b = count_black_pixels(image_b) / count_total_pixels(image_b)
            black_pixel_ratio_c = count_black_pixels(image_c) / count_total_pixels(image_c)

            black_pixels_ratio_diff_ab = black_pixel_ratio_b - black_pixel_ratio_a
            black_pixels_ratio_diff_ac = black_pixel_ratio_c - black_pixel_ratio_a

            potential_solutions = []
            for choice in range(1, 7):
                image_choice = problem_images[str(choice)]
                black_pixel_ratio_image_choice = count_black_pixels(image_choice) / count_total_pixels(image_choice)
                if black_pixel_ratio_image_choice - black_pixel_ratio_c == black_pixels_ratio_diff_ab:
                    potential_solutions.append(choice)

            if len(potential_solutions) == 1:
                return potential_solutions[0]

            potential_solutions = []
            for choice in range(1, 7):
                image_choice = problem_images[str(choice)]
                black_pixel_ratio_image_choice = count_black_pixels(image_choice) / count_total_pixels(image_choice)
                if black_pixel_ratio_image_choice - black_pixel_ratio_b == black_pixels_ratio_diff_ac:
                    potential_solutions.append(choice)

            if len(potential_solutions) == 1:
                return potential_solutions[0]
        elif problem_type == '3x3':
            image_a = problem_images['A']
            image_b = problem_images['B']
            image_c = problem_images['C']
            image_d = problem_images['D']
            image_e = problem_images['E']
            image_f = problem_images['F']
            image_g = problem_images['G']
            image_h = problem_images['H']

            black_pixel_ratio_a = count_black_pixels(image_a) / count_total_pixels(image_a)
            black_pixel_ratio_b = count_black_pixels(image_b) / count_total_pixels(image_b)
            black_pixel_ratio_c = count_black_pixels(image_c) / count_total_pixels(image_c)
            black_pixel_ratio_d = count_black_pixels(image_d) / count_total_pixels(image_d)
            black_pixel_ratio_e = count_black_pixels(image_e) / count_total_pixels(image_e)
            black_pixel_ratio_f = count_black_pixels(image_f) / count_total_pixels(image_f)
            black_pixel_ratio_g = count_black_pixels(image_g) / count_total_pixels(image_g)
            black_pixel_ratio_h = count_black_pixels(image_h) / count_total_pixels(image_h)


            black_pixels_ratio_diff_ab = black_pixel_ratio_b - black_pixel_ratio_a
            black_pixels_ratio_diff_bc = black_pixel_ratio_c - black_pixel_ratio_b

            black_pixels_ratio_diff_be = black_pixel_ratio_e - black_pixel_ratio_b

            black_pixels_ratio_diff_ad = black_pixel_ratio_d - black_pixel_ratio_a
            black_pixels_ratio_diff_gd = black_pixel_ratio_g - black_pixel_ratio_d
            black_pixels_ratio_diff_cf = black_pixel_ratio_f - black_pixel_ratio_c
            black_pixels_ratio_diff_gh = black_pixel_ratio_h - black_pixel_ratio_g
            black_pixels_ratio_diff_de = black_pixel_ratio_e - black_pixel_ratio_d
            black_pixels_ratio_diff_ef = black_pixel_ratio_f - black_pixel_ratio_e
            black_pixels_ratio_diff_eh = black_pixel_ratio_h - black_pixel_ratio_e

            horizontal_increase = False
            if black_pixels_ratio_diff_ab > 0 and black_pixels_ratio_diff_bc > 0:
                horizontal_increase = True

            potential_solutions = []
            for choice in range(1, 9):
                image_choice = problem_images[str(choice)]
                black_pixel_ratio_image_choice = count_black_pixels(image_choice) / count_total_pixels(image_choice)
                ratio_diff_horizontal = black_pixel_ratio_image_choice - black_pixel_ratio_h
                ratio_diff_vertical = black_pixel_ratio_image_choice - black_pixel_ratio_f
                if (horizontal_increase and ratio_diff_horizontal < 0) or abs(ratio_diff_horizontal/black_pixels_ratio_diff_ef) <= 0.09:
                    continue
                #horizontal increase ratio same
                if abs(black_pixels_ratio_diff_bc - black_pixels_ratio_diff_ab) <= 0.005:
                    if abs(ratio_diff_horizontal - black_pixels_ratio_diff_gh) <= 0.005:
                        potential_solutions.append(choice)
                        continue
                if abs(ratio_diff_horizontal - ratio_diff_vertical) <= 0.0001:
                    potential_solutions.append(choice)
            if len(potential_solutions) == 1:
                return potential_solutions[0]

            vertical_increase = False
            if black_pixels_ratio_diff_cf > 0 and black_pixels_ratio_diff_be > 0:
                vertical_increase = True

            potential_solutions = []
            for choice in range(1, 9):
                image_choice = problem_images[str(choice)]
                black_pixel_ratio_image_choice = count_black_pixels(image_choice) / count_total_pixels(image_choice)
                ratio_diff_vertical = black_pixel_ratio_image_choice - black_pixel_ratio_f
                if (vertical_increase and ratio_diff_vertical < 0):
                    continue
                if abs(ratio_diff_vertical - black_pixels_ratio_diff_cf) <= 0.01:
                    potential_solutions.append(choice)
            if len(potential_solutions) == 1:
                return potential_solutions[0]

            black_pixels_ratio_diff_ac = black_pixel_ratio_c/black_pixel_ratio_a
            potential_solutions = []
            for choice in range(1, 9):
                image_choice = problem_images[str(choice)]
                black_pixel_ratio_image_choice = count_black_pixels(image_choice) / count_total_pixels(image_choice)
                ratio_diff_horizontal = black_pixel_ratio_image_choice/black_pixel_ratio_g
                if abs(ratio_diff_horizontal - black_pixels_ratio_diff_ac) <= 0.05:
                    potential_solutions.append(choice)
                if len(potential_solutions) == 1:
                    return potential_solutions[0]
        return -1

    def transformation_unchanged(self, problem_images, problem_type):
        print('Solve by UNCHANGED transformation')
        if problem_type == '2x2':
            image_a = problem_images['A']
            image_b = problem_images['B']
            image_c = problem_images['C']

            is_same_ab = check_if_same(image_a, image_b)
            is_same_ac = check_if_same(image_a, image_c)
            #both A to B and A to C are unchanged
            if is_same_ab and is_same_ac:
                answers = get_answer_by_image(image_c, problem_images, problem_type)
                if (len(answers) == 1):
                    return answers[0]
            #A and C are unchanged
            elif is_same_ac:
                answers = get_answer_by_image(image_b, problem_images, problem_type)
                if (len(answers) == 1):
                    return answers[0]
            elif is_same_ab:
                answers = get_answer_by_image(image_c, problem_images, problem_type)
                if (len(answers) == 1):
                    return answers[0]
        if problem_type == '3x3':
            image_a = problem_images['A']
            image_b = problem_images['B']
            image_c = problem_images['C']
            image_d = problem_images['D']
            image_f = problem_images['F']
            image_g = problem_images['G']
            image_h = problem_images['H']

            is_same_ab = check_if_same(image_a, image_b)
            is_same_bc = check_if_same(image_b, image_c)
            is_same_ad = check_if_same(image_a, image_d)
            is_same_dg = check_if_same(image_d, image_g)
            is_same_gh = check_if_same(image_g, image_h)
            is_same_cf = check_if_same(image_c, image_f)

            if is_same_ab and is_same_bc and is_same_gh:
                answers = get_answer_by_image(image_h, problem_images, problem_type)
                if (len(answers) == 1):
                    return answers[0]
            elif is_same_ad and is_same_dg and is_same_cf:
                answers = get_answer_by_image(image_f, problem_images, problem_type)
                if (len(answers) == 1):
                    return answers[0]
        return -1

    def transformation_y_axis_reflection(self, problem_images, problem_type):
        print('Solve by Y-AXIS REFLECTION transformation')
        if problem_type == '2x2':
            image_a = problem_images['A']
            image_b = problem_images['B']
            image_c = problem_images['C']

            image_a_reflected = image_a.transpose(Image.FLIP_LEFT_RIGHT)

            is_same_ab = check_if_same(image_b, image_a_reflected)
            if is_same_ab:
                image_c_reflected = image_c.transpose(Image.FLIP_LEFT_RIGHT)
                answers = get_answer_by_image(image_c_reflected, problem_images, problem_type)
                if (len(answers) == 1):
                    return answers[0]

            is_same_ac = check_if_same(image_c, image_a_reflected)
            if is_same_ac:
                image_b_reflected = image_b.transpose(Image.FLIP_LEFT_RIGHT)
                answers = get_answer_by_image(image_b_reflected, problem_images, problem_type)
                if (len(answers) == 1):
                    return answers[0]
        elif problem_type == '3x3':
            image_a = problem_images['A']
            image_c = problem_images['C']
            image_d = problem_images['D']
            image_f = problem_images['F']
            image_g = problem_images['G']

            image_a_reflected = image_a.transpose(Image.FLIP_LEFT_RIGHT)
            image_d_reflected = image_d.transpose(Image.FLIP_LEFT_RIGHT)

            is_same_ac = check_if_same(image_c, image_a_reflected)
            is_same_df = check_if_same(image_f, image_d_reflected)
            #reflection from first to third frames
            if is_same_ac and is_same_df:
                image_g_reflected = image_g.transpose(Image.FLIP_LEFT_RIGHT)
                answers = get_answer_by_image(image_g_reflected, problem_images, problem_type)
                if (len(answers) == 1):
                    return answers[0]
        return -1

    def transformation_x_axis_reflection(self, problem_images, problem_type):
        print('Solve by X-AXIS REFLECTION transformation')
        image_a = problem_images['A']
        image_b = problem_images['B']
        image_c = problem_images['C']

        image_a_vertical_reflected = image_a.transpose(Image.FLIP_TOP_BOTTOM)

        is_same_ab = check_if_same(image_b, image_a_vertical_reflected)
        if is_same_ab:
            image_c_reflected = image_c.transpose(Image.FLIP_TOP_BOTTOM)
            answers = get_answer_by_image(image_c_reflected, problem_images, problem_type)
            if (len(answers) == 1):
                return answers[0]

        is_same_ac = check_if_same(image_c, image_a_vertical_reflected)
        if is_same_ac:
            image_b_reflected = image_b.transpose(Image.FLIP_TOP_BOTTOM)
            answers = get_answer_by_image(image_b_reflected, problem_images, problem_type)
            if (len(answers) == 1):
                return answers[0]
        return -1

    def transformation_rotation(self, problem_images, problem_type):
        print('Solve by ROTATION transformation')
        image_a = problem_images['A']
        image_b = problem_images['B']
        image_c = problem_images['C']

        degrees = [-45, -90, -135, -180, -225, -270, -315]
        for angle in degrees:
            image_a_rotated = image_a.rotate(angle)
            is_same_ab = check_if_same(image_a_rotated, image_b)
            is_same_ac = check_if_same(image_a_rotated, image_c)

            if is_same_ab:
                solutions = []
                image_c_rotated = image_c.rotate(angle)
                for choice in range(1,7):
                    image_choice = problem_images[str(choice)]
                    is_same_cd = check_if_same(image_c_rotated, image_choice)
                    if is_same_cd:
                        solutions.append(choice)
                return solutions[0] if len(solutions) == 1 else -1

            if is_same_ac:
                solutions = []
                image_b_rotated = image_b.rotate(angle)
                for choice in range(1,7):
                    image_choice = problem_images[str(choice)]
                    is_same_bd = check_if_same(image_b_rotated, image_choice)
                    if is_same_bd:
                        solutions.append(choice)
                return solutions[0] if len(solutions) == 1 else -1
        return -1

    def transformation_pixel_diff(self, problem_images, problem_type):
        print('Solve by PIXEL DIFFERENCE transformation')
        if problem_type == '2x2':
            image_a = problem_images['A']
            image_b = problem_images['B']
            image_c = problem_images['C']

            image_a_black = count_black_pixels(image_a)
            image_b_black = count_black_pixels(image_b)
            image_c_black = count_black_pixels(image_c)

            diff_ab = image_a_black - image_b_black
            diff_ac = image_a_black - image_c_black

            solutions = []
            for choice in range(1,7):
                image_choice = problem_images[str(choice)]
                image_choice_black = count_black_pixels(image_choice)
                curr_diff = image_c_black - image_choice_black
                if diff_ab - curr_diff <= 5:
                    solutions.append(choice)
            if (len(solutions) == 1):
                return solutions[0]

            for choice in range(1,7):
                image_choice = problem_images[str(choice)]
                image_choice_black = count_black_pixels(image_choice)
                curr_diff = image_b_black - image_choice_black
                if diff_ac - curr_diff <= 5:
                    solutions.append(choice)
            return solutions[0] if len(solutions) == 1 else -1

