
class SplayNode:
  
  def __init__(self, key, left = None, right = None, parent = None):
    self.left: SplayNode = left
    self.right: SplayNode = right
    self.parent: SplayNode = parent
    self.key: object = key

