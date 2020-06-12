# Extracting Frames for Emotion recognition
## For BAUM dataset
### Important Note
After downloading all the zip files of BAUM dataset. Extract them all and then copy all the Subject folders into a single directory.

**Functions**
1. **extract_frames.py [-h] [-s source_path] [-d destination_path] [-n number_of_frames]** :
This function extracts frames from each video of all subject and store them in a separate folder for further use.

*source_path*: The path of directory where all subjects folder are stored.

*destination_path*: The path of directory where you want to store all extracted frames.

*number_of_frames*: The number of frames you want to extract from each video.

How to call:
```
python3 extract_frames.py -s "/home/legolas/BAUM_dataset" -d "/home/legolas/Extracted" -n 16
```
For help:
```
python3 extract_frames.py -h
```
2. **create_list.py [-h] [-s source_path] [-d destination_path]** :
This function creates a text file of all the frames extracted with their emotion.

*source_path*: The path of directory where all extracted frames are stored.

*destination_path*: The path of text file you are going to create.

How to call:
```
python3 create_list.py -s "/home/legolas/Extracted" -d "main.txt"
```
For help:
```
python3 create_list.py -h
```
