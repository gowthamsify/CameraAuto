from appium import webdriver
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


class Appiumclass:

    def __init__(self, val):
        self.val = val
        print(val)
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

        self.camtest = webdriver.Remote('http://localhost:4723/wd/hub', desired_cap)
        self.camtest.implicitly_wait(10)

    def openappactivity(self, appactivity):
        """
                     Start an app-activity.
                     This will take a tuple.
                     openappactivity(self, app-activity):
                     :param Appactivity:
                     """

        self.camtest.start_activity(appactivity[0], appactivity[1])
        time.sleep(3)

    def clickbyid(self, id):
        """
            Click an element by ID.

            clickbyid(self, element_ID):
            :param Element_ID:
            """
        self.camtest.find_element(AppiumBy.ID, value=id).click()
        time.sleep(1)

    def clickbyxpath(self, valu):
        """
             Click an element using XPATH.

            clickbyid(self, element_XPATH):
            :param Element_XPATH:
            """
        self.camtest.find_element(AppiumBy.XPATH, value=valu).click()
        time.sleep(1)

    def checkelementexist(self, val):
        try:
            print("checking with id")
            elem = self.camtest.find_element(AppiumBy.ID, value=val)
            return elem
        except NoSuchElementException:
            try:
                print("checking with xpath")
                elem = self.camtest.find_element(AppiumBy.XPATH, value=val)
                return elem
            except NoSuchElementException:
                return 0

    def get_element(self, locator, return_multiple_elements=False, retried=False):
        """
               Returns element or elements.

               This will take either a tuple or a list of tuples.
               get_element((locator), return_multiple_elements=False, retried=False):
               :param locator:
               :param return_multiple_elements:
               :return:
               """
        try:
            if type(locator) == tuple:
                print(locator)
                a = type(locator)
                print(a)
                print(locator[0])
                if return_multiple_elements is False:
                    return self.get_element_by_type(method=locator[0], value=locator[1])
                else:
                    print("running elements")
                    return self.get_elements_by_type(method=locator[0], value=locator[1])
            elif type(locator) == list:
                for l in locator:
                    try:
                        if return_multiple_elements is False:
                            return self.get_element_by_type(method=l[0], value=l[1])
                        else:
                            return self.get_elements_by_type(method=l[0], value=l[1])
                    except NoSuchElementException:
                        pass
                raise NoSuchElementException
            else:
                raise Exception('Invalid locator type')
        except TypeError:
            if retried is False:
                self.get_element(locator, return_multiple_elements, True)

    def get_element_by_type(self, method, value):
        print(method)
        print(value)
        if method == 'ACCESSIBILITY_ID':
            return self.camtest.find_element(AppiumBy.ACCESSIBILITY_ID, value=value)
        elif method == 'XPATH':
            return self.camtest.find_element(AppiumBy.XPATH, value=value)
        elif method == 'ID':
            return self.camtest.find_element(AppiumBy.ID, value=value)
        elif method == 'NAME':
            return self.camtest.find_element(AppiumBy.NAME, value=value)
        elif method == 'CLASSNAME':
            return self.camtest.find_element(AppiumBy.CLASS_NAME, value=value)

    def get_elements_by_type(self, method, value):
        if method == 'ACCESSIBILITY_ID':
            return self.camtest.find_elements(AppiumBy.ACCESSIBILITY_ID, value=value)
        elif method == 'XPATH':
            return self.camtest.find_elements(AppiumBy.XPATH, value=value)
        elif method == 'ID':
            return self.camtest.find_elements(AppiumBy.ID, value=value)
        elif method == 'NAME':
            return self.camtest.find_elements(AppiumBy.NAME, value=value)
        elif method == 'CLASSNAME':
            return self.camtest.find_elements(AppiumBy.CLASS_NAME, value=value)

    '''def checkelementbyxpath(self, val):
        try:
            self.camtest.find_element(AppiumBy.XPATH, value=val)
            return 1
        except NoSuchElementException:
            return 0

    def find_element(self, pathid):

        camplc = self.camtest.find_element(AppiumBy.XPATH, value=pathid)
        print(camplc)
        return camplc'''

    def get_element_attributes(self, locator):
        """
        Return an elements coordinates and dimensions.
        :param locator:
        :return:
        """
        print(locator)
        try:
            # element = self.camtest.find_element(AppiumBy.XPATH, value=pathid)
            element = self.get_element(locator)
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

    def swipe_element(self, locator, direction, offset=3, duration=150):
        """
        Swipe an element up, down, left, or right
        :param locator:
        :param direction:
        :param offset:
        :param duration:
        :return:
        """
        # print(locator)
        element_attributes = self.get_element_attributes(locator)
        window_size = self.camtest.get_window_size()
        print(window_size)
        screen_bottom = window_size['height'] - offset
        screen_top = offset
        screen_left = offset
        screen_right = window_size['width'] - offset

        left_edge = element_attributes['left'] + offset
        right_edge = element_attributes['right'] - offset
        top_edge = element_attributes['top'] + offset
        bottom_edge = element_attributes['bottom'] - offset
        center_x = element_attributes['center_x']
        center_y = element_attributes['center_y']
        if direction == 'up':
            self.camtest.swipe(
                center_x,  # start x
                bottom_edge,  # start y
                center_x,  # end x
                screen_top,  # end y
                duration
            )
        elif direction == 'down':
            self.camtest.swipe(
                center_x,  # start x
                top_edge,  # start y
                center_x,  # end x
                screen_bottom,  # end y
                duration
            )
        elif direction == 'left':
            print("left")
            self.camtest.swipe(
                right_edge,  # start x
                center_y,  # start y
                screen_left,  # end x
                center_y,  # end y
                duration
            )
        elif direction == 'right':
            print("swiping right")
            self.camtest.swipe(
                left_edge,  # start x
                center_y,  # start y
                screen_right,  # end x
                center_y,  # end y
                duration
            )
        else:
            raise Exception('Invalid direction value: %s' % direction)

    def swipe_to_element(self, scrollable_element_locator, target_element_locator, direction, duration=200):
        """
        Swipe on a view until an element is visible.
        :param scrollable_element_locator:
        :param target_element_locator:
        :param direction:
        :param duration:
        :return:
        """
        scrollable_element_attributes = self.get_element_attributes(scrollable_element_locator)
        limit = 50
        attempts = 0
        while True:
            if attempts == limit:
                raise Exception('Could not swipe to element')
            if self.is_visible(target_element_locator):
                print("element found")
                break
            else:
                if direction == 'up':
                    self.camtest.swipe(
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['top'] + 100,
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['bottom'] - 100,
                        duration
                    )
                elif direction == 'down':
                    self.camtest.swipe(
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['bottom'] - 100,
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['top'] + 100,
                        duration
                    )
                elif direction == 'left':
                    self.camtest.swipe(
                        scrollable_element_attributes['left'] + 1,
                        scrollable_element_attributes['center_y'],
                        scrollable_element_attributes['right'] - 1,
                        scrollable_element_attributes['center_y'],
                        duration
                    )
                elif direction == 'right':
                    self.camtest.swipe(
                        scrollable_element_attributes['right'] - 1,
                        scrollable_element_attributes['center_y'],
                        scrollable_element_attributes['left'] + 1,
                        scrollable_element_attributes['center_y'],
                        duration
                    )
                else:
                    raise Exception('Invalid direction value: %s' % direction)
            attempts += 1

    def is_visible(self, locator):
        """
        Returns True if the element is visible.
        :param locator:
        :return:
        """
        try:
            return self.get_element(locator).is_displayed()
        except NoSuchElementException:
            return False

    def getelementpointer(self, locator):
        """
               Return an elements coordinates and dimensions

               Args:
                locator:(tuple) takes two positional value,getelementpoint(("ID or XPATH",element))

               return: elements location pointers
               """
        print(locator)
        method = []
        value = []
        try:
            if type(locator) == tuple:
                method = locator[0]
                value = locator[1]
            elif type(locator) == list:
                print("input list")
                print(locator)
                method = locator[0]
                value = locator[1]
        except:
            raise Exception("input type error")

        if method == 'ID':
            element = self.camtest.find_element(AppiumBy.ID, value=value)
        elif method == 'XPATH':
            element = self.camtest.find_element(AppiumBy.XPATH, value=value)
        return {
            'top': element.location['y'],
            'bottom': element.location['y'] + element.size['height'],
            'left': element.location['x'],
            'right': element.location['x'] + element.size['width'],
            'center_x': (element.size['width'] / 2) + element.location['x'],
            'center_y': (element.size['height'] / 2) + element.location['y']
        }

    def youtubeadhandler(self):

        """Checks for YouTube-ad elements and handles them """

        if self.is_visible(("ID", "com.google.android.youtube:id/content_thumbnail")):
            print("ad in progress")
            time.sleep(10)
            if self.is_visible(("ID", "com.google.android.youtube:id/skip_ad_button_container")):
                print("clicking skipping ad")
                self.clickbyid("com.google.android.youtube:id/skip_ad_button_container")
        elif self.is_visible(("ID", "com.google.android.youtube:id/skip_ad_button_container")):
            print("clicking skipping ad")
            self.clickbyid("com.google.android.youtube:id/skip_ad_button_container")
        else:
            print("ad not playing")

    def clickshutter(self):
        if self.is_visible(("ID", "com.android.camera:id/shutter_button_horizontal")):
            self.clickbyid("com.android.camera:id/shutter_button_horizontal")
        else:
            self.clickbyid('com.android.camera:id/shutter_button')

    # def getloc(self):

    def burstshot(self, burstsup):
        if self.is_visible(("ID", "com.android.camera:id/shutter_button_horizontal")):
            # shutterlocation = self.getelementpointer(('ID', 'com.android.camera:id/shutter_button'))
            shutterlocation = self.getelementpointer(("ID", "com.android.camera:id/shutter_button_horizontal"))
        else:
            shutterlocation = self.getelementpointer(('ID', 'com.android.camera:id/shutter_button'))
        shuttercentx = shutterlocation['center_x']
        shuttercenty = shutterlocation['center_y']
        screenend = self.camtest.get_window_size()
        if burstsup:
            # self.clickbyid("com.android.camera:id/up")
            # time.sleep(2)
            self.camtest.swipeandhold(start_x=shuttercentx, start_y=shuttercenty, end_y=shuttercenty, end_x=screenend['width'],
                              holdduration=3000)
        else:
            # self.clickbyxpath("//android.widget.TextView[@text='Press & hold Shutter button']")
            # time.sleep(2)
            # print("setting to burst")
            # self.clickbyxpath("//android.widget.CheckedTextView[@text='Burst shoot']")
            # time.sleep(2)
            # self.clickbyid("com.android.camera:id/up")
            # time.sleep(2)
            if self.is_visible(("ID", "com.android.camera:id/shutter_button_horizontal")):
                # self.long_press(('ID','com.android.camera:id/shutter_button'), duration=3000)
                self.camtest.longpress(("ID", "com.android.camera:id/shutter_button_horizontal"), duration=3000)
            else:
                self.camtest.longpress(('ID', 'com.android.camera:id/shutter_button'), duration=3000)

    def checkburstoption(self):
        limit = 3
        attempts = 0
        screenend = self.camtest.get_window_size()
        screenceny = screenend['height'] / 2
        screencenx = screenend['width'] / 2
        print(screencenx)
        print(screenceny)
        self.clickbyid("com.android.camera:id/top_config_12")
        time.sleep(2)
        print("clicking settings")
        self.clickbyxpath("//android.widget.FrameLayout[@content-desc='Settings']")
        time.sleep(2)
        while True:
            if attempts == limit:
                print("new burst")
                return True
            if self.is_visible(("XPATH", "//android.widget.TextView[@text='Press & hold Shutter button']")) is True:
                print("old long-press setting shutter to burst")
                self.clickbyxpath("//android.widget.TextView[@text='Press & hold Shutter button']")
                time.sleep(2)
                print("setting to burst")
                self.clickbyxpath("//android.widget.CheckedTextView[@text='Burst shoot']")
                time.sleep(2)
                self.clickbyid("com.android.camera:id/up")
                time.sleep(2)
                # return False
                break
            else:
                print("swipping")
                self.camtest.swipe(screencenx, screenceny, screenend['height'], screencenx)
            attempts += 1
            print(attempts)
        self.clickbyid("com.android.camera:id/up")
        time.sleep(2)
        return False


