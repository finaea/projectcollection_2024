import cv2

videoname = input("Enter input video name (.mp4): ") + ".mp4"
outputname = "output.mp4"
print("Please wait while the program is processing the video....")

# read the video, watermarks and xml file
vid = cv2.VideoCapture(videoname)
talk = cv2.VideoCapture('sample.mp4')
watermark1 = cv2.imread('watermark1.png')
watermark2 = cv2.imread('watermark2.png')
face_cascade = cv2.CascadeClassifier("face_detector.xml")

# acquiring the fps, height, width and total frames
fps = int(vid.get(cv2.CAP_PROP_FPS))
width = int(vid.get(3))
height = int(vid.get(4))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

total_no_frames_office = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
total_no_frames_talk = int(talk.get(cv2.CAP_PROP_FRAME_COUNT))

#resize the watermark according to video and create mask
watermark1 = cv2.resize(watermark1, (width, height))
watermark2 = cv2.resize(watermark2, (width, height))
mask1 = cv2.cvtColor(watermark1, cv2.COLOR_BGR2GRAY)
mask2 = cv2.cvtColor(watermark2, cv2.COLOR_BGR2GRAY)

# to write the file
out = cv2.VideoWriter(outputname, fourcc, fps, (width,height))

# declare variables
delay = 60
frame_list = [None] * delay
counter = 0
initial_delay = 0
loop = 1
using_watermark = 1

#run through all the main frames
for frame_count in range(0, int(total_no_frames_office)) :
    
    #capture frame-by-frame
    success, vid_frame = vid.read()
    
    #detect faces
    faces = face_cascade.detectMultiScale(vid_frame, 1.3, 5)
    
    #allocate the faces onto the list
    frame_list [counter] = faces
    
    #increment the delay if it has not reaches the limit yet
    if (initial_delay < delay):
        initial_delay = initial_delay + 1
    
    #blur the faces based on the last 60 frames
    for counter2 in range (0, initial_delay) :
        #blur the faces
        for (x, y, w, h) in frame_list[counter2]:
            edit_frame = vid_frame[y:y+h, x:x+w, :]
            out_frame = cv2.blur(edit_frame, (39,39), cv2.BORDER_REFLECT_101)
            vid_frame[y:y+h, x:x+w] = out_frame
    
    #increment the counter to allocate another faces
    counter = counter + 1
    
    #reset the counter to start allocation from the beginning
    if (counter == delay):
        counter = 0
        
    #the part for overlaying the talking video
    if (frame_count < total_no_frames_talk) :
        success, talk_frame = talk.read()
        # resize the talking video
        resizedTalk = cv2.resize(talk_frame, (250,150))
        
        # add border to the resized video
        borderedTalk = cv2.copyMakeBorder(resizedTalk,10,10,10,10,cv2.BORDER_CONSTANT,value=[0,0,0])
        
        # overlay the talking video on the top left corner of street video
        vid_frame[0:170, 0:270] = borderedTalk 
    
    #change watermark every 3 seconds or 90 frames
    if (loop % 90 == 0 and using_watermark == 1) :
        using_watermark = 2
    elif (loop % 90 == 0 and using_watermark == 2) :
        using_watermark = 1

    #apply watermark
    if (using_watermark == 1) :
        vid_frame[mask1 > 3] = watermark1[mask1 > 3]
    elif (using_watermark == 2) :
        vid_frame[mask2 > 3] = watermark2[mask2 > 3]
    
    loop = loop + 1
    
    # save the frame
    out.write(vid_frame)
    
print("Process completed. Output.mp4 has been generated!")