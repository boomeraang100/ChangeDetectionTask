from psychopy import visual, core, event, monitors
import numpy as np
import math


# ============================================================
# Wilken & Ma (2004) - 252-color response wheel
# Experiments 7-9
#
# Wheel:
#   252 colors
#   Outer diameter = 3.0 degrees
#   Inner diameter = 2.1 degrees
#   Annulus thickness = 0.45 degrees
#
# Color palette:
#   CLUT values specified in the paper
#
# Response:
#   Mouse click on the color wheel
# ============================================================


# ------------------------------------------------------------
# 1. WINDOW
# ------------------------------------------------------------

# Create monitor specification
mon = monitors.Monitor('myMonitor')

# IMPORTANT:
# Replace these with the actual physical width of your monitor
# and your viewing distance.
mon.setWidth(28.5)       # monitor width in cm — CHANGE THIS
mon.setDistance(66.0)    # viewing distance in cm — CHANGE THIS

# Your actual screen resolution
mon.setSizePix((1680, 1050))

win = visual.Window(
    size=(1680, 1050),
    fullscr=True,
    monitor=mon,
    units='deg',
    color=[-0.82, -0.82, -0.82],
    colorSpace='rgb',
    waitBlanking=True
)


# ------------------------------------------------------------
# 2. WHEEL PARAMETERS
# ------------------------------------------------------------

N_COLORS = 252

OUTER_DIAMETER = 3.0
INNER_DIAMETER = 2.1

OUTER_RADIUS = OUTER_DIAMETER / 2.0
INNER_RADIUS = INNER_DIAMETER / 2.0


# ------------------------------------------------------------
# 3. CREATE THE 252-COLOR PALETTE
#
# The paper specifies:
#
# n = 1 ... 84:
#   255 * [1-n/84, n/84, 0]
#
# n = 85 ... 168:
#   255 * [0, 2-n/84, n/84-1]
#
# n = 169 ... 252:
#   255 * [n/84-2, 0, 3-n/84]
#
# Fractional values are rounded upward.
# ------------------------------------------------------------

colors_rgb255 = []

for n in range(1, N_COLORS + 1):

    if n <= 84:

        r = 255 * (1 - n / 84)
        g = 255 * (n / 84)
        b = 0

    elif n <= 168:

        r = 0
        g = 255 * (2 - n / 84)
        b = 255 * (n / 84 - 1)

    else:

        r = 255 * (n / 84 - 2)
        g = 0
        b = 255 * (3 - n / 84)

    # "rounded to the next highest whole number"
    r = math.ceil(r)
    g = math.ceil(g)
    b = math.ceil(b)

    # Make absolutely sure numerical floating-point
    # errors cannot produce values outside 0-255.
    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))

    colors_rgb255.append([r, g, b])


# ------------------------------------------------------------
# 4. CREATE THE 252 WHEEL SEGMENTS
#
# Color 1 starts at 0 degrees (right side).
# Colors increase counter-clockwise.
#
# The paper does not specify the rotational starting position,
# so this is a necessary implementation choice.
# ------------------------------------------------------------

wheel_segments = []

for i in range(N_COLORS):

    # Angular boundaries of this segment
    angle_start = (2 * math.pi) * i / N_COLORS
    angle_end = (2 * math.pi) * (i + 1) / N_COLORS

    # Four corners of the annular segment
    vertices = [
        (
            OUTER_RADIUS * math.cos(angle_start),
            OUTER_RADIUS * math.sin(angle_start)
        ),
        (
            OUTER_RADIUS * math.cos(angle_end),
            OUTER_RADIUS * math.sin(angle_end)
        ),
        (
            INNER_RADIUS * math.cos(angle_end),
            INNER_RADIUS * math.sin(angle_end)
        ),
        (
            INNER_RADIUS * math.cos(angle_start),
            INNER_RADIUS * math.sin(angle_start)
        )
    ]

    segment = visual.ShapeStim(
        win=win,
        vertices=vertices,
        closeShape=True,
        fillColor=colors_rgb255[i],
        lineColor=colors_rgb255[i],
        colorSpace='rgb255',
        interpolate=True,
        units='deg'
    )

    wheel_segments.append(segment)


