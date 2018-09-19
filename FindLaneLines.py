## Draw line Function

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap, sanity = 1):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    
    lineImg = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    vertex = drawLane(lineImg, lines, linecol=[255,0,0], linethick = 10)
    
    if sanity==1:
        lineImg = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        sanityFilter(lineImg, vertex, linecol, linethick)
    
    return lineImg

def drawLane(img, hlines, linecol=[255,0,0], linethick = 10):
    """
    NOTE: Extrapolate the two lines (left and right) of the lane and draw on top
    of img. 
    The starting point is the  Hough lines, that can be obtained from a 
    grayscale img2.
    hlines = cv2.HoughLinesP(img2, rho, theta, threshold, 
                        np.array([]), min_line_len, max_line_gap)
    The function apply filters to select those Hough lines based on
    1. The slope of the lines, and 
    2. The position of the lines with respect to four quadrandts. 
    Then, it fits a linear regression line. The lane lines is the linear 
    regression line starting from points around the middle of the picture and 
    ending on the bottom of the picture
    """
    
    hwd = img.shape
    
    # parameters for min and max slope of the two (left and right) lane lines
    # From the picture the lane line slope should be around 1.5
    lowslope = 0.5
    highslope = 2
    
    rightslope = []
    leftslope = []
    rightline1 = []
    leftline1 = []

    # Filter based on slope: if the slope is negative the line is on the left side
    # as the picture has y order inverted
    for line in hlines:
        x1, y1, x2, y2  = line[0]
        if x2!=x1:
            slope = ((y2-y1)/(x2-x1))
        else:
            slope = 9999
            
        if (slope > lowslope and slope < highslope):
            rightslope.append(slope)
            rightline1.append(line)
        elif (slope < -lowslope and slope > -highslope):
            leftslope.append(slope)
            leftline1.append(line)       
            
    # Filter based on position: Check for position of right and left line with respect to middle point
    hmidpoint = hwd[1]/2
    vmidpoint = hwd[0]/2 + 0.1*hwd[0]
    rightline2 = []
    leftline2 = []
    # note: (x1, y1) is the upper end of the line an (x2, y2) the lower end
    for line in leftline1:
        x1, y1, x2, y2  = line[0]
        if (x1 < hmidpoint and y1 > vmidpoint):
            leftline2.append(line)
    for line in rightline1:
        x1, y1, x2, y2  = line[0]
        if (x1 > hmidpoint and y1 > vmidpoint):
            rightline2.append(line)
            
    # Fit a regression line through all points for respectively
    # left and right line to get intercept ans slope of the two lane lines
    xleft = []
    yleft = []
    xright = []
    yright = []

    for line in leftline2:
        x1, y1, x2, y2  = line[0]
        xleft.append(x1)
        xleft.append(x2)
        yleft.append(y1)
        yleft.append(y2)
    
    for line in rightline2:
        x1, y1, x2, y2  = line[0]
        xright.append(x1)
        xright.append(x2)
        yright.append(y1)
        yright.append(y2)
        
    # If any of the vectors xleft, yleft, xright, yright is empty 
    # the function will return an error. 
    # The following is a hack. I draw a roughly possible symmetric line 
    # [see comments in reflections]
    if (len(xleft)<2 and len(xright)<2): 
        xleft = [hwd[1]/2 - 0.15*hwd[1], 0.2*hwd[1]]
        xright = [hwd[1]/2 + 0.15*hwd[1], 0.8*hwd[1]]
        yleft = [hwd[0]/2 + 0.05*hwd[0], hwd[0]]
        yright = [hwd[0]/2 + 0.05*hwd[0], hwd[0]]
    elif (len(xleft)<2 and len(xright)>=2): 
        xleft = [hwd[1] - xright[i] for i in range(len(xright))]
        yleft = yright
    elif (len(xleft)>=2 and len(xright)<2): 
        xright = [hwd[1] - xleft[i] for i in range(len(xleft))]
        yright = yleft
   
    # fit y = a + bx
    b_l, a_l = np.polyfit(xleft, yleft, 1) 
    b_r, a_r = np.polyfit(xright, yright, 1)
       
    # find two end points to draw line: x = (y- a)/b
    # bottom left coordinates
    y_bl = int(hwd[0]) # set to border of the picture 
    x_bl = int((y_bl - a_l) / b_l)

    # upper left coordinates
    y_ul = int(hwd[0]/2 + 0.1*hwd[0])  # slightly below middle
    x_ul = int((y_ul - a_l) / b_l)

    # bottom right coordinates
    y_br = int(hwd[0]) # set to border of the picture 
    x_br = int((y_br - a_r) / b_r)

    # upper right coordinates
    y_ur = int(hwd[0]/2 + 0.1*hwd[0])  # slightly below middle
    x_ur = int((y_ur - a_r) / b_r)

    # Draw lines on top of original img
    cv2.line(img, (x_ul,y_ul), (x_bl,y_bl), linecol, linethick)
    cv2.line(img, (x_ur,y_ur), (x_br,y_br), linecol, linethick)    
    
    #
    lanevertex = [[x_ul, y_ul], [x_bl, y_bl],[x_ur, y_ur],[x_br, y_br]]
    
    return lanevertex
    
    
