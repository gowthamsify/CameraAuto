import os.path
import subprocess
import time

import xlsxwriter


class Excelwriter:
    """Update test result in realtime to excel"""

    def __init__(self):
        # self.prt = prt
        # print(prt)
        self.device_fingerprint_cmd = "adb shell getprop ro.build.fingerprint"
        self.devic_id_cmd = "adb shell getprop ro.product.vendor.device"
        self.std_out_id = subprocess.run(self.devic_id_cmd, capture_output=True, text=True)
        time.sleep(5)
        self.tim_stamp = str(time.strftime("_%Y_%m_%d_%H_%M_%S_"))
        print(self.tim_stamp)
        self.device_id = self.std_out_id.stdout.rstrip() + self.tim_stamp
        # print(device_id)
        self.std_out_finger = subprocess.run(self.device_fingerprint_cmd, capture_output=True, text=True)
        time.sleep(5)
        self.device_fingerprint = self.std_out_finger.stdout.rstrip()
        self.excel_path = os.path.dirname(os.path.abspath("report")) + "\\reports\\"
        # exc_path = ex_path.replace('\\', "/")
        self.excel_name = self.excel_path + self.device_id + '.xlsx'
        print(self.excel_name)
        time.sleep(2)
        self.workbook = xlsxwriter.Workbook(self.excel_name)

        # self.sheetnam = self.workbook.add_worksheet(f"{sheetnam}")

        # self.smallimgaspect = self.workbook.add_worksheet("smallimgaspect_test")
        # self.smallimgmode = self.workbook.add_worksheet("smallimgallmode")
        # self.switchmode = self.workbook.add_worksheet("switchmode_test")
        # self.capturecrash = self.workbook.add_worksheet("capturecrash")

        self.col = 0
        self.row = 0
        self.rr = 2
        self.rc = 2
        self.urw = 2
        self.am = 2
        self.sheetn = "test"

    def creatsheet(self, sheetname):
        sheets = self.workbook.add_worksheet(sheetname)
        print(f"sheet created{sheets}")
        return sheets

    '''def smallimgallaspect(self, imgname, aspect, resol, result):
        """update entry to sheet
        :param: takes three positional entries"""

        print("updating excel")
        self.smallimgaspect.write(self.row, self.col, self.device_fingerprint)
        self.smallimgaspect.write(self.row + 1, self.col, 'File_name')
        self.smallimgaspect.write(self.row + 1, self.col + 1, 'Aspect')
        self.smallimgaspect.write(self.row + 1, self.col + 2, 'Resolution')
        self.smallimgaspect.write(self.row + 1, self.col + 3, 'Result')
        self.smallimgaspect.write(self.row + self.urw, self.col, imgname)
        self.smallimgaspect.write(self.row + self.urw, self.col + 1, aspect)
        self.smallimgaspect.write(self.row + self.urw, self.col + 2, resol)
        self.smallimgaspect.write(self.row + self.urw, self.col + 3, result)
        self.urw += 1
        time.sleep(2)

    def smallimgallmode(self, imgname, aspect, resol, result):
        """update entry to sheet
        :param: takes three positional entries"""

        print("updating excel")
        self.smallimgmode.write(self.row, self.col, self.device_fingerprint)
        self.smallimgmode.write(self.row + 1, self.col, 'File_name')
        self.smallimgmode.write(self.row + 1, self.col + 1, 'Aspect')
        self.smallimgmode.write(self.row + 1, self.col + 2, 'Resolution')
        self.smallimgmode.write(self.row + 1, self.col + 3, 'Result')
        self.smallimgmode.write(self.row + self.am, self.col, imgname)
        self.smallimgmode.write(self.row + self.am, self.col + 1, aspect)
        self.smallimgmode.write(self.row + self.am, self.col + 2, resol)
        self.smallimgmode.write(self.row + self.am, self.col + 3, result)
        self.am += 1
        time.sleep(2)

    def switchmodeupdate(self, mode, result):
        """update entry to sheet
            :parameter: takes two positional entries"""
        print("updating excel")
        self.switchmode.write(self.row, self.col, self.device_fingerprint)
        self.switchmode.write(self.row + 1, self.col, 'Mode')
        self.switchmode.write(self.row + 1, self.col + 1, 'Result')
        self.switchmode.write(self.row + self.rr, self.col, mode)
        self.switchmode.write(self.row + self.rr, self.col + 1, result)
        self.rr += 1
        time.sleep(2)

    def captureallmode(self, mode, result):
        """update entry to sheet
            :parameter: takes two positional entries"""
        print("updating excel")
        self.capturecrash.write(self.row, self.col, self.device_fingerprint)
        self.capturecrash.write(self.row + 1, self.col, 'Mode')
        self.capturecrash.write(self.row + 1, self.col + 1, 'Result')
        self.capturecrash.write(self.row + self.rc, self.col, mode)
        self.capturecrash.write(self.row + self.rc, self.col + 1, result)
        self.rc += 1
        time.sleep(2)'''

    def updatesheet(self, sheetname, filename, aspect='use case', actresol='use case', result='UP'):
        # self.workbook.add_worksheet(f"{sheetname}_test")
        # self.row = 0
        # self.col = 0
        if self.sheetn == sheetname:
            print("not new sheet")
        else:
            self.urw = 2
            print("new sheet initialing row")

        sheetnam = sheetname
        print("updating excel")
        sheetnam.write(self.row, self.col, self.device_fingerprint)
        sheetnam.write(self.row + 1, self.col, 'File_name')
        sheetnam.write(self.row + 1, self.col + 1, 'Aspect_Mode')
        sheetnam.write(self.row + 1, self.col + 2, 'Resolution')
        sheetnam.write(self.row + 1, self.col + 3, 'Result')
        sheetnam.write(self.row + self.urw, self.col, filename)
        sheetnam.write(self.row + self.urw, self.col + 1, aspect)
        sheetnam.write(self.row + self.urw, self.col + 2, actresol)
        sheetnam.write(self.row + self.urw, self.col + 3, result)
        self.sheetn = sheetname
        self.urw += 1
        time.sleep(2)


'''excobj = Excelwriter()

# excobj.createsheet('test1')
# excobj.createsheet('test2')
test = excobj.creatsheet('test0')
test1 = excobj.creatsheet('test1')
for i in range(5):
    excobj.sheetupdate(test, 'dsd', 'dsd', 'dsd', 'dsd')
# excobj = Excelwriter('test 2')
for j in range(5):
    excobj.sheetupdate(test1, 'dsd', 'dsd', 'dsd', 'dsd')
print("done")
excobj.workbook.close()'''