# ------------------------------------------------------------
# 5. OPTIONAL CENTRAL FIXATION/REFERENCE POINT
#
# The paper describes the wheel as an annulus, so the centre
# is empty. We leave it empty here.
# ------------------------------------------------------------


# ------------------------------------------------------------
# 6. MOUSE
# ------------------------------------------------------------

mouse = event.Mouse(
    win=win,
    visible=True
)


# ------------------------------------------------------------
# 7. DISPLAY INSTRUCTIONS
# ------------------------------------------------------------

instruction = visual.TextStim(
    win=win,
    text="Click the color that most closely matches the remembered color.",
    height=0.5,
    pos=(0, -3.0),
    color='white',
    units='deg'
)

instruction.draw()

for segment in wheel_segments:
    segment.draw()

win.flip()


# ------------------------------------------------------------
# 8. WAIT FOR MOUSE CLICK
# ------------------------------------------------------------

mouse.clickReset()

selected_color = None
selected_rgb = None
selected_angle = None


while selected_color is None:

    # Allow experimenter to quit with ESC
    if 'escape' in event.getKeys():
        win.close()
        core.quit()

    # Draw wheel
    for segment in wheel_segments:
        segment.draw()

    instruction.draw()

    win.flip()

    # Mouse coordinates are in degrees because the window
    # uses units='deg'.
    mouse_x, mouse_y = mouse.getPos()

    # Distance from centre
    radius = math.sqrt(
        mouse_x ** 2 +
        mouse_y ** 2
    )

    # Only accept clicks on the annulus
    if (
        INNER_RADIUS <= radius <= OUTER_RADIUS
        and mouse.getPressed()[0]
    ):

        # ----------------------------------------------------
        # Calculate angle
        #
        # atan2 gives:
        #   0 degrees = right
        #   positive = counter-clockwise
        # ----------------------------------------------------

        angle = math.atan2(
            mouse_y,
            mouse_x
        )

        # Convert -pi ... +pi to 0 ... 2pi
        angle = (angle + 2 * math.pi) % (2 * math.pi)

        # Convert angle to color index
        color_index = int(
            angle / (2 * math.pi) * N_COLORS
        )

        # Safety bounds
        color_index = min(
            N_COLORS - 1,
            max(0, color_index)
        )

        selected_color = color_index + 1
        selected_rgb = colors_rgb255[color_index]
        selected_angle = math.degrees(angle)

        break

    core.wait(0.001)


# ------------------------------------------------------------
# 9. PRINT RESPONSE
# ------------------------------------------------------------

print("--------------------------------------------")
print("Wilken & Ma color-wheel response")
print("--------------------------------------------")
print("Selected color number:", selected_color)
print("RGB / CLUT value:", selected_rgb)
print("Angle (degrees):", selected_angle)
print("--------------------------------------------")


# ------------------------------------------------------------
# 10. DISPLAY SELECTED COLOR
# ------------------------------------------------------------

selected_patch = visual.Rect(
    win=win,
    width=2.0,
    height=2.0,
    pos=(0, -3.0),
    fillColor=selected_rgb,
    lineColor=selected_rgb,
    colorSpace='rgb255',
    units='deg'
)

response_text = visual.TextStim(
    win=win,
    text=f"Selected color: {selected_color}",
    height=0.5,
    pos=(0, 3.0),
    color='white',
    units='deg'
)

for segment in wheel_segments:
    segment.draw()

selected_patch.draw()
response_text.draw()

win.flip()

core.wait(2.0)


# ------------------------------------------------------------
# 11. CLOSE
# ------------------------------------------------------------

win.close()
core.quit()