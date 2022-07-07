import queue
import subprocess
import threading
import time

from stresstest.globalfunctions import *


class AsynchronousFileReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queu):
        assert isinstance(queu, queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queu

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()


def smallimageverifier():
    # You'll need to add any command line arguments here.
    process = subprocess.Popen("adb logcat | grep \"JPEG\"", stdout=subprocess.PIPE)

    # Launch the asynchronous readers of the process' stdout.
    stdout_queue = queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()

    # Check the queues if we received some output (until there is nothing more to get).
    while not stdout_reader.eof():
        while not stdout_queue.empty():
            line = stdout_queue.get()
            print(line)
            checkpoint = line
            reslution = "output size (JPEG):= 4640x3472"
            # reslution = "ouput image: w x h = [\d+]x[\d+]"
            if reslution in str(checkpoint):
                # subprocess.Popen.terminate()
                print("true")
                time.sleep(2)
                logscreencap()
                bugreport()
                time.sleep(10)
            '''else:
                time.sleep(2)
                print("no small image generated")
                #adb("adb logcat -c")
                #subprocess.Popen.terminate()'''


# smallimageverifier()

img_list_cmd = "adb shell ls /sdcard/DCIM/Camera"
print(img_list)