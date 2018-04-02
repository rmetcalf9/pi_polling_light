import unicornhat as unicorn
import signal
import time

#Main application has an array of colours and how it lights the hat depends on the number of entries in an array
# it is designed to run on an 8 x 4 array

# array length -> Description
#  0 -> black
#  1 -> All lights that colour
#  2 -> aaaabbbb
#       aaaabbbb
#       aaaabbbb
#       aaaabbbb
#  3 -> aaabbccc
#       aaabbccc
#       aaabbccc
#       aaabbccc
#  4 -> aaaabbbb
#       aaaabbbb
#       ccccdddd
#       ccccdddd
# other numbers will error (TODO extend this code to cover more patterns if required)

class appObjClass:
  width = 0
  height = 0

  displayArray = [ [255,128,0], [128,0,255], [0,255,128], [255,255,255] ]

  class ServerTerminationError(Exception):
    def __init__(self):
      pass
    def __str__(self):
      return "Server Terminate Error"

  isInitOnce = False
  def init(self):
    self.initOnce()

  def initOnce(self):
    if self.isInitOnce:
      return
    self.isInitOnce = True
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(0.2)

    width,height=unicorn.get_shape()
    self.width = width
    self.height = height
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully) #sigterm is sent by docker stop command


  def exit_gracefully(self, signum, frame):
    self.running = False
    print("Exit Gracefully called")
    raise self.ServerTerminationError

  running = True
  def run(self):
    self.running = True
    try:
      while self.running:
        self.loopIteration()
    except self.ServerTerminationError:
      unicorn.off()
      print("Stopped")

  lastDisplayArray = []
  def loopIteration(self):
    if self.displayArray != self.lastDisplayArray:
      self.lastDisplayArray = list(self.displayArray) #copy the array each time
      if len(self.lastDisplayArray) == 0:
        unicorn.off()
      elif len(self.lastDisplayArray) == 1:
        for x in range(0,self.width):
          for y in range(0,self.height):
            unicorn.set_pixel(x, y, self.lastDisplayArray[0][0], self.lastDisplayArray[0][1], self.lastDisplayArray[0][2])
      elif len(self.lastDisplayArray) == 2:
        for x in range(0,4):
          for y in range(0,self.height):
            unicorn.set_pixel(x, y, self.lastDisplayArray[0][0], self.lastDisplayArray[0][1], self.lastDisplayArray[0][2])
        for x in range(4,self.width):
          for y in range(0,self.height):
            unicorn.set_pixel(x, y, self.lastDisplayArray[1][0], self.lastDisplayArray[1][1], self.lastDisplayArray[1][2])
      elif len(self.lastDisplayArray) == 3:
        for x in range(0,3):
          for y in range(0,self.height):
            unicorn.set_pixel(x, y, self.lastDisplayArray[0][0], self.lastDisplayArray[0][1], self.lastDisplayArray[0][2])
        for x in range(3,5):
          for y in range(0,self.height):
            unicorn.set_pixel(x, y, self.lastDisplayArray[1][0], self.lastDisplayArray[1][1], self.lastDisplayArray[1][2])
        for x in range(5,8):
          for y in range(0,self.height):
            unicorn.set_pixel(x, y, self.lastDisplayArray[2][0], self.lastDisplayArray[2][1], self.lastDisplayArray[2][2])
      elif len(self.lastDisplayArray) == 4:
        for x in range(0,4):
          for y in range(0,2):
            unicorn.set_pixel(x, y, self.lastDisplayArray[0][0], self.lastDisplayArray[0][1], self.lastDisplayArray[0][2])
        for x in range(4,self.width):
          for y in range(0,2):
            unicorn.set_pixel(x, y, self.lastDisplayArray[1][0], self.lastDisplayArray[1][1], self.lastDisplayArray[1][2])
        for x in range(0,4):
          for y in range(2,4):
            unicorn.set_pixel(x, y, self.lastDisplayArray[2][0], self.lastDisplayArray[2][1], self.lastDisplayArray[2][2])
        for x in range(4,self.width):
          for y in range(2,4):
            unicorn.set_pixel(x, y, self.lastDisplayArray[3][0], self.lastDisplayArray[3][1], self.lastDisplayArray[3][2])
      else:
        raise Exception("Invalid display array length " + len(self.lastDisplayArray))
      unicorn.show()
    time.sleep(1)


appObj = appObjClass()

