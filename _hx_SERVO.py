'''
@author: hxbj1737
@date: 2025-07-25
@description:
    -SERVO类——设置舵机ID、位置范围、速度、加速度、波特率和串口及其他功能。
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

class SERVO(sts, PortHandler):
    def __init__(self, id=1,pos_range=(1000, 3000), speed=2400, acc=50, baudrate=1_000_000, com_port='COM13'):
        '''
        初始化 SERVO（舵机）控制器，设置舵机ID、位置范围、速度、加速度、波特率和串口。
        参数:
        id (int, 可选): 舵机ID，默认1。
        pos_range (tuple, 可选): 舵机位置范围，默认(1000, 3000)。
        speed (int, 可选): 舵机速度，默认2400。
        acc (int, 可选): 舵机加速度，默认50。
        baudrate (int, 可选): 串口波特率，默认1_000_000。
        com_port (str, 可选): 串口端口，默认'COM13'。
        异常:
        SystemExit: 如果串口无法打开或波特率设置失败则退出程序。
        '''
        self.id = id
        self.max = pos_range[1]
        self.min = pos_range[0]
        self.mid = (self.max + self.min) // 2
        self.speed = speed
        self.acc = acc
        self.baudrate = baudrate
        self.com_port = com_port
        self.portHandler = PortHandler(self.com_port)
        self.packetHandler = sts(self.portHandler)

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

    def set_pos(self, pos):
        pos=max(self.min, min(self.max, pos))
        ret, err = self.packetHandler.WritePosEx(
            self.id, pos, self.speed, self.acc)
        if ret != COMM_SUCCESS:
            print("pos failed:%s" % self.packetHandler.getTxRxResult(ret))
        elif err != 0:
            print("pos error:%s" % self.packetHandler.getRxPacketError(err))

    def add_pos(self, add):
        pos, _, _, _ = self.get_pos_speed()
        pos = max(self.min, min(self.max, pos + add))
        self.set_pos(pos)

    def get_pos_speed(self):
        pos, speed, ret, err = self.packetHandler.ReadPosSpeed(self.id)
        if ret != COMM_SUCCESS:
            print("pos_speed failed:%s" %
                  self.packetHandler.getTxRxResult(ret))
        elif err != 0:
            print("pos_speed error:%s" %
                  self.packetHandler.getRxPacketError(err))
        return pos, speed

    def get_moving(self):
        moving, ret, err = self.packetHandler.ReadMoving(self.id)
        if ret != COMM_SUCCESS:
            print("v_moving failed:%s" % self.packetHandler.getTxRxResult(ret))
        return moving

    def change_id(self, old_id, new_id):
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