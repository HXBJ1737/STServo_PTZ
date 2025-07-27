'''
@author: hxbj1737
@date: 2025-07-23
@description:
    -PTZ（云台）控制类，设置舵机ID、位置范围、速度、加速度、波特率和串口及其他功能。
'''
import sys
import os
import time
from STservo_sdk import *

if os.name == 'nt':
    import msvcrt

    def getch():
        return msvcrt.getch().decode()
else:
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class PTZ(sts, PortHandler):
    def __init__(self, v_id=1, h_id=2, v_pos_range=(1000, 3000), h_pos_range=(0, 1800), v_speed=2400, h_speed=2400, v_acc=50, h_acc=50, baudrate=1_000_000, com_port='COM13'):
        '''
        初始化 PTZ（云台）控制器，设置舵机ID、位置范围、速度、加速度、波特率和串口。
        参数:
        v_id (int, 可选): 垂直舵机ID，默认1。
        h_id (int, 可选): 水平舵机ID，默认2。
        v_pos_range (tuple, 可选): 垂直舵机位置范围，默认(0, 4095)。
        h_pos_range (tuple, 可选): 水平舵机位置范围，默认(922, 2807)。
        v_speed (int, 可选): 垂直舵机速度，默认2400。
        h_speed (int, 可选): 水平舵机速度，默认2400。
        v_acc (int, 可选): 垂直舵机加速度，默认50。
        h_acc (int, 可选): 水平舵机加速度，默认50。
        baudrate (int, 可选): 串口波特率，默认1_000_000。
        com_port (str, 可选): 串口端口，默认'COM13'。
        异常:
        SystemExit: 如果串口无法打开或波特率设置失败则退出程序。
        '''
        self.v_id = v_id
        self.h_id = h_id
        self.v_max = v_pos_range[1]
        self.v_min = v_pos_range[0]
        self.h_max = h_pos_range[1]
        self.h_min = h_pos_range[0]
        self.v_mid = (self.v_max + self.v_min) // 2
        self.h_mid = (self.h_max + self.h_min) // 2
        self.v_speed = v_speed
        self.h_speed = h_speed
        self.v_acc = v_acc
        self.h_acc = h_acc
        self.baudrate = baudrate
        self.com_port = com_port
        self.portHandler = PortHandler(self.com_port)
        self.packetHandler = sts(self.portHandler)

        self.KEEP = -1  # 保持角度不变

        # Open port
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()
        # Set port baudrate
        if self.portHandler.setBaudRate(self.baudrate):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

    def set_v_pos(self, pos):
        ret, err = self.packetHandler.WritePosEx(
            self.v_id, pos, self.v_speed, self.v_acc)
        if ret != COMM_SUCCESS:
            print("v_pos failed:%s" % self.packetHandler.getTxRxResult(ret))
        elif err != 0:
            print("v_pos error:%s" % self.packetHandler.getRxPacketError(err))

    def set_h_pos(self, pos):
        ret, err = self.packetHandler.WritePosEx(
            self.h_id, pos, self.h_speed, self.h_acc)
        if ret != COMM_SUCCESS:
            print("h_pos failed:%s" % self.packetHandler.getTxRxResult(ret))
        elif err != 0:
            print("h_pos error:%s" % self.packetHandler.getRxPacketError(err))

    def set_pos(self, v_pos, h_pos):
        if v_pos != self.KEEP:
            v_pos = max(self.v_min, min(self.v_max, v_pos))
        if h_pos != self.KEEP:
            h_pos = max(self.h_min, min(self.h_max, h_pos))
        self.set_v_pos(v_pos)
        self.set_h_pos(h_pos)

    def sync_set_pos(self, v_pos, h_pos):
        '''
        同步设置垂直和水平舵机的位置。
        参数:
        v_pos (int): 垂直舵机目标位置。
        h_pos (int): 水平舵机目标位置。
        '''
        ret = self.packetHandler.SyncWritePosEx(
            self.v_id, v_pos, self.v_speed, self.v_acc)
        if ret != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % self.v_id)

        ret = self.packetHandler.SyncWritePosEx(
            self.h_id, h_pos, self.h_speed, self.h_acc)
        if ret != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % self.h_id)

       # Syncwrite goal position
        ret = self.packetHandler.groupSyncWrite.txPacket()
        if ret != True:
            print("%s" % self.packetHandler.getTxRxResult(ret))
        # Clear syncwrite parameter storage
        self.packetHandler.groupSyncWrite.clearParam()

    def add_pos(self, v_add, h_add):
        v_pos, h_pos, _, _ = self.get_pos_speed()
        v_pos = max(self.v_min, min(self.v_max, v_pos + v_add))
        h_pos = max(self.h_min, min(self.h_max, h_pos + h_add))
        self.set_pos(v_pos, h_pos)
    def get_v_pos(self):
        pos, ret, err = self.packetHandler.ReadPos(self.v_id)
        if ret != COMM_SUCCESS:
            print("v_pos failed:%s" % self.packetHandler.getTxRxResult(ret))
        elif err != 0:
            print("v_pos error:%s" % self.packetHandler.getRxPacketError(err))
        return pos
    def get_h_pos(self):
        pos, ret, err = self.packetHandler.ReadPos(self.h_id)
        if ret != COMM_SUCCESS:
            print("h_pos failed:%s" % self.packetHandler.getTxRxResult(ret))
        elif err != 0:
            print("h_pos error:%s" % self.packetHandler.getRxPacketError(err))
        return pos
    
    def get_pos(self):
        v_pos = self.get_v_pos()
        h_pos = self.get_h_pos()
        return v_pos, h_pos
    def get_v_pos_speed(self):
        pos, speed, ret, err = self.packetHandler.ReadPosSpeed(self.v_id)
        if ret != COMM_SUCCESS:
            print("v_pos_speed failed:%s" %
                  self.packetHandler.getTxRxResult(ret))
        elif err != 0:
            print("v_pos_speed error:%s" %
                  self.packetHandler.getRxPacketError(err))
        return pos, speed

    def get_h_pos_speed(self):
        pos, speed, ret, err = self.packetHandler.ReadPosSpeed(self.h_id)
        if ret != COMM_SUCCESS:
            print("h_pos_speed failed:%s" %
                  self.packetHandler.getTxRxResult(ret))
        elif err != 0:
            print("h_pos_speed error:%s" %
                  self.packetHandler.getRxPacketError(err))
        return pos, speed

    def get_pos_speed(self):
        v_pos, v_speed = self.get_v_pos_speed()
        h_pos, h_speed = self.get_h_pos_speed()
        return v_pos, h_pos, v_speed, h_speed

    def get_v_moving(self):
        moving, ret, err = self.packetHandler.ReadMoving(self.v_id)
        if ret != COMM_SUCCESS:
            print("v_moving failed:%s" % self.packetHandler.getTxRxResult(ret))
        return moving

    def get_h_moving(self):
        moving, ret, err = self.packetHandler.ReadMoving(self.h_id)
        if ret != COMM_SUCCESS:
            print("h_moving failed:%s" % self.packetHandler.getTxRxResult(ret))
        return moving

    def get_moving(self):
        v_moving = self.get_v_moving()
        h_moving = self.get_h_moving()
        return v_moving, h_moving

    def __change_id(self, old_id, new_id):
        COMM_SUCCESS = 0
        comm_result, error = self.packetHandler.unLockEprom(old_id)
        if comm_result != COMM_SUCCESS or error != 0:
            print("Failed to unlock EEPROM")
            return False

        comm_result, error = self.packetHandler.write1ByteTxRx(
            old_id, STS_ID, new_id)
        if comm_result != COMM_SUCCESS or error != 0:
            print("Failed to change ID")
            return False

        comm_result, error = self.packetHandler.LockEprom(new_id)
        if comm_result != COMM_SUCCESS or error != 0:
            print("Failed to lock EEPROM")
            return False

        print(f"ID changed successfully to {new_id}")
        self.portHandler.closePort()
        quit()

    def close(self):
        self.portHandler.closePort()
