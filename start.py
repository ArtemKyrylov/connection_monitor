from time import sleep
# from update_rrd_base import Update_rrd_base
# from create_rrd_base import Rrd_base_create
# from draw_rrd_graph import Draw_rrd_data_graphs
from threading import Thread
import subprocess
import re
import os

hosts = []
response_data = {}
rrd_db_path = "rrd_db"
rrd_graph_path = "rrd_graph"
hosts_file = "hosts.txt"


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


class Hosts(object):

    @staticmethod
    def create_hosts_file(file_name):
        file = open(file_name, "w+")
        file.close()

    @staticmethod
    def check_if_file_exist(file_name):
        if os.path.isfile(file_name):
            return True
        else:
            return False

    @staticmethod
    def check_if_file_not_empty(file_name):
        if os.stat(file_name).st_size == 0:
            return False
        else:
            return True

    @staticmethod
    def read_host_file(self):
        with open(hosts_file, "r+") as hf:
            for line in hf:
                return line

    @staticmethod
    def reformat_host_line(self, line):
        line = ''.join(line)
        hostname = line.replace('\n', '')

    @staticmethod
    def add_host_to_list(self, hostname):
        hosts.append(hostname)

    @staticmethod
    def delete_host_from_list(self, hostname):
        for item in hosts:
            item = ''.join(item)
            if re.match(hostname, item):
                hosts.remove(item)


def main():
    host_file_work = Hosts()
    hosts_file_check = host_file_work.check_if_file_exist(hosts_file)
    if hosts_file_check is True:
        print("Hosts file Exist")
        hosts_file_check = host_file_work.check_if_file_not_empty(hosts_file)
        if hosts_file_check is True:
            print("Error!: File empty")
    else:
        print("Error!: Hosts file does not exist!")
        print("Creating hosts file txt: please add hosts to file line by line, for example: www.facebook.com")
        host_file_work.create_hosts_file(hosts_file)
        hosts_file_check = host_file_work.check_if_file_exist(hosts_file)
        if hosts_file_check is True:
            print("Hosts file created successfully")
            hosts_file_check = host_file_work.check_if_file_not_empty(hosts_file)
            if hosts_file_check is True:
                print("Error!: File empty")
                print("Please add hosts to file line by line, for example: www.facebook.com")
        else:
            print("Error!: Hosts file NOT created please check folder permission or create file manually!")
    
    threads = []
    for item, url in enumerate(hosts):
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
        main()
        print(response_data)
        sleep(1)