'''
Handwritten Digit Recognition Using CNN
CNN(Convolution Neutral Network)

Description :
            Just write a digit between 0 - 9 on the console using hardware(MOUSE) and see
            Software predict digit for you.

Library :
    tensorflow : For dataSet and model.
    OpenCv : Work with Image
    tkinter : GUI Interface.

Package Installer : Use Requirement.txt
'''

import cv2
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import tkinter as tk
'''import win32gui'''
import PIL
from PIL import ImageGrab , ImageTk ,Image
import pyscreenshot
import io
from keras.models import load_model
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

# Load Model
model = load_model('./res/mnist.h5')


'''
Function for drawing digits on canvas on the motion of mouse event.
classify_btn will automatically enabled by state=NORMAL.
'''
def draw_rect(event):
    x , y = event.x,event.y
    #print(f"X : {x} , Y : {y}")
    r = 8
    canvas.create_oval(x-r,y-r,x+r,y+r,fill="black")
    classify_btn.configure(state=NORMAL)


# Function for exit.
def destroy_canvas():
    root.destroy()

# Fucntion clearing canvas. Event of Clear Button on TK window.
def clear_canvas():
    classify_btn.configure(state=DISABLED)
    canvas.delete("all")
    try:
        #Once the window got clear All the Information Predicted in past will be cleard by below destroy() function
        lab1.destroy()
    except:
        pass


'''
Function for capturing Image from canvas of handwritten digit 
and then it will send image to PRED_DIGIT() Function for prediction of digit.
'''
def classify_handwritting():
    global lab1,lab2
    im = ImageGrab.grab(bbox=(921,130,1400,510))
    im.save('./res/nitzz.png','PNG')
    digit=pred_digit(im)
    #im.show()
    #digit, acc = pred_digit(im)
    lab1 = tk.Label(root, text='Predicted Digit is : ' + str(digit), width=24, height=2, fg="#3e7d75", bg="black",
                   font=('Lucida Typewriter', 16, ' bold '))
    lab1.place(x=10, y=420)


'''
Calls from CLASSIFY_HANDWRITING().
Here is the most inevitable function that actually the predict the digit.
'''
def pred_digit(img):
    image = cv2.imread('./res/nitzz.png')
    grey = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    returns, thresh = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV)
    contours, hierachy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    preprocessed_digits = []

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)

        # Creating a rectangle around the digit in the original image (for displaying the digits fetched via contours)
        cv2.rectangle(image, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

        # Cropping out the digit from the image corresponding to the current contours in the for loop
        digit = thresh[y:y + h, x:x + w]

        # Resizing that digit to (18, 18)
        resized_digit = cv2.resize(digit, (18, 18))

        # Padding the digit with 5 pixels of black color (zeros) in each side to finally produce the image of (28, 28)
        padded_digit = np.pad(resized_digit, ((5, 5), (5, 5)), "constant", constant_values=0)

        # Adding the preprocessed digit to the list of preprocessed digits
        preprocessed_digits.append(padded_digit)
    # print("\n\n\n----------------Contoured Image--------------------")
    # plt.imshow(image, cmap="gray")
    # plt.show()
    # print("END")
    # print("PADDED DIGIT : ", padded_digit)


    res = model.predict(padded_digit.reshape(1, 28, 28, 1))
    return np.argmax(res)


# Function for Opening Ttkinter window in Center of the Screen On Device.
def center_window():
    # Putting window in center
    w = 800
    h = 650

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2) - 20
    y = (hs / 2) - (h / 2) - 50

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.resizable(width=False, height=False)



if __name__ == '__main__':
    root = tk.Tk() # create a Tk root window
    root.configure(background='white')
    root.title("Hand-written digit recognition")
    center_window()

    im = PIL.Image.open('./res/man1.jpg')
    im =im.resize((800,400), PIL.Image.ANTIALIAS)
    wp_img = ImageTk.PhotoImage(im)
    panel4 = Label(root, image=wp_img,bg = 'white')
    panel4.pack()
    panel4.place(x=0, y=10)


    # Initializing elements of window

    canvas = tk.Canvas(height=300,width=366,bg="white",cursor="dotbox",highlightthickness=5)
    lab = tk.Label(root, text="Draw Digit Above", width=24, height=2, fg="#3e7d75",bg="white",
                    font=('Lucida Typewriter', 16, ' bold '))
    lab.place(x=450, y=334)

    canvas1 = tk.Canvas(height=218,width=400,bg="#3e7d75", borderwidth = '8')
    canvas1.pack()
    canvas1.place(x=0,y=412)

    classify_btn = tk.Button( text = 'Predict Digit',state=DISABLED,command = classify_handwritting,width = 15,borderwidth=0,bg = '#d5d6de',fg = 'Black',font = ('Lucida Typewriter',16))
    classify_btn.pack()
    classify_btn.place(x=500,y=450)

    clear_btn = tk.Button(text = "Clear Window",command=clear_canvas,width = 15,borderwidth=0,bg ='#d5d6de',fg = 'black',font = ('Lucida Typewriter',16))
    clear_btn.pack()
    clear_btn.place(x=500,y=510)

    exit_btn = tk.Button(text = "Close",command=destroy_canvas,width = 15,borderwidth=0,bg ='#be1a02',fg = 'white',font = ('Lucida Typewriter',16))
    exit_btn.pack()
    exit_btn.place(x=500,y=570)

    # grid structure (Used for setting elements on particular position on screen.
    canvas.grid(row=0, column=0,padx=386,pady=20)

    # Event occurs while dragging mouse
    canvas.bind("<B1-Motion>",draw_rect)

    #To start execution of tkinter
    tk.mainloop()


