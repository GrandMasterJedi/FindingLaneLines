# **Finding Lane Lines on the Road** 

This repository contains the program pipeline to identify lane lines from pictures or videos taken from a car-mounted camera. The identified lines on the road would serve as a constant reference for where to steer the vehicle.

This project is my solution to assignment (1.1) of the Udacity Self Driving Nanodegree. I detect lines using Python and OpenCV.

 
---
## Examples
The Jupitter Notebook FindLaneLines.ipynb contains the pipeline as a function and also the code to test on the test images and test videos
The directory test_video_output contains the result of the program pipeline applied to three clips.

[//]: # (Image References)
[image1]: ./Example/0_OriginalPic.jpg "Picture1"
[image2]: ./Example/1_WhiteYellowMask.jpg "Color Mask"
[image3]: ./Example/2_GrayScale.jpg "Gray Scale"
[image4]: ./Example/3_GaussianBlur.jpg "Gaussian Smoothing"
[image5]: ./Example/4_CannyEdges.jpg "Canny Edges"
[image6]: ./Example/5_RegionInterest.jpg "Region of Interest"
[image7]: ./Example/6_IdentifiedLines.jpg "Hough Lines"
[image8]: ./Example/7_FinalWeighted.jpg "Final Lane Lines"

---

## Reflection

We encourage using images in your writeup to demonstrate how your pipeline works.  
All that said, please be concise!  We're not looking for you to write a book here: just a brief description.

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I .... 
In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...
If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]

### 2. Identify potential shortcomings with your current pipeline
```
code section
```


The present program pipeline have shortcoming with road that contain many signs
One problem is the canny edge 


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


Filter hough lines based on the position before regressing a line through all the extreme points of the line. The position is set to mid vertical point plus 10%


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...


---
## Resources
* [Udacity Self-Driving Car Nanodegree](https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013) 
* Udacity [project assignment and template](https://github.com/udacity/CarND-LaneLines-P1)
* Project [rubric](https://review.udacity.com/#!/rubrics/322/view)
---
