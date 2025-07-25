import _hx_SERVO as hx_SERVO
import _PTZ_data as data
import time

servo = hx_SERVO.SERVO(id=data.PTZ1["h_id"], pos_range=data.PTZ1["h_pos_range"],
                       speed=2400, acc=50, baudrate=1_000_000, com_port='COM16')

servo.set_pos(servo.mid)
while True:
    mov = servo.get_moving()
    if not mov:
        break
time.sleep(1)
pos, _ = servo.get_pos_speed()
print("Servo is not moving, current position:", pos)

# SER_list=[servo.min,servo.mid,servo.max]
# while True:
#     for pos in SER_list:
#         servo.set_pos(pos)
#         while True:
#             mov = servo.get_moving()
#             if not mov:
#                 break
#         time.sleep(1)
#         pos, _ = servo.get_pos_speed()
#         print("Servo is not moving, current position:", pos)
