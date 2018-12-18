#/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os, time, cv2
import datetime
import ffmpy3

def scan_files(directory, prefix=None):
    files_list = []
    postfix = [".rmvb", ".flv", ".vob", ".mp4", ".mov", ".3gp", ".wmv", ".mp3", ".mkv", ".mpg", ".ts", ".mpeg",".avi", ".rm", ".wav", ".asf", ".divx", ".mpg", ".mpe", ".vod"]
    for root, sub_dirs, files in os.walk(directory):
       for special_file in files:
          #print(special_file)
           for i in range(len(postfix)):
               if postfix[i]:
                   if special_file.endswith(postfix[i]):
                       #print(special_file.endswith(postfix[i]))
                       files_list.append(os.path.join(root, special_file))
    return files_list


def avtom_path_ass(i, outname):
    ff = ffmpy3.FFmpeg(
            inputs = {i: '-y'},
            outputs = {'/vod/avtom_finish/'+str(outname): '-vf "ass=avtom.ass" -c:v h264_nvenc -c:a copy'}
            )   
    ff.run()

def Tran_720(i, domain, outname):
    outname = outname.split('.')[0]+'-720p.'+outname.split('.')[-1]
    ff = ffmpy3.FFmpeg(
            inputs = {i: '-y -hwaccel cuvid -c:v h264_cuvid'},
            outputs = {'/vod/Transcoding/'+domain+'/'+str(outname): '-vf scale_npp=-1:720 -b:v 1024K -c:v h264_nvenc -c:a copy'}
            )   
    ff.run()

def make_path(p):
    if os.path.exists(p):  # 判断文件夹是否存在
        pass
    else:
        os.mkdir(p)  # 创建文件夹

def path_ass(i, outname, size):
    make_path('/vod/598fl_finish/'+str(datetime.date.today()))
    ff = ffmpy3.FFmpeg(
            inputs = {i: '-y'},
            outputs = {'/vod/598fl_finish/'+str(datetime.date.today())+'/'+str(outname): '-vf "movie='+str(size)+'.png[wm];[i][wm]overlay=main_w-overlay_w-0:main_h-overlay_h-0,ass=logo.ass[out]" -b:v 1024k -c:v h264_nvenc -c:a copy -y'}
            )
    ff.run()


while True:
    file = scan_files('/vod/Transcoding')
    try:
        for i in file:
            if os.path.isfile(i):
                print(os.path.isfile(i))
                cap = cv2.VideoCapture(i)
                size = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                if 720 == size:
                    if 'avtom' in i:
                        avtom_path_ass(i,i.split('/')[-1])
                        os.remove(i)
                        time.sleep(5)
                    elif '598fl' in i:
                        path_ass(i, i.split('/')[-1], size)
                        os.remove(i)
                        time.sleep(5)
                elif 480 ==size:
                    if 'avtom' in i:
                        avtom_path_ass(i,i.split('/')[-1])
                        os.remove(i)
                        time.sleep(5)
                    elif '598fl' in i:
                        path_ass(i, i.split('/')[-1], size)
                        os.remove(i)
                        time.sleep(5)
                elif 1080 ==size:
                    if 'avtom' in i:
                        Tran_720(i, 'avtom', i.split('/')[-1])
                        os.remove(i)
                        time.sleep(5)
                    elif '598fl' in i:
                        Tran_720(i, '598fl', i.split('/')[-1])
                        os.remove(i)
                        time.sleep(5)
                else:
                    if 'avtom' in i:
                        avtom_path_ass(i,i.split('/')[-1])
                        os.remove(i)
                        time.sleep(5)
                    elif '598fl' in i:
                        path_ass(i, i.split('/')[-1], '480')
                        os.remove(i)
                        time.sleep(5)
    except:
        time.sleep(3)
