import json
import socket

import sys

from libs import contants
from libs.utils import deal_all_tcp


# 整体多次发送模式
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
        self.offset = 0

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
        self.tcp_client.connect((contants.IP, contants.TCP_INFO_PORT))

    # tcp发送数据
    def send_data(self):
        # 发送硬件配置信息
        config_dict = deal_all_tcp(contants.TCP_CONFIG_DATA.encode(), self.tcp_client)
        print(config_dict)
        # 启动上传
        start_dict = deal_all_tcp(contants.TCP_STARTUP_DATA.encode(), self.tcp_client)
        # 停止上传
        stop_dict = deal_all_tcp(contants.TCP_STOPUP_DATA.encode(), self.tcp_client)
        # 查看当前上传状态
        upstatus_dict = deal_all_tcp(contants.TCP_UPSTATUS_DATA.encode(), self.tcp_client)
        # 清空缓存
        clearcache_dict = deal_all_tcp(contants.TCP_CLEARPHOTOS_DATA.encode(), self.tcp_client)
        # 查询剩余电量
        power_dict = deal_all_tcp(contants.TCP_GETBATTERY_DATA.encode(), self.tcp_client)
        # 查询相机连接状态
        camerastatus_dict = deal_all_tcp(contants.TCP_DSLRSTATUS_DATA.encode(), self.tcp_client)
        # 构造响应数据
        content = {
            'config_dict': config_dict,
            'start_dict': start_dict,
            'stop_dict': stop_dict,
            'upstatus_dict': upstatus_dict,
            'clearcache_dict': clearcache_dict,
            'power_dict': power_dict,
            'camerastatus_dict':camerastatus_dict
        }
        return content

    # 多次发送
    def run_send(self):
        data_list = []
        while self.offset < contants.SEND_NUM:
            content = self.send_data()
            data_list.append(content)
            self.offset += 1
        return data_list

    # 保存结果
    def save_data(self, data_list):
        with open('deal_all_tcp.txt', 'w') as f:
            for data in data_list:
                data_str = json.dumps(data) + '\n'
                f.write(data_str)
    # 运行
    def run(self):
        self.tcp_connect()
        data_list = self.run_send()
        self.save_data(data_list)
        self.tcp_client.close()
# 参数化运行
def main():
    contants.IP = sys.argv[1]
    print(contants.IP)
    xiaochuan = XiaoChuan(contants.IP, contants.TCP_INFO_PORT)
    xiaochuan.run()

if __name__ == '__main__':
    main()


