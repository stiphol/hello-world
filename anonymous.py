import paramiko
import csv
import re

number_of_strings = 2000

host = 'us-u1.r10tech.net'
user = 'damaskin'


def csv_reader(file_obj):
	ip_list = []
	i = 0
	# Skip the first line
	file_obj.readline()
	for ip in file_obj:
		result = ip.split(",")[1]
		ip_list.append(result[1:-1].strip("\n"))
		i+=1
		if i>number_of_strings:
			break
	return ip_list


def anonymous_reading():
	anonymous_ip = []
	with open("GeoIP2-Anonymous-IP-Blocks-IPv4.csv", "r") as a:
		# Skip the first line
		a.readline()
		for line in a:
			result = re.search(r'^[0-9.]+', line.split(",")[0])
			ip = result[0]
			anonymous_ip.append(ip.strip("\n"))
	return anonymous_ip



if __name__ == "__main__":

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# Connection
	client.connect(hostname=host, username=user)

	# Change directory
	client.exec_command('cd /home/damaskin/dmsk')
	stdin, stdout, stderr = client.exec_command('ls -l')

	# read ip
	data = stdout.read() + stderr.read()
	csv_path = "imp.csv"
	with open(csv_path, "r") as f_obj:
		ip_list = csv_reader(f_obj)
	client.close()

	#read local file with Anonymous IP
	anonymous_ip = anonymous_reading()


	for current_ip in ip_list:
		if current_ip in anonymous_ip:
			print(current_ip)
