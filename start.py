from time import sleep
from connection_checker import CheckConnection
from connection_checker import response_data
from hosts import Hosts
from hosts import hosts_list
from create_rrd_base import RrdBaseCreate
# from update_rrd_base import Update_rrd_base
# from draw_rrd_graph import Draw_rrd_data_graphs

rrd_db_path = "rrd_db"
rrd_graph_path = "rrd_graph"


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


def compare_hosts_file():
    host_file_work = Hosts()
    file_hostname_updated = []
    hosts_file_read = host_file_work.read_host_file()
    for item in hosts_file_read:
        hostname = host_file_work.reformat_host_line(item)
        file_hostname_updated.append(hostname)
    for t_item in file_hostname_updated:
        if t_item not in hosts_list:
            host_file_work.add_host_to_list(t_item)
    for h_item in hosts_list:
        if h_item not in file_hostname_updated:
            hosts_list.remove(h_item)


if __name__ == "__main__":
    work_with_hosts_file()
    get_connection_hosts_info()
    while True:
        compare_hosts_file()
        print(hosts_list)
        print(response_data)
        sleep(60)
    # rrd_create = Rrd_base_create(host, rrd_db_path)
    # rrd_create.check_if_base_path_exist()
    # rrd_update = Update_rrd_base(response_data, rrd_db_path)
    # rrd_update.update_rrd_base()
    # rrd_graph_create = Draw_rrd_data_graphs(host, rrd_graph_path, rrd_db_path)
    # rrd_graph_create.check_if_graph_path_exist()