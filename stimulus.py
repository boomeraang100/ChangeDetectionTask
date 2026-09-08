import math
import numpy as np
import scipy as sp
import params as pm
from psychopy import visual, core, event

class BlockStimulus:
  def __init__(
                self,
                win: visual.Window,
                color: str = "blue",
                width: int = pm.SQUARE_WIDTH,
                height: int = pm.SQUARE_HEIGHT,
                units: str = "pix",
                pos=None,
  ) -> None:
    if pos is None:
      pos = np.zeros(2)

    self.win = win
    self.color = color
    self.width = width
    self.height = height
    self.units = units
    self.pos = pos
    
    self.square = visual.Rect(
      win=win,
      width=width,
      height=height,
      units=units,
      fillColor=color,
      pos=pos
      )
    
  def draw(self) -> None:
    self.square.draw()