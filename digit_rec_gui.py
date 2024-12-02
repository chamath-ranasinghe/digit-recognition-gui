from keras.models import load_model
import tkinter as tk
import tempfile
import os
from PIL import ImageGrab, Image, ImageDraw
import numpy as np

model = load_model('mnist.keras')

def canvas_to_image(canvas):
    # Generate the canvas content as a postscript (EPS)
    ps = canvas.postscript(colormode='color')
    
    # Create a temporary file to save the postscript data
    with tempfile.NamedTemporaryFile(suffix=".ps", delete=False) as temp_file:
        temp_file.write(ps.encode())  # Write the postscript data to the file
        temp_file.close()  # Close the temporary file
        
        # Open the saved postscript file using Pillow
        img = Image.open(temp_file.name)
    
    # Clean up the temporary file after use
    
    return img,temp_file.name

def predict_digit(img):
    #resize image to 28x28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    #reshaping for model normalization
    img = img.reshape(1,28,28,1)
    img = img/255.0
    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        # Creating elements
        self.canvas = tk.Canvas(self, width=200, height=200, bg = "black", cursor="cross")
        self.label = tk.Label(self, text="Analyzing..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Search", command = self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Delete", command = self.clear_all)
        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky='W' )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        #self.canvas.bind("", self.start_pos)
        self.canvas.bind("<Button-1>", self.draw_lines)
        self.canvas.bind("<B1-Motion>", self.draw_lines)
    def clear_all(self):
        self.canvas.delete("all")
    def classify_handwriting(self):
        #Hd = self.canvas.winfo_id() # to fetch the handle of the canvas
        #rect = win32gui.GetWindowRect(Hd) # to fetch the edges of the canvas
        #im = ImageGrab.grab(rect)

        im, file_name = canvas_to_image(self.canvas)
        im.show()
        digit, acc = predict_digit(im)
        self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')
        os.remove(file_name)
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='white')

app = App()
app.mainloop()