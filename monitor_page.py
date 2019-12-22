import os
import numpy as np
http_monitor_path = "http_monitor"
http_monitor_page = "index.html"
graph_files_path = "rrd_graph"
graph_files_list = []


def get_graph_files():
    files = os.listdir(graph_files_path)
    for item in files:
        graph_files_list.append(item)
    create_html()


def create_html():
    file_counter = 0
    files_html = []
    tr_open = "<tr>"
    tr_close = "</tr>"
    th_open = "<th>"
    th_close = "</th>"
    html_head = """<html><table style="width:100%">"""
    html_end = """</table><html>"""
    img_open = "<img src=\""
    for item in graph_files_list:


# f = open(http_monitor_path + '/' + http_monitor_page, 'w')
#
#
#
# f.write(message)
# f.close()

get_graph_files()