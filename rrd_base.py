import rrdtool
import os
rrd_db_path = "rrd_db"


class RrdBaseCreate:

    @staticmethod
    def check_if_base_path_exist():
        if os.path.exists(rrd_db_path):
            print("Base path exist")
        else:
            print("Error!: Base path is not exist")
            print("Creating new base path")
            os.mkdir(rrd_db_path)

    @staticmethod
    def check_if_base_exist(hostname):
        hostname = hostname.replace(".", "")
        path_to_db = rrd_db_path + "/" + hostname + ".rrd"
        if os.path.isfile(path_to_db):
            print("RRD base " + hostname + " exist!")
            return True
        else:
            print("RRD base " + hostname + " not exist!")
            return False

    @staticmethod
    def create_rrd_base(hostname):
        hostname = hostname.replace(".", "")
        path_to_db = rrd_db_path + "/" + hostname + ".rrd"
        rrdtool.create(path_to_db, '--step', '60s', 'DS:' + hostname + ':GAUGE:120:0:999', 'RRA:MAX:0.5:1:1500')

    @staticmethod
    def delete_base(hostname):
        hostname = hostname.replace(".", "")
        path_to_db = rrd_db_path + "/" + hostname + ".rrd"
        os.remove(path_to_db)
