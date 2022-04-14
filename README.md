"# VivotekCameraOptimization" 

This was developed to mass update Vivotek cameras on a per IP address basis.  

Optimized settings were determined, which were able to be changed via HTTP Post requests in Python.

There are a number of things to be changed for optimization and best use of the cameras, including edge recording to an SD card via motion detection, updating to the latest firmware, streaming mode, codec, resolution and framerate. 

The order in which these settings needed to be made was important, as some would clear settings in other portions of the camera.

The individual camera settings were setup in a JSON data file, which included firmware package names referenced in the vivotekdata script.

Firmware files as well as virtual camera application files (configurations for the motion detection application) would be set in an accessible network location which is labeled as a global variable in the vivotekdata script.

The ip addresses that the script would apply to are set in the cameralist.csv file, which is first called by the addresslist script, which is then pulled by the vivotekmaster.exe

To keep this script up to date, the only thing necessary would be to change the latest firmware files in the JSON file.
