import socket, json
import contants
from utils import deal_tcp

# 挨个多次发送模式
class XiaoChuan(object):
    # 初始化信息
    def __init__(self, ip ,port):
        self.ip = ip
        self.tcp_port = port
        # 创建udp_client套接字
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 创建tcp_client套接字
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.ip, contants.UDP_PORT)

    # udp发送广播
    def send_radio(self):
        offset = 0
        udp_data = []
        while offset < contants.SEND_NUM:
            # udp数据包
            data = contants.UDP_SEND_DATA.encode()
            # 设置广播
            self.udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # 发送upd数据包
            self.udp_client.sendto(data,self.addr)
            # 接受udp响应数据
            recv_data = self.udp_client.recvfrom(1024)
            udp_data.append(recv_data[0].decode())
            offset += 1
        self.udp_client.close()
        # 存储为txt文件
        with open('u_recvdata.txt', 'w') as f:
            for data in udp_data:
                data_str = data + '\n'
                f.write(data_str)
        # 简单判断下是否有无响应现象
        if len(udp_data)< contants.SEND_NUM:
            print('有无响应现象')
    # tcp连接
    def tcp_connect(self):
        self.tcp_client.connect((self.ip, self.tcp_port))
    # tcp获取硬件配置信息
    def get_config(self):
        send_data = contants.TCP_CONFIG_DATA.encode()
        deal_tcp(self.tcp_client, send_data, 't_config')

    # 设置WIFI并重连：Set Wifi Config
    def set_wifi(self):
        send_data = contants.TCP_WIFI_DATA.encode()
        deal_tcp(self.tcp_client, send_data, 't_setwifi')

    # 启动上传
    def start_upload(self):
        send_data = contants.TCP_STARTUP_DATA.encode()
        deal_tcp(self.tcp_client, send_data, 't_start_upload')

    # 停止上传
    def stop_upload(self):
        send_data = contants.TCP_STOPUP_DATA.encode()
        deal_tcp(self.tcp_client, send_data, 't_stop_upload')

    # 查看当前上传状态
    def get_status(self):
        send_data = contants.TCP_UPSTATUS_DATA.encode()
        deal_tcp(self.tcp_client, send_data, 't_upload_status')

    # 清空缓存
    def clear_cache(self):
        send_data = contants.TCP_CLEARPHOTOS_DATA.encode()
        deal_tcp(self.tcp_client, send_data, 't_clear_cache')

    # 查询剩余电量
    def get_batterypercen(self):
        send_data = contants.TCP_GETBATTERY_DATA.encode()
        offset = 0
        config_datas = []
        error_datas = []
        power_data = []
        while offset < contants.SEND_NUM:
            self.tcp_client.send(send_data)
            recv_data = self.tcp_client.recv(1024)
            print(json.loads(recv_data.decode()))
            recv_dict = json.loads(recv_data.decode())
            status = recv_dict.get('errno')
            power = recv_dict.get('batterypercent')
            power_data.append(power)
            if status != 0:
                print('获取配置信息失败')
                # 整理错误数据
                content = {
                    'error': status,
                    'description': '获取配置信息失败',
                    'location': offset
                }
                error_datas.append(content)
            # 存储全部响应信息
            config_datas.append(recv_data.decode())
            offset += 1
        # 全部响应写入文件
        with open('t_batterypercen.txt', 'w') as f:
            for config_data in config_datas:
                data_str = config_data + '\n'
                f.write(data_str)
        # 响应失败信息写入文件
        if len(error_datas) > 1:
            with open('t_batterypercen_error' + '.txt', 'w') as f:
                for error_data in error_datas:
                    error_data_str = error_data + '\n'
                    f.write(error_data_str)
        else:
            print('暂无错误响应')
        # 把小传电量写入文件
        with open('power.txt', 'w') as f:
            for p in power_data:
                p_str = str(p) + ','
                f.write(p_str)

    # 查询相机连接状态
    def DSLR_connectionstatus(self):
        send_data = contants.TCP_DSLRSTATUS_DATA.encode()
        deal_tcp(self.tcp_client, send_data, 't_DSLR_connectionstatus')
    # 接收图片
    def recv_img(self):
        self.tcp_client.connect((self.ip,contants.TCP_IMG_PORT))
        while True:
            recv_data = self.tcp_client.recv(1024)
            if recv_data:
                with open('aaa.jpg', 'wb+') as f:
                    f.write(recv_data)


    def run(self):
        # self.send_radio()
        self.tcp_connect()
        # self.get_config()
        # self.start_upload()
        # self.stop_upload()
        # self.get_status()
        # self.clear_cache()
        self.get_batterypercen()
        # self.DSLR_connectionstatus()
        self.tcp_client.close()


if __name__ == '__main__':
    xiaochuan = XiaoChuan(contants.IP, contants.TCP_INFO_PORT)
    xiaochuan.run()




