from psychopy import visual, core, event, gui
#from ReachingTask import rt_params
#import pylink
import platform
import params
import helpers as hp
import random
import sys
import os
import exp
from pathlib import Path

def main():
  # Switch to the script folder
  script_path = os.path.dirname(sys.argv[0])
  if len(script_path) != 0:
    os.chdir(script_path)
    
  dlg = gui.Dlg(title = "Introduce participant's ID")
  dlg.addField('Participant ID', required = True)
  ok_data = dlg.show()
  if dlg.OK:
    if ok_data[0].strip() == '':
      print('No participant alias was entered.\nPlease start again and fill in alias.')
      quit()
    participantID = ok_data[0]
  else:
      quit()
      
  ## Does data folder exist? If not create it
  os.makedirs(os.path.dirname(__file__)+"/data", exist_ok=True)
  
  ## Does participant's folder exist? If not create it
  participant_folder = os.path.dirname(__file__)+"/data/"+ participantID
  os.makedirs(participant_folder, exist_ok=True)
  win = hp.initialize_window()
  
  #participant_folder = Path(__file__).parent / "data" / participantID
  #participant_folder.mkdir(parents=True, exist_ok=True)
  
  exp.run_exp(win=win)
  
main()