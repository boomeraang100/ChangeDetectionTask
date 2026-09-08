from psychopy import visual, core, event
from PIL import Image
import numpy as np
import pandas as pd
import params as pm
import random
import os
import csv
from stimulus import BlockStimulus
import math
#from utils.monitors import load_default_monitor


def initialize_window():
  # initialize PsychoPy window
  win = visual.Window(size=(1920, 1080), fullscr=True, color = pm.BACKGROUND_COLOR, units=pm.UNITS, screen=1)
  return win

def update(participant_id, data_dir, cond, block, trial_nr, csv_dict):
  '''
  Create new csv file if needed and add new row of data
  '''
  # Define filename/-path of a trial, create path if it does not exist yet
  file_name = f"participant_{participant_id}_cond_{cond}.csv"
  file_path = os.path.join(data_dir, file_name)
  file_exists = os.path.exists(file_path)
  # Open csv file
  with open(file_path, "a", newline="") as f:
    writer = csv.writer(f)
    #write first line of csv file if not written yet
    if not file_exists:
      if cond == "set-size":
        writer.writerow(["cond", "block_nr", "trial_nr", "change", "set-size", "target", "old_color", "new_color", "change_detected", "rt"]) # reaction time
      elif cond == "target":
        writer.writerow(["cond", "block_nr", "trial_nr", "set-size", "target-1", "old_color-1", "new_color-1", "target-2", "old_color-2", "new_color-2", "target-3", "old_color-3", "new_color-3", "target-4", "old_color-4", "new_color-4", "change_detected"]) # reaction time
      else:
        writer.writerow(["cond", "block_nr", "trial_nr", "set-size", "target", "target_color", "selected_color", "rt"])
    # add row of data
    if cond == "set-size":
      writer.writerow([
        cond,
        block,
        trial_nr,
        csv_dict["change_cond"], 
        csv_dict["set-size"],
        csv_dict["target"],
        csv_dict["old_color"],
        csv_dict["new_color"],
        csv_dict["change_detected"],
        csv_dict["rt"]
      ])
    elif cond == "target":
      writer.writerow([
        cond,
        block,
        trial_nr,
        csv_dict["set-size"],
        csv_dict["target-1"],
        csv_dict["old_color-1"],
        csv_dict["new_color-1"],
        csv_dict["target-2"],
        csv_dict["old_color-2"],
        csv_dict["new_color-2"],
        csv_dict["target-3"],
        csv_dict["old_color-3"],
        csv_dict["new_color-3"],
        csv_dict["target-4"],
        csv_dict["old_color-4"],
        csv_dict["new_color-4"],
        csv_dict["change_detected"]
      ])
    else:
      writer.writerow([
        cond,
        block,
        trial_nr,
        csv_dict["set-size"],
        csv_dict["target"],
        csv_dict["target_color"],
        csv_dict["selected_color"],
        csv_dict["rt"],
      ])

def stim_list(win, cond, set_size: int = 8) -> list:
  stim_list = []
  pos_list = pm.STIM_POS.copy()
  colors_rgb255 = color_wheel_palette()
  #random.shuffle(pos_list)
  for stim in range(set_size):
    stim_pos=pos_list.pop(0)
    #if not cond == "continuous":
    if stim == 0:
      if not cond == "continuous":
        stim_color = random.choice(pm.PALETTE)
      else:
        stim_color = random.choice(colors_rgb255)
    else:
      previous_color = stim_list[-1].color
      if not cond == "continuous":
        available_colors = [
          color for color in pm.PALETTE
          if color != previous_color
        ]
      else:
        available_colors = [
          color for color in colors_rgb255
          if color != previous_color
        ]
      stim_color = random.choice(available_colors)
    #stim_color = random.choice(pm.PALETTE)
    block = BlockStimulus(win=win, pos=stim_pos, color=stim_color)
    block.pos = stim_pos
    if cond == "continuous":
      block.colorSpace = "rgb255"
      block.square.colorSpace = "rgb255"
    block.fillColor = stim_color
    block.square.fillColor = stim_color
    print(stim_color)
    stim_list.append(block)
      
  if set_size > 2 and stim_list[-1].color == stim_list[0].color:
    print(stim_list)
    if not cond == "continuous":
      available_colors = [
        color for color in pm.PALETTE
        if color != stim_list[-1].color
        and color != stim_list[-2].color
      ]
    else:
      available_colors = [
        color for color in colors_rgb255
        if color != stim_list[-1].color
        and color != stim_list[-2].color
      ]
    new_color = random.choice(available_colors)
    stim_list[-1].color = new_color
    stim_list[-1].square.color = new_color

  return stim_list

def empty_target(win, target_pos):
  target = BlockStimulus(win, color=None, pos=target_pos)
  target.square.lineColor = "black"
  return target

def color_wheel_palette():
  colors_rgb255 = []

  for n in range(1, pm.N_COLORS + 1):
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
  return colors_rgb255

