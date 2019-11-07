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

class ImageTransformationFunc:
    def __init__(self):
        self.OpenImage = []
        self.RotateImage = []
        self.TranslateImage = []
        self.PerspectiveImage = []

    def ChooseAndLoadImage(self):
        self.OpenImage = []
        self.filename = filedialog.askopenfilename( initialdir = "C:/User/USER/Pictures",
        title = "Select Image",
        filetype = (("png files","*.png"),("All file","*.*")))

        if(self.filename == ""):
            print("you have not choose the Image, Please choose again.")
        else:
            self.OpenImage = cv2.imread(self.filename)
            self.OriginImage = cv2.imread(self.filename)

    def Rotation_Scaling_Translation(self):
        # ------------GetValue---------------
        self.angel_value = int(Entry_AngelValue.get())
        self.scale_value = float(Entry_ScaleValue.get())
        self.Tx_value = int(Entry_TxValue.get())
        self.Ty_value = int(Entry_TyValue.get())
        # -----------ImageLoad---------------
        self.ChooseAndLoadImage()
        # ------------rotate-----------------
        self.RotateMatrix = cv2.getRotationMatrix2D((130,125), self.angel_value, self.scale_value)
        self.RotateImage = cv2.warpAffine(self.OpenImage, self.RotateMatrix, 
                                            (self.OpenImage.shape[1],self.OpenImage.shape[0]))
        cv2.imshow("Translate Result",self.RotateImage)
        # -----------translate---------------
        self.Matrix = np.float32([[1, 0, self.Tx_value], [0, 1, self.Ty_value]])
        self.TranslateImage = cv2.warpAffine(self.RotateImage, self.Matrix,
                                                 (self.RotateImage.shape[1],self.RotateImage.shape[0]))
        cv2.imshow("Translate Result", self.TranslateImage)

    def Perspective_Transformation(self):
        # -----------Initialize--------------
        self.PositionXYList = []
        # ------------LoadImage--------------
        self.ChooseAndLoadImage()
        # -----------buttonClick-------------
        def click_event(event, x, y, flags, param):
            if (len(self.PositionXYList) == 4):
                cv2.destroyAllWindows()
                self.pts1 = np.float32([self.PositionXYList[0], self.PositionXYList[1],
                                self.PositionXYList[2], self.PositionXYList[3]])
                self.pts2 = np.float32([[0,0], [490,0], [490,490], [0,490]]) # resize the display image 490 x 490
                self.PTMatrix = cv2.getPerspectiveTransform(self.pts1, self.pts2)
                self.PerspectiveImage = cv2.warpPerspective(self.OriginImage, self.PTMatrix, (490, 490))
                cv2.imshow("Perspective transformation Result", self.PerspectiveImage)

            elif (event == cv2.EVENT_LBUTTONDOWN):
                self.PositionXYList.append([x, y]) 
                # list.append() will return None so if you use list = list.append will become notype
                cv2.circle(self.OpenImage, (x, y), 5, (0, 0, 255), -1) #circle(image, pos. , radius, color, line_size) 
                cv2.imshow("Image", self.OpenImage)
        # ----perspective transformation-----
        cv2.imshow("Image",self.OpenImage)
        cv2.setMouseCallback("Image",click_event)

