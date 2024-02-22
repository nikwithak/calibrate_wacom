# Wacom Tablet Area Helper

This is a quick utility for mapping my Wacom tablet to a specific area on the
screen. It was tested with a Wacom Intuos S, on Ubuntu running i3wm. It uses
`xsetwacom` to map the pen to a specific area on the screen.

This was thrown together to fit my needs, and may not work with your setup. If
you encounter issues, please file an issue on GitHub.

The logic for getting the window bounds was modified from
[remarkable-mouse](https://github.com/Evidlo/remarkable_mouse), which is
licensed under GPL3, and so this utility is released under the same license.

## Usage

Ensure your wacom tablet is powered on and connected to your computer, and that
you have tkinter installed (`sudo apt install python3-tk`)

0. `pip install -r requirements.txt`
1. `python ./calibrate_wacom.py`
2. Move the window to the area you would like to map the tablet to.
3. Click the button in the window (or press Enter)

That's it! If it worked, your tablet should now be mapped to the screen area you
selected. If not, please file an issue.
