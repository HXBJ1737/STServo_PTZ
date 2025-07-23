import sys
sys.path.append("..")
from STservo_sdk import *

DEVICENAME = 'COM13'  # 串口号
BAUDRATE = 1000000    # 波特率
OLD_ID = 1            # 当前舵机ID
NEW_ID = 2            # 目标ID

portHandler = PortHandler(DEVICENAME)
packetHandler = sts(portHandler)

if portHandler.openPort() and portHandler.setBaudRate(BAUDRATE):
    COMM_SUCCESS = 0
    comm_result, error = packetHandler.unLockEprom(OLD_ID)
    comm_result, error = packetHandler.write1ByteTxRx(OLD_ID, STS_ID, NEW_ID)
    comm_result, error = packetHandler.LockEprom(NEW_ID)
    if comm_result == COMM_SUCCESS and error == 0:
        print(f"ID修改成功，新的ID为{NEW_ID}")
    else:
        print("ID修改失败")
    portHandler.closePort()
else:
    print("串口打开或波特率设置失败")