from time import sleep
# from update_rrd_base import Update_rrd_base
# from create_rrd_base import Rrd_base_create
# from draw_rrd_graph import Draw_rrd_data_graphs
from threading import Thread
import subprocess
import re
import os
response_data = {}
rrd_db_path = "rrd_db"
rrd_graph_path = "rrd_graph"


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





class GetHostsFromFile:

    def __init__(self):
        self.host_file = 'hosts.txt'
        self.host_list = []
        self.line = ""

    @staticmethod
    def check_if_host_file_exist(self):
        if os.path.isfile(self.host_file):
            return True
        else:
            print("No hosts file, please create hosts.txt file, with host line - for example: www.facebook.com, "
                  "Attention! all host must be added with new line")
            return False

    def read_host_file(self):
        with open(self.host_file, 'r+') as file:
            for line in file:
                line = line.replace('\n', '')
                self.host_list.append(line)
                return self.line

    def if_hostname_does_not_exist_in_host_list(self):
        if self.line





    def get_host():
        host_file_name = 'hosts.txt'
        if os.path.isfile(host_file_name):
            file = open(host_file_name, 'r+')
            for line in file:
                line = line.replace('\n','')
                if line not in host:
                    host.append(line)
                    for item in host:
                        item = ''.join(item)
                        if item not in file.read():
                            host.remove(item)
        else:
        print("No hosts file, please add hosts.txt file, with host line - for example: www.facebook.com")
    print(host)


def main():
    threads = []
    for item, url in enumerate(host):
        name = "Stream %s" % (item + 1)
        thread = CheckConnection(url, name)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    # rrd_create = Rrd_base_create(host, rrd_db_path)
    # rrd_create.check_if_base_path_exist()
    # rrd_update = Update_rrd_base(response_data, rrd_db_path)
    # rrd_update.update_rrd_base()
    # rrd_graph_create = Draw_rrd_data_graphs(host, rrd_graph_path, rrd_db_path)
    # rrd_graph_create.check_if_graph_path_exist()


if __name__ == "__main__":
    while True:
        get_host()
        main()
        print(response_data)
        sleep(1)