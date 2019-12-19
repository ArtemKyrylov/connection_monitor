from time import sleep
# from update_rrd_base import Update_rrd_base
# from create_rrd_base import Rrd_base_create
# from draw_rrd_graph import Draw_rrd_data_graphs
from threading import Thread
import subprocess
import re
import os

hosts_list = []
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

    def __init__(self):
        self.hosts_file = hosts_file

    def create_hosts_file(self):
        file = open(self.hosts_file, "w+")
        file.close()

    def check_if_file_exist(self):
        if os.path.isfile(self.hosts_file):
            return True
        else:
            return False

    def check_if_file_not_empty(self):
        if os.stat(self.hosts_file).st_size == 0:
            return True
        else:
            return False

    def read_host_file(self):
        with open(self.hosts_file, "r+") as hf:
            line = hf.readlines()
            while line:
                return line

    def get_file_size(self):
        f_size = os.stat(self.hosts_file)
        return f_size.st_size

    @staticmethod
    def reformat_host_line(line):
        line = ''.join(line)
        line = line.replace('\n', '')
        return line

    @staticmethod
    def add_host_to_list(hostname):
        hosts_list.append(hostname)

    @staticmethod
    def delete_host_from_list(hostname):
        for item in hosts_list:
            if not re.match(hostname, item):
                hosts_list.remove(item)


def work_with_hosts_file():
    file_status = False
    host_file_work = Hosts()
    hosts_file_check = host_file_work.check_if_file_exist()
    if hosts_file_check is True:
        print("Hosts file Exist")
        hosts_file_check = host_file_work.check_if_file_not_empty()
        if hosts_file_check is True:
            print("Error!: File empty")
            file_status = False
        else:
            file_status = True
    else:
        print("Error!: Hosts file does not exist!")
        print("Creating hosts file txt: please add hosts to file line by line, for example: www.facebook.com")
        host_file_work.create_hosts_file()
        hosts_file_check = host_file_work.check_if_file_exist()
        if hosts_file_check is True:
            print("Hosts file created successfully")
            hosts_file_check = host_file_work.check_if_file_not_empty()
            if hosts_file_check is True:
                print("Error!: File empty")
                print("Please add hosts to file line by line, for example: www.facebook.com")
                file_status = False
        else:
            print("Error!: Hosts file NOT created please check folder permission or create file manually!")
            file_status = False
    if file_status is True:
        hosts_file_read = host_file_work.read_host_file()
        for item in hosts_file_read:
            hostname = host_file_work.reformat_host_line(item)
            if hostname not in hosts_list:
                host_file_work.add_host_to_list(hostname)
    file_size = host_file_work.get_file_size()
    return file_size


def get_connection_hosts_info():
    threads = []
    for item, url in enumerate(hosts_list):
        name = "Stream %s" % (item + 1)
        thread = CheckConnection(url, name)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def compare_hosts_file_size(file_size):
    host_file_work = Hosts()
    file_size_check = host_file_work.get_file_size()
    print("file size check", file_size_check)
    if file_size < file_size_check:
        hosts_file_read = host_file_work.read_host_file()
        for item in hosts_file_read:
            hostname = host_file_work.reformat_host_line(item)
            if hostname not in hosts_list:
                host_file_work.add_host_to_list(hostname)
    elif file_size > file_size_check:
        hosts_file_read = host_file_work.read_host_file()
        for item_file in hosts_file_read:
            hostname = host_file_work.reformat_host_line(item_file)
            host_file_work.delete_host_from_list(hostname)
    file_size = file_size_check
    return file_size


if __name__ == "__main__":
    size = work_with_hosts_file()
    get_connection_hosts_info()
    while True:
        size = compare_hosts_file_size(size)
        print(size)
        print(hosts_list)
        sleep(5.0)
    #     main()
    #     # print(response_data)
    #     sleep(1)
    # rrd_create = Rrd_base_create(host, rrd_db_path)
    # rrd_create.check_if_base_path_exist()
    # rrd_update = Update_rrd_base(response_data, rrd_db_path)
    # rrd_update.update_rrd_base()
    # rrd_graph_create = Draw_rrd_data_graphs(host, rrd_graph_path, rrd_db_path)
    # rrd_graph_create.check_if_graph_path_exist()