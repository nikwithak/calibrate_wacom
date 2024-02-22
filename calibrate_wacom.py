import subprocess
import tkinter as tk
import re
from tkinter import ttk

def get_coords():
    window = tk.Tk()
    (left, top, width, height) = (0, 0, 0, 0)
    def get_window():
        nonlocal left
        nonlocal top
        nonlocal width
        nonlocal height
        left = window.winfo_x()
        top = window.winfo_y()
        width =window.winfo_width()
        height = window.winfo_height()
        window.destroy()
        return (left, top, width, height)

    confirm = ttk.Button(
        window,
        text="Resize and move this window, then click or press Enter",
        command=get_window
    )
    confirm.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    window.bind('<Return>', lambda _: get_window())

    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.attributes('-alpha', 0.3)
    window.title("Wacom Calibrator")

    window.mainloop()
    print(left, top, width, height)
    return (left, top, width, height)


def get_stylus_id():
    """
    Uses some hacky regex to get the ID of the Wacom Stylus using xsetwacom.
    Raises an exception if zero, or more than one, styli are found.
    """
    devices = subprocess.check_output(["xsetwacom", "--list", "devices"])
    devices = [x for x in (devices.decode("utf-8")).split('\n') if re.search("type: STYLUS", x) is not None]
    stylus_ids =  [re.findall(r'id:\w*\s*\t*(\d+)\t*.*type', device) for device in devices]
    if len(stylus_ids) != 1:
        raise Exception(f"Found {len(stylus_ids)} IDs - expected exactly one.")
    return stylus_ids[0][0]


def set_wacom_area(coords, stylus_id):
    """
    Sets the coordinates of the stylus using xsetwacom. There's some funky math to
    map the stylus area to the wacom tablet - unfortunately the mapping is backwards
    from the logical way of "set the screen coordinates to map the tablet to", instead
    it's a weird thing where you set the part of the screen that the pen maps to
    *relative to the default area of the tablet*.

    This may be different for your setup? It was really confusing to figure out.
    Please raise an issue in GitHub if this isn't working for you.
    """
    subprocess.run(["xsetwacom","--set", stylus_id, "ResetArea"])
    (new_left, new_top, new_right, new_bottom) = (
        coords[0],
        coords[1],
        coords[2],
        coords[3],
    )

    print(new_left, new_top, new_right, new_bottom)
    print(["xsetwacom","--set", stylus_id, "map_to_output", f"{new_right}x{new_bottom}+{new_left}+{new_top}",])
    if subprocess.run(["xsetwacom","--set", stylus_id, "maptooutput", f"{new_right}x{new_bottom}+{new_left}+{new_top}",]).returncode == 0:
        print("Success! Set new Wacom coordinates")
    else:
        raise Exception("Failed to set the new coordinates.")


if __name__ == "__main__":
    coords = get_coords()
    id = get_stylus_id()
    set_wacom_area(coords, id)
