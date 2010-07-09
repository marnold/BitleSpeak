## File: FestivalClient.py: BitleSpeak Client Driver for festival
## Author: Matt Arnold <matt@thegnuguru.org> 
## This file is part of BitleSpeak

## BitleSpeak is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## BitleSpeak is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with BitleSpeak.  If not, see <http://www.gnu.org/licenses/>.


from subprocess import *
import signal
from bitle.config import *

class FestivalClient(object):
     
    def __init__(self, args):
         
        self.drvparm = {"DEBUG": DEBUG, "USE_PULSE": 1} ## lets make pulseaudio sane until i
        ## get configparser in place 6-28
        self.festival_proc = None
        if args == None:
            self.festival_args = " "
        else:
            self.festival_args = args 
        self.paused = False
    
    # Ok this will be weird but due to how this engine works we need some non-public  
    # methods for pipe control here before we can actually implement the interface
    
    def _tts_isopen(self):
        
        return self.festival_proc != None and self.festival_proc.poll() == None
        ## Beazley pp 402-403  
    
    def _tts_open(self):
        
        if self._tts_isopen():
            return - 1
        else:
            cmdline = "festival --tts " + self.festival_args
            self.festival_proc = Popen(cmdline, stdin=PIPE,
                                       stderr=PIPE, shell=True)
    def speak(self, text):
        
        if self._tts_isopen():
            self.festival_proc.communicate(input=text)
        else:
            self._tts_open()
            self.speak(text)
    
    def stop(self):
        
        if self._tts_isopen():
            self.festival_proc.terminate()
    
    def pause(self):
        
        if (self._tts_isopen()) and not self.paused:
            self.festival_proc.send_signal(signal.SIGINT)
            self.pause = True
        elif self.paused:
            self.resume()
        else:
            return
        return
    def re
     

