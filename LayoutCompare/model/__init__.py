class Element:
  def __init__(self):
    self.width  = 0
    self.height = 0
    self.X = 0
    self.Y = 0
    self.id = None
    self.area = 0
    self.PenaltyIfSkipped = 0
    

class Layout:
  def __init__(self):
    self.canvasWidth = 0
    self.canvasHeight = 0
    self.elements = [] 
    self.id = None
    self.N = 0
    self.Xsum = 0
    self.Ysum = 0
    self.Wsum = 0
    self.Hsum = 0
    self.AreaSum = 0
