import os


def send_adb_tap(x: int, y: int) -> bool:
    adb_command = f"adb shell input tap {x} {y}"
    error_code = os.system(adb_command)
    return error_code == 0


def turn_screen_off() -> bool:
    adb_command = "adb shell input keyevent 26"
    error_code = os.system(adb_command)
    return error_code == 0
