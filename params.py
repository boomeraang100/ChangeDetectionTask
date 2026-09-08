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

RESPONSE_1_TEXT = "Have noticed a change in block colors?\nPlease press the button that corresonds to your answer.\ny = Yes, n = No"
RESPONSE_2_TEXT = "How confident are you in your judgment?\nPlease press the button that corresonds to your answer.\n1 = not sure; 4 = very confident"
CONTINUOUS_REPORT_INSTR = "Click the color that most closely matches the marked target's color."
CONTINUOUS_REPORT_POS = (0, 470)
REACHED_TARGET = "Success"
MISSED_TARGET = "Fail"

###############################################
################### STIMULI ###################
###############################################

STIM_POS = [(0, 400), (200, 200), (400, 0), (200, -200), (0, -400), (-200, -200), (-400, 0), (-200, 200)]
PALETTE = [(57.2, 79.7, 62.8), (85.4, -87.2, 78.4), "green", (91.1, -41.6, -31.6), (97.2, -16.1, 91.4), (66.6, 97, -68.8), (2.1, -4.4, -3.8)]
PALETTE_TAR = [(57.2, 79.7, 62.8), (85.4, -87.2, 78.4), "green", (91.1, -41.6, -31.6), (97.2, -16.1, 91.4), (66.6, 97, -68.8), (2.1, -4.4, -3.8), (61.7, 68.4, 65.7)]
SQUARE_WIDTH = 50
SQUARE_HEIGHT = 50

###############################################
################### TRIALS ####################
###############################################

BLOCKS = 2
SET_SIZE_SEQ = [[3, True], [4, True], [6, True], [8, True], [3, False], [4, False], [6, False], [8, False]]
CONTINUOUS_SEQ = [3, 4, 6, 8]
TARGET_SEQ = [0, 1, 2, 3, 4]
TRIALS_PER_BLOCK = 8 #40
FEEDBACK_TIME = 2 # sec
FIRST_DISPLAY_T = 2
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