from appium import webdriver
import time
from appium.webdriver.common.appiumby import AppiumBy
import subprocess

# from globalfunctions import *
from selenium.common.exceptions import NoSuchElementException

desired_cap = {
    "platformName": "Android",
    # "platformVersion": "11",
    # "deviceName": "f53b0d3f",  # DEVICE SERIAL
    # "appPackage": "com.android.camera",
    # "appActivity": "com.android.camera.Camera",
    "autoGrantPermissions": True,
    "newCommandTimeout": 300000,
    "adbExecTimeout": 200000
}
camtest = webdriver.Remote('http://localhost:4723/wd/hub', desired_cap)
camtest.implicitly_wait(10)


def testcamopen():
    camtest.start_activity("com.android.camera", "com.android.camera.Camera")
    time.sleep(3)
    camtest.find_element(AppiumBy.ID, "com.android.camera:id/shutter_button").click()
    time.sleep(2)
    camtest.find_element(AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='More']").click()


def adhandler():
    adb("am start")
    camtest.start_activity("com.google.android.googlequicksearchbox", "com.google.android.googlequicksearchbox")


def getelementpointer(locator):
    """
           Return an elements coordinates and dimensions.
           :param locator:(tuple) takes two positional value,
           getelementpoint(("ID or XPATH",element))
           :return: elements location pointers
           """
    print(locator)
    try:
        if type(locator) == tuple:
            method = locator[0]
            value = locator[1]
        elif type(locator) == list:
            for i in locator:
                method = locator[0]
                value = locator[1]
        if method == 'ID':
            element = camtest.find_element(AppiumBy.ID, value=value)
        elif method == 'XPATH':
            element = camtest.find_element(AppiumBy.XPATH, value=value)
    except:
        raise Exception("element not found")
    return {
        'top': element.location['y'],
        'bottom': element.location['y'] + element.size['height'],
        'left': element.location['x'],
        'right': element.location['x'] + element.size['width'],
        'center_x': (element.size['width'] / 2) + element.location['x'],
        'center_y': (element.size['height'] / 2) + element.location['y']
    }


def alarmdismissnotif():
    """Dismiss alarm from notification"""
    screen_size = camtest.get_window_size()
    print(screen_size['height'])
    camtest.swipe(start_x=0, start_y=0, end_x=0, end_y=screen_size['height'])  # Swipe down notification
    time.sleep(2)
    try:
        camtest.find_element(AppiumBy.XPATH, value="//android.widget.Button[@text='SILENCE']").is_displayed()
        print("Silence button visible")
        camtest.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='SILENCE']").click()
        print("Timer stopped")
    except NoSuchElementException:
        try:
            element = camtest.find_element(AppiumBy.XPATH, value="//android.widget.TextView[@text='Timer']")
            print("alarm notification found")
            alrmleftx = element.location['x']  # left side pointer
            alrmlefty = element.location['y']  # top pointer
            print(alrmleftx)
            print(alrmlefty)
            print("taping the left corner to expand")
            subprocess.Popen(f'adb shell input tap {alrmleftx - 50} {alrmlefty}')
            time.sleep(2)
            camtest.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='SILENCE']").click()
            print("Timer stopped")
        except:
            raise Exception("alarm element not found")


def size():
    elem = camtest.find_elements(AppiumBy.XPATH, value="//android.widget.ImageView")
    print(len(elem))
    elear = []
    for i in elem:
        val = i.get_attribute("content-desc")
        elear.append(val)
    print(elear)


#alarmdismissnotif()
#size()
