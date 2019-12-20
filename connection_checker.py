from threading import Thread
import subprocess
import re
response_data = {}


class CheckConnection(Thread):

    def __init__(self, url, name):
        Thread.__init__(self)
        self.name = name
        self.url = url

    def run(self):
        command = "ping " + self.url + " -c 1"
        ping = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        ping_out = ping.communicate()[0]
        pattern_ping_time = r'(time=\d{0,4}.\d{0,2})'
        pattern_connection_lost = r'(100% packet loss)'
        if re.findall(pattern_connection_lost, ping_out):
            time_r_s = 999
            print(self.url, time_r_s)
            response_data.update({self.url: time_r_s})
        elif re.findall(pattern_ping_time, ping_out):
            response_time = re.findall(pattern_ping_time, ping_out)
            time_r_s = ''.join(response_time)
            time_r_s = time_r_s.strip('time=')
            time_r_s = float(time_r_s)
            print(self.url, time_r_s)
            response_data.update({self.url: time_r_s})
        else:
            time_r_s = 999
            print(self.url, time_r_s)
            response_data.update({self.url: time_r_s})