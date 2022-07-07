import xlsxwriter
import subprocess
import time
import os

device_fingerprint_cmd = "adb shell getprop ro.build.fingerprint"
devic_id_cmd = "adb shell getprop ro.product.vendor.device"
std_out_id = subprocess.run(devic_id_cmd, capture_output=True, text=True)
time.sleep(5)
tim_stamp = str(time.strftime("_%Y_%m_%d_%H_%M_%S_"))
print(tim_stamp)
device_id = std_out_id.stdout.rstrip() + tim_stamp
# print(device_id)
std_out_finger = subprocess.run(device_fingerprint_cmd, capture_output=True, text=True)
time.sleep(5)
device_fingerprint = std_out_finger.stdout.rstrip()
excel_path = os.path.dirname(os.path.abspath("report")) + "\\reports\\"
# exc_path = ex_path.replace('\\', "/")
excel_name = excel_path + device_id + '.xlsx'
print(excel_name)
time.sleep(2)
workbook = xlsxwriter.Workbook(excel_name)


def creatsheet(sheetname):
    sheert = workbook.add_worksheet(sheetname)
    return sheert

rr = 2
row = 0
col = 0

def updateresults(sheetn, imgname, aspect, resol, result):
    sheett = sheetn
    sheett.write(row, col, device_fingerprint)
    sheett.write(row + 1, col, 'File_name')
    sheett.write(row + 1, col + 1, 'Aspect')
    sheett.write(row + 1, col + 2, 'Resolution')
    sheett.write(row + 1, col + 3, 'Result')
    sheett.write(row + rr, col, imgname)
    sheett.write(row + rr, col + 1, aspect)
    sheett.write(row + rr, col + 2, resol)
    sheett.write(row + rr, col + 3, result)
    rr += 1
    time.sleep(2)


def addval():
    test = creatsheet('testsheet0')
    test1 = creatsheet('testsheet1')
    test2 = creatsheet('testsheet2')
    for i in range(3):
        updateresults(test, f'test{i}', 'test', 'fsfs', 'fdsfsd')
        # updateresults(test1, f'test{i}', 'test', 'fsfs', 'fdsfsd')
        # updateresults(test2, f'test{i}', 'test', 'fsfs', 'fdsfsd')
        print(i)


addval()
workbook.close()
