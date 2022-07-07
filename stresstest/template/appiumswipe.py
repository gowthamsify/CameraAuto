from time import sleep
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from appium.webdriver.common.mobileby import MobileBy as By
from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver


class Screen:
    global_timeout = 60
    wait_timeout = 15

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

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_cap)
    driver.implicitly_wait(10)

    def __init__(self, val):
        self.val = val
        print(val)

    '''def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.wait_timeout)'''

    # get elements
    def _find_element(self, locator, return_multiple_elements=False, retried=False):
        """
        Returns element or elements.

        This will take either a tuple or a list of tuples.
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
                    print("flaseassign")
                    return self.get_element_by_type(method=locator[0], value=locator[1])
                else:
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
                self._find_element(locator, return_multiple_elements, True)

    def find_element(self, locator):
        return self._find_element(locator)

    def find_elements(self, locator):
        return self._find_element(locator, return_multiple_elements=True)

    def get_element_by_type(self, method, value):
        """
        Returns an element for the given method and locator
        :param method:
        :param value:
        :return:
        """
        print(method)
        print(value)
        if method == By.ACCESSIBILITY_ID:
            return self.driver.find_element_by_accessibility_id(value)
        elif method == By.ANDROID_UIAUTOMATOR:
            return self.driver.find_element_by_android_uiautomator('new UiSelector().%s' % value)
        elif method == By.IOS_UIAUTOMATION:
            return self.driver.find_element_by_ios_uiautomation(value)
        elif method == By.CLASS_NAME:
            return self.driver.find_element_by_class_name(value)
        elif method == By.ID:
            return self.driver.find_element_by_id(value)
        elif method == "By.XPATH":
            return self.driver.find_element_by_xpath(value)
        elif method == By.NAME:
            return self.driver.find_element_by_name(value)
        else:
            raise Exception('Invalid locator method.')

    def get_elements_by_type(self, method, value):
        """
        Returns a list of elements based on provided locator.
        :param method:
        :param value:
        :return:
        """
        if method == By.ACCESSIBILITY_ID:
            return self.driver.find_elements_by_accessibility_id(value)
        elif method == By.ANDROID_UIAUTOMATOR:
            return self.driver.find_elements_by_android_uiautomator('new UiSelector().%s' % value)
        elif method == By.IOS_UIAUTOMATION:
            return self.driver.find_elements_by_ios_uiautomation(value)
        elif method == By.CLASS_NAME:
            return self.driver.find_elements_by_class_name(value)
        elif method == By.ID:
            return self.driver.find_elements_by_id(value)
        elif method == By.XPATH:
            return self.driver.find_elements_by_xpath(value)
        elif method == By.NAME:
            return self.driver.find_elements_by_name(value)
        else:
            raise Exception('Invalid locator method.')

    def get_element_value(self, locator):
        """
        Returns the value of the element.
        :param locator:
        :return:
        """
        return self.wait_present(locator).get_attribute('value')

    def is_visible(self, locator):
        """
        Returns True if the element is visible.
        :param locator:
        :return:
        """
        try:
            return self.find_element(locator).is_displayed()
        except NoSuchElementException:
            return False

    def is_present(self, locator):
        """
        Returns True is the element is present.
        :param locator:
        :return:
        """
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False

    def is_enabled(self, locator):
        """
        Returns True if an element is enabled.

        Use this if you want to verify if a button is enabled and tappable.
        :param locator:
        :return:
        """
        return self.find_element(locator).is_enabled()

    def is_checked(self, locator):
        """
        Returns True if an element is enabled.

        Use this to verify if a checkbox is checked.
        :param locator:
        :return:
        """
        checked = self.find_element(locator).get_attribute('checked')
        if checked == 'false':
            return False
        elif checked == 'true':
            return True
        else:
            raise Exception('Not sure if this thing is checked or not.')

    def wait_visible(self, locator, timeout=global_timeout):
        """
        Wait for element to become visible, return element if visible, if not, return False.
        :param locator:
        :param timeout:
        :return:
        """
        count = 0
        while count != timeout:
            try:
                element = self.find_element(locator)
                if element.is_displayed() is True:
                    return element
            except NoSuchElementException:
                pass
            count += 1
            sleep(1)
        return False

    def wait_not_visible(self, locator, timeout=global_timeout):
        """
        Wait for element to become not visible.
        :param locator:
        :param timeout:
        :return:
        """
        count = 0
        while count != timeout:
            try:
                element_visible = self.is_visible(locator)
                if element_visible is False:
                    return True
            except NoSuchElementException:
                pass
            count += 1
            sleep(1)
        return False

    def wait_for_text(self, locator, text, timeout=global_timeout):
        """
        Wait for text to become visible.
        :param locator:
        :param text:
        :param timeout:
        :return:
        """
        count = 0
        while count != timeout:
            try:
                element = self.find_element(locator)
                element_text = element.text
                if element_text.lower() == text.lower():
                    return True
            except NoSuchElementException:
                pass
            count += 1
            sleep(1)
        return False

    def wait_clickable(self, locator):
        """
        Wait for an element to be clickable.

        :param locator:
        :return:
        """
        try:
            return self.wait.until(ec.element_to_be_clickable(locator))
        except TypeError:
            return self.wait.until(ec.element_to_be_clickable(locator))

    def wait_present(self, locator):
        """
        Wait for an element to be present

        :param locator:
        :return:
        """
        try:
            return self.wait.until(ec.presence_of_element_located(locator))
        except TypeError:
            return self.wait.until(ec.presence_of_element_located(locator))

    def click(self, locator):
        """
        Click an element with a fallback to tap.
        :param locator:
        :return:
        """
        try:
            if type(locator) == tuple:
                self.wait_clickable(locator).click()
                return True
            elif type(locator) == list:
                for l in locator:
                    try:
                        self.wait_clickable(l).click()
                        return True
                    except NoSuchElementException:
                        pass
                    except TimeoutException:
                        pass
            else:
                raise Exception('Cannot click element. Invalid locator type.')
            raise Exception('Unable to click element.')
        except WebDriverException:
            # iOS is sometimes annoying and won't let you click, try tap as a fallback
            self.tap(locator)
            return True

    def tap(self, locator=None, x=None, y=None):
        """
        Taps an element.
        :param locator:
        :return:
        """
        element = None
        if locator is not None:
            if type(locator) == tuple:
                element = self.wait_present(locator)
            elif type(locator) == list:
                for l in locator:
                    try:
                        element = self.wait_present(l)
                        break
                    except NoSuchElementException:
                        pass
                    except TimeoutException:
                        pass
            else:
                raise Exception('Cannot click element. Invalid locator type.')
            if element is None:
                raise Exception('Could not tap. Element not found.')

        action = TouchAction(self.driver)

        # try tapping again if it fails the first time twice
        try:
            action.tap(element, x=x, y=y).perform()
            return True
        except WebDriverException:
            action.tap(element, x=x, y=y).perform()
            return True

    def send_keys(self, locator, text, force_send_keys=False):
        """
        Input text into an field.

        Text input is more reliable and faster on iOS if you use set_value(), so this will be used on iOS by default.

        Sometimes you'll need to use send_keys() on iOS, so you can force that to be used by passing it a True param.
        :param locator:
        :param text:
        :param force_send_keys:
        :return:
        """
        if text is None or text == '':
            raise Exception('Text cannot be blank')

        element = self.wait.until(ec.visibility_of_element_located(locator))
        if force_send_keys is True:
            element.send_keys(text)
            return True
        elif self.driver.name == 'iOS':
            element.set_value(text)
            return True
        else:
            element.send_keys(text)
            return True

    def clear_text(self, locator, expected_text=None):
        """
        Clear value from an input.

        Some devices do not clear the entire text field with the build in clear method.

        This attempts to clear an input several times. expected_text is used for fields that have placeholder text.
        :param locator:
        :param expected_text:
        :return:
        """
        attempts = 0
        text_field = self.wait.until(ec.visibility_of_element_located(locator))
        text_field_cleared = False
        while attempts < 50:

            # Temp fix for Appium issue with clearing fields
            # text_field.clear()
            try:
                text_field.clear()
            except WebDriverException:
                pass
            text_field = self.find_element(locator)
            if expected_text is None:
                if text_field.text == '':
                    text_field_cleared = True
                    break
            else:
                expected_texts = ['']
                if type(expected_text) is list:
                    expected_texts.extend(expected_text)
                elif type(expected_text) is str:
                    expected_texts.append(expected_text)
                else:
                    raise Exception('Expected text is an unexpected variable type: {}'.format(type(expected_text)))
                if text_field.text in expected_texts:
                    text_field_cleared = True
                    break
            attempts += 1
        assert text_field_cleared, 'Text field was not cleared, still have this text: "{}".'.format(text_field.text)

    def swipe_to_element(self, scrollable_element_locator, target_element_locator, direction, duration=2000):
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
                break
            else:
                if direction == 'up':
                    self.driver.swipe(
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['top'] + 50,
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['bottom'] - 50,
                        duration
                    )
                elif direction == 'down':
                    self.driver.swipe(
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['bottom'] - 50,
                        scrollable_element_attributes['center_x'],
                        scrollable_element_attributes['top'] + 50,
                        duration
                    )
                elif direction == 'left':
                    self.driver.swipe(
                        scrollable_element_attributes['left'] + 1,
                        scrollable_element_attributes['center_y'],
                        scrollable_element_attributes['right'] - 1,
                        scrollable_element_attributes['center_y'],
                        duration
                    )
                elif direction == 'right':
                    self.driver.swipe(
                        scrollable_element_attributes['right'] - 1,
                        scrollable_element_attributes['center_y'],
                        scrollable_element_attributes['left'] + 1,
                        scrollable_element_attributes['center_y'],
                        duration
                    )
                else:
                    raise Exception('Invalid direction value: %s' % direction)
            attempts += 1

    def swipe_element(self, locator, direction, offset=3, duration=150):
        """
        Swipe an element up, down, left, or right
        :param locator:
        :param direction:
        :param offset:
        :param duration:
        :return:
        """
        element_attributes = self.get_element_attributes(locator)
        window_size = self.driver.get_window_size()
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
            self.driver.swipe(
                center_x,  # start x
                bottom_edge,  # start y
                center_x,  # end x
                screen_top,  # end y
                duration
            )
        elif direction == 'down':
            self.driver.swipe(
                center_x,  # start x
                top_edge,  # start y
                center_x,  # end x
                screen_bottom,  # end y
                duration
            )
        elif direction == 'left':
            self.driver.swipe(
                right_edge,  # start x
                center_y,  # start y
                screen_left,  # end x
                center_y,  # end y
                duration
            )
        elif direction == 'right':
            self.driver.swipe(
                left_edge,  # start x
                center_y,  # start y
                screen_right,  # end x
                center_y,  # end y
                duration
            )
        else:
            raise Exception('Invalid direction value: %s' % direction)

    def long_press(self, locator, duration=1000):
        """
        Tap and hold on an element for a given duration.
        :param locator:
        :param duration:
        :return:
        """
        element = None
        if type(locator) == tuple:
            element = self.find_element(locator)
        elif 'appium.webdriver.webelement.WebElement' in str(type(locator)):
            element = locator
        action = TouchAction(self.driver)
        action.long_press(element, None, None, duration).perform()

    def get_element_attributes(self, locator):
        """
        Return an elements coordinates and dimensions.
        :param locator:
        :return:
        """
        element = self.find_element(locator)
        return {
            'top': element.location['y'],
            'bottom': element.location['y'] + element.size['height'],
            'left': element.location['x'],
            'right': element.location['x'] + element.size['width'],
            'center_x': (element.size['width'] / 2) + element.location['x'],
            'center_y': (element.size['height'] / 2) + element.location['y']
        }

    def pull_to_refresh(self, locator, duration=1000):
        """
        Pull down on a given scrollable element to refresh.
        :param locator:
        :param duration:
        :return:
        """
        scrollable_element_attributes = self.get_element_attributes(locator)
        self.driver.swipe(
            scrollable_element_attributes['center_x'],
            scrollable_element_attributes['top'] + 1,
            scrollable_element_attributes['center_x'],
            scrollable_element_attributes['bottom'] - 1,
            duration
        )

    def hide_keyboard(self):
        """
        Hides keyboard if present.
        :return:
        """
        try:
            sleep(.1)
            self.driver.hide_keyboard()
        except WebDriverException:
            pass


dc = Screen('strat')
a = ['By.ID', '//com.miui.home:id/title[@text="WhatsApp"]']
b = '//com.miui.home:id/title[@text="WhatsApp"]'
dc.swipe_element(('By.XPATH', "//com.miui.home:id/title[@text='WhatsApp']"), 'left')
