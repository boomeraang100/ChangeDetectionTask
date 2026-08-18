from psychopy import visual, core, event
from PIL import Image
import numpy as np
import pandas as pd
import params as pm
import random
import os
import csv
from stimulus import BlockStimulus
#from utils.monitors import load_default_monitor


def initialize_window():
    # initialize PsychoPy window
    win = visual.Window(fullscr=True, color = pm.BACKGROUND_COLOR, units=pm.UNITS, screen=1)
    return win

def stim_list(win, set_size: int = 8, tar: bool = False) -> list:
  stim_list = []
  pos_list = pm.STIM_POS.copy()
  random.shuffle(pos_list)
  for stim in range(set_size):
    stim_pos=pos_list.pop(0)
    if tar:
      stim_color = random.choice(pm.PALETTE)
    else:
      stim_color = random.choice(pm.PALETTE_TAR)
    block = BlockStimulus(win=win, pos=stim_pos, color=stim_color)
    block.pos = stim_pos
    block.color = stim_color
    stim_list.append(block)
  return stim_list

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

def set_size_seq():
  sequence = [2, 4, 6, 8]
  #change_trials = int(pm.TRIALS_PER_BLOCK/2)
  sequence = sequence * int(pm.TRIALS_PER_BLOCK/4)
  random.shuffle(sequence)
  return sequence

def target_seq():
  sequence = [1, 2, 3, 4]
  change_trials = int(pm.TRIALS_PER_BLOCK/2)
  sequence = sequence * int(change_trials/4)
  random.shuffle(sequence)
  return sequence

def csv_dict(cond):
  if cond == "set-size":
    csv_dict = {
      "set-size": None,
      "target": None,
      "old_color": None,
      "new_color": None,
      "change_detected": None
    }
  else:
    csv_dict = {
      "set-size": 8,
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
  return csv_dict

def change_detection(win, wait_for_keypress=True):
  msg = visual.TextStim(win, pm.RESPONSE_1_TEXT)
  clear_screen(win)
  msg.draw()
  win.flip()
  change_detected = None
  # wait indefinitely, terminates upon any key press
  if wait_for_keypress:
    while True:
      keys = event.waitKeys(keyList=['escape', 'y', 'n'])
      if 'escape' in keys:
        win.close()
        core.quit()
      if 'y' in keys:
        change_detected = True
        break
      if 'n' in keys:
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