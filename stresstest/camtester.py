from stresstest.globalfunctions import *
from stresstest.imgsizeverifier import smallimagverifier

'''def readcordinates():
    opencam()
    time.sleep(5)
    adb("adb exec-out screencap -p > C:\\Users\\Stresstest\\screenshot.png")
    shutterx, shuttery = image_position("C:\\Users\\Stresstest\\shutterbutton.jpg",
                                        "C:\\Users\\Stresstest\\screenshot.png")
    print(shutterx, shuttery)
    click(shutterx, shuttery)
    time.sleep(3)
    portraitx, portraity = image_position("C:\\Users\\Stresstest\\portrait.jpg",
                                          "C:\\Users\\Stresstest\\screenshot.png")
    print(portraitx, portraity)
    click(portraitx, portraity)
    time.sleep(3)
    photox, photoy = image_position("C:\\Users\\Stresstest\\photo.jpg", "C:\\Users\\Stresstest\\screenshot.png")
    print(photox, photoy)
    click(photox, photoy)


def switchmode():
    portraitcmd = "adb shell input tap 434 1177"
    videocmd = "adb shell input tap 222 1177"
    procmd = "adb shell input tap 141 1177"

    subprocess.run(portraitcmd)
    time.sleep(3)
    subprocess.run(videocmd)
    time.sleep(3)
    subprocess.run(videocmd)
    time.sleep(3)
    subprocess.run(procmd)
    time.sleep(3)
    subprocess.run(portraitcmd)
    time.sleep(3)


if __name__ == "__main__":
    opencam()
    for i in range(1000):
        capture()
        time.sleep(5)
        switchmode()
        time.sleep(5)
        c = validate()
        print("total number", c)'''


def test():
    opencam()
    time.sleep(5)
    shutrx, shutry = readshutter()
    portx, porty = readportrait()
    click(portx, porty)
    time.sleep(2)
    photx, photy = readphotpos()
    click(photx, photy)
    time.sleep(2)
    vhdrsonx, vhdrsony = readhdrson()
    click(vhdrsonx, vhdrsony)
    time.sleep(2)
    vhdronx, vhdrony = readhdron()
    click(vhdronx, vhdrony)
    time.sleep(2)
    vhdrsoffx, vhdrsoffy = readhdrsoff()
    click(vhdrsoffx, vhdrsoffy)
    time.sleep(2)
    vhdroffx, vhdroffy = readhdroff()
    click(vhdroffx, vhdroffy)
    time.sleep(2)
    for i in range(500):
        click(shutrx, shutry)
        time.sleep(3)
        smallimagverifier()
        click(portx, porty)
        time.sleep(3)
        click(shutrx, shutry)
        time.sleep(3)
        smallimagverifier()
        click(photx, photy)
        time.sleep(3)
        click(vhdrsonx, vhdrsony)
        time.sleep(2)
        click(vhdronx, vhdrony)
        time.sleep(2)
        click(shutrx, shutry)
        time.sleep(3)
        smallimagverifier()
        click(vhdrsoffx, vhdrsoffy)
        time.sleep(1)
        click(vhdroffx, vhdroffy)

    lock = "adb shell input keyevent 26"
    subprocess.run(lock)

'''shutrx, shutry = '412', '1910'
morex, morey = '938', '126'
aspec34x, aspec34y = '327', '162'
aspec19x, aspec19y = '552', '162'
aspecfullx, aspecfully = '777', '162'
aspec11x, aspec11y = '102', '162'


def j20camtest():
    opencam()
    time.sleep(5)
    click(shutrx, shutry)
    time.sleep(3)
    smallimagverifier()
    click(morex, morey)
    time.sleep(2)
    click(aspec19x, aspec19y)
    time.sleep(2)
    click(shutrx, shutry)
    time.sleep(3)
    smallimagverifier()
    click(morex, morey)
    time.sleep(2)
    click(aspecfullx, aspecfully)
    time.sleep(2)
    click(shutrx, shutry)
    time.sleep(3)
    smallimagverifier()
    click(morex, morey)
    time.sleep(2)
    click(aspec11x, aspec11y)
    time.sleep(2)
    click(shutrx, shutry)
    time.sleep(3)
    smallimagverifier()
    click(morex, morey)
    time.sleep(2)
    click(aspec34x, aspec34y)
    time.sleep(2)'''


if __name__ == "__main__":
    test()
    '''for i in range(2):
        ite = i + 1
        #j20camtest()
        print("iteration completed:" + str(ite))
    clr_rect()
    lock = "adb shell input keyevent 26"
    subprocess.run(lock)'''