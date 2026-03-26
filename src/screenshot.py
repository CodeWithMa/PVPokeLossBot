import os
import subprocess
import platform
import logging
os.makedirs("screenshots", exist_ok=True)

def capture_screenshot(filename: str) -> bool:
    """
    Captures a screenshot of the Android screen using adb and saves it to a file.
    Returns True if the adb command was successful, False otherwise.
    """
    try:
        if platform.system() == "Windows":
            # On Windows, use different approach to handle output redirection
            result = subprocess.run(
                ["adb", "exec-out", "screencap", "-p"],
                capture_output=True,
                timeout=15
            )
            
            if result.returncode != 0:
                logging.error(f"ADB screenshot command failed: {result.stderr}")
                return False
            
            # Save the binary screenshot data to file
            with open(filename, 'wb') as f:
                f.write(result.stdout)
        else:
            # On Unix-like systems, use shell redirection
            result = subprocess.run(
                f"adb exec-out screencap -p > {filename} 2> /dev/null",
                shell=True,
                timeout=15
            )
            
            if result.returncode != 0:
                logging.error("ADB screenshot command failed")
                return False
        
        logging.debug(f"Screenshot saved to {filename}")
        return True
    
    except subprocess.TimeoutExpired:
        logging.error("ADB screenshot command timed out")
        return False
    except (FileNotFoundError, OSError) as e:
        logging.error(f"ADB screenshot command failed: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error during screenshot capture: {e}")
        return False
