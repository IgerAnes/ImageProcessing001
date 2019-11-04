import tkinter as tk
import cv2
from tkinter import filedialog
# from PIL import Image, ImageTk
import numpy as np
from matplotlib import pyplot as plt

class ImageProcessingFunc:
    def __init__(self):
        self.OpenImage = []
        self.ColorConversionImage = []
        self.FlippingImage = []
        self.BlendedImage = []
        self.filename = ""
        self.numpy_horizontal = []
        self.trackbar_value = 0

    def ChooseAndLoadImage(self):
        self.OpenImage = []
        self.filename = filedialog.askopenfilename( initialdir = "C:/User/USER/Pictures",
        title = "Select Image",
        filetype = (("jpeg files","*.jpg"),("All file","*.*")))

        if(self.filename == ""):
            print("you have not choose the Image, Please choose again.")
        else:
            self.OpenImage = cv2.imread(self.filename)
            cv2.imshow("Image Window",self.OpenImage) #cv2.imshow(window title, the Image you want open)
            # cv2.waitKey(0) # wait until user press any button or key, do the thing below
            self.height, self.width, self.dimension = self.OpenImage.shape
            print("height: ", self.height)
            print("width: ", self.width)
            print("dimension:", self.dimension)

    def ColorConversion(self):
        self.ColorConversionImage = cv2.cvtColor(self.OpenImage, cv2.COLOR_BGR2RGB)
        self.numpy_horizontal = np.hstack((self.OpenImage,self.ColorConversionImage))
        cv2.imshow("Conversion Input & Result",self.numpy_horizontal)

    def ImageFlipping(self):
        self.numpy_horizontal = []
        self.FlippingImage = cv2.flip(self.OpenImage, 1) # image flip horizontal
        self.numpy_horizontal = np.hstack((self.OpenImage, self.FlippingImage))
        cv2.imshow("Flipping Input & Result", self.numpy_horizontal)

    def ImageBlended(self):

        def ImageRefresh(x): # why x?
            self.trackbar_value = cv2.getTrackbarPos("Weights: ", "Blended Image")
            
            if self.trackbar_value == 0:
                self.WeightsforBlended = self.trackbar_value
            else:
                self.WeightsforBlended = self.trackbar_value / 100

            self.BlendedImage = cv2.addWeighted(self.OpenImage, self.WeightsforBlended,
            self.FlippingImage, 1 - self.WeightsforBlended, 0.0)
            print(self.WeightsforBlended)
            cv2.imshow("Blended Image", self.BlendedImage)

        self.BlendedImage = self.OpenImage
        self.FlippingImage = cv2.flip(self.OpenImage, 1)
        cv2.namedWindow("Blended Image")
        cv2.createTrackbar("Weights: ", "Blended Image", 0, 100, ImageRefresh)

class AdaptiveThresholdFunc:
    def __init__(self):
        self.OpenImage = []
        self.MedianBlurImage = []
        self.GlobalThresholdImage = []
        self.LocalThresholdImage = []


    def ChooseAndLoadImage(self):
        self.OpenImage = []
        self.filename = filedialog.askopenfilename( initialdir = "C:/User/USER/Pictures",
        title = "Select Image",
        filetype = (("png files","*.png"),("All file","*.*")))

        if(self.filename == ""):
            print("you have not choose the Image, Please choose again.")
        else:
            self.OpenImage = cv2.imread(self.filename,0)

    def Global_Threshold(self):
        self.ChooseAndLoadImage()
        while(self.OpenImage ==[]):
            self.ChooseAndLoadImage()
        # self.MedianBlurImage = cv2.medianBlur(self.OpenImage,5) # median blurring method, use a 5x5 windows to finish it
        self.Global_ret, self.GlobalThresholdImage = cv2.threshold(self.OpenImage, 80, 255, 
                                                    cv2.THRESH_BINARY)
        cv2.imshow("Global Threshold Result",self.GlobalThresholdImage)

    def Local_Threshold(self):
        self.ChooseAndLoadImage()
        while(self.OpenImage ==[]):
            self.ChooseAndLoadImage()
        # self.MedianBlurImage = cv2.medianBlur(self.OpenImage,5)
        self.LocalThresholdImage = cv2.adaptiveThreshold(self.OpenImage, 255, 
                                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                            cv2.THRESH_BINARY, 19, -1)
        cv2.imshow("Local Threshold Result",self.LocalThresholdImage) 

IPF = ImageProcessingFunc()
ATF = AdaptiveThresholdFunc()

MainWindow = tk.Tk()
MainWindow.title("Graghic User Interface")
MainWindow.geometry("700x400")
# MainWindow.grid_rowconfigure(1, weight = 1)
# MainWindow.grid_columnconfigure(0, weight = 1)

Frame_P1 = tk.Frame(MainWindow)
Frame_P1.grid(column = 0, row = 0, sticky = "wn")

Frame_P2 = tk.Frame(MainWindow)
Frame_P2.grid(column = 1, row = 0, sticky = "wn")

Frame_P3 = tk.Frame(MainWindow) #If we put grid behind this case, it will set to MainWin not the frame we create
Frame_P3.grid(column = 2, row = 0, sticky = "wn")

Frame_P3_part1 = tk.Frame(Frame_P3)
Frame_P3_part1.grid(column = 0, row = 1)

Frame_P3_para = tk.Frame(Frame_P3_part1)
Frame_P3_para.grid(column = 0, row = 1)

Frame_P4 = tk.Frame(Frame_P2)
Frame_P4.grid(column = 0, row = 3)

# ------------------------label------------------------------------
Label_title01 = tk.Label(Frame_P1, text = "1. Image Processing")
Label_title01.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "W")

