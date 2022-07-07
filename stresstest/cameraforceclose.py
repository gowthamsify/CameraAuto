import time

from globalfunctions import *


def modeswipestress(loop):
    """Swipes through the camera modes and checks the stability
        :param: enter the loop count"""
    modeswipe = excelobj.creatsheet('modeswipe')
    try:
        cammode = []
        moremode = []
        opencam()
        time.sleep(5)
        elemval = cameratest.get_element(("ID", "com.android.camera:id/mode_select_item"), True)
        for i in elemval:
            modeval = i.__getattribute__("text")
            cammode.append(modeval)
            cammode.sort(reverse=True)
        cammode.remove('More')
        print(cammode)

        cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
        time.sleep(1)
        moreelemt = cameratest.get_element(("ID", "com.android.camera:id/mode_name"), True)
        for l in moreelemt:
            moreval = l.__getattribute__("text")
            moremode.append(moreval)
        ed = "Edit"
        if ed in moremode:
            moremode.remove('Edit')
        else:
            print("more has no edit button")
        print(moremode)

        for a in range(loop):
            prevval = ""
            for j in cammode:
                print(j)
                testt = f"//android.widget.TextView[@text='{j}']"
                print(testt)
                if prevval == "Pro":
                    move = 'right'
                else:
                    move = 'left'
                elemvisi = cameratest.is_visible(("XPATH", f"//android.widget.TextView[@text='{j}']"))
                if elemvisi is False:
                    print("element not visible, swiping to element")
                    print(move)
                    cameratest.swipe_to_element(("ID", "com.android.camera:id/mode_select_scrollview"),
                                                ("XPATH", f"//android.widget.TextView[@text='{j}']"), move)
                    validatresult(modeswipe, j)
                    cameratest.clickbyxpath(f"//android.widget.TextView[@text='{j}']")
                    validatresult(modeswipe, j)
                    time.sleep(3)
                    prevval = j
                else:
                    print("element visible")
                    cameratest.clickbyxpath(f"//android.widget.TextView[@text='{j}']")
                    time.sleep(3)
                    validatresult(modeswipe, j)
                    prevval = j
            for k in moremode:
                elemvisi = cameratest.is_visible(("XPATH", "//android.widget.TextView[@text='More']"))
                if elemvisi is False:
                    print("element not visible, swiping to element")
                    cameratest.swipe_to_element(("ID", "com.android.camera:id/mode_select_scrollview"),
                                                ("XPATH", "//android.widget.TextView[@text='More']"), 'right')
                    validatresult(modeswipe, k)
                    cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
                    time.sleep(3)
                    validatresult(modeswipe, k)
                else:
                    print("elemnt more visible")
                    cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
                    validatresult(modeswipe, k)
                cameratest.clickbyxpath(f"//android.widget.TextView[@text='{k}']")
                time.sleep(2)
                validatresult(modeswipe, k)
                cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")
                time.sleep(2)
                validatresult(modeswipe, k)
                print("completed cycle:", a + 1)
        closecam()
    except NoSuchElementException:
        if validate("com.android.camera") is False:
            print("app is closed")
            excelobj.updatesheet(modeswipe, "camera App crashed", "camera App crashed")
        else:
            print("app is active element is not found")
            excelobj.updatesheet(modeswipe, "test error", "test error")


def validatresult(shname, case):
    if validate("com.android.camera") is False:
        excelobj.updatesheet(shname, case, result='FAIL')
    else:
        excelobj.updatesheet(shname, case, result='PASS')


