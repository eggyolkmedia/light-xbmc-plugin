import Queue
import time
import threading
import socket
import sys
import xbmc
import xbmcaddon

MSG_START = "movie_start"
MSG_STOP = "movie_stop"
MSG_TERMINATE = "terminate"

class LightMonitor(xbmc.Player):

  def __init__(self):
    xbmc.Player.__init__(self)
    self.playing = self.isPlayingVideo()

  def setQueue(self, queue):
    self.queue = queue

  def onPlayBackStarted(self):
    log("playback started")
    self.mediaStarted()

  def onPlayBackResumed(self):
    log("playback resumed")
    self.mediaStarted()

  def onPlayBackStopped(self):
    log("playback stopped")
    self.mediaStopped()

  def onPlayBackPaused(self):
    log("playback paused")
    self.mediaStopped()

  def onPlayBackEnded(self):
    log("playback ended")
    self.mediaStopped()

  def mediaStarted(self):
    if not self.playing and self.isPlayingVideo():
      self.queue.put(MSG_START)
    self.playing = True

  def mediaStopped(self):
    if self.playing:
      self.queue.put(MSG_STOP)
    self.playing = False


class ServerThread(threading.Thread):

  def __init__(self, queue):
    threading.Thread.__init__(self, name="SERVER_THREAD")
    self.queue = queue

    addon = xbmcaddon.Addon()
    self.server_host = addon.getSetting('server-host')
    self.server_port = int(addon.getSetting('server-port'))

  def run(self):
    while True:
      cmd = queue.get()
      if cmd == MSG_TERMINATE:
        queue.task_done()
        break

      try:
        self.sendCommand(cmd)
      except:  # sendCommand() should handle all exceptions.
        log("Undefined error: {}".format(sys.exc_info()[0]))
      finally:
        queue.task_done()

  def sendCommand(self, cmd):
    xmlcmd = '<request name="{}" immediate="0"/>'.format(cmd)

    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((self.server_host, self.server_port))
      s.sendall(xmlcmd)
      response = s.recv(128)

      # todo parse response?
      log("sent {} to {}/{}, received: {}".format(xmlcmd, self.server_host, self.server_port, response))

    except:
      log("failed to send command [{}]: {}".format(xmlcmd, sys.exc_info()[0]))
    

def log(msg):
  xbmc.log('[ZL] ' + msg, level=xbmc.LOGDEBUG)

if __name__ == '__main__':
  queue = Queue.Queue()
  monitor = LightMonitor()
  monitor.setQueue(queue)
  server_thread = ServerThread(queue)
  server_thread.start()

  log("Started")
  xbmc.Monitor().waitForAbort()

  log("Terminating...")
  queue.put(MSG_TERMINATE)
  server_thread.join()
  queue.join()

  log("Terminated")
  sys.exit(0)