Label_title02 = tk.Label(Frame_P2, text = "2. Adaptive Threshold")
Label_title02.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "W")

Label_title03 = tk.Label(Frame_P3, text = "3. Image Transformation")
Label_title03.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "W")

Label_title04 = tk.Label(Frame_P4, text = "4. Convolution")
Label_title04.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "W")

Label_subtitle01 = tk.Label(Frame_P3_part1, text = "3.1 Rot, scale, Translate")
Label_subtitle01.grid(row = 0, column = 0, sticky = "W", padx = 15)

Label_subtitle02 = tk.Label(Frame_P3_para, text = "Parameters")
Label_subtitle02.grid(row = 0, column = 0, padx = 18, pady = 4, sticky = "E")

Label_Angeltitle = tk.Label(Frame_P3_para, text = "Angel:")
Label_Angeltitle.grid(row = 1, column = 0, padx = 2, pady = 2, sticky = "E")

Label_Scaletitle = tk.Label(Frame_P3_para, text = "Scale:")
Label_Scaletitle.grid(row = 2, column = 0, padx = 2, pady = 2, sticky = "E")

Label_Txtitle = tk.Label(Frame_P3_para, text = "Tx:")
Label_Txtitle.grid(row = 3, column = 0, padx = 2, pady = 2, sticky = "E")

Label_Tytitle = tk.Label(Frame_P3_para, text = "Ty:")
Label_Tytitle.grid(row = 4, column = 0, padx = 2, pady = 2, sticky = "E")

Label_AngelUnit = tk.Label(Frame_P3_para, text = "deg")
Label_AngelUnit.grid(row = 1, column = 2, padx = 5, pady = 5)

Label_TxUnit = tk.Label(Frame_P3_para, text = "pixel")
Label_TxUnit.grid(row = 3, column = 2, padx = 5, pady = 5)

Label_TyUnit = tk.Label(Frame_P3_para, text = "pixel")
Label_TyUnit.grid(row = 4, column = 2, padx = 5, pady = 5)

# ------------------------entry------------------------------------
Entry_AngelValue = tk.Entry(Frame_P3_para)
Entry_AngelValue.grid(row = 1, column = 1)

Entry_ScaleValue = tk.Entry(Frame_P3_para)
Entry_ScaleValue.grid(row = 2, column = 1)

Entry_TxValue = tk.Entry(Frame_P3_para)
Entry_TxValue.grid(row = 3, column = 1)

Entry_TyValue = tk.Entry(Frame_P3_para)
Entry_TyValue.grid(row = 4, column = 1)

# ------------------------button------------------------------------
# ------------------------button for frame1-------------------------
Button_LoadImage = tk.Button(Frame_P1, text = "1.1 Load Image", 
command = lambda:IPF.ChooseAndLoadImage(),
width = "20", height = "1")
Button_LoadImage.grid(row = 1, column = 0, padx = 8, pady = 8)

Button_ColorConversion = tk.Button(Frame_P1, text = "1.2 Color Conversion",
command = lambda:IPF.ColorConversion(),
width = "20", height = "1")
Button_ColorConversion.grid(row = 2, column = 0, padx = 8, pady = 8)

Button_ImageFlipping = tk.Button(Frame_P1, text = "1.3 Image Flipping",
command = lambda:IPF.ImageFlipping(),
width = "20", height = "1")
Button_ImageFlipping.grid(row = 3, column = 0, padx = 8, pady = 8)

Button_ImageBlended = tk.Button(Frame_P1, text = "1.4 Image Blended",
command = lambda:IPF.ImageBlended(),
width = "20", height = "1")
Button_ImageBlended.grid(row = 4, column = 0, padx = 8, pady = 8)

# ------------------------button for frame2-------------------------
Button_GlobalThreshold = tk.Button(Frame_P2, text = "2.1 Global Threshold",
command = lambda:ATF.Global_Threshold(),
width = "20", height = "1")
Button_GlobalThreshold.grid(row = 1, column = 0, padx = 8, pady = 8)

Button_LocalThreshold = tk.Button(Frame_P2, text = "2.2 Local Threshold",
command = lambda:ATF.Local_Threshold(),
width = "20", height = "1")
Button_LocalThreshold.grid(row = 2, column = 0, padx = 8, pady = 8)
# ------------------------button for frame3-------------------------
Button_Rotation_etc = tk.Button(Frame_P3_part1, text = "3.1 Rotation, scaling, translation",
width = "30", height = "1")
Button_Rotation_etc.grid(row = 2, column = 0, padx = 8, pady = 8)

Button_Perspective = tk.Button(Frame_P3, text = "3.2 Perspective Transform",
width = "25", height = "1")
Button_Perspective.grid(row = 2, column = 0, padx = 8, pady = 8)
# ------------------------button for frame4-------------------------
Button_Guassian = tk.Button(Frame_P4, text = "4.1 Gaussian",
width = "20", height = "1")
Button_Guassian.grid(row = 1, column = 0, padx = 8, pady = 8)

Button_SobelX = tk.Button(Frame_P4, text = "4.2 Sobel X",
width = "20", height = "1")
Button_SobelX.grid(row = 2, column = 0, padx = 8, pady = 8)

Button_SobelY = tk.Button(Frame_P4, text = "4.3 Sobel Y",
width = "20", height = "1")
Button_SobelY.grid(row = 3, column = 0, padx = 8, pady = 8)

Button_Magnitude = tk.Button(Frame_P4, text = "4.4 Magnitude",
width = "20", height = "1")
Button_Magnitude.grid(row = 4, column = 0, padx = 8, pady = 8)

if __name__ == '__main__':
    MainWindow.mainloop()