def allmodestress(loop, burstop):
    global a
    attempts = 0
    allmodecap = excelobj.creatsheet("allmodecapstress")
    try:
        cammode = []
        moremode = []
        videomodes = ['Video', 'Slow motion', 'Time-lapse', 'Movie effect', 'Long exposure', 'Dual video',
                      'Short video', 'Panorama']
        opencam()
        time.sleep(5)
        elemval = cameratest.get_element(("ID", "com.android.camera:id/mode_select_item"), True)
        for i in elemval:
            modeval = i.__getattribute__("text")
            cammode.append(modeval)
            cammode.sort(reverse=True)
        cammode.remove('More')
        print(cammode)

        cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
        time.sleep(1)
        moreelemt = cameratest.get_element(("ID", "com.android.camera:id/mode_name"), True)
        for l in moreelemt:
            moreval = l.__getattribute__("text")
            moremode.append(moreval)
        ed = "Edit"
        if ed in moremode:
            moremode.remove('Edit')
        else:
            print("more has no edit button")
        moremode.remove('Clone')
        print(moremode)

        # moremode.sort()

        for a in range(loop):
            prevval = ""
            for j in cammode:
                print(f"Mode in progress: {j}")
                # testt = f"//android.widget.TextView[@text='{j}']"
                # print(testt)
                if prevval == "Pro":
                    move = 'right'
                else:
                    move = 'left'
                elemvisi = cameratest.is_visible(("XPATH", f"//android.widget.TextView[@text='{j}']"))
                if elemvisi is False:
                    print("element not visible, swiping to element")
                    print(move)
                    cameratest.swipe_to_element(("ID", "com.android.camera:id/mode_select_scrollview"),
                                                ("XPATH", f"//android.widget.TextView[@text='{j}']"), move)
                    cameratest.clickbyxpath(f"//android.widget.TextView[@text='{j}']")
                    time.sleep(3)
                    if j in videomodes:
                        print(f"video mode start recoding: {j}")
                        cameratest.clickshutter()
                        time.sleep(20)
                        if j == 'Short video':
                            print("saving short video")
                            cameratest.clickbyid('com.android.camera:id/live_preview_save')
                            time.sleep(10)
                        else:
                            print("stopping rec")
                            cameratest.clickshutter()
                            time.sleep(3)
                        # validatforclose("com.android.camera", f"capture:'{j}'")
                        validatresult(allmodecap, f"capture:'{j}'")
                    elif j == 'Documents':
                        print("document mode")
                        cameratest.clickshutter()
                        time.sleep(3)
                        if validate("com.miui.extraphoto/.docphoto.document.DocPhotoPostProcessingActivity", bug=False):
                            print("clicking discard")
                            cameratest.clickbyid('com.miui.extraphoto:id/discard')
                            # validatforclose("com.android.camera", f"capture:'{j}'")
                            validatresult(allmodecap, f"capture:'{j}'")
                        else:
                            print('Dynamic Document')
                            # validatforclose("com.android.camera", f"capture:'{j}'")
                            validatresult(allmodecap, f"capture:'{j}'")
                    elif j == 'VLOG':
                        cameratest.swipe_to_element(('ID', 'com.android.camera:id/vv_gallery_item_image'), (
                            'XPATH', "//android.widget.TextView[@text='Dreams']"), 'right')
                        cameratest.clickbyxpath("//android.widget.TextView[@text='Dreams']")
                        cameratest.clickshutter()
                        for i in range(5):
                            cameratest.clickbyid("com.android.camera:id/vv_preview_save_circle")
                            time.sleep(5)
                        cameratest.clickbyid("com.android.camera:id/vv_preview_save")
                        time.sleep(10)
                        validatresult(allmodecap, f"capture:'{j}'")

                    else:
                        # cameratest.clickbyid('com.android.camera:id/shutter_button')
                        cameratest.clickshutter()
                        time.sleep(3)
                        # validatforclose("com.android.camera", f"capture:'{j}'")
                        validatresult(allmodecap, f"capture:'{j}'")
                    time.sleep(2)
                else:
                    print("element visible")
                    cameratest.clickbyxpath(f"//android.widget.TextView[@text='{j}']")
                    time.sleep(1)
                    if j in videomodes:
                        print("video mode start recoding")
                        cameratest.clickshutter()
                        time.sleep(20)
                        if j == 'Short video':
                            print("saving short video")
                            cameratest.clickbyid('com.android.camera:id/live_preview_save')
                            time.sleep(10)
                        else:
                            print("stopping rec")
                            cameratest.clickshutter()
                            time.sleep(3)
                        # validatforclose("com.android.camera", f"capture:'{j}'")
                        validatresult(allmodecap, f"capture:'{j}'")

                    elif j == 'Documents':
                        print("document mode")
                        cameratest.clickshutter()
                        time.sleep(3)
                        if validate("com.miui.extraphoto/.docphoto.document.DocPhotoPostProcessingActivity",
                                    bug=False) is True:
                            print("clicking discard")
                            cameratest.clickbyid('com.miui.extraphoto:id/discard')
                            # validatforclose("com.android.camera", f"capture:'{j}'")
                            # validatresult(allmodecap, f"capture:'{j}'")
                        else:
                            print('Dynamic Document')
                            # validatforclose("com.android.camera", f"capture:'{j}'")
                        validatresult(allmodecap, f"capture:'{j}'")

                    elif j == 'VLOG':
                        cameratest.swipe_to_element(('ID', 'com.android.camera:id/vv_gallery_item_image'), (
                            'XPATH', "//android.widget.TextView[@text='Dreams']"), 'right')
                        cameratest.clickbyxpath("//android.widget.TextView[@text='Dreams']")
                        cameratest.clickshutter()
                        for i in range(5):
                            cameratest.clickbyid("com.android.camera:id/vv_preview_save_circle")
                            time.sleep(5)
                        cameratest.clickbyid("com.android.camera:id/vv_preview_save")
                        time.sleep(10)
                        validatresult(allmodecap, f"capture:'{j}'")
                    else:
                        cameratest.clickshutter()
                        time.sleep(3)
                        # validatforclose("com.android.camera", f"capture:'{j}'")
                        validatresult(allmodecap, f"capture:'{j}'")
                prevval = j
            for k in moremode:
                print(f"more in progress: {k}")
                elemvisi = cameratest.is_visible(("XPATH", "//android.widget.TextView[@text='More']"))
                if elemvisi is False:
                    print("element not visible, swiping to element")
                    cameratest.swipe_to_element(("ID", "com.android.camera:id/mode_select_scrollview"),
                                                ("XPATH", "//android.widget.TextView[@text='More']"), 'right')
                    # validatforclose("com.android.camera", f"capture:'{k}'")
                    # validatresult(allmodecap, f"capture:'{k}'")
                    cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
                    time.sleep(2)
                else:
                    print("elemnt more visible")
                    cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
                cameratest.clickbyxpath(f"//android.widget.TextView[@text='{k}']")
                time.sleep(2)
                if k in videomodes:
                    print(f"video mode start recoding: {k}")
                    cameratest.clickshutter()
                    time.sleep(20)
                    if k == 'Short video':
                        print(" saving short video")
                        cameratest.clickbyid('com.android.camera:id/live_preview_save')
                        time.sleep(10)
                    else:
                        print("stopping rec")
                        cameratest.clickshutter()
                        time.sleep(3)
                    # validatforclose("com.android.camera", f"capture:'{k}'")
                    validatresult(allmodecap, f"capture:'{k}'")
                    #     cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")
                elif k == 'Documents':
                    print("document mode")
                    cameratest.clickshutter()
                    time.sleep(3)
                    if validate("com.miui.extraphoto/.docphoto.document.DocPhotoPostProcessingActivity", bug=False):
                        print("clicking discard")
                        cameratest.clickbyid('com.miui.extraphoto:id/discard')
                        # validatforclose("com.android.camera", f"capture:'{k}'")
                        # validatresult(allmodecap, f"capture:'{k}'")
                        # cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")
                    else:
                        print('Dynamic Document')
                        # validatforclose("com.android.camera", f"capture:'{k}'")
                    validatresult(allmodecap, f"capture:'{k}'")
                    # cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")
                elif k == 'VLOG':
                    cameratest.swipe_to_element(('ID', 'com.android.camera:id/vv_gallery_item_image'), (
                        'XPATH', "//android.widget.TextView[@text='Dreams']"), 'right')
                    cameratest.clickbyxpath("//android.widget.TextView[@text='Dreams']")
                    cameratest.clickshutter()
                    for i in range(5):
                        cameratest.clickbyid("com.android.camera:id/vv_preview_save_circle")
                        time.sleep(5)
                    cameratest.clickbyid("com.android.camera:id/vv_preview_save")
                    time.sleep(10)
                    validatresult(allmodecap, f"capture:'{k}'")
                else:
                    cameratest.clickshutter()
                    time.sleep(3)
                    # # validatforclose("com.android.camera", f"capture:'{k}'")
                    # validatresult(allmodecap, f"capture:'{k}'")
                    # cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")
                    # time.sleep(2)
                    validatresult(allmodecap, f"capture:'{k}'")
                cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")

            cameratest.burstshot(burstop)
            validatresult(allmodecap, f"capture:'burst-mode'")
            print("completed cycle:", a + 1)
        closecam()
    except NoSuchElementException:
        attempts += 1
        remainloop = loop - a
        print(remainloop)
        if validate("com.android.camera") is False:
            print("app is closed")
            excelobj.updatesheet(allmodecap, "camera has closed", "camera has closed")
        else:
            print("app is active element is not found")
            excelobj.updatesheet(allmodecap, "test error", "test error")
        if attempts == 3:
            print("max try done")
            closecam()
        else:
            allmodestress(remainloop)
            closecam()


