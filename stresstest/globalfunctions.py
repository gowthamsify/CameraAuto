import os
import time

import cv2
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS
from ppadb import client
from appiumkey import *
import re
# from imgsizeverifier import *
from excelupdater import *


cameratest = Appiumclass('strt')
excelobj = Excelwriter()

adb = client.Client(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037

devices = adb.devices()
if len(devices) == 0:
    print("no device is present")
    quit()

device = devices[0]

'''client = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037
client.remote_connect("192.168.204.135", 5555)
device = client.device("192.168.204.135:5555")

devices = client.devices()
print(devices)
if len(devices) == 0:
    print("no device is present")
    quit()


device = devices[0]'''


def image_position(small_image, big_image):
    img_rgb = cv2.imread(big_image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(small_image, 0)
    height, width = template.shape[::]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF)
    _, _, top_left, _ = cv2.minMaxLoc(res)
    bottom_right = (top_left[0] + width, top_left[1] + height)
    return (top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2


def opencam():
    limit = 10
    attempts = 0
    cameratest.openappactivity(("com.android.camera", "com.android.camera.Camera"))
    while True:
        if attempts == limit:
            print("unable to launch camera")
        if validate("com.android.camera") is True:
            print("camera app launched")
            break
        else:
            cameratest.openappactivity(("com.android.camera", "com.android.camera.Camera"))
    # cameratest.clickbyxpath("//android.widget.TextView[@text='Portrait']")
    attempts += 1


def closecam():
    limit = 3
    attempts = 0
    while True:
        if attempts == limit:
            print("unable to clear app")
            break
        else:
            cameratest.camtest.keyevent(3)
            time.sleep(3)
            cameratest.camtest.keyevent(187)
            time.sleep(2)
            if cameratest.is_visible(("XPATH", "//android.widget.TextView[@text='Camera']")) is False:
                cameratest.camtest.keyevent(3)
                time.sleep(2)
                print("camera app cleared")
                break
            else:
                cameratest.swipe_element(("XPATH", "//android.widget.TextView[@text='Camera']"), 'left')
                time.sleep(2)
            attempts += 1


def readshutter():
    adb("adb exec-out screencap -p > C:\\Users\\Stresstest\\screenshot.png")
    shutterx, shuttery = image_position("C:\\Users\\Stresstest\\shutterbutton.jpg",
                                        "C:\\Users\\Stresstest\\screenshot.png")
    print(shutterx, shuttery)
    # click(shutterx, shuttery)
    return shutterx, shuttery


def readportrait():
    adb("adb exec-out screencap -p > C:\\Users\\Stresstest\\screenshot.png")
    portraitx, portraity = image_position("C:\\Users\\Stresstest\\portrait.jpg",
                                          "C:\\Users\\Stresstest\\screenshot.png")
    print(portraitx, portraity)
    # click(portraitx, portraity)
    return portraitx, portraity


def readhdrson():
    adb("adb exec-out screencap -p > C:\\Users\\Stresstest\\screenshot.png")
    hdrsonx, hdrsony = image_position("C:\\Users\\Stresstest\\HDRSON.jpg",
                                      "C:\\Users\\Stresstest\\screenshot.png")
    print(hdrsonx, hdrsony)
    return hdrsonx, hdrsony


def readhdron():
    adb("adb exec-out screencap -p > C:\\Users\\Stresstest\\screenshot.png")
    hdronx, hdrony = image_position("C:\\Users\\Stresstest\\HDRON.jpg",
                                    "C:\\Users\\Stresstest\\screenshot.png")
    print(hdronx, hdrony)
    return hdronx, hdrony


def readhdrsoff():
    adb("adb exec-out screencap -p > C:\\Users\\Stresstest\\screenshot.png")
    hdrsoffx, hdrsoffy = image_position("C:\\Users\\Stresstest\\HDRSOFF.jpg",
                                        "C:\\Users\\Stresstest\\screenshot.png")
    print(hdrsoffx, hdrsoffy)
    return hdrsoffx, hdrsoffy


def readhdroff():
    adb("adb exec-out screencap -p > C:\\Users\\Stresstest\\screenshot.png")
    hdroffx, hdroffy = image_position("C:\\Users\\Stresstest\\HDROFF.jpg",
                                      "C:\\Users\\Stresstest\\screenshot.png")
    print(hdroffx, hdroffy)
    return hdroffx, hdroffy


def readphotpos():
    adb("adb exec-out screencap -p > C:\\Users\\Stresstest\\screenshot.png")
    photox, photoy = image_position("C:\\Users\\Stresstest\\photo.jpg", "C:\\Users\\Stresstest\\screenshot.png")
    print(photox, photoy)
    return photox, photoy


def adb(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    line = proc.stdout.readline()
    print(line)
    return line


def click(tap_x, tap_y):
    # adb("adb shell input tap {} {}".format(tap_x, tap_y))
    device.shell("input tap {} {}".format(tap_x, tap_y))


def logscreencap():
    currnttime = str(time.strftime("_%Y_%m_%d_%H_%M_%S_"))
    screenshotcmd = "adb shell screencap -p /sdcard/" + currnttime + ".png"
    # bugreportcmd = "adb shell bugreport"

    subprocess.Popen(screenshotcmd)
    # subprocess.Popen(bugreportcmd)
    print("screenshot")
    time.sleep(2)


def validate(app, bug=True):
    checkappactiv = "adb shell dumpsys activity activities | FIND \"mResumedActivity\""
    cmdoutput = subprocess.run(checkappactiv, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    testout = cmdoutput.stdout.rstrip()
    valid = app
    act = str(testout)
    print(act)
    if valid in act:
        print("pass")
        return True
    else:
        print("fail")
        if bug == True:
            logscreencap()
            bugreport()
            time.sleep(20)
        else:
            print("skipping bug")
        return False


def bugreport():
    print("generating bugreport")
    bugpath = os.path.dirname(os.path.abspath("report")) + "\\reports\\"
    subprocess.run("adb bugreport" + " " + bugpath)
    time.sleep(30)


def clr_rect():
    clearx, cleary = '420', '1947'
    device.shell("input keyevent 3")
    time.sleep(2)
    device.shell("input keyevent KEYCODE_MENU")
    time.sleep(3)
    click(clearx, cleary)


def checkforelement(eleid):
    print(eleid)
    try:
        elevalu = cameratest.checkelementbyid(eleid)
        print("check with id")
        return elevalu

    except BaseException as error:
        print("check with xpath")
        print('An exception occurred: {}'.format(error))
        elevalu = cameratest.checkelementbyxpath(eleid)
        return elevalu


def validatforclose(app, case):
    if validate(app) is False:
        excelobj.switchmodeupdate(case, 'fail')
    else:
        excelobj.switchmodeupdate(case, 'pass')


def initia_cam():
    adb('adb shell pm clear com.android.camera')
    opencam()
    cameratest.clickbyid('android:id/button1')
    time.sleep(2)
    cameratest.clickbyid('com.android.permissioncontroller:id/permission_allow_foreground_only_button')
    time.sleep(2)
    downloadcamodes()


def downloadcamodes():
    maxtry = 10
    attempts = 0
    while True:
        try:
            elemvisi = cameratest.is_visible(("XPATH", "//android.widget.TextView[@text='More']"))
            if elemvisi is False:
                print("element not visible, swiping to element")
                cameratest.swipe_to_element(("ID", "com.android.camera:id/mode_select_scrollview"),
                                            ("XPATH", "//android.widget.TextView[@text='More']"), 'right')
            else:
                cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
            if attempts == maxtry:
                print("unable to download modes")
            else:
                cameratest.clickbyid('com.android.camera:id/mode_bg')
                time.sleep(5)
                if cameratest.is_visible(('ID', 'com.android.camera:id/mode_edit_title')):
                    print("all modes downloaded")
                    closecam()
                    break
                else:
                    attempts += 1
                    print(attempts)
        except NoSuchElementException:
            print("all modes downloaded")
            closecam()
            break
