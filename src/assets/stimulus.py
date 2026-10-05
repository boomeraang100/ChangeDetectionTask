from psychopy import visual
import src.assets.params as pm
import numpy as np

class BlockStimulus:
  def __init__(
                self,
                win: visual.Window,
                color: str = "blue",
                width: int = pm.SQUARE_WIDTH,
                height: int = pm.SQUARE_HEIGHT,
                units: str = "pix",
                pos=None,
                colorSpace = "rgb255",
  ) -> None:
    if pos is None:
      pos = np.zeros(2)

    self.win = win
    self.color = color
    self.width = width
    self.height = height
    self.units = units
    self.pos = pos
    self.colorSpace = colorSpace
    
    self.square = visual.Rect(
                              win=win,
                              width=width,
                              height=height,
                              units=units,
                              fillColor=color,
                              pos=pos,
                              colorSpace = colorSpace
    )
    
  def draw(self) -> None:
    self.square.draw()