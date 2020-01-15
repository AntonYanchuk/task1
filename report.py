import psutil
import os

bgcolor_mem = '#00ff00'
bgcolor_proccess = '#00ff00'
host_report = os.uname()[1]
# host_report = 'machine'
print(host_report)
a = psutil.virtual_memory()
mem_percent = 100.0 - float(a.percent)
mem_percent = round(mem_percent, 2)
mem_total = round(a.total / (1024.0 ** 3), 2)

if mem_percent < 20:
    bgcolor_mem = '#FF0000'
print("Total RAM: {}GB".format(mem_total))
print("RAM Free: {}%".format(mem_percent))

disks = psutil.disk_partitions()
disks_report = list()
disks_value = str("")
disk_count = len(disks)
for n in range(disk_count):
    disk_name = disks[n][1]
    b = psutil.disk_usage(disk_name)
    disk_total = round(b.total / (1024.0 ** 3), 2)
    disk_percent = 100.0 - float(b.percent)
    bgcolor_disks = '#00ff00'
    if disk_percent < 20:
        bgcolor_disks = '#FF0000'
    disks_value += "<tr><td style=\"width: 155.667px;\">DISK SPACE {disk_name}</td><td style=\"width: 155.667px; text-align: center;\">&nbsp;{disk_total} GB</td><td style=\"width: 155.667px; text-align: center;\">&nbsp;<span style=\"color: {bgcolor_disks};\">{disk_percent}</span></td></tr>\n".format(
        disk_name=disk_name, disk_total=disk_total, disk_percent=disk_percent, bgcolor_disks=bgcolor_disks)


pid_result = None

for root, dirs, files in os.walk("/opt"):
    for file in files:
        if file.endswith("cq.pid"):
            pid_path = os.path.join(root, file)
            f = open(pid_path, "r")
            content = int(f.read())
            print(content)
            pid_result = psutil.pid_exists(content)
            print(pid_result)
        else:
            pid_result = 'false'
            print('Can\'t find AEM pid file')
            bgcolor_proccess = '#8B0000'

if pid_result is None:
    pid_result = 'false'
    print('Can\'t find AEM pid file')
    bgcolor_proccess = '#8B0000'

message = """
<html>
<head></head>
<body>
<p>Memory report from {host}</p>
<h2>Status of AEM Proccess: <span style="color: {bgcolor_proccess};">{pid_result}</span></h2>
<table style="height: 77px;" width="489">
<tbody>
<tr>
<td style="width: 155.667px;">&nbsp;</td>
<td style="width: 155.667px; text-align: center;">Total</td>
<td style="width: 155.667px; text-align: center;">% Free</td>
</tr>
<tr>
<td style="width: 155.667px;">RAM</td>
<td style="width: 155.667px; text-align: center;">&nbsp;{mem_total} GB</td>
<td style="width: 155.667px; text-align: center;">&nbsp;<span style="color: {bgcolor_mem};">{mem_percent}</span></td></tr>
{disks0}
</tbody>
</table>
<p>&nbsp;</p>
  </body>
</html>
""".format(host=host_report, mem_total=mem_total, mem_percent=mem_percent, disks0=disks_value, pid_result=pid_result,
           bgcolor_proccess=bgcolor_proccess, bgcolor_mem=bgcolor_mem)

f = open('/tmp/helloworld.html', 'w')

f.write(message)
f.close()
