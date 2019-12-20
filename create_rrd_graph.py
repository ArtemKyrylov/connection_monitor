import rrdtool
import os


class RrdBaseCreate:

    @staticmethod
    def __init__(self, social_host_list, rrd_db_path):
        self.social_host_list = social_host_list
        self.rrd_db_path = rrd_db_path

    @staticmethod
    def check_if_base_path_exist(self):
        if os.path.exists(self.rrd_db_path):
            print("Base path exist")
        else:
            print("Base path is not exist")
            os.mkdir(self.rrd_db_path)
        self.check_if_base_exist()

    @staticmethod
    def check_if_base_exist(self):
        for item in self.social_host_list:
            ds = ''.join(item)
            ds = ds.replace(".", "")
            path_to_db = self.rrd_db_path + "/" + ds + ".rrd"
            if os.path.isfile(path_to_db):
                print("RRD base " + ds + " exist!")
            else:
                print("RRD base " + ds + " not exist!")
                print("Create base")
                self.create_rrd_base(ds, path_to_db)

    @staticmethod
    def create_rrd_base(ds, path_to_db):
        rrdtool.create(path_to_db, "--step", "60s", "DS:" + ds + ":GAUGE:120:0:999", "RRA:MAX:0.5:1:1500")