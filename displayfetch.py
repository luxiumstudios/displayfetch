#!/usr/bin/env python3
import gi
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk
import math
import subprocess
from OpenGL import GL
from OpenGL.GL import glGetString, GL_RENDERER, GL_VENDOR

def get_monitors():
    display = Gdk.Display.get_default()
    monitors_info = []
    for i in range(display.get_n_monitors()):
        monitor = display.get_monitor(i)
        geometry = monitor.get_geometry()
        scale = monitor.get_scale_factor()
        width_px = geometry.width * scale
        height_px = geometry.height * scale
        width_mm = monitor.get_width_mm()
        height_mm = monitor.get_height_mm()
        diagonal_inch = math.sqrt(width_mm**2 + height_mm**2) / 25.4 if width_mm and height_mm else None
        model = monitor.get_model() or "Unknown Model"
        manufacturer = monitor.get_manufacturer() or "Unknown Manufacturer"

        monitors_info.append({
            "name": f"{manufacturer} {model}",
            "resolution": f"{width_px}x{height_px}",
            "diagonal_inch": diagonal_inch
        })
    return monitors_info

def get_gpu():
    try:
        renderer = glGetString(GL_RENDERER).decode()
        vendor = glGetString(GL_VENDOR).decode()
        return f"{vendor} - {renderer}"
    except Exception:
        # fallback: lspci
        gpu_list = []
        output = subprocess.check_output(["lspci"]).decode()
        for line in output.splitlines():
            if "VGA" in line or "3D" in line:
                gpu_list.append(line.strip())
        return ", ".join(gpu_list) if gpu_list else "Unknown GPU"

def main():
    print("X11")
    print("Monitors:")
    for monitor in get_monitors():
        diag = f", {monitor['diagonal_inch']:.1f}\" diagonal" if monitor['diagonal_inch'] else ""
        print(f"  {monitor['name']}: {monitor['resolution']}{diag}")

    print("\nGPU:")
    print(f"  {get_gpu()}")

if __name__ == "__main__":
    main()