def validatforclose(app, case):
    if validate(app) is False:
        excelobj.captureallmode(case, 'fail')
    else:
        excelobj.captureallmode(case, 'pass')


# swipemodestress(2)
# checkcamswip()

def individualmodes(modes, loop):
    """Executes individual modes
    :parameter : 1st Mode to execute, 2nd number of loops"""
    global a, b
    attempts = 0
    indivimode = excelobj.creatsheet("select-mode")
    mode = [modes]
    try:
        cammode = []
        moremode = []
        videomodes = ['Video', 'Slow motion', 'Time-lapse', 'Movie effect', 'Long exposure', 'Dual video', 'VLOG',
                      'Short video', 'Panorama']
        opencam()
        time.sleep(5)
        elemval = cameratest.get_element(("ID", "com.android.camera:id/mode_select_item"), True)
        for i in elemval:
            modeval = i.__getattribute__("text")
            cammode.append(modeval)
            cammode.sort(reverse=True)
        cammode.remove('More')
        print(cammode)

        cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
        time.sleep(1)
        moreelemt = cameratest.get_element(("ID", "com.android.camera:id/mode_name"), True)
        for l in moreelemt:
            moreval = l.__getattribute__("text")
            moremode.append(moreval)
        ed = "Edit"
        if ed in moremode:
            moremode.remove('Edit')
        else:
            print("more has not edit")
        print(moremode)

        for b in range(loop):
            prevval = ""
            for j in cammode:
                print(j)
                testt = f"//android.widget.TextView[@text='{j}']"
                print(testt)
                if prevval == "Pro":
                    move = 'right'
                else:
                    move = 'left'
                if j in mode:
                    elemvisi = cameratest.is_visible(("XPATH", f"//android.widget.TextView[@text='{j}']"))
                    if elemvisi is False:
                        print("element not visible, swiping to element")
                        print(move)
                        cameratest.swipe_to_element(("ID", "com.android.camera:id/mode_select_scrollview"),
                                                    ("XPATH", f"//android.widget.TextView[@text='{j}']"), move)
                        cameratest.clickbyxpath(f"//android.widget.TextView[@text='{j}']")
                        time.sleep(3)
                        if j in videomodes:
                            print("video mode start recoding")
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(10)
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(3)
                            # validatforclose("com.android.camera", f"capture:'{j}'")
                            validatresult(indivimode, f"capture:'{j}'")
                        elif j == 'Documents':
                            print("document mode")
                            cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(3)
                            if validate(
                                    "com.miui.extraphoto/.docphoto.document.DocPhotoPostProcessingActivity",
                                    bug=False) is True:
                                print("clicking discard")
                                cameratest.clickbyid('com.miui.extraphoto:id/discard')
                                # validatforclose("com.android.camera", f"capture:'{j}'")
                                validatresult(indivimode, f"capture:'{j}'")
                            else:
                                print('Dynamic Document')
                                # validatforclose("com.android.camera", f"capture:'{j}'")
                                validatresult(indivimode, f"capture:'{j}'")
                        else:
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(3)
                            # validatforclose("com.android.camera", f"capture:'{j}'")
                            validatresult(indivimode, f"capture:'{j}'")
                        time.sleep(2)
                        prevval = j
                    else:
                        print("element visible")
                        cameratest.clickbyxpath(f"//android.widget.TextView[@text='{j}']")
                        time.sleep(1)
                        if j in videomodes:
                            print("video mode start recoding")
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(10)
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(3)
                            if j == 'Short video':
                                cameratest.clickbyid('com.android.camera:id/live_preview_save')
                                time.sleep(10)
                            # validatforclose("com.android.camera", f"capture:'{j}'")
                            validatresult(indivimode, f"capture:'{j}'")
                        elif j == 'Documents':
                            print("document mode")
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(3)
                            if validate(
                                    "com.miui.extraphoto/.docphoto.document.DocPhotoPostProcessingActivity",
                                    bug=False) is True:
                                print("clicking discard")
                                cameratest.clickbyid('com.miui.extraphoto:id/discard')
                                # validatforclose("com.android.camera", f"capture:'{j}'")
                                validatresult(indivimode, f"capture:'{j}'")
                            else:
                                print('Dynamic Document')
                                validatforclose("com.android.camera", f"capture:'{j}'")
                        else:
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(3)
                            # validatforclose("com.android.camera", f"capture:'{j}'")
                            validatresult(indivimode, f"capture:'{j}'")
                    prevval = j
                else:
                    print(f"mode not selected{j}")
                    prevval = j
                for k in moremode:
                    if k in mode:
                        elemvisi = cameratest.is_visible(("XPATH", "//android.widget.TextView[@text='More']"))
                        if elemvisi is False:
                            print("element not visible, swiping to element")
                            cameratest.swipe_to_element(("ID", "com.android.camera:id/mode_select_scrollview"),
                                                        ("XPATH", "//android.widget.TextView[@text='More']"), 'right')
                            # validatforclose("com.android.camera", f"capture:'{k}'")
                            validatresult(indivimode, f"capture:'{j}'")
                            cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
                            time.sleep(2)
                        else:
                            print("elemnt more visible")
                            cameratest.clickbyxpath("//android.widget.TextView[@text='More']")
                        cameratest.clickbyxpath(f"//android.widget.TextView[@text='{k}']")
                        time.sleep(2)
                        if k in videomodes:
                            print("video mode start recoding")
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(10)
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(3)
                            if k == 'Short video':
                                cameratest.clickbyid('com.android.camera:id/live_preview_save')
                                time.sleep(10)
                            # validatforclose("com.android.camera", f"capture:'{k}'")
                            validatresult(indivimode, f"capture:'{k}'")
                            cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")
                        elif k == 'Documents':
                            print("document mode")
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(3)
                            if validate(
                                    "com.miui.extraphoto/.docphoto.document.DocPhotoPostProcessingActivity",
                                    bug=False) is True:
                                print("clicking discard")
                                cameratest.clickbyid('com.miui.extraphoto:id/discard')
                                # validatforclose("com.android.camera", f"capture:'{k}'")
                                validatresult(indivimode, f"capture:'{k}'")
                                cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")
                            else:
                                print('Dynamic Document')
                                # validatforclose("com.android.camera", f"capture:'{k}'")
                                validatresult(indivimode, f"capture:'{k}'")
                                cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")
                        else:
                            cameratest.clickshutter()
                            # cameratest.clickbyid('com.android.camera:id/shutter_button')
                            time.sleep(3)
                            # validatforclose("com.android.camera", f"capture:'{k}'")
                            validatresult(indivimode, f"capture:'{k}'")
                            cameratest.clickbyid("com.android.camera:id/bottom_external_mode_close")
                            time.sleep(2)
                        print("completed cycle:", b + 1)
                    else:
                        print(f"mode not selected{k}")

        closecam()
    except NoSuchElementException:
        attempts += 1
        if validate("com.android.camera") is False:
            print("app is closed")
            excelobj.updatesheet(indivimode, "camera has closed", "camera has closed")
            reamingcycle = loop - b
            if attempts == 3:
                print("maxed out retries")

        else:
            print("app is active element is not found")
            closecam()
            excelobj.captureallmode(indivimode, "test error", "test error")


# def burstshot():
#     shutterlocation = cameratest.getelementpointer(('ID', 'com.android.camera:id/shutter_button'))
#     shuttercentx = shutterlocation['center_x']
#     shuttercenty = shutterlocation['center_y']
#
#
#     cameratest.swipe_element(('ID', 'com.android.camera:id/shutter_button'), 'right', duration=3000)
#
#
#
# def swipvlo():
#     cameratest.swipe_to_element(('ID', 'com.android.camera:id/vv_gallery_item_image'), (
#         'XPATH', "//android.widget.TextView[@text='Dreams']"), 'right')
#     cameratest.clickbyxpath("//android.widget.TextView[@text='Dreams']")
#     cameratest.clickshutter()
#     for i in range(5):
#         cameratest.clickbyid("com.android.camera:id/vv_preview_save_circle")
#         time.sleep(5)
#     cameratest.clickbyid("com.android.camera:id/vv_preview_save")
#     time.sleep(10)
# swipvlo()
# cameratest.burstshot(True)
