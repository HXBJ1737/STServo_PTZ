from STservo_sdk import *
import _hx_PTZ as hx_PTZ
import _PTZ_data as data
ptz = hx_PTZ.PTZ(v_id=data.PTZ1["v_id"], h_id=data.PTZ1["h_id"],
                 v_pos_range=data.PTZ1["v_pos_range"], h_pos_range=data.PTZ1["h_pos_range"],
                 v_speed=2400, h_speed=2400, v_acc=50, h_acc=50, baudrate=1_000_000, com_port='COM16')
while True:
    v_pos, h_pos, _, _ = ptz.get_pos_speed()
    print("Current Position: V=%d, H=%d" % (v_pos, h_pos))
    time.sleep(0.1)
