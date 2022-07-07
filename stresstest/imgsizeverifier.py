import os
import re
import time

from PIL import Image
from PIL.ExifTags import TAGS
from ppadb import client
from globalfunctions import *

'''abd = client.Client(host="127.0.0.1", port=5037)

client.remote_connect("172.20.0.1", 5555) #replace with phone IP

device = client.device("172.20.0.1:5555") #replace with phone IP

#adb tcpip 5555 (setup in device)
# Disconnect all devices
client.remote_disconnect()'''

##Disconnect 172.20.0.1
# client.remote_disconnect("172.20.0.1")
##Or
# client.remote_disconnect("172.20.0.1", 5555)

adb = client.Client(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037

devices = adb.devices()
if len(devices) == 0:
    print("no device is present")
    quit()

device = devices[0]


def smallimagverifier(usecase, resl):
    """Verifies the last captured image for small image by reading the image information
        :param: pass the use-case for result entry """

    list_images = device.shell("ls /sdcard/DCIM/Camera")
    print(list_images)
    reg_exp = "IMG_[\d]+_[\d]+.jpg"
    list_of_all_img = re.findall(reg_exp, list_images)
    list_of_all_img.sort()
    print(list_of_all_img)
    print(list_of_all_img[len(list_of_all_img) - 1])
    img_name = str(list_of_all_img[len(list_of_all_img) - 1]).strip()
    print(img_name)
    imgpullcmd = (
            "adb pull /sdcard/DCIM/Camera/" + img_name + " " + "C:\\Users\\gowth\\PycharmProjects\\StressAutomation"
                                                               "\\stresstest\\")
    print(imgpullcmd)
    subprocess.run(imgpullcmd)
    time.sleep(2)
    print("image_fetched   .........")
    imgpath = ("C:\\Users\\gowth\\PycharmProjects\\StressAutomation\\stresstest\\" + img_name)
    print(imgpath)
    delcmd = ("del" + " " + imgpath)
    print(delcmd)
    image_name = f"{list_of_all_img[len(list_of_all_img) - 1]}"

    image = Image.open(image_name)
    exif_data = image.getexif()
    ex_data = []
    for tag_id in exif_data:
        tag = TAGS.get(tag_id, tag_id)
        data = str(exif_data.get(tag_id))
        ex_data.append(str(tag) + " " + str(data))
        if isinstance(data, bytes):
            data = data.decode()

        print(f"{tag:2}:{data}")

    re_ex = "[\d]+"
    resolution1 = re.findall(re_ex, ex_data[0])
    resolution2 = re.findall(re_ex, ex_data[1])
    print("The main data ", ex_data)
    print(ex_data)
    print(int(resolution1[0]), int(resolution2[0]))
    imgresW = int(resolution1[0])
    imgresL = int(resolution2[0])
    print(imgresW, imgresL)
    imgreslou = str(imgresW) + 'X' + str(imgresL)
    if imgresW < 1200:
        print("small image")
        bugreport()
        if usecase == "aspect":
            excelobj.smallimgallaspect(img_name, resl, imgreslou, "FAIL")
        else:
            excelobj.smallimgallmode(img_name, resl, imgreslou, "FAIL")
    else:
        print("pass")
        image.close()
        os.remove(imgpath)
        time.sleep(5)
        if usecase == "aspect":
            excelobj.smallimgallaspect(img_name, resl, imgreslou, "PASS")
        else:
            excelobj.smallimgallmode(img_name, resl, imgreslou, "PASS")

