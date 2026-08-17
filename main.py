from psychopy import visual, core, event, gui, logging
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
from utils.config import import_config

def main(
  debug: bool = False,
):
  # Switch to the script folder
  """Run the experiment.

    Args:
        debug: (bool) If True, run in debug mode.
    Returns:
        None (psychopy window, data file (.csv, .log, .psydata))
    """
  # Logging settings
  if not debug:
      # logging.console.setLevel(logging.EXP)
      log_file_level = logging.INFO
  else:
      #logging.console.setLevel(logging.INFO)
      log_file_level = logging.DEBUG
      logging.info("### Debug mode enabled. ###")

  print("starting dialog")
  script_path = os.path.dirname(sys.argv[0])
  if len(script_path) != 0:
    os.chdir(script_path)
    
  dlg = gui.Dlg(title = "Introduce participant's ID")
  dlg.addField('Participant ID') #, required = True
  ok_data = dlg.show()
  if dlg.OK:
    if ok_data[0].strip() == '':
      print('No participant alias was entered.\nPlease start again and fill in alias.')
      quit()
    participantID = ok_data[0]
  else:
      quit()
  print("starting done")
      
  ## Does data folder exist? If not create it
  print("data file")
  os.makedirs(os.path.dirname(__file__)+"/data", exist_ok=True)
  print("data file done")

  ## Does participant's folder exist? If not create it
  print("participant file")
  participant_folder = os.path.dirname(__file__)+"/data/"+ participantID
  os.makedirs(participant_folder, exist_ok=True)
  print("participant file done")
  print("initialise window", flush=True)

  package_name = os.path.dirname(__file__).split(os.path.sep)[-1]

  config = import_config(
        debug=debug,
        file_name= r"C:\Users\Haniah\ChangeDetectionTask\config.yml",
    )

  win = hp.initialize_window(config)
  print("initialise window done", flush=True)
  
  #participant_folder = Path(__file__).parent / "data" / participantID
  #participant_folder.mkdir(parents=True, exist_ok=True)
  
  exp.run_exp(win=win)
  
main()