## Dependencies
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
%matplotlib inline
import math

# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML

from FindLaneLine import *



## Global parameters

# Gaussian blur
ksize = 5

# Canny edges
lt = 50
ht = 150

# Hough transform and Draw Lines
rho = 1
theta = np.pi/180
threshold = 10
min_line_len = 1
max_line_gap = 5

# Lane line
linecol = [255,0,0] 
linethick = 10



## loop all images in the directory and save to output directory
outpath = ("test_images_output/")
if not os.path.isdir(outpath):
    os.makedirs(outpath)
    
for filename in os.listdir("test_images/"):
    if filename.endswith(".jpg"):
        im = mpimg.imread(os.path.join("test_images/",filename))
        f = PicLanePipeline(im)
        #cv2.imwrite(os.path.join(outpath, "outlines_"+ filename), f)
        # above the red and blue colors are inverted
        cv2.imwrite(os.path.join(outpath, "outlines_"+ filename), 
                    cv2.cvtColor(f, cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        #plt.figure()
        #plt.imshow(f)


## Apply the pipeline to videos
outpath = ("test_videos_output/")
if not os.path.isdir(outpath): os.makedirs(outpath)
    
clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
clip2 = VideoFileClip("test_videos/solidYellowLeft.mp4")

outclip1 = clip1.fl_image(process_image) 
fulloutpath1 = os.path.join(outpath, "out_solidWhiteRight.mp4")
%time outclip1.write_videofile(fulloutpath1, audio=False)

outclip2 = clip2.fl_image(process_image) 
fulloutpath2 = os.path.join(outpath, "out_solidYellowLeft.mp4")
%time outclip2.write_videofile(fulloutpath2, audio=False)