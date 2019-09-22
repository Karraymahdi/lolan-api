from bottle import *
from lolan_cmd import Serial_Comm
import service
import serial
from xmodem import XMODEM
from time import sleep
SET="SET"
GET="GET"
CONTROL=['soft_reset_mcu' , 'save_settings']
info=['tag_unique', 'fw_version', 'unique_id/hi', 'unique_id/lo']
tagsettings= ['tag_id', 'active/pak_interval', 'active/ext_pak_nth', 'active/timeout', 'quiescent/pak_interval', 'quiescent/ext_pak_nth', 'accel/rest_threshold', 'accel/rest_avgnum', 'accel/highresolution', 'maqi_packet_delay']
STATUS=['status', 'battery/level', 'battery/charge_complete', 'lastaccel/x', 'lastaccel/y', 'lastaccel/z', 'lastaccel/databits', 'temperature', 'pressure', 'packets_after_last_charge', 'lastmag/x', 'lastmag/y', 'lastmag/z']
DW1000SETTINGS=['channel_num', 'preamble/code', 'preamble/len', 'bitrate', 'prf', 'txpwr_header', 'txpwr_other']
@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Access-Control-Allow-Headers'] = 'content-type'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'

@route('<any:path>', method='OPTIONS')
def response_for_options(**kwargs):
    return {}
@route('/reset',method='GET')
def reset():
   Serial_Comm.Reset(Serial_Port)
   return None

@route('/arrays',method='GET')
def arrays():
   Result_json = {"info": info, "tagsettings": tagsettings, "DW1000SETTINGS": DW1000SETTINGS, "CONTROL": CONTROL, "STATUS": STATUS}
   return (Result_json)


@route('/firmwareUpdater',method='POST')
def firmwareUpdater():
   def getc(size, timeout=1):
      return ser.read(size) or None
   def putc(data, timeout=1):
      ser.write(data) or None
   response.set_header('Content-Type', 'application/json')
   upload = request.files.get('file')
   upload.save("fw.bin", overwrite=True)
   for x in range(2):
      ser = serial.Serial(Serial_Port, timeout=1)
      ser.write(b'RST}')
      sleep(2)

      ser.close()
   ser = serial.Serial(Serial_Port
                       , timeout=1)
   
   modem = XMODEM(getc, putc)
   f = open('fw.bin', 'rb')
   ser.flushInput()
   ser.flushOutput()
   status = modem.send(f)
   sleep(2)
   ser.flushInput()
   ser.flushOutput()
   ser.write(b'b')
   f.close()
   ser.close()
   return None

#[1,x,x] INFO variable group (R)

#[1,1,0] INFO/tag_unique (uint32) #Unique identifier of the hardware
@route('/<LoLaNid>/info/tag_unique',method='GET')
def tag_unique(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "1,1,0", LoLaNid, GET, None)
   Result_json={"TagID": LoLaNid,"Result": result}
   return Result_json
