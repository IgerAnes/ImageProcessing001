import tkinter as tk
import cv2
from tkinter import filedialog
# from PIL import Image, ImageTk
import numpy as np

class ImageProcessingFunc:
    def __init__(self):
        self.OpenImage = []
        self.ColorConversionImage = []
        self.FlippingImage = []
        self.BlendedImage = []
        self.filename = ""
        self.numpy_horizontal = []

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

        def ImageRefresh(self):
            self.TrackbarValue = cv2.getTrackbarPos("Weights: ", "Blended Image")

            if self.TrackbarValue == 0:
                self.WeightsforBlended = self.TrackbarValue
            else:
                self.WeightsforBlended = self.TrackbarValue / 100

            self.BlendedImage = cv2.addWeighted(self.OpenImage, self.WeightsforBlended,
            self.FlippingImage, 1 - self.WeightsforBlended, 0.0)
            print(self.WeightsforBlended)
            cv2.imshow("Blended Image", self.BlendedImage)

        self.BlendedImage = self.OpenImage
        self.FlippingImage = cv2.flip(self.OpenImage, 1)
        cv2.namedWindow("Blended Image")
        cv2.createTrackbar("Weights: ", "Blended Image", 0, 100, ImageRefresh)

IPF = ImageProcessingFunc()

MainWindow = tk.Tk()
MainWindow.title("Graghic User Interface")
MainWindow.geometry("600x600")

Label_title01 = tk.Label(MainWindow, text = "1. Image Processing")
Label_title01.grid(row = 0, column = 0, padx = 10, pady = 5)

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

if __name__ == '__main__':
    MainWindow.mainloop()
