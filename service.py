import time
import xbmc
 
if __name__ == '__main__':
    monitor = xbmc.Monitor()
 
    while True:
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            break
        xbmc.log("ZL TEST %s" % time.time(), level=xbmc.LOGDEBUG)