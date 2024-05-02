import os
import time
import subprocess
import threading

def clock():

    schedule_folder = './schedule'

    def clock_thread():
        while True:
            current_time = int(time.time())
            for file in os.listdir(schedule_folder):
                file_time, interval = file.split('_')[0], file.split('_')[1].split('.')[0]
                if int(file_time) <= current_time and (current_time - int(file_time)) % int(interval) == 0:
                    subprocess.call(['python', os.path.join(schedule_folder, file)])
            time.sleep(0.75)
            
    threading.Thread(target=clock_thread).start()
