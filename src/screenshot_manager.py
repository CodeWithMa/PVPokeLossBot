import os
import glob
import subprocess
import logging

save_dir = "screenshots"
os.makedirs(save_dir, exist_ok=True)

def get_screenshot_files(directory, pattern="screenshot*.png"):
    """Return a list of screenshot files sorted by creation time."""
    files = glob.glob(os.path.join(directory, pattern))
    return sorted(files, key=os.path.getctime)

def limit_screenshots(directory, max_count=5):
    """Delete oldest screenshots if there are more than max_count in the directory."""
    screenshots = get_screenshot_files(directory)
    while len(screenshots) >= max_count:
        os.remove(screenshots[0])
        screenshots.pop(0)

def next_screenshot_filename(directory):
    """Determine the next screenshot filename based on existing files."""
    screenshots = get_screenshot_files(directory)
    nums = []
    for f in screenshots:
        base = os.path.basename(f)
        num_str = base.replace("screenshot", "").replace(".png", "")
        if num_str.isdigit():
            nums.append(int(num_str))
    next_num = max(nums) + 1 if nums else 1
    return os.path.join(directory, f"screenshot{next_num}.png")

def save_new_screenshot(directory=save_dir):
    """Limit screenshots to 5 and save a new screenshot as screenshotN.png in the given directory."""
    os.makedirs(directory, exist_ok=True)
    limit_screenshots(directory, max_count=5)
    new_filename = next_screenshot_filename(directory)
    try:
        subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/screenshot.png'], check=True)
        subprocess.run(['adb', 'pull', '/sdcard/screenshot.png', new_filename], check=True)
        subprocess.run(['adb', 'shell', 'rm', '/sdcard/screenshot.png'], check=True)
        logging.info(f"Saved screenshot: {new_filename}")
        return new_filename
    except subprocess.CalledProcessError as e:
        logging.error(f"ADB command failed: {e}")
        return None

# Usage:
# save_new_screenshot()  # uses "screenshots" folder by default
