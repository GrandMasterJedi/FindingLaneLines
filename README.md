# **Finding Lane Lines on the Road** 

This repository contains the program pipeline to identify lane lines from pictures or videos taken from a car-mounted camera. The identified lines on the road would serve as a constant reference for where to steer the vehicle.

This project is my solution to assignment (1.1) of the Udacity Self Driving Nanodegree. I detect lines using Python and OpenCV.

 
---
## Examples
The Jupitter Notebook FindLaneLines.ipynb contains the pipeline as a function and also the code to test on the test images and test videos. To try the pipeline download the notebook, test_images and test_videos directories and run the code on the notebook. 

[//]: # (Image References)
[image1]: ./Example/0_OriginalPic.jpg "Picture1"
[image2]: ./Example/1_WhiteYellowMask.jpg "Color Mask"
[image3]: ./Example/2_GrayScale.jpg "Gray Scale"
[image4]: ./Example/3_GaussianBlur.jpg "Gaussian Smoothing"
[image5]: ./Example/4_CannyEdges.jpg "Canny Edges"
[image6]: ./Example/5_RegionInterest.jpg "Region of Interest"
[image7]: ./Example/6_IdentifiedLines.jpg "Hough Lines"
[image8]: ./Example/7_FinalWeighted.jpg "Final Lane Lines"

The program identifies the lane lines as highlighted in red color as in the picture below
![alt text][image8]


The directory test_video_output contains the result of the program applied to three clips. 


---

## Reflection

### 1. Program Pipeline

Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

The pipeline consists of the 7 steps below.

* 1) I build a color mask that filter out white or yellow colors, because the lane lines could be either one of this two colors. The white, _RGBw=[255, 255, 255]_ and the yellow, _RGBy=[255, 255, 0]_, may have different color gradient. Therefore, all colors withing the mask
_RGB = [([200, 200, 200], [255, 255, 255])]_ or _RGB = [([200,200,0], [255,255,200])]_, are selected. 
![alt text][image2]

* 2) I convert to gray scale with OpenCV.
![alt text][image3]

* 3) I blur the gray image with OpenCV. This remove noise from the image and helps in finding edges.
![alt text][image4]

* 4) I apply the OpenCV Canny Edges detection.
![alt text][image5]

* 5) I select a region of interest. I consider only the detected edges within this region. The region has a trapezoid shape, with the two upper vertices slightly below the mid vertical coordinate (below means higher y coordinate, as the y axis is inverted in the image) and horizontal coordinates symmetric around te mix horizontal coordinate, and the two lower vertices touching the bottow line of the image and, horizontally, indented with respect to the bottom corners of the image.
![alt text][image6]

* 6) I apply the Hough line (OpenCV) function that yields all possible lines given by the canny edges. From those lines, the `DrawLane()` function 
filter out all those lines that are reasonably not lane lines, then it fits two regression lines, one for the left lane line and one for the right lane line. 
In more detail, the filter applied are, respectively, slope of the lines and position of the lines. The slope is selected on between |0.5, 2|, with the sign opposite for the left and right lines, and the position is selected to be either on the lower right or lower left quadrant. On those lines that are selected with the filter, two regression lines are fit on the lines endpoints for respectively left lines and right lines. The two regression lines, with top y coordinates slightly higher than the image center y coordinate and bottom y coordinates equal to the image bottom y coordinate, represent the lane lines.
![alt text][image7]

* 7) Change the color of the identified lane lines to translucent and and draw them on top of the original picture





### 2. Potential shortcomings with the pipeline
```
code section
```

The present program pipeline have shortcoming with road that contain many signs

Color filter is set to relatively wide range, including some colors that are not much yellow. However some line 

Both the region filter 5) and the lines filter in 6) works reasonably well for a smooth driving, with camera mounted in the middle of the car and lane line that have a intermediate weight. If the camera is not mounted in the middle top of the car, or if the lane is very large While turning 
When steering One problem is the canny edge 

Filter hough lines based on the position before regressing a line through all the extreme points of the line. The position is set to mid vertical point plus 10%


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to apply color filter after the grayscaling or another color transformation





---

## Known Problems 
On Windows machine repeating `clip = VideoFileClip("\...")`  and `clip1 = clip.fl_image(process_image)` may result in error or the OS not able to open the video. Closing both clips as below can resove 
```
clip.reader.close()
clip.audio.reader.close_proc()  
clip1.reader.close()
clip1.audio.reader.close_proc()  
``` 

---
## Resources
* Udacity Self-Driving Car [Nanodegree](https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013) 
* Udacity project assignment and template on [GitHub](https://github.com/udacity/CarND-LaneLines-P1)
* Project [rubric](https://review.udacity.com/#!/rubrics/322/view)
---
