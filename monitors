from psychopy.monitors import Monitor
from screeninfo import get_monitors
import math
from dotenv import load_dotenv
import os

def get_monitor_resolution():
    """
    Gets the primary monitor's resolution.
    
    Returns:
        tuple: A tuple containing the width and height of the monitor in pixels.
    """
    monitors = get_monitors()
    if monitors:
        primary_monitor = monitors[0]
        return (primary_monitor.width, primary_monitor.height)
    else:
        raise ValueError("No monitors found.")

def calculate_monitor_width(resolution, diagonal_size_inches):
    """
    Calculates the width of the monitor in centimeters.

    Args:
        resolution (tuple): A tuple containing the width and height of the monitor in pixels.
        diagonal_size_inches (float): The diagonal size of the monitor in inches.

    Returns:
        float: The width of the monitor in centimeters.
    """
    width_pixels, height_pixels = resolution
    diagonal_pixels = math.sqrt(width_pixels**2 + height_pixels**2)
    width_ratio = width_pixels / diagonal_pixels
    diagonal_size_cm = diagonal_size_inches * 2.54
    width_cm = width_ratio * diagonal_size_cm
    width_cm_rounded = math.ceil(width_cm)
    return width_cm_rounded

def load_default_monitor(config):
        load_dotenv()
        monitor_width_diagonal = os.getenv('MONITOR_WIDTH', 24)
        monitor_width_diagonal = int(monitor_width_diagonal) 
        monitor_name = "experiment_monitor" # who cares?
        monitor_resolution = get_monitor_resolution()
        monitor_width = calculate_monitor_width(monitor_resolution, monitor_width_diagonal)  # LAB PC has 24!
        monitor_distance = config.screen.distance
        monitor = Monitor(monitor_name)
        monitor.setWidth(monitor_width)
        monitor.setDistance(monitor_distance)
        monitor.setSizePix(monitor_resolution)
        return monitor
