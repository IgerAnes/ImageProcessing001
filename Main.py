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
MainWindow.geometry("600x600")

Label_title01 = tk.Label(MainWindow, text = "1. Image Processing")
Label_title01.grid(row = 0, column = 0, padx = 10, pady = 5)

Label_title02 = tk.Label(MainWindow, text = "2. Adaptive Threshold")
Label_title02.grid(row = 0, column = 1, padx = 10, pady = 5)

Label_title03 = tk.Label(MainWindow, text = "3. Image Transformation")
Label_title03.grid(row = 0, column = 2, padx = 10, pady = 5)

Label_subtitle01 = tk.Label(MainWindow, text = "3.1 Rot, scale, Translate")
Label_subtitle01.grid(row = 1, column = 2)

Label_subtitle02 = tk.Label(MainWindow, text = "Parameters")
Label_subtitle02.grid(row = 2, column = 2, padx = 20, pady = 4)

Label_Angeltitle = tk.Label(MainWindow, text = "Angel:")
Label_Angeltitle.grid(row = 3, column = 3, padx = 5, pady = 2)

Label_Scaletitle = tk.Label(MainWindow, text = "Scale:")
Label_Scaletitle.grid(row = 4, column = 3, padx = 5, pady = 2)

Label_Txtitle = tk.Label(MainWindow, text = "Tx:")
Label_Txtitle.grid(row = 5, column = 3, padx = 5, pady = 2)

Label_Tytitle = tk.Label(MainWindow, text = "Ty:")
Label_Tytitle.grid(row = 6, column = 3, padx = 5, pady = 2)

Label_AngelUnit = tk.Label(MainWindow, text = "deg")
Label_AngelUnit.grid(row = 3, column = 5, padx = 10, pady = 5)

Label_TxUnit = tk.Label(MainWindow, text = "pixel")
Label_TxUnit.grid(row = 5, column = 5, padx = 10, pady = 5)

Label_TyUnit = tk.Label(MainWindow, text = "pixel")
Label_TyUnit.grid(row = 6, column = 5, padx = 10, pady = 5)

Entry_AngelValue = tk.Entry(MainWindow)
Entry_AngelValue.grid(row = 3, column = 4)

Entry_ScaleValue = tk.Entry(MainWindow)
Entry_ScaleValue.grid(row = 4, column = 4)

Entry_TxValue = tk.Entry(MainWindow)
Entry_TxValue.grid(row = 5, column = 4)

Entry_TyValue = tk.Entry(MainWindow)
Entry_TyValue.grid(row = 6, column = 4)

Button_LoadImage = tk.Button(MainWindow, text = "1.1 Load Image", 
command = lambda:IPF.ChooseAndLoadImage(),
width = "20", height = "1")
Button_LoadImage.grid(row = 1, column = 0, padx = 8, pady = 8)

Button_ColorConversion = tk.Button(MainWindow, text = "1.2 Color Conversion",
command = lambda:IPF.ColorConversion(),
width = "20", height = "1")
Button_ColorConversion.grid(row = 2, column = 0, padx = 8, pady = 8)

Button_ImageFlipping = tk.Button(MainWindow, text = "1.3 Image Flipping",
command = lambda:IPF.ImageFlipping(),
width = "20", height = "1")
Button_ImageFlipping.grid(row = 3, column = 0, padx = 8, pady = 8)

Button_ImageBlended = tk.Button(MainWindow, text = "1.4 Image Blended",
command = lambda:IPF.ImageBlended(),
width = "20", height = "1")
Button_ImageBlended.grid(row = 4, column = 0, padx = 8, pady = 8)

Button_GlobalThreshold = tk.Button(MainWindow, text = "2.1 Global Threshold",
command = lambda:ATF.Global_Threshold(),
width = "20", height = "1")
Button_GlobalThreshold.grid(row = 1, column = 1, padx = 8, pady = 8)

Button_LocalThreshold = tk.Button(MainWindow, text = "2.2 Local Threshold",
command = lambda:ATF.Local_Threshold(),
width = "20", height = "1")
Button_LocalThreshold.grid(row = 2, column = 1, padx = 8, pady = 8)

if __name__ == '__main__':
    MainWindow.mainloop()
