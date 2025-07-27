import numpy as np
from STservo_sdk import *
import _hx_PTZ as hx_PTZ
import _PTZ_data as data
import math

ptz = hx_PTZ.PTZ(v_id=data.PTZ1["v_id"], h_id=data.PTZ1["h_id"],
                 v_pos_range=data.PTZ1["v_pos_range"], h_pos_range=data.PTZ1["h_pos_range"],
                 v_speed=1000, h_speed=1000, v_acc=100, h_acc=100, baudrate=1_000_000, com_port='COM13')

# vPos_list = [1950,1950,1900,1900]
# hPos_list = [650,700,700,650]
# h_range = (650, 700)
# h_pos_list = [i for i in range(h_range[0], h_range[1]+1, 5)]
# v_pos_list = [int(math.sin((i-h_range[0])/(h_range[1]-h_range[0])*1*3.14)*30+1920)
#               for i in range(h_range[0], h_range[1]+1, 5)]

# print(h_pos_list)
# print(v_pos_list)
# quit()


# 设置坐标轴范围
x_min, x_max = 500, 700
y_min, y_max = 1800, 2000

# 计算圆心和半径（使圆适合给定的范围）
center_x = (x_min + x_max) / 2
center_y = (y_min + y_max) / 2
radius = min((x_max - x_min)/2, (y_max - y_min)/2) * 0.9  # 使用90%的最大可能半径

# 生成圆的数据点
theta = np.linspace(0, 2*np.pi, 100)
x = center_x + radius * np.cos(theta)
y = center_y + radius * np.sin(theta)
print(y)
print(x)

while True:
    for v_pos, h_pos in zip(y, x):
        print(h_pos)
        ptz.sync_set_pos(int(v_pos),int( h_pos))
        print(f'v_pos: {v_pos}, h_pos: {h_pos}')
        while True:
            vp, hp = ptz.get_pos()
            print(f'v_pos: {vp}, h_pos: {hp}')
            # time.sleep(0.01)
            moving1, moving2 = ptz.get_moving()
            if moving1 == 0 and moving2 == 0:
                break
