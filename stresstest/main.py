from cameraforceclose import *
from smallimgtestcase import *

if __name__ == "__main__":
    try:
        #initia_cam()
        opencam()
        burst = cameratest.checkburstoption()
        print(burst)
        # modeswipestress(20)
        allmodestress(20, burst)
        # allmodesmallimageverfier(5)
        # allaspectsmallimgverifier(5)
        # individualmodes('Portrait', 2)
        closecam()
        excelobj.workbook.close()
    except BaseException as error:
        print("error{}".format(error))
        excelobj.workbook.close()

