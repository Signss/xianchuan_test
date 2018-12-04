# 发送次数
SEND_NUM = 10
# 小传ip
IP = '192.168.43.5'
# udp发送端口
UDP_PORT = 5
# tcp获取硬件信息端口
TCP_INFO_PORT = 2000
# tcp传图端口
TCP_IMG_PORT = 3000
# 获取设备ip:port及小传地址
UDP_SEND_DATA = 'type=tubo_finding'
# tcp端口2000需要测试的数据包
# 获取硬件配置信息
TCP_CONFIG_DATA = '{"type": "getconfig"}'
# 设置WIFI并重连：Set Wifi Config
TCP_WIFI_DATA = '{"type": "setconfig", "SSID1": "sealap", "Key1": "12345678"}'
# 启动上传
TCP_STARTUP_DATA = '{"type": "startupload"}'
# 停止上传
TCP_STOPUP_DATA = '{"type": "stopupload"}'
# 查看当前上传状态
TCP_UPSTATUS_DATA = '{"type": "getuploadstatus"}'
# 清空硬件缓存照片
TCP_CLEARPHOTOS_DATA= '{"type": "clearphotos"}'
# 查询剩余电量
TCP_GETBATTERY_DATA = '{"type": "getbatterypercent"}'
# 查看相机连接状态
TCP_DSLRSTATUS_DATA = '{"type": "DSLR_connectionstatus"}'
