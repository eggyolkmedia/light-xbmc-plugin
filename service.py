import time
import sys
import xbmc
import xbmcaddon

class LightMonitor(xbmc.Player):

  def __init__(self):
    xbmc.Player.__init__(self)
    addon = xbmcaddon.Addon()
    self.server_host = addon.getSetting('server-host')
    self.server_port = addon.getSetting('server-port')
    self.media_types = addon.getSetting('media-types').split(',')

    log("Starting; host={}, port={}, media types={}".format(self.server_host, self.server_port, self.media_types))

  def onPlayBackStarted(self):
    log("started")
    self.mediaStarted()

  def onPlayBackResumed(self):
    log("resumed")
    self.mediaStarted()

  def onPlayBackStopped(self):
    log("stopped")
    self.mediaStopped()

  def onPlayBackPaused(self):
    log("paused")
    self.mediaStopped()

  def onPlayBackEnded(self):
    log("ended")
    self.mediaStopped()

  def mediaStarted(self):
    # log("Playback started")
    log("video? {}".format(self.isPlayingVideo()))

  def mediaStopped(self):
    # log("Playback stopped")
    pass

def log(msg):
  xbmc.log('[ZL] ' + msg, level=xbmc.LOGDEBUG)

if __name__ == '__main__':
  monitor = LightMonitor()

  while not xbmc.abortRequested:
    xbmc.sleep(500)

  log("Shutting down")
  sys.exit(0)

