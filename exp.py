from psychopy import visual, core, data, event, logging
from psychopy.hardware import keyboard
#from psychopy import iohub
import params as pm
import helpers
import random

def show_msg(win, text, wait_for_keypress=True):
  """ Show task instructions on screen"""

  msg = visual.TextStim(win, text,
                        wrapWidth=pm.SCREEN_WIDTH_H/2)
  helpers.clear_screen(win)
  msg.draw()
  win.flip()

  # wait indefinitely, terminates upon any key press
  if wait_for_keypress:
    while True:
      keys = event.waitKeys(keyList=['return', 'escape'])
      if 'return' in keys:
        break
      if 'escape' in keys:
        win.close()
        core.quit()
    helpers.clear_screen(win)

def feedback(win, success):
  if success:
    msg = visual.TextStim(win, pm.REACHED_TARGET)
  else:
    msg = visual.TextStim(win, pm.MISSED_TARGET)
  helpers.clear_screen(win)
  msg.draw()
  win.flip()
  core.wait(pm.FEEDBACK_TIME)

def run_trial(win):
  visual.ImageStim(win, image=f"images/fixTarget.bmp").draw()
  timer = core.Clock()
  win.flip()
  while True:
    keys = event.waitKeys(keyList=['escape', 'return'])
    if 'escape' in keys:
      win.close()
      core.quit()
    elif 'return' in keys and timer.getTime() > 0.2:
      break
          
  stim_list = helpers.stim_list(win)
  do_change = random.choice([True, False])
  if do_change:
    target = random.choice(stim_list)

  # begin with displaying all blocks
  for block in stim_list:
    block.draw()

  win.flip()
  core.wait(pm.FIRST_DISPLAY_T)
  win.flip()
  core.wait(pm.BREAK_T)
  for block in stim_list:
    if do_change:
      if block is target:
        target.square.color = pm.ALT_COLOR
    block.draw()
  win.flip()
  core.wait(pm.SECOND_DISPLAY_T)
  helpers.change_detection(win)
  helpers.confidence_rating(win)

def run_trials(win, trials_num):
  for trial in range(trials_num):
    run_trial(win)

def run_exp(win):
    #io = iohub.launchHubServer(window=win)
    #mouse = io.devices.mouse

    run_trials(win, pm.TRIALS_NUM)
    
    win.close()
    core.quit()
