import sys
import os
import subprocess

# find the path to xia-core
sys.path.append('/usr/local/lib')

from c_xsocket import *

def cal_sid_port(name):
	port = 0

	for i in range(0, len(name)):
		port += (ord(name[i]) - 10) * (10 ** i)

	while (port > 65535):
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

audio_command = ["gnome-terminal", "-x","mediastream", "--local", str(local_port), "--remote", remote_ad + "\\" + remote_hid + ":" + str(remote_port), "--payload", "110"]
video_command = ["gnome-terminal", "-x","mediastream", "--local", str(local_port + 1), "--remote", remote_ad + "\\" + remote_hid + ":" + str(remote_port + 1), "--payload", "102", "--mtu", "1450"]

p_video = subprocess.Popen(video_command)
p_audio = subprocess.Popen(audio_command)
p_video.poll()
p_audio.poll()
