###############################################
################### WINDOW ####################
###############################################

FULLSCREEN = True
BACKGROUND_COLOR = "grey"
UNITS = "pix"
SCREEN_WIDTH = 52.7 #cm
SCREEN_HEIGHT = 29.4 #cm
SCREEN_WIDTH_H = 28.5 #cm
SCREEN_HEIGHT_H = 18 #cm

###############################################
################## TEXTBOXES ##################
###############################################
INTRODUCTION_SET_SIZE = "This experiment consists of 4 blocks. In each block, you will see a set of squares multiple times. Every square has a different color. After their initial display, they will disappear and reappear shortly after.\nPress ENTER to continue."
INTRODUCTION_SET_SIZE_2 = "Your task is to identify any color change after the squares reappear. For your response, you can press the key \"y\" for yes, if you observed a color change, or \"n\" for no, if you did not observe a color change.\nPress ENTER to continue."
TAKING_BREAKS = "To start a trial, look at the fixation cross and press enter. You can take breaks at any time, except during a trial.\nPress ENTER to continue."
QUESTIONS = "Do you have any questions left? If so, you can ask your experimenter now.\nOtherwise, press ENTER to start the experiment."
RESPONSE_1_TEXT = "Have noticed a change in block colors?\nPlease press the key that corresonds to your answer.\ny = Yes, n = No"
RESPONSE_2_TEXT = "How confident are you in your judgment?\nPlease press the key that corresonds to your answer.\n1 = not sure; 4 = very confident"
CONTINUOUS_REPORT_INSTR = "Click the color that most closely matches the marked target's color."
CONTINUOUS_REPORT_POS = (0, 470)
REACHED_TARGET = "Success"
MISSED_TARGET = "Fail"
EXP_FINISHED = "You have finished the experiment.\nThank you for participating :)"

###############################################
################### STIMULI ###################
###############################################

STIM_POS = [(0, 400), (200, 200), (400, 0), (200, -200), (0, -400), (-200, -200), (-400, 0), (-200, 200)]
PALETTE1 = [(255, 34, 31), (255, 81, 31), (0, 250, 3), (20, 253, 255)] # red, blue, green, cyan
PALETTE2 = [(253, 254, 21), (255, 41, 255), (0, 11, 16), (7, 5, 255)] # yellow, purple, black, orange
FULL_PALETTE = [(255, 34, 31), (0, 248, 27), (0, 250, 3), (20, 253, 255), (253, 254, 21), (255, 41, 255), (0, 11, 16), (255, 81, 31)]
SQUARE_WIDTH = 50
SQUARE_HEIGHT = 50

###############################################
################### TRIALS ####################
###############################################

BLOCKS = 4
SET_SIZE_SEQ = [[3, True], [4, True], [6, True], [8, True], [3, False], [4, False], [6, False], [8, False]]
CONTINUOUS_SEQ = [3, 4, 6, 8]
TARGET_SEQ = [0, 1, 2, 3, 4]
TRIALS_PER_BLOCK = 40
FEEDBACK_TIME = 2 # sec
FIRST_DISPLAY_T = 0.1
BREAK_T = 1.5
SECOND_DISPLAY_T = 0.1
MASK_BEFORE_RESPONSE = 0.5

###############################################
################### TRIALS ####################
###############################################

N_COLORS = 252
OUTER_DIAMETER = 150
INNER_DIAMETER = 100
OUTER_RADIUS = OUTER_DIAMETER / 2.0
INNER_RADIUS = INNER_DIAMETER / 2.0