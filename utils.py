import contants, json
# tcp发送数据包通用处理方法
def deal_tcp(tcp_client, send_data, filename):
    offset = 0
    config_datas = []
    error_datas = []
    # 获取硬件配置信息

    while offset < contants.SEND_NUM:
        tcp_client.send(send_data)
        recv_data = tcp_client.recv(1024)
        print(json.loads(recv_data.decode()))
        recv_dict = json.loads(recv_data.decode())
        status = recv_dict.get('errno')
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
    with open(filename + '.txt', 'w') as f:
        for config_data in config_datas:
            data_str = config_data + '\n'
            f.write(data_str)
    # 响应失败信息写入文件
    if len(error_datas) > 1:
        with open(filename + 'error' + '.txt', 'w') as f:
            for error_data in error_datas:
                error_data_str = error_data + '\n'
                f.write(error_data_str)
    else:
        print('暂无错误响应')


def deal_all_tcp(send_data, tcp_client):
    tcp_client.send(contants.TCP_CONFIG_DATA.encode())
    name_data = tcp_client.recv(1024)
    return json.loads(name_data)