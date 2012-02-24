import boto
from time import strftime, gmtime
from django.http import HttpResponse
import json
import os

SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60
SECONDS_PER_INTERVAL=300
UTC_EDT_OFFSET_HOURS = -1
BUSY_THRESH = 60

domain_name=os.environ['SDB_DOMAIN']


def pad_count(count):
    '''
    Prefix the MAC address "count" for each db entry so that each count attribute is of consistent length,
    in order to be compatible with SimpleDB's lexicographical comparisons
    '''

    final_num_digits = 8 # The number of digits the output string should contain
    digs=len(str(count))
    prefix=''
    for x in range(final_num_digits - digs):
        prefix = prefix+'0'
    return prefix+str(count)

def format_date(timestamp):
    ''' take UNIX timestamp, return pretty date string'''
    return "(new Date('" + str(strftime("%c", gmtime(int(timestamp) + (SECONDS_IN_MINUTE * MINUTES_IN_HOUR * UTC_EDT_OFFSET_HOURS)))) + "'))"

def make_intervals(rs):
    cont_seg_list=[]
    old_ts = 0
    it = 0

    for datapoint in rs:
        if int(datapoint['time_int']) - old_ts - SECONDS_PER_INTERVAL: # It's time to D-D-D-D-DUEL
            it+=1
            cont_seg_list.append([datapoint])
        else:
            try:
                cont_seg_list[it].append(datapoint)
            except IndexError:
                cont_seg_list.append([datapoint])
        old_ts=int(datapoint['time_int'])

    return cont_seg_list

def simple_izitbz(request):
    conn = boto.connect_sdb()
    dom = conn.get_domain(domain_name)
    query = "select * from `" + domain_name + "` where `time_int` is not null order by `time_int`"
    data = dom.select(query)
    responseSet = []
    sample_size = 4 # Number of datapoints to average
    for dp in data:
        responseSet.append(dp)
    responseSet = responseSet[-sample_size:]

    average = 0
    for dp in responseSet:
        average += int(dp['count'])
    average /= sample_size


    response = "<html>\n<title>Is it busy?</title>"
    response += """<style media="screen" type="text/css">

    body {
    font-family: Georgia;
    font-size: 60px;
    text-align: center;
    margin-top: 200px;
    color: #477EB4
    }

    .link {
    font-size: 14px;
    }

    </style>"""
    response += "\n<div font-family:sans-serif>"
    response += "It's busy!" if (average > BUSY_THRESH) else "It's not busy."
    response += "</div>"
    response += """<br/><br/><div class="link"><a href="/chart" target="_blank">Data!</a></div></html>"""
    return HttpResponse(response)

def latest_chart(request):
    conn = boto.connect_sdb()
    dom = conn.get_domain(domain_name)

    busy_thresh = pad_count(BUSY_THRESH)

    all_query="select * from `" + domain_name + "` where `time_int` is not null order by `time_int`"
    busy_query="select * from `" + domain_name + "` where `time_int` is not null and `count` > '" + busy_thresh + "' order by `time_int`"
    not_busy_query="select * from `" + domain_name + "` where `time_int` is not null and `count` < '" + busy_thresh + "' order by `time_int`"
    rs = dom.select(all_query)
    busy_rs = dom.select(busy_query)
    not_busy_rs = dom.select(not_busy_query)

    busy_segments=make_intervals(busy_rs)
    not_busy_segments=make_intervals(not_busy_rs)

    json_table = {}
    colors_switches = []
    cols_it = 1
    rows_it = 0

    json_table['cols'] = []
    json_table['rows'] = []

    json_table['cols'].append({})
    json_table['cols'][0]['id']="'timestamp'"
    json_table['cols'][0]['label']="'Timestamp'"
    json_table['cols'][0]['type']="'datetime'"

    for segments in busy_segments:
        json_table['cols'].append({})
        json_table['cols'][cols_it]['id']="'count'"
        json_table['cols'][cols_it]['label']="'# of unique MACs'"
        json_table['cols'][cols_it]['type']="'number'"
        colors_switches.append('red')

        for datapoint in segments:
            json_table['rows'].append({})
            json_table['rows'][rows_it]['c'] = []
            for x in range(2+len(not_busy_segments) + len(busy_segments)):
                json_table['rows'][rows_it]['c'].append({"v": 'null'})
            json_table['rows'][rows_it]['c'][0]['v'] = format_date(datapoint['time_int'])
            json_table['rows'][rows_it]['c'][cols_it]['v'] = str(int(datapoint['count']))
            rows_it += 1
        cols_it += 1

    for segments in not_busy_segments:
        json_table['cols'].append({})
        json_table['cols'][cols_it]['id']="'count'"
        json_table['cols'][cols_it]['label']="'# of unique MACs'"
        json_table['cols'][cols_it]['type']="'number'"
        colors_switches.append('blue')

        for datapoint in segments:
            json_table['rows'].append({})
            json_table['rows'][rows_it]['c'] = []
            for x in range(2+len(busy_segments) + len(not_busy_segments)):
                json_table['rows'][rows_it]['c'].append({"v": 'null'})
            json_table['rows'][rows_it]['c'][0]['v'] = format_date(datapoint['time_int'])
            json_table['rows'][rows_it]['c'][cols_it]['v'] = str(int(datapoint['count']))
            rows_it += 1
        cols_it += 1


    #print json_table

    json_data =  json.dumps(json_table).replace('"','')

    output="""<html>\n \
            <head>\n \
            <script type="text/javascript" src="https://www.google.com/jsapi"></script>\n \
            <script type="text/javascript">\n \
            google.load("visualization", "1", {packages:["corechart"]});\n \
            google.setOnLoadCallback(drawChart);\n \
            function drawChart() {\n \
            var data = new google.visualization.DataTable(\n"""
    output += json_data
    output += ");\n"
    #old_t = -1337
    #for item in busy_rs:
        #t_int = int(item['time_int']) - (SECONDS_IN_MINUTE * MINUTES_IN_HOUR * UTC_EDT_OFFSET_HOURS)
        ##t_int_str = strftime("%Y-%m-%dT%H:%M-04:00",gmtime(int(t_int)))
        #if t_int - old_t is not SECONDS_PER_INTERVAL and old_t is not -1337:
            #t_int_str = str(old_t + SECONDS_PER_INTERVAL)
            #count = ""
        #else:
            #t_int_str = str(t_int)
            #count = str(int(item['count']))
        #output += "[" + t_int_str + ", " + count + "],\n"
        #old_t += int(t_int_str)

    #output = output[:-2]
    output += """
            var options = {
              title: 'Is It Busy?',
              width: '1200',
              series: ["""

    for color in colors_switches:
        output += "{color: '" + color + "', visibleInLegend: false},"
    output = output[:-1]
    output += """]

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

    return HttpResponse(output)
