#Description
#___________________________________________________________________________________
#This script accesses Vivotek Camera web interfaces.
# > Updates configuration files for optimization of live vs record.
# > Updates NTP server. Sets up local motion detection and records to local SD cards.
# > Updates firmware if out of date.


## These are the modules that must be imported to run functions
import requests
import urllib3
import re
import time
import json
from pathlib import Path

## This sets the class for object oriented programming to be referred to in the "vivotekmaster" script.
class camera:

  ## This is the file you should have in the same folder as both the data script and master script.
  ## It holds the values to assign for each function. 
  d = open('vivotekdata.json')
  data = json.load(d)

  print('Username:')
  username = input()
  print('Password:')
  password = input()
  ## These are the variables for VCA file installation on 9387 cameras for motion detection
  VCApath = 'VCA/cgi-bin/upload_file.cgi'
  Firmwarepath = 'cgi-bin/admin/upgrade.cgi'
  ## This is the parent folder location for all camera models that will hold VCA config files and firmware files.
  Folder = "//Your/Network/Folder/Location"
  
  ## This allows for the class to call objects to the master script.
  def __init__(self,address):
      self.address=address
      urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

      print('Setting camera parameters (%s)... ' % address, end='')

      self.auth = requests.auth.HTTPBasicAuth(self.username, self.password);

  ## This communicates with the camera's web interface to begin the process of getting or setting paramters.
  def cameraGet(self, path):
      uri='http://%s/%s' %(self.address, path)
      r = requests.get(uri,
        verify=False,
        auth=self.auth,
      )
    
      if r.status_code != requests.codes.ok: # 200
        raise Exception('getparams failed with status %s' % r.status_code)
  
      return r
    
   ## This function gets parameters from the camera, can specify which arguments to return.
  def getParams(self, level, params):
      params = '&'.join(params)

      r = self.cameraGet('cgi-bin/%s/getparam.cgi?%s' % (level, params))

      vals = {}

      for line in r.text.splitlines():
          match = re.search('([a-z0-9_]+)=\'([A-Za-z0-9_.-]+)\'', line)
          vals[match.group(1)] = match.group(2)

      return vals
    
  ## There are different permission levels for parameters.  This allows for admin level permissions.
  def getAdminParams(self, params):
      return self.getParams('admin', params)
    
  ## This will set values with admin level permissions.    
  def setAdminParams(self, params):
      response = requests.post('http://%s/cgi-bin/admin/setparam.cgi?' % self.address, 
        data=params,
        verify=False,
        auth=self.auth,
      )

  
  ## Camera mode needs to be set first, with the proper wait time after, as it clears motion detection and events.
  ## All further functions follow this one.
  def setcameramode(self):
        if self.getCameraMode() == '0':
          print('Mode is already correct!')
        else:
           capabilityrotation = self.getAdminParams(['capability_videoin_c0_rotation'])['capability_videoin_c0_rotation']
           self.setAdminParams(self.data['videomode'])
           if capabilityrotation == '1':
             print('Please Wait')
             time.sleep(7)
           else:
             while True :
               mode=self.getCameraMode()
               print(mode)
               if mode == '0':
                 break
               print('Still Updating')
               time.sleep(1)
               
   ## This gets the current camera mode value to determine if the script will move forward.
  def getCameraMode(self):
    r = self.getAdminParams(['videoin_c0_mode'])
    mode = r['videoin_c0_mode']
    return mode
  
  
  ## SDcard needs to be formatted to ext4 to allow for larger files to be recorded.
  def formatsdcard(self):
    self.setAdminParams(self.data['sdcard'])
  
  
  ## These will set the parameters for the various camera models.  Minor camera model differences can share same settings, e.g. 9387-HTV with 9387-HTV-

  def setfd8377(self):
    self.setAdminParams(self.data['common' ])
    self.setAdminParams(self.data['fd8377'])
   
  def setfd9387htv(self):
    self.setAdminParams(self.data['common' ])
    self.setAdminParams(self.data['fd9387htv'])

  def setfd9387htva(self):
    self.setAdminParams(self.data['common' ])
    self.setAdminParams(self.data['fd9387htva'])
    
  ## fd9387 Cameras need motion detection set up in an application package on the camera.  This will upload the config file for this.  
  def setVCA(self, VCA):
     response = requests.post(
       'http://%s/%s' % (self.address, self.VCApath),
       auth=self.auth,
       files={ 'fimage': open(Path("%s/%s" % (self.Folder, VCA)), 'rb')  },
       verify=False,
     )
     print('VCA configured!')

  def fd9387htvvca(self):
    self.setVCA(self.data['fd9387htvvca'])

  def fd9387htvavca(self):
    self.setVCA(self.data['fd9387htvavca'])  

  ## This section defines the firmware files to be uploaded if the camera is using older firmware.
  def updatefirmware(self, firmware):
    response = requests.post(
       'http://%s/%s' % (self.address, self.Firmwarepath),
       auth=self.auth,
       files={ 'fimage': open(Path("%s/%s" % (self.Folder, firmware)), 'rb') },
       verify=False,
    )
    print('Firmware updated!')

  def fd8377htvfirmware(self):
     self.updatefirmware(self.data['fd8377htvfirmware'])

  def fd8377ehtvfirmware(self):
     self.updatefirmware(self.data['fd8377ehtvfirmware'])

  def fd9387htvfirmware(self):
     self.updatefirmware(self.data['fd9387htvfirmware'])

  def fd9387htvafirmware(self):
     self.updatefirmware(self.data['fd9387htvafirmware'])

