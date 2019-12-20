import rrdtool
import os


class RrdBaseCreate:

    @staticmethod
    def check_if_base_path_exist(rrd_db_path):
        if os.path.exists(rrd_db_path):
            print("Base path exist")
        else:
            print("Error!: Base path is not exist")
            print("Creating new base path")
            os.mkdir(rrd_db_path)

    @staticmethod
    def check_if_base_exist(rrd_db_path, hostname):
        path_to_db = rrd_db_path + "/" + hostname + ".rrd"
        if os.path.isfile(path_to_db):
            print("RRD base " + hostname + " exist!")
        else:
            print("RRD base " + hostname + " not exist!")

    @staticmethod
    def create_rrd_base(hostname, rrd_db_path):
        path_to_db = rrd_db_path + "/" + hostname + ".rrd"
        rrdtool.create(path_to_db, '--step', '60s', 'DS:' + hostname + ':GAUGE:120:0:999', 'RRA:MAX:0.5:1:1500')

    @staticmethod
    def delete_base(hostname, rrd_db_path):
        path_to_db = rrd_db_path + "/" + hostname + ".rrd"
        os.remove(path_to_db)
