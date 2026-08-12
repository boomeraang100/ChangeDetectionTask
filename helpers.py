from psychopy import visual, core, event
from PIL import Image
import numpy as np
import pandas as pd
import params as pm
import random
import os
import csv
from stimulus import BlockStimulus


def initialize_window():
    # initialize PsychoPy window
    # mon = monitors.Monitor('myMonitor', width=28.5, distance=70.0) #TODO width=pm.MON_WIDTH, distance=pm.MON_DISTANCE
    return visual.Window(fullscr=pm.FULLSCREEN, color = pm.BACKGROUND_COLOR, units=pm.UNITS)

def stim_list(win) -> list:
  stim_list = []
  for stim in range(len(pm.STIM_POS)):
    stim_list.append(BlockStimulus(win=win, pos=pm.STIM_POS[stim], color=pm.STIM_COLORS[stim]))
  return stim_list

def change_color(target: BlockStimulus, alt_color) -> list:
  target.square.color = alt_color

def clear_screen(win):
  """ clear up the PsychoPy window"""

  win.fillColor = pm.BACKGROUND_COLOR
  win.flip()

def change_detection(win, wait_for_keypress=True):
  msg = visual.TextStim(win, pm.RESPONSE_1_TEXT)
  clear_screen(win)
  msg.draw()
  win.flip()

  # wait indefinitely, terminates upon any key press
  if wait_for_keypress:
    while True:
      keys = event.waitKeys(keyList=['escape', 'y', 'n'])
      if 'escape' in keys:
        win.close()
        core.quit()
      if 'y' in keys:
        break
      if 'n' in keys:
        break
    clear_screen(win)

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