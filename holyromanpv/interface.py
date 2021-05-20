from struct import pack
import socket
import json
import time
import pandas
import datetime
import pytz


def encrypt(string):
    key = 171
    result = pack('>I', len(string))
    for i in string:
        a = key ^ ord(i)
        key = a
        result += chr(a).encode('latin-1')
    return result

def decrypt(string):
    key = 171
    result = ""
    for i in string:       
        a = key ^ int(i)
        key = int(i)
        result += chr(a)
    return result 


class Interface:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        
    def get_data(self, json_cmd):
        cmd = json.dumps(json_cmd).replace(' ', '')
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((self.ip, self.port))
        sock_tcp.send(encrypt(cmd))
        
        data = sock_tcp.recv(2048)
        # The daystats is larger than 2048 bytes; we fetch a second response
        data += sock_tcp.recv(2048)
        
        sock_tcp.close()
        data = decrypt(data[4:])
        data = dict(json.loads(data))
        return data

    def get_info(self):
        cmd = {"system":{"get_sysinfo":""}}
        data = self.get_data(cmd)
        return data
        
    def turn_on(self):
        cmd = {"system":{"set_relay_state":{"state":1}}}
        data = self.get_data(cmd)
        return data
        
    def turn_off(self):
        cmd = {"system":{"set_relay_state":{"state":0}}}
        data = self.get_data(cmd)
        return data
        
    def turn_led_off(self):
        cmd =  {"system":{"set_led_off":{"off":1}}}
        data = self.get_data(cmd)
        return data 
        
    def get_realtime(self):
        cmd = {"emeter": {"get_realtime": {}}}
        data = self.get_data(cmd)['emeter']['get_realtime']    
        data['power'] = float(data['power'])
        if data['power'] > 1:
            data['power'] = 283233 - data['power']
        data = pandas.DataFrame([data])
        now = datetime.datetime.now()
        data['timestamp'] = str(pytz.timezone('US/Pacific').localize(now))
        return data
        
    def get_daystats(self, year, month):
        cmd = {'emeter': {'get_daystat': {'month': month, 'year': year}}}
        data = self.get_data(cmd)['emeter']['get_daystat']['day_list']
        df = pandas.DataFrame(data)
        df['timestamp'] = pandas.to_datetime(df[['year', 'month','day']])
        df.drop(columns=['year', 'month','day'], inplace=True)
        return df

    def get_monthstats(self, year):
        cmd = {'emeter': {'get_monthstat': {'year': year}}}
        data = self.get_data(cmd)['emeter']['get_monthstat']['month_list']
        df = pandas.DataFrame(data)
        df['day'] = 1
        df['timestamp'] = pandas.to_datetime(df[['year', 'month', 'day']])
        df.drop(columns=['year', 'month', 'day'], inplace=True)    
        return df

    
if __name__ == '__main__':
    ip = '192.168.0.14'
    port = 9999
    interface = Interface(ip, port)
    cmd = {'emeter': {'get_daystat': {'month': 3, 'year': 2021}}}
    interface.get_data(cmd)
    
    
