from psychopy import gui
import src.assets.helpers as hp
import src.exp as exp
import sys
import os

def main():
  # Switch to the script folder
  
  
  script_path = os.path.dirname(sys.argv[0])
  if len(script_path) != 0:
    os.chdir(script_path)
    
  dlg = gui.Dlg(title = "Introduce participant's ID")
  dlg.addField('Participant ID') #, required = True
  dlg.addField('Condition', choices = ["Select...", "set-size", "target", "continuous"]) #, required = True
  ok_data = dlg.show()
  if dlg.OK:
    if ok_data[0].strip() == '':
      print('No participant alias was entered.\nPlease start again and fill in alias.')
      quit()
    if ok_data[1].strip() == 'Select...':
      print('No condition was selected.\nPlease start again and select a condition.')
      quit()
    participantID = ok_data[0]
    cond = ok_data[1]
  else:
      quit()
      
  ## Does data folder exist? If not create it
  data_dir = os.path.dirname(__file__)+"/data"
  os.makedirs(data_dir, exist_ok=True)

  win = hp.initialize_window()
  win.mouseVisible = False
  
  exp.run_exp(win=win, participant_id = participantID, data_dir=data_dir, cond=cond)
  
main()