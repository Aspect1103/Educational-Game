# Brief
This is an educational game made for a University team project.

# How to run
Extract game.zip and run window.exe (your computer will say it is a virus, it is not, check [VirusTotal](https://www.virustotal.com/gui/file/fb713a88d85eccf2b2abc6bf28e2b981392da8e9177bccc98ac1e69b5fcd5f55?nocache=1)).

# How to build
Clone the repository and create a virtual environment using requirements.txt. Then run build.py to compile the game with PyInstaller.

If PyInstaller returns this error:
```
Error: geos_c.dll not found, required by hook-shapely.py.
Please check your installation or provide a pull request to PyInstaller to update hook-shapely.py.
```
Then download the correct Shapely build from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely). This project uses the 64 bit Python 3.9 Shapely 1.8.1.post1 build [here](https://download.lfd.uci.edu/pythonlibs/x6hvwk7i/Shapely-1.8.1.post1-cp39-cp39-win_amd64.whl).