class ConvolutionFunc:
    def __init__(self):
        self.OpenImage = []
        self.GaussianImage = []
        self.SobelXImage = []
        self.SobelYImage = []
        self.MagnitudeImage = []

    def ChooseAndLoadImage(self):
        self.OpenImage = []
        self.filename = filedialog.askopenfilename( initialdir = "C:/User/USER/Pictures",
        title = "Select Image",
        filetype = (("jpeg files","*.jpg"),("All file","*.*")))

        if(self.filename == ""):
            print("you have not choose the Image, Please choose again.")
        else:
            self.OpenImage = cv2.imread(self.filename)
            self.OpenImage = cv2.cvtColor(self.OpenImage, cv2.COLOR_RGB2GRAY) # default data type is uint8 0 ~ 255
            cv2.imshow("Open Image", self.OpenImage)
    
    def Gaussian_Filter(self):
        # ---------------Load Image------------------------------
        self.ChooseAndLoadImage()
        # ---------------create a Gaussian Kernal----------------
        self.x, self.y = np.mgrid[-1:2, -1:2]
        self.gaussian_kernal = np.exp(-(self.x**2 + self.y**2))
        self.gaussian_kernal = self.gaussian_kernal / self.gaussian_kernal.sum()
        self.gaussian_kernal = np.flipud(np.fliplr(self.gaussian_kernal))
        # ---------------start to use kernal for convolution------
        # self.kernal = np.flipud(np.fliplr(self.gaussian_kernal))
        # self.OutputImage = np.zeros_like(self.OpenImage)
        # self.ImagePadded = np.zeros((self.OpenImage.shape[0] + 2, self.OpenImage.shape[1] + 2))
        # self.ImagePadded[1:-1 , 1:-1] = self.OpenImage
        # for i in range(self.OpenImage.shape[1]):
        #     for j in range(self.OpenImage.shape[0]):
        #         self.OutputImage[j,i] = (self.kernal*self.ImagePadded[ j:j+3 , i:i+3 ]).sum()
        self.GaussianImage = self.Convolution(self.OpenImage, self.gaussian_kernal)
        cv2.imshow("Gaussian Result", self.GaussianImage)

    def Convolution(self, image, kernal):      
        kernal_row, kernal_col = kernal.shape
        pad_height = int((kernal_row - 1)/2)
        pad_width = int((kernal_col - 1)/2)

        OutputImage = np.zeros_like(image, dtype = np.uint8)
        ImagePadded = np.zeros((image.shape[0] + (2 * pad_height),
                                 image.shape[1] + (2 * pad_width)))
        ImagePadded[pad_height:ImagePadded.shape[0] - pad_height,
                     pad_width:ImagePadded.shape[1] - pad_width] = image
        # ImagePadded[pad_height:-1,
        #              pad_width:-1] = image
        kernal_sum = np.sum(kernal)
        if(kernal_sum == 0):
            for row in range(image.shape[0]):
                for col in range(image.shape[1]):
                    OutputImage[row, col] = np.abs(np.sum(kernal* ImagePadded[ row:row + kernal_row , 
                                                    col:col + kernal_col ])) / 2
        else:
            for row in range(image.shape[0]):
                for col in range(image.shape[1]):
                    OutputImage[row, col] = np.abs(np.sum(kernal* ImagePadded[ row:row + kernal_row , 
                                                    col:col + kernal_col ])) / kernal_sum
        return OutputImage

    def Sobel_X(self):
        # -------------Continue Image above---------------------
        # -------------set vertical filter mask-----------------
        self.verticalMatrix = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        self.SobelXImage = self.Convolution(self.GaussianImage, self.verticalMatrix)
        cv2.imshow("Sobel X Result", self.SobelXImage)

    def Sobel_Y(self):
        # -------------Continue Image above---------------------
        # -------------set horizontal filter mask-----------------
        self.horizontalMatrix = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        self.SobelYImage = self.Convolution(self.GaussianImage, self.horizontalMatrix)
        cv2.imshow("Sobel Y Result", self.SobelYImage)

    def Magnitude(self):
        # -------------Continue Image above---------------------
        # -------------start Magnitude process-----------------
        self.MagnitudeImage = np.sqrt(np.square(self.SobelXImage /8) +
                                        np.square(self.SobelYImage /8))
        self.MagnitudeImage *= 255.0 / self.MagnitudeImage.max()
        print("aaaa")
        print("before:", self.MagnitudeImage)
        self.MagnitudeImage = np.uint8(self.MagnitudeImage)
        print("after:", self.MagnitudeImage)
        cv2.imshow("Magnitude Result", self.MagnitudeImage)



IPF = ImageProcessingFunc()
ATF = AdaptiveThresholdFunc()
ITF = ImageTransformationFunc()
CF = ConvolutionFunc()

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
command = lambda:ITF.Rotation_Scaling_Translation(),
width = "30", height = "1")
Button_Rotation_etc.grid(row = 2, column = 0, padx = 8, pady = 8)

Button_Perspective = tk.Button(Frame_P3, text = "3.2 Perspective Transform",
command = lambda:ITF.Perspective_Transformation(),
width = "25", height = "1")
Button_Perspective.grid(row = 2, column = 0, padx = 8, pady = 8)
# ------------------------button for frame4-------------------------
Button_Guassian = tk.Button(Frame_P4, text = "4.1 Gaussian",
command = lambda:CF.Gaussian_Filter(),
width = "20", height = "1")
Button_Guassian.grid(row = 1, column = 0, padx = 8, pady = 8)

Button_SobelX = tk.Button(Frame_P4, text = "4.2 Sobel X",
command = lambda:CF.Sobel_X(),
width = "20", height = "1")
Button_SobelX.grid(row = 2, column = 0, padx = 8, pady = 8)

Button_SobelY = tk.Button(Frame_P4, text = "4.3 Sobel Y",
command = lambda:CF.Sobel_Y(),
width = "20", height = "1")
Button_SobelY.grid(row = 3, column = 0, padx = 8, pady = 8)

Button_Magnitude = tk.Button(Frame_P4, text = "4.4 Magnitude",
command = lambda:CF.Magnitude(),
width = "20", height = "1")
Button_Magnitude.grid(row = 4, column = 0, padx = 8, pady = 8)

if __name__ == '__main__':
    MainWindow.mainloop()
