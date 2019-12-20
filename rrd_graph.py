import rrdtool
import os
import datetime
from rrd_base import rrd_db_path
rrd_graph_path = "rrd_graph"


class RrdDataGraphs:

    @staticmethod
    def check_if_graph_path_exist():
        if os.path.exists(rrd_graph_path):
            print("Graph path exist")
        else:
            print("Graph path is not exist")
            print("Create graph path")
            os.mkdir(rrd_graph_path)

    @staticmethod
    def check_if_graph_file_exist(hostname):
        hostname = ''.join(hostname)
        hostname = hostname.replace(".", "")
        graph_name = rrd_graph_path + "/" + hostname + ".png"
        if os.path.isfile(rrd_graph_path):
            print("RRD graph " + graph_name + " exist!")
            return True
        else:
            print("RRD graph " + graph_name + " not exist!")
            return False

    @staticmethod
    def create_graph(host):
        host = ''.join(host)
        full_host_name = host
        host = host.replace(".", "")
        graph_name = rrd_graph_path + "/" + host + ".png"
        rrd_base_name = rrd_db_path + "/" + host + ".rrd"
        date_time = datetime.datetime.now()
        rrdtool.graph(graph_name, "-w", "700", "-h", "360", "-a", "PNG", "--slope-mode", "--start", "-86400", "--end", "now",
                          "--font", "WATERMARK:7:Liberation Sans", "--font", "TITLE:15:Liberation Sans",
                          "--font", "AXIS:12:Liberation Sans", "--font", "AXIS:12:Liberation Sans",
                          "--font", "UNIT:12:Liberation Sans", "--font", "LEGEND:12:Liberation Sans",
                          "--title", full_host_name, "--watermark", "Generated " + str(date_time),
                          "--vertical-label", "Average rtt", "--lower-limit", "0", "--upper-limit", "999",
                          "--right-axis", "1:0", "--x-grid", "MINUTE:10:HOUR:1:MINUTE:120:0:%R", "--alt-y-grid",
                          "--rigid", "DEF:" + host + "=" + rrd_base_name + ":" + host + ":LAST",
                          "HRULE:100#ff0000::dashes=2", "LINE2:" + host + "#0000cc:" + host,
                          "GPRINT:" + host + ":LAST:" + "%6.3lf%s")