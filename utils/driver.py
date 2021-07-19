from gpiozero import  MCP3008

class AnalogOutput:
  def __init__(self, channel):
    self.device = MCP3008(channel = channel)
  def getDeviceValue(self):
    return self.device.value