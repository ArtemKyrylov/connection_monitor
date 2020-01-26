from time import sleep
from connection_checker import CheckConnection
from connection_checker import response_data
from hosts import Hosts
from hosts import hosts_list
from rrd_base import RrdBaseCreate
from rrd_graph import RrdDataGraphs
from update_rrd_db import UpdateRrdBase
from http_monitor.http_server import start_http_server
from http_monitor.page import load_monitor_page


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


def get_connection_hosts_info():
    threads = []
    for item, url in enumerate(hosts_list):
        name = "Stream %s" % (item + 1)
        thread = CheckConnection(url, name)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def create_rrd_base():
    rrd = RrdBaseCreate()
    rrd.check_if_base_path_exist()
    for item in hosts_list:
        rrd_db_name = ''.join(item)
        rrd_db = rrd.check_if_base_exist(rrd_db_name)
        if rrd_db is False:
            rrd.create_rrd_base(rrd_db_name)
        else:
            continue


def delete_rrd_base(h_item):
    rrd = RrdBaseCreate()
    rrd.delete_base(h_item)


def create_rrd_graph():
    rrd = RrdDataGraphs()
    rrd.check_if_graph_path_exist()
    for item in hosts_list:
        rrd.create_graph(item)


def delete_rrd_graph(h_item):
    rrd = RrdDataGraphs()
    rrd.delete_graph(h_item)


def compare_hosts_file():
    host_file_work = Hosts()
    file_hostname_updated = []
    hosts_file_read = host_file_work.read_host_file()
    hosts_file_check = host_file_work.check_if_file_not_empty()
    if hosts_file_check is True:
        return 0
    for item in hosts_file_read:
        hostname = host_file_work.reformat_host_line(item)
        file_hostname_updated.append(hostname)
        load_monitor_page()
    for t_item in file_hostname_updated:
        if t_item not in hosts_list:
            host_file_work.add_host_to_list(t_item)
            create_rrd_base()
            create_rrd_graph()
            load_monitor_page()
    for h_item in hosts_list:
        if h_item not in file_hostname_updated:
            hosts_list.remove(h_item)
            h_item = ''.join(h_item)
            if h_item in response_data:
                del response_data[h_item]
            delete_rrd_base(h_item)
            delete_rrd_graph(h_item)
            load_monitor_page()


def update_rrd_base():
    rrd_update = UpdateRrdBase(response_data)
    rrd_update.update_rrd_base()


if __name__ == "__main__":
    work_with_hosts_file()
    get_connection_hosts_info()
    create_rrd_base()
    create_rrd_graph()
    start_http_server()
    while True:
        compare_hosts_file()
        get_connection_hosts_info()
        update_rrd_base()
        create_rrd_graph()
        sleep(60)
