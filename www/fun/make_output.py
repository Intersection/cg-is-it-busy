#!/usr/bin/env python

import boto
from time import strftime, gmtime

SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60
UTC_EDT_OFFSET_HOURS = 3

conn = boto.connect_sdb()
dom = conn.get_domain('izitbz-izitbzsdb-1SYEBQOQKR1G3')

query="select * from `izitbz-izitbzsdb-1SYEBQOQKR1G3` where `time_int` is not null order by `time_int`"
rs = dom.select(query)

output="""<html>\n \
  <head>\n \
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>\n \
    <script type="text/javascript">\n \
      google.load("visualization", "1", {packages:["corechart"]});\n \
      google.setOnLoadCallback(drawChart);\n \
      function drawChart() {\n \
        var data = google.visualization.arrayToDataTable([\n"""

output += "['Time Interval', '# of unique MACs'],\n"
for item in rs:
    t_int = int(item['time_int']) - (SECONDS_IN_MINUTE * MINUTES_IN_HOUR * UTC_EDT_OFFSET_HOURS)
    t_int_str = strftime("%a %b %d %I:%M %p",gmtime(int(t_int)))
    output += "['" + t_int_str + "', " + str(int(item['count'])) + "],\n"

output = output[:-1]
output += """]);
        var options = {
          title: 'Is It Busy?',
          width: '1200',
          is3D: true
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>"""
print output
