

from pythonping import ping
response_list = ping('52.84.150.36', size=40, count=10).rtt_avg_ms

print(response_list)

