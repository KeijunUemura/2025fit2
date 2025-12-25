# -*- coding: utf-8 -*-

import pyxel

class APP:
  def __init__(self):
      pyxel.init(128, 128, title="pyxel")
      
      pyxel.load('情報基礎2.pyxres')
      
      pyxel.run(self.update, self.draw)
     
  def update(self):
      pass

  def draw(self):
      pyxel.cls(0)

      pyxel.blt(50, 50, 0, 0, 0, 16, 16, 0)
      
     
      
      
APP()

