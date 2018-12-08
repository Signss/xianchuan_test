import json
import socket
import sys
import re

from libs import contants
from libs.utils import deal_tcp


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
        # udp响应结果
        self.udp_err_data = []
        self.tcp_data = []

    # udp发送广播
    def send_radio(self):

        # udp数据包
        data = contants.UDP_SEND_DATA.encode()
        # 设置广播
        self.udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # 发送upd数据包
        self.udp_client.sendto(data,self.addr)
        # 接受udp响应数据
        recv_data = self.udp_client.recvfrom(1024)
        response = recv_data[0].decode()
        if not recv_data:
            content = {
                'upd': False,
                'type': 'udp无响应'
            }
            self.udp_err_data.append(content)
        else:
            pattern = re.compile(r'(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})(\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})){3}')
            str = response
            result = pattern.search(str)
            if result == None:
                content = {
                    'upd': False,
                    'type': 'udp响应错误'
                }
                self.udp_err_data.append(content)
            else:
                # 存储为txt文件
                with open('u_recvdata.txt', 'w') as f:
                        f.write(response)
        self.udp_client.close()
    # tcp连接
    def tcp_connect(self):
        self.tcp_client.connect((self.ip, self.tcp_port))

    # tcp处理
    def tcp_send(self):
        # tcp获取硬件配置信息
        config_data = contants.TCP_CONFIG_DATA.encode()
        config_dict = deal_tcp(self.tcp_client, config_data, 't_config')
        self.tcp_data.append(config_dict)
        # 设置WIFI并重连：Set Wifi Config
        wifi_data = contants.TCP_WIFI_DATA.encode()
        wifi_dict = deal_tcp(self.tcp_client, wifi_data, 't_setwifi')
        self.tcp_data.append(wifi_dict)
        # 启动上传
        up_data = contants.TCP_STARTUP_DATA.encode()
        up_dict = deal_tcp(self.tcp_client, up_data, 't_start_upload')
        self.tcp_data.append(up_dict)
        # 停止上传
        stop_data = contants.TCP_STOPUP_DATA.encode()
        stop_dict = deal_tcp(self.tcp_client, stop_data, 't_stop_upload')
        self.tcp_data.append(stop_dict)
        # 查看当前上传状态
        status_data = contants.TCP_UPSTATUS_DATA.encode()
        status_dict = deal_tcp(self.tcp_client, status_data, 't_upload_status')
        self.tcp_data.append(status_dict)
        # 清空缓存
        clearcache_data = contants.TCP_CLEARPHOTOS_DATA.encode()
        clearcache_dict = deal_tcp(self.tcp_client, clearcache_data, 't_clear_cache')
        self.tcp_data.append(clearcache_dict)
        # 查询电量
        getbattery_data = contants.TCP_GETBATTERY_DATA.encode()
        getbattery_dict = deal_tcp(self.tcp_client, getbattery_data, 't_getbattery')
        self.tcp_data.append(getbattery_dict)
        # 查询相机连接状态
        DSL_data = contants.TCP_DSLRSTATUS_DATA.encode()
        DSL_dict = deal_tcp(self.tcp_client, DSL_data, 't_DSLR_connectionstatus')
        self.tcp_data.append(DSL_dict)


    # tcp响应结果处理
    def deal_tcp_response(self):
        for content in self.tcp_data:
            # 获取单个测试通过状态
            status = content.get('status')
            # 单个测试状态有一个未通过即为测试未通过
            if status is False:
                print('tcp2000端口测试未通过')
                return

    # 测试tcp接受图片
    def deal_tcp_img(self):
        # 上传图片数据包
        up_data = contants.TCP_STARTUP_DATA.encode()
        # 开启上传
        self.tcp_connect()
        self.tcp_client.send(up_data)
        # 创建接受图片tcp客户端
        img_tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        img_tcp_client.connect((self.ip, contants.TCP_IMG_PORT))
        while True:
            recv_data = self.tcp_client.recv(1024)
            # 未接受到图片即为未通过
            if not recv_data:
                print('tcp3000端口接受图片测试未通过')
                break
            img_tcp_client.close()
        return

    # 运行函数
    def run(self):
        self.send_radio()
        self.tcp_send()
        self.deal_tcp_response()
        self.deal_tcp_img()


def main():
    ip = sys.argv[1]
    xiaochuan = XiaoChuan(ip, contants.TCP_INFO_PORT)
    xiaochuan.run()

if __name__ == '__main__':
    main()