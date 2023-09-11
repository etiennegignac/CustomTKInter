import os
import tkinter
import customtkinter
from PIL import Image

customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
# customtkinter.set_appearance_mode("system")  # default value
# customtkinter.set_appearance_mode("dark")
customtkinter.set_appearance_mode("light")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Size of Raspberry Pi's touchscreen
        self.geometry("800x480")
        
        # Configure grid layout
        # 3 columns
        # middle column is divided in 4 row
        self.grid_columnconfigure((0,1,2), weight=1) # Make the 3 columns same with
        
        # This is the current path of this .py file, used to find other resources in subfolders
        current_path = os.path.dirname(os.path.realpath(__file__))
        
        # Load image used when left seat is off (currently same for light and dark mode)
        leftSeatOffImage = customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/leftSeatOff.png"), dark_image=Image.open(current_path + "/res/seats/leftSeatOff.png"), size=(180,220))
        
        # Load image used when right seat is off (currently same for light and dark mode)
        rightSeatOffImage = customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/rightSeatOff.png"), dark_image=Image.open(current_path + "/res/seats/rightSeatOff.png"), size=(180,220))
        
        # Create button for left seat control
        self.leftSeatButton = customtkinter.CTkButton(self, width=180, height=220, text="", command=self.leftSeatPressed, image=leftSeatOffImage)
        self.leftSeatButton.grid(row=0, column=0)
        # self.leftSeatButton.pack(padx=20,pady=20)
        
        # Create button for right seat control
        self.rightSeatButton = customtkinter.CTkButton(self, width=180, height=220, text="", command=self.rightSeatPressed, image=rightSeatOffImage)
        self.rightSeatButton.grid(row=0, column=2)
        #self.rightSeatButton.pack(padx=20,pady=20)

    # Callback function when left seat button is pressed
    def leftSeatPressed(self):
        print("left CLICK!!")
        
    # Callback function when right seat button is pressed
    def rightSeatPressed(self):
        print("right CLICK!!")



app = App()
app.mainloop()