from STservo_sdk import *
import _hx_PTZ as hx_PTZ
import _PTZ_data as data
ptz = hx_PTZ.PTZ(v_id=data.PTZ1["v_id"], h_id=data.PTZ1["h_id"],
                 v_pos_range=data.PTZ1["v_pos_range"], h_pos_range=data.PTZ1["h_pos_range"],
                 v_speed=100, h_speed=100, v_acc=50, h_acc=50, baudrate=1_000_000, com_port='COM16')

vPos_list = [2060,2060,1950,1950]
hPos_list = [660,875,875,660]
while True:
    for v_pos, h_pos in zip(vPos_list, hPos_list):
        ptz.set_pos(v_pos+50, h_pos)
        print(f'v_pos: {v_pos}, h_pos: {h_pos}')
        while True:
            moving1,moving2= ptz.get_moving()
            if moving1==0 and  moving2==0:
                time.sleep(1)
                if moving1==0 and  moving2==0:
                    break
