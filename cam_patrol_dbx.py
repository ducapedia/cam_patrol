  #!/usr/bin/env python2
# -*- coding: utf-8-*-
# each hour or half hour go to every preset point and take a snapshot
import urllib2
import time
import dropbox
import os

# Camera Access Parameters
ip = '(camera IP)'
port = '(camera port)'
user = '(camera login)'
pwd = '(camera password)'

# URL components
cam = 'http://' + ip + ':' + port + '/'
auth = '&user=' + user + '&pwd=' + pwd
shot = '/snapshot.cgi?'
#Set patrol rate speed to Fastest
speed = '/set_misc.cgi?ptz_patrol_rate=' + '12'

# Working directory
os.chdir("/usr/local/share/cam_patrol")

# Dropbbox
app_key = '(dropbox key)'
app_secret = '(dropbox secret)'
access_token = '(dropbox token)'

# URL command
url_speed = cam + speed + auth
url_shot = cam + shot + auth
cam_cmd_speed = urllib2.urlopen(url_speed)

#Preset positions - 1 to 6 (2 is default home position (entrance door))
#Using dictionary
pos_dict = {'31':'place1','33':'place2', '35':'place3', '37':'place4', '39':'place5', '41':'place6'}
for code, place in sorted(pos_dict.items()):
	goto = '/decoder_control.cgi?command=' + code
	url_goto = cam + goto + auth
	cam_cmd_goto = urllib2.urlopen(url_goto)
	time.sleep(30)
	cam_cmd_shot = urllib2.urlopen(url_shot)
	#change name to position + timestamp
	timestamp = time.strftime("%Y%m%d-%H%M%S")
	filename = timestamp + "-" + place + ".jpg"
	snapshot = open(filename,'wb')
	snapshot.write(cam_cmd_shot.read())
	snapshot.close()
	file_ftp_up = open(filename, 'rb')
	dbx = dropbox.Dropbox('access_token')
	dbx.files_upload(file_ftp_up,'/Apps/cam_patrol/' + filename, mute=True)
	file_ftp_up.close()

#Go Back to position 2 (home position (door))
ftp_nas.quit()
go_home = '/decoder_control.cgi?command=' + '33'
url_home = cam + go_home + auth
cam_cmd_home = urllib2.urlopen(url_home)
