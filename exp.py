from psychopy import visual, core, data, event, logging
from psychopy.hardware import keyboard
#from psychopy import iohub
import params as pm
import helpers
import random
import os
import csv

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

def run_continuous_trial(win, cond, trialnr):
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
  print(trialnr)  
  stim_list = helpers.stim_list(win, cond)
  target_pos = random.choice(pm.STIM_POS.copy())
  csv_dict = helpers.csv_dict(cond)
  csv_dict["target"] = target_pos
  
  for block in stim_list:
    if block.pos == target_pos:
      csv_dict["target_color"] = block.color
    block.draw()

  win.flip()
  core.wait(pm.FIRST_DISPLAY_T)
  win.flip()
  core.wait(pm.BREAK_T)
  win.flip()
  csv_dict = helpers.continuous_report(win, target_pos, csv_dict)
  return csv_dict
        
def run_trial(win, trial_change, size_cond, target_cond, cond):
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
  
  stim_list = None
  targets_list = []
  csv_dict = helpers.csv_dict(cond)
  try:
    if cond == "set-size":
      csv_dict["set-size"] = size_cond[0]
      csv_dict["change_cond"] = size_cond[1]
      stim_list = helpers.stim_list(win, cond, set_size=size_cond[0])
      for i, block in enumerate(stim_list):
        print(i, block.pos, block.color)
    elif cond == "target":
      stim_list = helpers.stim_list(win)
  except:
    raise ValueError(f"No valid condition chosen: {cond}")
  if trial_change:
    if cond == "set-size":
      target = random.choice(stim_list)
      csv_dict["target"] = target.square.pos
    else:
      copy_stim_list = stim_list.copy()
      for tar in range(target_cond):
        target = random.choice(copy_stim_list)
        copy_stim_list.remove(target)
        targets_list.append(target)
        

  # begin with displaying all blocks
  for block in stim_list:
    block.draw()

  win.flip()
  core.wait(pm.FIRST_DISPLAY_T)
  win.flip()
  core.wait(pm.BREAK_T)
  target_counter = 1
  for block in range(len(stim_list)):
    if trial_change:
      if cond == "set-size":
        if stim_list[block] is target:
          old_color = target.color
          csv_dict["old_color"] = old_color
          previous_block = stim_list[(block - 1) % len(stim_list)]
          next_block = stim_list[(block + 1) % len(stim_list)]
          available_colors = [
            color for color in pm.PALETTE
            if color != old_color
            and color != previous_block.color
            and color != next_block.color
          ]
          new_color = random.choice(available_colors)
          target.color = new_color
          target.square.color = new_color
          csv_dict["new_color"] = new_color
      else: #target condition
        if stim_list[block] in targets_list:
          csv_dict[f"target-{target_counter}"] = stim_list[block].square.pos
          old_color = stim_list[block].color
          csv_dict[f"old_color-{target_counter}"] = old_color
          new_color = target.color
          while new_color == old_color:
            new_color = random.choice(pm.PALETTE_TAR)
            csv_dict[f"new_color-{target_counter}"] = new_color
          stim_list[block].square.color = new_color
          target_counter += 1
    stim_list[block].draw()
  win.flip()
  core.wait(pm.SECOND_DISPLAY_T)
  win.flip()
  core.wait(pm.MASK_BEFORE_RESPONSE)
  change_detected = helpers.change_detection(win, csv_dict)
  csv_dict["change_detected"] = change_detected
  return csv_dict

def run_block2(win, participant_id, data_dir, cond, block):
  sequence = helpers.set_size_seq2()
  for trial in range(pm.TRIALS_PER_BLOCK):
    trial_cond = sequence.pop(0)
    csv_dict = run_trial(win, trial_cond[1], trial_cond[0], None, cond)
    helpers.update(participant_id=participant_id, data_dir=data_dir, cond=cond, block=block, trial_nr=trial, csv_dict=csv_dict)

def run_block(win, participant_id, data_dir, cond, block):
  change_seq = helpers.change_seq()
  size_seq = []
  target_seq = []
  continuous_seq = []
  try:
    if cond == "set-size":
      size_seq = helpers.set_size_seq2()
      print(size_seq)
    elif cond == "target":
      target_seq = helpers.target_seq()
    elif cond == "continuous":
      continuous_seq = helpers.continuous_seq()
  except:
    raise Exception("No valid condition chosen")
  for trial in range(pm.TRIALS_PER_BLOCK):
    # pop = size_seq.pop(0)
    # print(pop)
    # trial_change = pop[1]
    trial_change = change_seq.pop(0)
    size_cond = None
    target_cond = None
    continuous_cond = None
    csv_dict = None
    if cond == "set-size":
      size_cond = size_seq.pop(0)
      csv_dict = run_trial(win, trial_change, size_cond, target_cond, cond)
      helpers.update(participant_id=participant_id, data_dir=data_dir, cond=cond, block=block, trial_nr=trial, csv_dict=csv_dict)
    elif cond == "target":
      target_cond = target_seq.pop(0)
      csv_dict = run_trial(win, trial_change, size_cond, target_cond, cond)
    elif cond == "continuous":
      continuous_cond = continuous_seq.pop(0)
      csv_dict = run_continuous_trial(win, cond, trial)
      helpers.update(participant_id=participant_id, data_dir=data_dir, cond=cond, block=block, trial_nr=trial, csv_dict=csv_dict)
  

def run_exp(win, participant_id, data_dir, cond):
  #io = iohub.launchHubServer(window=win)
  #mouse = io.devices.mouse

  for block in range(pm.BLOCKS):
    run_block(win, participant_id, data_dir, cond, block)
    if block + 1 < pm.BLOCKS:
      show_msg(win, text="Now, you can take a break.\nPress enter to continue.")
  
  win.close()
  core.quit()
