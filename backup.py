#!/usr/bin/env python3
import subprocess
import os
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
if len(sys.argv) == 2:
    driveName = sys.argv[1]
    batcmd="system_profiler SPUSBDataType"
    connected_devices = subprocess.check_output(batcmd, shell=True)
    isDriveConn = "/Volumes/{}".format(driveName) in str(connected_devices)
    if isDriveConn:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for i in file_list:
            if i['title'] == 'pictures':
                folderId = i['id']
        photo_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folderId)}).GetList()
        if not os.path.exists("/Volumes/{}/Pictures".format(driveName)):
            os.makedirs("/Volumes/{}/Pictures".format(driveName))
        setOnGoogle = set(map(lambda x: x['title'], photo_list))
        setOnDrive = set(os.listdir("/Volumes/{}/Pictures".format(driveName)))
        for i in setOnDrive.difference(setOnGoogle):
            file1 = drive.CreateFile({'title': i, 'parents': [{'id': folderId}]})
            file1.SetContentFile('/Volumes/{}/Pictures/{}'.format(driveName,i))
            file1.Upload()
            print(i)
    else:
        print('Error: The drive isnt connected')
else:
    print('Error: [Name of drive]')