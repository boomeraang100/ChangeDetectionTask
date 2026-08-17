print("1: starting", flush=True)

from psychopy import visual

print("2: imported visual", flush=True)

win = visual.Window(
    size=(800, 600),
    fullscr=False,
    allowGUI=True,
    waitBlanking=False,
    useFBO=False,
)

print("3: WINDOW CREATED", flush=True)

win.flip()

print("4: FLIP DONE", flush=True)

input("Press Enter to close...")

win.close()

print("5: CLOSED", flush=True)