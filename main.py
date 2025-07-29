import numpy as np
from STservo_sdk import *
import _hx_PTZ as hx_PTZ
import _PTZ_data as data
import matplotlib.pyplot as plt
import math
from decimal import Decimal

# ---------------------------------矩形
# y = [2000,2000,1900,1900]
# x = [650,800,800,650]
# -----------------------------------Sine
h_range = (700, 900)
step = 1
Ts = 10
x = [i for i in range(h_range[0], h_range[1]+1, step)]
l = len(x)
y = [50*math.sin(i*Ts*3.14/((h_range[1]-h_range[0]))*step)+2000 for i in range(l)]
y = [Decimal(i).quantize(Decimal("1"), rounding="ROUND_HALF_UP") for i in y]  # 四舍五入

# aa = (2*(h_range[1]-h_range[0])/(Ts*step))
# for i in range(l):
#     if i % aa == aa/4:
#         y[i]+=y[i]*0.001
#     elif (i+aa/2) % aa == aa/4:
#         y[i]-=y[i]*0.001
print(len(y))
plt.plot(x, y, '.')
plt.show()
quit()


# ------------------------------------圆

# x_min, x_max = 700, 900
# y_min, y_max = 1950, 2100


# center_x = (x_min + x_max) / 2
# center_y = (y_min + y_max) / 2
# radius = min((x_max - x_min)/2, (y_max - y_min)/2) * 0.9  # 使用90%的最大可能半径


# theta = np.linspace(0, 2*np.pi, 100)
# x = center_x + radius * np.cos(theta)*1.1
# y = center_y + radius * np.sin(theta)
# x= [round(x) for x in x]
# y = [Decimal(i).quantize(Decimal("1"), rounding="ROUND_HALF_UP") for i in y]  # 四舍五入

# fig, ax = plt.subplots(figsize=(8, 8))
# ax.set_xlim(x_min, x_max)
# ax.set_ylim(y_min, y_max)
# ax.set_aspect('equal')  # 确保圆不会变形

# ax.plot(x, y, 'b.', linewidth=2)
# ax.set_title('Circle in Specified Range')
# ax.grid(True)

# plt.show()
# print(y)
# print(x)
# ---------------------------------------三角波

# x_min, x_max = 700, 900
# y_min, y_max = 1950, 2050


# # 计算参数
# x_range = x_max - x_min
# y_range = y_max - y_min
# period = x_range / 2  # 两个周期，所以每个周期长度为50
# amplitude = y_range / 2 * 0.8  # 使用80%的可用高度
# vertical_offset = y_min + y_range / 2  # 垂直居中

# # 生成三角波数据
# x = np.linspace(x_min, x_max, 300)
# # 使用模运算创建三角波
# triangle_wave = amplitude * (2 * np.abs(2 * ((x - x_min) / period - np.floor((x - x_min) / period + 0.5))) - 1)
# y = triangle_wave + vertical_offset
# plt.plot(x, y, 'b.', linewidth=2)
# plt.show()

# print(x)
# print(y)
# ----------------------------------------------------方波
# x_min, x_max = 600, 800
# y_min, y_max = 1900, 2000

# # 计算参数
# x_range = x_max - x_min
# period = x_range / 5  # 两个周期，所以每个周期长度为50
# amplitude = (y_max - y_min) * 0.4  # 使用40%的可用高度
# vertical_offset = (y_min + y_max) / 2  # 垂直居中
# # 生成方波数据
# x = np.linspace(x_min, x_max, 50)
# # 使用模运算创建方波
# square_wave = amplitude * np.sign(np.sin(2 * np.pi * (x - x_min) / period))
# y = square_wave + vertical_offset
# y=[round(i) for i in y]
# # 绘制方波
# plt.plot(x, y, 'b.', linewidth=2)
# plt.show()
# -------------------------------------斜线
# h_range = (700, 800)
# v_range = (1950, 2050)
# step=2
# x = [i for i in range(h_range[0], h_range[1]+1, step)]
# y = [i for i in range(v_range[0], v_range[1]+1, step)]
# plt.plot(x, y,'.')
# plt.show()
# --------------------
# quit()

ptz = hx_PTZ.PTZ(v_id=data.PTZ1["v_id"], h_id=data.PTZ1["h_id"],
                 v_pos_range=data.PTZ1["v_pos_range"], h_pos_range=data.PTZ1["h_pos_range"],
                 v_speed=4000, h_speed=4000, v_acc=200, h_acc=200, baudrate=1_000_000, com_port='COM14')


err = 5
while True:
    # ptz.set_pos(ptz.KEEP, 600)
    # time.sleep(1)
    for v_pos, h_pos in zip(y, x):
        ptz.set_pos(v_pos, h_pos)
        print(f'v_pos: {v_pos}, h_pos: {h_pos}')
    # for v_pos, h_pos in zip(y[::-1], x[::-1]):
    #     ptz.set_pos(int(v_pos), int(h_pos))
    #     print(f'v_pos: {v_pos}, h_pos: {h_pos}')
    #     time.sleep(0.03)

        while True:
            # vp, hp = ptz.get_pos()
            # if abs(vp-v_pos)<err and abs(hp-h_pos)<err:
            #     break
            # print(f'v_pos: {vp}, h_pos: {hp}')
            time.sleep(0.01)
            moving1, moving2 = ptz.get_moving()
            if moving1 == 0 and moving2 == 0:
                break
