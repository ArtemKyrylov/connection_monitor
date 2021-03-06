from jinja2 import Environment
import os
from rrd_base import RrdBaseCreate

monitor_file = "index.html"
image_folder = "rrd_graph"
image_list = []
HTML = """
<html>
<head>
<meta http-equiv="refresh" content="60" />
<title>monitor_page</title>
</head>
<body>
<table>
<tr>
{% for image_source in images %}
  <td><img src="{{ image_source }}"></td>
  {% if (loop.index0 % 4) == 3 %}
  </tr>
  {% endif %}
{% endfor %}
</tr>
</table>
</body>
</html>
"""


def monitor_page():
    if os.path.exists(monitor_file):
        f = open(monitor_file, 'w')
        f.close()
    else:
        f = open(monitor_file, 'w')
        f.close()


def get_image_list():
    image_list.clear()
    try:
        for file in os.listdir(image_folder):
            image_path = image_folder + "/" + file
            image_list.append(image_path)
        put_image_to_html()
    except FileNotFoundError:
        rrd = RrdBaseCreate()
        rrd.check_if_base_path_exist()
        for file in os.listdir(image_folder):
            image_path = image_folder + "/" + file
            image_list.append(image_path)
        put_image_to_html()


def put_image_to_html():
    page = Environment().from_string(HTML).render(images=image_list)
    write_to_page(page)


def write_to_page(page):
    file = open(monitor_file, 'r+')
    file.write(page)
    file.close()


def load_monitor_page():
    monitor_page()
    get_image_list()