#[1,2,0] INFO/fw_version (uint16) #Firmware version number
@route('/<LoLaNid>/info/fw_version',method='GET')
def fw_version(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "1,2,0", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return Result_json

#[[1,3,1] INFO/unique_id/hi
@route('/<LoLaNid>/info/unique_id/hi',method='GET')
def tag_unique_hi(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "1,3,1", LoLaNid, GET, None)
   Result_json={"TagID": LoLaNid,"Result": result}
   return Result_json

#[1,3,2] INFO/unique_id/lo
@route('/<LoLaNid>/info/unique_id/lo',method='GET')
def tag_unique_lo(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "1,3,2", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return Result_json

#[2,x,x] TAG SETTINGS variable group (R/W)

#[2,1,0] TAGSETTINGS/tag_id
@route('/<LoLaNid>/tagsettings/tag_id',method='GET')
def tag_unique_lo(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,1,0", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return Result_json

@route('/<LoLaNid>/tagsettings/tag_id',method='POST')
def tag_id(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= (service.LoLaN_REST(Serial_Port, "2,1,0", LoLaNid, SET, NewValue))
   Result_json = {"TagID": LoLaNid, "Result": result[2][1]}
   return (Result_json)
#[2,2,1] TAGSETTINGS/active/pak_interval
@route('/<LoLaNid>/tagsettings/active/pak_interval',method='GET')
def Active_pak_interval(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,2,1", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/tagsettings/active/pak_interval',method='POST')
def pak_interval(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "2,2,1", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[2][2][1]}
   return (Result_json)
#[2,2,2] TAGSETTINGS/active/ext_pak_nth
@route('/<LoLaNid>/tagsettings/active/ext_pak_nth',method='GET')
def Active_ext_pak_nth(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,2,2", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/tagsettings/active/ext_pak_nth',method='POST')
def Active_ext_pak_nth(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "2,2,2", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[2][2][2]}
   return (Result_json)
#[2,2,3] TAGSETTINGS/active/timeout
@route('/<LoLaNid>/tagsettings/active/timeout',method='GET')
def timeout(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,2,3", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/tagsettings/active/timeout',method='POST')
def timeout(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "2,2,3", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[2][2][3]}
   return (Result_json)
#[2,3,1] TAGSETTINGS/quiescent/pak_interval
@route('/<LoLaNid>/tagsettings/quiescent/pak_interval',method='GET')
def pak_interval(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,3,1", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/tagsettings/quiescent/timeout',method='POST')
def pak_interval(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "2,3,1", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[2][3][1]}
   return (Result_json)

#[2,3,2] TAGSETTINGS/quiescent/ext_pak_nth
@route('/<LoLaNid>/tagsettings/quiescent/ext_pak_nth',method='GET')
def ext_pak_nth(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,3,2", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/tagsettings/quiescent/ext_pak_nth',method='POST')
def ext_pak_nth(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "2,3,2", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[2][3][2]}
   return (Result_json)

#[2,4,1] TAGSETTINGS/accel/rest_threshold
@route('/<LoLaNid>/tagsettings/accel/rest_threshold',method='GET')
def rest_threshold(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,4,1", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/tagsettings/accel/rest_threshold',method='POST')
def rest_threshold(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "2,4,1", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[2][4][1]}
   return (Result_json)

#[2,4,2] TAGSETTINGS/accel/rest_avgnum
@route('/<LoLaNid>/tagsettings/accel/rest_avgnum',method='GET')
def rest_avgnum(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,4,2", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/tagsettings/accel/rest_avgnum',method='POST')
def rest_avgnum(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "2,4,2", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[2][4][2]}
   return (Result_json)

#[2,4,3] TAGSETTINGS/accel/highresolution
@route('/<LoLaNid>/tagsettings/accel/highresolution',method='GET')
def highresolution(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,4,3", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/tagsettings/accel/highresolution',method='POST')
def highresolution (LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "2,4,3", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[2][4][3]}
   return (Result_json)

#[2,5,1] TAGSETTINGS/maqi_packet_delay
@route('/<LoLaNid>/tagsettings/maqi_packet_delay',method='GET')
def maqi_packet_delay(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "2,5,1", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/tagsettings/maqi_packet_delay',method='POST')
def maqi_packet_delay (LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "2,5,1", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[2][5][1]}
   return (Result_json)

#[3,x,x] DW1000 SETTINGS variable group (R/W)


#[3,1,0] DW1000SETTINGS/maqi_packet_delay
@route('/<LoLaNid>/DW1000SETTINGS/channel_num',method='GET')
def maqi_packet_delay(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "3,1,0", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/DW1000SETTINGS/channel_num',method='POST')
def maqi_packet_delay (LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "3,1,0", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[3][1]}
   return (Result_json)
#[3,2,1] DW1000SETTINGS/preamble/code
@route('/<LoLaNid>/DW1000SETTINGS/preamble/code',method='GET')
def code(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "3,2,1", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/DW1000SETTINGS/preamble/code',method='POST')
def code (LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "3,2,1", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[3][2][1]}
   return (Result_json)

#[3,2,2] DW1000SETTINGS/preamble/len
@route('/<LoLaNid>/DW1000SETTINGS/preamble/len',method='GET')
def len(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "3,2,2", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/DW1000SETTINGS/preamble/len',method='POST')
def len (LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "3,2,2", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[3][2][2]}
   return (Result_json)

#[3,3,0] DW1000SETTINGS/bitrate
@route('/<LoLaNid>/DW1000SETTINGS/bitrate',method='GET')
def bitrate(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "3,3,0", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/DW1000SETTINGS/bitrate',method='POST')
def bitrate (LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "3,3,0", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[3][3]}
   return (Result_json)

#[3,4,0] DW1000SETTINGS/prf
@route('/<LoLaNid>/DW1000SETTINGS/prf',method='GET')
def prf(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "3,4,0", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/DW1000SETTINGS/prf',method='POST')
def prf (LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "3,4,0", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[3][4]}
   return (Result_json)

#[3,5,1] DW1000SETTINGS/txpwr_header
@route('/<LoLaNid>/DW1000SETTINGS/txpwr_header',method='GET')
def txpwr_header(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "3,5,1", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/DW1000SETTINGS/txpwr_header',method='POST')
def txpwr_header(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "3,5,1", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[3][5][1]}
   return (Result_json)

#[3,5,2] DW1000SETTINGS/txpwr_other
@route('/<LoLaNid>/DW1000SETTINGS/txpwr_other',method='GET')
def txpwr_other(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "3,5,2", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
@route('/<LoLaNid>/DW1000SETTINGS/txpwr_other',method='POST')
def txpwr_other(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "3,5,2", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[3][5][2]}
   return (Result_json)

#[4,x,x] CONTROL variable group (W)

#[4,1,0] CONTROL/soft_reset_mcu
@route('/<LoLaNid>/CONTROL/soft_reset_mcu',method='POST')
def soft_reset_mcu(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "4,1,0", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[4][1]}
   return (Result_json)
#[4,2,0] CONTROL/save_settings
@route('/<LoLaNid>/CONTROL/save_settings',method='POST')
def save_settings(LoLaNid):
   NewValue = (request.json.get('newValue', None))
   result= service.LoLaN_REST(Serial_Port, "4,2,0", LoLaNid, SET, NewValue)
   Result_json = {"TagID": LoLaNid, "Result": result[4][2]}
   return (Result_json)

#[5,x,x] STATUS variable group (R)

#[5,1,0] STATUS/status
@route('/<LoLaNid>/STATUS/status',method='GET')
def status(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,1,0", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
#[5,2,1] STATUS/battery/level
@route('/<LoLaNid>/STATUS/battery/level',method='GET')
def battery_level(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,2,1", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
#[5,2,2] STATUS/battery/charge_complete
@route('/<LoLaNid>/STATUS/battery/charge_complete',method='GET')
def charge_complete(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,2,2", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

#[5,3,1] STATUS/lastaccel/x
@route('/<LoLaNid>/STATUS/lastaccel/x',method='GET')
def lastaccel_x(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,3,1", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

#[5,3,2] STATUS/lastaccel/y
@route('/<LoLaNid>/STATUS/lastaccel/y',method='GET')
def lastaccel_y(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,3,2", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

#[5,3,3] STATUS/lastaccel/z
@route('/<LoLaNid>/STATUS/lastaccel/z',method='GET')
def lastaccel_z(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,3,3", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

#[5,3,4] STATUS/lastaccel/databits
@route('/<LoLaNid>/STATUS/lastaccel/databits',method='GET')
def databits(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,3,4", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

#[5,4,0] STATUS/temperature
@route('/<LoLaNid>/STATUS/temperature',method='GET')
def temperature(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,4,0", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

#[5,5,0] STATUS/pressure
@route('/<LoLaNid>/STATUS/pressure',method='GET')
def pressure(LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,5,0", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)
#[5,6,0] STATUS/packets_after_last_charge
@route('/<LoLaNid>/STATUS/packets_after_last_charge',method='GET')
def packets_after_last_charge (LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,6,0", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

#[5,7,1] STATUS/lastmag/x
@route('/<LoLaNid>/STATUS/lastmag/x',method='GET')
def lastmag_x (LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,7,1", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

#[5,7,1] STATUS/lastmag/y
@route('/<LoLaNid>/STATUS/lastmag/y',method='GET')
def lastmag_y (LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,7,2", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

#[5,7,1] STATUS/lastmag/z
@route('/<LoLaNid>/STATUS/lastmag/z',method='GET')
def lastmag_z (LoLaNid):
   result= service.LoLaN_REST(Serial_Port, "5,7,3", LoLaNid, GET, None)
   Result_json = {"TagID": LoLaNid, "Result": result}
   return (Result_json)

if __name__=='__main__':
    print("SERIAL PORT :")
    Serial_Port = input()
    run(host='localhost', port=8080, debug=True)
