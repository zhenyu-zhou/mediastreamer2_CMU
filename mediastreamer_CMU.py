import sys
import os
import time

# find the path to xia-core
sys.path.append('/usr/local/lib')

from c_xsocket import *

def cal_sid_port(name):
	port = 0

	for i in range(0, len(name)):
		port += (ord(name[i]) - 10) * (10 ** i)

	while (port > 60000):
		port /= 2

	hex_port = str(hex(port))[2:]

	sid = "SID:"
	for i in range(0, 40 - len(hex_port)):
		sid += "0"
	sid += hex_port

	return (sid, port)

def getAD_HID(dag):
	for i in range(0, len(dag)):
		if dag[i] == 'A' and dag[i + 1] == 'D' and dag[i + 2] == ':':
			ad = dag[i:(i + 43)]
			break

	for i in range(0, len(dag)):
		if dag[i] == 'H':
			hid = dag[i:(i + 44)]
			break
	return (ad, hid)

try:
	local_name = raw_input("Please enter your name:")

	sock = Xsocket(XSOCK_DGRAM)
	(local_ad, local_hid, fid) = XreadLocalHostAddr(sock)
	local_dag = "RE %s %s %s" % (local_ad, local_hid, cal_sid_port(local_name)[0])
	local_port = cal_sid_port(local_name)[1]

	XregisterName(local_name, local_dag)

	remote_name = raw_input("Please enter your partener's name:")
	remote_dag = XgetDAGbyName(remote_name)
	(remote_ad, remote_hid) = getAD_HID(remote_dag)
	remote_port = cal_sid_port(remote_name)[1]

	audio_command = "gnome-terminal -x mediastream --local %d --remote %s\\ %s:%d --payload 110" % (local_port + 16, remote_ad, remote_hid, remote_port + 16)
	video_command = "gnome-terminal -x mediastream --local %d --remote %s\\ %s:%d --payload 102 --mtu 1450" % (local_port, remote_ad, remote_hid, remote_port)

	os.system(video_command)
	time.sleep(1)
	os.system(audio_command)
except:
	print "Oops, an error occured."
