import time
from socket import *

# RECV_BUF_SIZE = 1024 #每次最多接收1k字节

class TcpConnect:
    def __init__(self,judge_ip = '192.168.1.66',judge_port = 6666) -> None:
        '''
        judge_ip : 裁判的IP地址
        judge_port : 裁判端口号
        '''
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.connect((judge_ip,judge_port))
    	
    def send_message(self,msg:str,data_type:int):
        '''
        发送消息
        msg : 发送的内容,要求为str类型
        data_type : 发送数据的类型,0=发送队伍ID,1=发送3D识别结果,2=发送工业测量结果,3=转动云台
        '''

        bytes_msg = self.string(msg)
        data_length = len(bytes_msg)
        real_msg = self.int32(data_type) + self.int32(data_length) + bytes_msg
        return self.socket.send(real_msg)
    
    def send_team_info(self,team_id:str):
        '''发送队伍信息'''
        return self.send_message(team_id,data_type=0)

    def send_detect_result(self,result:str):
        '''发送3D识别结果'''
        return self.send_message(result,data_type=1)
    
    def send_industry_result(self,result:str):
        '''发送工业测量结果'''
        return self.send_message(result,data_type=2)
    
    def send_rotate_pantilt_1(self):
        '''发送转动云台Ver.1'''
        return self.send_message("0000",data_type=3)
    
    # def send_rotate_pantilt_2(self):
    #     '''发送转动云台Ver.2'''
    #     bytes_msg = self.int32(0)
    #     data_length = len(bytes_msg)
    #     real_msg = self.int32(3) + self.int32(data_length) + bytes_msg
    #     return self.socket.send(real_msg)
    
    def close(self):
        '''关闭连接'''
        self.socket.close()

    @staticmethod
    def int32(val:int):
        '''将int32按大端方式转为字节'''
        return bytearray(val.to_bytes(4, byteorder='big'))
    
    @staticmethod
    def string(val:str):
        '''将字符串转化为字节'''
        return bytearray(val.encode(encoding='utf8'))
    

if __name__ == '__main__':
    while True:
        input()
        
        team = 'yunluxiaodui'
        text = 'START'
        
        tcp_connect = TcpConnect(judge_ip = '127.0.0.1')
        time.sleep(0.3)
        l = tcp_connect.send_team_info(team)
        print("发送长度:",l)
        time.sleep(0.3)
        l = tcp_connect.send_industry_result(text)
        l = tcp_connect.send_detect_result()
        l = tcp_connect.send_rotate_pantilt_1()
        tcp_connect.close()
