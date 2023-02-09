#M3U File Path Converter
##What does it do?
Converts the filepaths stored in a M3U file exported from an Android system. The paths are converted from the Android Filesystem to your PC's file system so the same playlist can be used on PC.

Please note: This only converts the M3U playlist file, in order to use the playlist you must have the same files stored on your android device on your PC.

##How can I use it?
There are executable files provided in the release folder. In order to download them please click on the executable of your choice.

Right click Raw, and select Save Link As.

![Image](<images/>)

To use the converter, simply select your exported M3U file using the "Select Input Files" Button, the folder your music is stored in using the "Select Music Folder" button and the desired output folder for your playlists using the "Select Output Folder" button.

![Image](<images/2023-02-09 21_53_07-gui.py - Python - Visual Studio Code.png>)


Click Convert and you can now use your new M3U files. 


##How can I compile the source code?

Use the following command to compile the code into an executable, make sure to install PyInstaller if you have not already:
    python -m PyInstaller .\src\gui.py