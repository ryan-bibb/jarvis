import time
import platform
import subprocess

def open_app(app_name):
    system = platform.system()

    if system == "Darwin":
        subprocess.run(["open", "-a", app_name])
    elif system == "Windows":
        subprocess.run(["start", app_name], shell=True)
    elif system == "Linux":
        subprocess.run([app_name])

# TODO: add more specific times rather than just morning and afternoon
def is_morning():
    local_time = time.localtime()
    is_morning = True if local_time.tm_hour < 12 else False

    return is_morning

def get_local_time():
    local_time = time.localtime()
    hour = local_time.tm_hour - 12 if local_time.tm_hour > 12 else local_time.tm_hour
    minute = local_time.tm_min

    return str(hour) + " " + str(minute)

def hours_to_seconds(hours):
    return hours * 60 * 60

def minutes_to_seconds(minutes):
    return minutes * 60

def format_seconds(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}:{minutes:02d}:{seconds:02d}"

def start_timer(hours, minutes, seconds):
    total_time = hours_to_seconds(hours) + minutes_to_seconds(minutes) + seconds

    for i in range(total_time, 0, -1):
        print(format_seconds(total_time))
        time.sleep(1)
        total_time -= 1

    print("Timer done")