def sanityFilter(img, vx, linecol, linethick):
    """
    While steering, it is possible that lines of other lanes are inside the region of interest. 
    The algorithm will average out different lane lines. This filter, filter out the identified lines that are unlikely and
    apply an approximation
    vx contains the end points of the two lines: 
    vx = [[x_ul, y_ul], [x_bl, y_bl],[x_ur, y_ur],[x_br, y_br]]
    """
    hwd = img.shape

    if (vx[1][0] < 0 and vx[3][0]< hwd[1]): #bottom left over frame edge
        vx[1][0] = hwd[1] - vx[3][0]
    elif (vx[1][0] > 0 and vx[3][0]> hwd[1]): # bottom right over frame edge
        vx [3][0] = hwd[1] - vx[1][0]
    elif (vx[1][0] > 0 and vx[3][0]> hwd[1]): # both bottom right and left ends over frame edges
        vx[1][0], vx [3][0] = 0.1*hwd[1], 0.9*hwd[1]
        
        
    if (vx[0][0] > 1.1*hwd[1]/2):
        vx[0][0] = hwd[1]/2
    elif (vx[2][0] < 0.9*hwd[1]/2):
        vx[2][0] = hwd[1]/2
        
       
    # Draw lines on top of original img
    cv2.line(img, (int(vx[0][0]),int(vx[0][1])), (int(vx[1][0]),int(vx[1][1])), linecol, linethick)
    cv2.line(img, (int(vx[2][0]),int(vx[2][1])), (int(vx[3][0]),int(vx[3][1])), linecol, linethick)    
        
    return vx


## Help Functions
def whiteYellowMask(image):
    """
    Apply either a white or yellow mask
    white = [255,255,255]
    """
    whitebound = [([200, 200, 200], [255, 255, 255])]
    yellowbound = [([200,200,0], [255,255,200])]

    for (lower, upper) in whitebound:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        mask = cv2.inRange(image, lower, upper)
        output1 = cv2.bitwise_and(image, image, mask = mask)

    for (lower, upper) in yellowbound:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        mask = cv2.inRange(image, lower, upper)
        output2 = cv2.bitwise_and(image, image, mask = mask)

    imout = output1+output2

    return imout

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.  
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:  initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)

## Program pipeline
def PicLanePipeline(image, sanity = 0):
    
    # 1 Color Mask
    i1 = whiteYellowMask(image)
    
    # 2 Grayscaling
    i2 = grayscale(i1)

    # 3 Gaussian blur
    i3 = gaussian_blur(i2, ksize)

    # 4 Canny edges
    i4 = canny(i3, lt, ht)

    # 5 select region of interst (to avoid multiple lane problem, also cut out lines that are not lane lines)
    hwd = image.shape
    bl = [0.05*hwd[1], hwd[0]]
    br = [0.95*hwd[1], hwd[0]]
    apex = [hwd[1]/2, hwd[0]/2]
    ul = [hwd[1]/2 - 0.05*hwd[1], 0.95*hwd[0]/2]
    ur = [hwd[1]/2 + 0.05*hwd[1], 0.95*hwd[0]/2]
    vertices = np.array([[bl, br, ur, ul]] , dtype=np.int32)
    i5 = region_of_interest(i4, vertices)

    # 6 Draw lines
    i6 = hough_lines(i5, rho, theta, threshold, min_line_len, max_line_gap)
    

    # 7 Final Weighted color image
    ifin = weighted_img(i6, image)
    
    return ifin

def process_image(image):
    """
    NOTE: The output you return should be a color image (3 channel) 
    for processing video below
    """
    result = PicLanePipeline(image)

    return result