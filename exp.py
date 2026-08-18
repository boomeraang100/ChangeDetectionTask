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
          writer.writerow(["cond", "block_nr", "trial_nr", "set-size", "target", "old_color", "new_color", "change_detected"])
        else:
          writer.writerow(["cond", "block_nr", "trial_nr", "set-size", "target-1", "old_color-1", "new_color-1", "target-2", "old_color-2", "new_color-2", "target-3", "old_color-3", "new_color-3", "target-4", "old_color-4", "new_color-4", "change_detected"])
      # add row of data
      if cond == "set-size":
        writer.writerow([
          cond,
          block,
          trial_nr,
          csv_dict["set-size"],
          csv_dict["target"],
          csv_dict["old_color"],
          csv_dict["new_color"],
          csv_dict["change_detected"]
        ])
      else:
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
      csv_dict["set-size"] = size_cond
      stim_list = helpers.stim_list(win, set_size=size_cond)
    elif cond == "target":
      stim_list = helpers.stim_list(win, tar=True)
  except:
    raise Exception("No valid condition chosen")
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
  for block in stim_list:
    if trial_change:
      if cond == "set-size":
        if block is target:
          old_color = block.color
          csv_dict["old_color"] = old_color
          new_color = target.color
          while new_color == old_color:
            new_color = random.choice(pm.PALETTE)
          target.square.color = new_color
          csv_dict["new_color"] = new_color
      else: #target condition
        if block in targets_list:
          csv_dict[f"target-{target_counter}"] = block.square.pos
          old_color = block.color
          csv_dict[f"old_color-{target_counter}"] = old_color
          new_color = target.color
          while new_color == old_color:
            new_color = random.choice(pm.PALETTE_TAR)
            csv_dict[f"new_color-{target_counter}"] = new_color
          block.square.color = new_color
          target_counter += 1
    block.draw()
  win.flip()
  core.wait(pm.SECOND_DISPLAY_T)
  change_detected = helpers.change_detection(win)
  csv_dict["change_detected"] = change_detected
  return csv_dict

def run_block(win, participant_id, data_dir, cond, block):
  change_seq = helpers.change_seq()
  size_seq = []
  target_seq = []
  try:
    if cond == "set-size":
      size_seq = helpers.set_size_seq()
    elif cond == "target":
      target_seq = helpers.target_seq()
  except:
    raise Exception("No valid condition chosen")
  for trial in range(pm.TRIALS_PER_BLOCK):
    trial_change = change_seq.pop(0)
    size_cond = None
    target_cond = None
    if cond == "set-size":
      size_cond = size_seq.pop(0)
    elif cond == "target":
      if trial_change:
        target_cond = target_seq.pop(0)
    csv_dict = run_trial(win, trial_change, size_cond, target_cond, cond)
    update(participant_id=participant_id, data_dir=data_dir, cond=cond, block=block, trial_nr=trial, csv_dict=csv_dict)
  

def run_exp(win, participant_id, data_dir, cond):
  #io = iohub.launchHubServer(window=win)
  #mouse = io.devices.mouse

  for block in range(pm.BLOCKS):
    run_block(win, participant_id, data_dir, cond, block)
    if block + 1 < pm.BLOCKS:
      show_msg(win, text="Now, you can take a break.\nPress enter to continue.")
  
  win.close()
  core.quit()
