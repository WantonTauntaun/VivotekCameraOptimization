

import vivotekdata
import time
import addresslist


## This is the list of addresses populated in the cameralist.csv
addresses = (addresslist.addresses)

for address in addresses:
    c = vivotekdata.camera(address)
    try:
       
       p = c.getAdminParams(['system_info_modelname', 'system_info_firmwareversion'])
         
       print("  Camera model: ", p['system_info_modelname'])
       print("  firmware version: ", p['system_info_firmwareversion'])
    except Exception as e:
       print(e)

    else:

       if p['system_info_modelname'] == 'FD9387-HTV':
           if p['system_info_firmwareversion'] != 'FD9387-VVTK-2.2002.23.01k':
              c.fd9387htvfirmware()
              time.sleep(120)
           c.setcameramode()
           c.fd9387htvvca()
           c.formatsdcard()
           c.setfd9387htv()
       elif p['system_info_modelname'] == 'FD9387-HTV-A':
           if p['system_info_firmwareversion'] != 'FD9387A-VVTK-0101b':
              c.fd9387htvafirmware()
              time.sleep(120)
           c.setcameramode()
           c.fd9387htvavca()
           c.formatsdcard()
           c.setfd9387htva()
       elif p['system_info_modelname'] == 'FD8377-HTV':
           if p['system_info_firmwareversion'] != 'FD8377-VVTK-0113b':
               c.fd8377htvfirmware()
               time.sleep(120)
           c.setcameramode()
           c.formatsdcard()
           c.setfd8377()
       elif p['system_info_modelname'] == 'FD8377-EHTV':
           if p['system_info_firmwareversion'] != 'FD8377-VVTK-0113b':
               c.fd8377ehtvfirmware()
               time.sleep(120)
           c.setcameramode()
           c.formatsdcard()
           c.setfd8377()      
       else: print('Camera model not in BLS Vivotek library.')

print('done!')
input("Press Enter to continue...")

