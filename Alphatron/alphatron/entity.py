"""Basic classes and functions defining a component system"""

from abc import ABCMeta, abstractmethod, abstractproperty

class Worldspace(object):
  """Meta-object containing all entities, components, and systems"""
  def __init__(self, components, systems, masks = None):
    self.components = components
    self.systems = systems

    if masks:
      self.masks = masks
    else:
      self.masks = []

  def get(self, guid):
    return self[guid]

  def __getitem__(self, guid):
    data = {}

    if len(self.masks) > guid:
      mask = self.masks[guid]
    else:
      raise IndexError, str(guid) + " is not a valid GUID"

    for compmask in self.components.keys():
      #print compmask & mask, compmask, mask
      if compmask & mask:
        data[compmask] = self.components[compmask][guid]
    return data

  def update(self):
    for system in self.systems:
      system.update(self)

class System(object):
  """Baseclass for all systems"""
  __metaclass__ = ABCMeta

  @abstractmethod
  def update(self, world):
    pass

  @abstractproperty
  def mask(self):
    pass
