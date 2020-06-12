import cv2
import numpy as np
import os
import shutil
import matplotlib.pyplot as plt
import argparse

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def rotate(image):
  l1=[]
  eyes = eye_cascade.detectMultiScale(image)
  for (ex,ey,ew,eh) in eyes:
      l1.append((ex+ew/2,ey+eh/2))

  if(len(l1)==2):
    dist_x = l1[1][0]-l1[0][0]
    dist_y = l1[1][1] - l1[0][1]
    if dist_x<0:
      dist_y = -dist_y
    dist_x = np.abs(dist_x)
    angle = np.arctan(dist_y/(dist_x+1e-8)) * 180/3.14
    M = cv2.getRotationMatrix2D((240, 240), angle, 1.0)
    image = cv2.warpAffine(image, M,(480,480))
  return image

def crop(image,x_factor=2.1,y_factor=3.2):
  l1=[]
  eyes = eye_cascade.detectMultiScale(image)
  for (ex,ey,ew,eh) in eyes:
      l1.append((ex+ew/2,ey+eh/2))
  if(len(l1)==2):
    dist = np.sqrt((l1[0][0]-l1[1][0])**2+(l1[0][1]-l1[1][1])**2)
    center_x = image.shape[1]//2
    center_y = image.shape[0]//2
    shift_x = int(dist*x_factor)//2
    shift_y = int(dist*y_factor)//2
    start_x = center_x - shift_x
    start_x = max(start_x,0)
    end_x = center_x+shift_x
    end_x = min(end_x,image.shape[1])
    start_y = center_y - shift_y
    start_y = max(start_y,0)
    end_y = center_y + shift_y
    end_y = min(end_y,image.shape[0])
    image = image[start_y:end_y,start_x:end_x]
  return image



def extract(video,folder,n):
    vidcap = cv2.VideoCapture(video)
    total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    frames_step = total_frames//n
    j=0
    for i in range(n):
        #here, we set the parameter 1 which is the frame number to the frame (i*frames_step)
        vidcap.set(1,i*frames_step)
        success,image = vidcap.read()
        faces = face_cascade.detectMultiScale(image)
        if(len(faces)==1):
            for (x,y,w,h) in faces:
                image = image[y:y+h,x:x+h]
            image = cv2.resize(image,(480,480), interpolation = cv2.INTER_AREA)
            image = rotate(image)
            image = crop(image)
            image = cv2.resize(image,(48,48), interpolation = cv2.INTER_AREA)
            image_path = folder+"/"+str(i)+".jpg"
            cv2.imwrite(image_path,image)
            j+=1
    vidcap.release()
    return j



def main_func(src_path,dest_path,n):
    if os.path.exists(src_path) ==False:
        print("No such Folder exists. Check your source folder")
        exit(0)
    if os.path.exists(dest_path)==False:
        os.mkdir(dest_path)
    subjects = os.listdir(src_path)
    for subject in subjects:
        i=0
        j=0
        print("Extracting Frames for "+subject+"...")
        dest_subject = dest_path+"/"+subject
        os.mkdir(dest_subject)
        src_subject = src_path+"/"+subject
        vid_loc = src_subject+"/avi"
        emotion_loc = src_subject+"/emotion"
        videos = os.listdir(vid_loc)
        for video in videos:
            i+=1
            src_vid = vid_loc+"/"+video
            dest_vid = dest_subject+"/"+video[:-4]
            os.mkdir(dest_vid)
            dest_vid_image = dest_vid+"/frames"
            os.mkdir(dest_vid_image)
            shutil.copyfile(emotion_loc+"/"+video[:-4]+".txt", dest_vid+"/emotion.txt")
            num = extract(src_vid,dest_vid_image,n)
            j+=num
        print(i,"Videos Found,",j,"Frames Extracted")
    print("Extraction Completed!")
def main():
    parser = argparse.ArgumentParser(description = "Extacts frames from videos")
    parser.add_argument("-s", "--src", type = str, nargs = 1,metavar = "source_path", default = None, help = "Location of Folder where all Subject folders are stored")
    parser.add_argument("-d", "--des", type = str, nargs = 1, metavar = "destination_path", default = None,help = "Location of Folder where you want to store all extracted frames.")
    parser.add_argument("-n", "--frames", type = int, nargs = 1,metavar = "number_of_frames", default = 16,help = "Number of Frames you want to extract for each video(optional)")
    args = parser.parse_args()
    if args.src == None or args.des == None:
        print("Source or Destination Folders not specified\nUse 'python3 extract_frames.py -h' for help.")
        exit(0)
    main_func(args.src[0],args.des[0],args.frames)
main()
