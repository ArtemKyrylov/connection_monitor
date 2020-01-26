import os
hosts_file = "hosts.txt"
hosts_list = []


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
            print("Hosts file is empty")
            return True
        else:
            return False

    def read_host_file(self):
        with open(self.hosts_file, "r+") as hf:
            line = hf.readlines()
            while line:
                return line

    @staticmethod
    def reformat_host_line(line):
        line = ''.join(line)
        line = line.replace('\n', '')
        return line

    @staticmethod
    def add_host_to_list(hostname):
        hosts_list.append(hostname)
