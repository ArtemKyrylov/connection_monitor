import rrdtool
from rrd_base import rrd_db_path


class UpdateRrdBase:

    def __init__(self, response_data):
        self.response_data = response_data

    def update_rrd_base(self):
        for key, value in self.response_data.items():
            host = ''.join(key)
            host = host.replace(".", "")
            path_to_db = rrd_db_path + "/" + host + ".rrd"
            rrdtool.update(path_to_db, 'N:' + str(value))
