import os
import argparse
def get_emotion(loc):
    file_emotion = open(loc,'r')
    line = file_emotion.readline()
    file_emotion.close()
    return line.strip()[0]


def create_list(main_dir,file_loc = "main.txt"):
    if os.path.exists(main_dir)==False:
        print("Not a valid path")
        exit(0)
    file1 = open(file_loc,'w')
    subjects = sorted(os.listdir(main_dir))
    i=0
    for subject in subjects:
        sub_loc = main_dir+"/"+subject
        videos = sorted(os.listdir(sub_loc))
        for video in videos:
            video_loc = sub_loc+"/"+video
            emotion = get_emotion(video_loc+"/emotion.txt")
            frames = sorted([int(x[:-4]) for x in os.listdir(video_loc+"/frames")])
            for frame in frames:
                file1.write(video_loc+"/frames/"+str(frame)+".jpg"+" "+emotion+'\n')
                i+=1
    print("Total Number of Frames:",i)
    file1.close()

def main():
    parser = argparse.ArgumentParser(description = "Create List for all frames with their emotions")
    parser.add_argument("-s", "--src", type = str, nargs = 1,metavar = "source_path", default = None, help = "Location of Folder where all Subject folders with extracted frames are stored")
    parser.add_argument("-d", "--des", type = str, nargs = 1, metavar = "destination_path", default = "main.txt",help = "Loaction of main text file to be created")
    args = parser.parse_args()
    if args.src == None :
        print("Source Folder not specified\nUse 'python3 create_list.py -h' for help.")
        exit(0)
    create_list(args.src[0],args.des[0])
main()