def color_wheel(win):
  colors_rgb255 = color_wheel_palette()
  wheel_segments = []

  for i in range(pm.N_COLORS):
    # Angular boundaries of this segment
    angle_start = (2 * math.pi) * i / pm.N_COLORS
    angle_end = (2 * math.pi) * (i + 1) / pm.N_COLORS
    # Four corners of the annular segment
    vertices = [
      (
        pm.OUTER_RADIUS * math.cos(angle_start),
        pm.OUTER_RADIUS * math.sin(angle_start)
      ),
      (
        pm.OUTER_RADIUS * math.cos(angle_end),
        pm.OUTER_RADIUS * math.sin(angle_end)
      ),
      (
        pm.INNER_RADIUS * math.cos(angle_end),
        pm.INNER_RADIUS * math.sin(angle_end)
      ),
      (
        pm.INNER_RADIUS * math.cos(angle_start),
        pm.INNER_RADIUS * math.sin(angle_start)
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
      units='pix'
    )

    wheel_segments.append(segment)
  return wheel_segments

def continuous_report(win, target_pos, csv_dict):
  colors_rgb255 = color_wheel_palette()
  wheel_segments = color_wheel(win)
  target = empty_target(win, target_pos)
  mouse = event.Mouse(win=win, visible=True)
  instruction = visual.TextStim(
    win=win,
    text=pm.CONTINUOUS_REPORT_INSTR,
    pos=pm.CONTINUOUS_REPORT_POS,
    units='pix'
  )
  timer = core.Clock()
  instruction.draw()
  target.draw()
  #mouse.draw()
  for segment in wheel_segments:
    segment.draw()
  win.flip()
  mouse.clickReset()
  selected_color = None
  selected_rgb = None
  selected_angle = None
  while True:
    keys = event.getKeys(keyList=['escape', 'return'])
    if 'escape' in keys:
      win.close()
      core.quit()
    if 'return' in keys:
      if not selected_rgb == None:
        csv_dict["selected_color"] = selected_rgb
        csv_dict["rt"] = timer.getTime()
        break
    mouse_x, mouse_y = mouse.getPos()
    #print(mouse_x, mouse_y)
    # Distance from centre
    radius = math.sqrt(
      mouse_x ** 2 +
      mouse_y ** 2
    )
    if (
        pm.INNER_RADIUS <= radius <= pm.OUTER_RADIUS
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
            angle / (2 * math.pi) * pm.N_COLORS
        )
        # Safety bounds
        color_index = min(pm.N_COLORS - 1,max(0, color_index))
        selected_color = color_index + 1
        selected_rgb = colors_rgb255[color_index]
        selected_angle = math.degrees(angle)
        #print(
        #  "index:", selected_color,
        #  "angle:", selected_angle,
        #  "RGB:", selected_rgb
        #)
        target.square.colorSpace = 'rgb255'
        target.square.fillColor = selected_rgb
        target.square.lineColor = None
        
        instruction.draw()
        target.draw()
        for segment in wheel_segments:
            segment.draw()
        win.flip()
  return csv_dict

def change_color(target: BlockStimulus, alt_color) -> list:
  target.square.color = alt_color

def clear_screen(win):
  """ clear up the PsychoPy window"""

  win.fillColor = pm.BACKGROUND_COLOR
  win.flip()
  
def change_seq():
  sequence = [True, False]
  sequence = sequence * int(pm.TRIALS_PER_BLOCK/2)
  random.shuffle(sequence)
  return sequence

def set_size_seq2():
  sequence = pm.SET_SIZE_SEQ
  sequence = sequence * int(pm.TRIALS_PER_BLOCK/8) #int(pm.TRIALS_PER_BLOCK/8)
  random.shuffle(sequence)
  return sequence

def continuous_seq():
  sequence = pm.CONTINUOUS_SEQ
  sequence = sequence * int(pm.TRIALS_PER_BLOCK/4)
  random.shuffle(sequence)
  return sequence

def set_size_seq():
  sequence = [2, 4, 6, 8]
  #change_trials = int(pm.TRIALS_PER_BLOCK/2)
  sequence = sequence * int(pm.TRIALS_PER_BLOCK/4)
  random.shuffle(sequence)
  return sequence

def target_seq():
  sequence = pm.TARGET_SEQ
  sequence = sequence * int(pm.TRIALS_PER_BLOCK/5)
  random.shuffle(sequence)
  return sequence

def csv_dict(cond):
  if cond == "set-size":
    csv_dict = {
      "set-size": None,
      "change_cond": None,
      "target": None,
      "old_color": None,
      "new_color": None,
      "change_detected": None,
      "rt": None
    }
  elif cond == "target":
    csv_dict = {
      "set-size": 8,
      "change_cond": None,
      "nmbr_targets": None,
      "target-1": None,
      "old_color-1": None,
      "new_color-1": None,
      "target-2": None,
      "old_color-2": None,
      "new_color-2": None,
      "target-3": None,
      "old_color-3": None,
      "new_color-3": None,
      "target-4": None,
      "old_color-4": None,
      "new_color-4": None,
      "change_detected": None
    }
  else:
    csv_dict = {
      "set-size": 8,
      "target": None,
      "target_color": None,
      "selected_color": None,
      "rt": None
    }
  return csv_dict

def change_detection(win, csv_dict, wait_for_keypress=True):
  msg = visual.TextStim(win, pm.RESPONSE_1_TEXT)
  clear_screen(win)
  msg.draw()
  win.flip()
  timer = core.Clock()
  change_detected = None
  # wait indefinitely, terminates upon any key press
  if wait_for_keypress:
    while True:
      keys = event.waitKeys(keyList=['escape', 'y', 'n'])
      if 'escape' in keys:
        win.close()
        core.quit()
      if 'y' in keys:
        csv_dict["rt"] = timer.getTime()
        change_detected = True
        break
      if 'n' in keys:
        csv_dict["rt"] = timer.getTime()
        change_detected = False
        break
    clear_screen(win)
  return change_detected

def confidence_rating(win, wait_for_keypress=True):
  msg = visual.TextStim(win, pm.RESPONSE_2_TEXT)
  clear_screen(win)
  msg.draw()
  win.flip()

  # wait indefinitely, terminates upon any key press
  if wait_for_keypress:
    while True:
      keys = event.waitKeys(keyList=['escape', '1', '2', '3', '4'])
      if 'escape' in keys:
        win.close()
        core.quit()
      if '1' in keys:
        break
      if '2' in keys:
        break
      if '3' in keys:
        break
      if '4' in keys:
        break
    clear_screen(win)