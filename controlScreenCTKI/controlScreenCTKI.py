import os
import tkinter
import customtkinter
import threading
# import RPi.GPIO
# import minimalmodbus
from PIL import Image

customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
# customtkinter.set_appearance_mode("system")  # default value
# customtkinter.set_appearance_mode("dark")
customtkinter.set_appearance_mode("light")

# GLOBAL VARIABLES
drvSeatStatus = 0; # 0 = off, 1 = A/C, 2 = Heat
passSeatStatus = 0; # 0 = off, 1 = A/C, 2 = Heat
appearance_mode_status = 0 # 0 = light, 1 = dark
transferCaseStatus = 0 # 0 = Unknown, 1 = 2WD, 2 = 4WD_HIGH, 3 = 4WD_LOW

# This is the current path of this .py file, used to find other resources in subfolders
current_path = os.path.dirname(os.path.realpath(__file__))


# MODBUS related
# RPI is the MODBUS server.  Slaves are other modules that have the data. 
#instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1) # port name, slave address in decimalà
# configure serial port, could use same port for multiple slaves (same config?)
    


# MAIN APP
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Size of Raspberry Pi's touchscreen
        self.geometry("800x480")
        self.title("Fummins Control Screen")
        self.attributes("-fullscreen", "True")
        
        # Configure grid layout
        # 3 columns
        # middle column is divided in 4 row
        self.grid_columnconfigure((0,2), weight=1) # Make the side columns same with and expand width-wise
        self.grid_columnconfigure(1, weight=1) # Center column will only be as wide as necessary
        self.grid_rowconfigure(0, weight=1) # Top row will expand as required
        self.grid_rowconfigure((1,2,3,4), weight=0) # Rows 2,3,4,5 will only be as high as necessary
        
        # Load image used when left seat is off (currently same for light and dark mode)
        leftSeatOffImage = customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/leftSeatOff.png"), dark_image=Image.open(current_path + "/res/seats/leftSeatOff.png"), size=(180,220))
        
        # Load image used when right seat is off (currently same for light and dark mode)
        rightSeatOffImage = customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/rightSeatOff.png"), dark_image=Image.open(current_path + "/res/seats/rightSeatOff.png"), size=(180,220))
        
        # Create button for left seat control
        self.drvSeatButton = customtkinter.CTkButton(self, width=180, height=220, text="", command=self.leftSeatPressed, image=leftSeatOffImage)
        self.drvSeatButton.grid(row=0, column=0, rowspan=5)
        # self.leftSeatButton.pack(padx=20,pady=20)
        
        # Create button for right seat control
        self.passSeatButton = customtkinter.CTkButton(self, width=180, height=220, text="", command=self.rightSeatPressed, image=rightSeatOffImage)
        self.passSeatButton.grid(row=0, column=2, rowspan=5)
        #self.rightSeatButton.pack(padx=20,pady=20)
        
        # Middle column
        
        # Drivetrain icon
        driveTrainImage = customtkinter.CTkImage(light_image=Image.open(current_path + "/res/drivetrain/missing_200_250.png"), dark_image=Image.open(current_path + "/res/drivetrain/missing_200_250.png"), size=(200,250))
        self.drivetrainLabel = customtkinter.CTkLabel(self, width=200, height=250, text="", image=driveTrainImage)
        self.drivetrainLabel.grid(row=0, column=1)
        
        # Air tank psi label
        self.airTankLabel = customtkinter.CTkLabel(self, font=("Helvetica",30), text="Air tank: --- psi")
        self.airTankLabel.grid(row=1, column=0, columnspan=3)
        
        # Electric compressor label
        self.compressorLabel = customtkinter.CTkLabel(self, font=("Helvetica",30), text="Electric compressor: OFF")
        self.compressorLabel.grid(row=2, column=0, columnspan=3)
        
        # House battery voltage label
        self.houseBattVoltLabel = customtkinter.CTkLabel(self, font=("Helvetica",30), text="House battery voltage: --.- Volts")
        self.houseBattVoltLabel.grid(row=3, column=0, columnspan=3)
        
        # Bottom row buttons
        
        # Theme button (dark/light)
        self.themeButton = customtkinter.CTkButton(self, text="Theme", height=50, command=self.switchThemePressed)
        self.themeButton.grid(row=4, column=1, pady=(20,20))
        
        # Quit button
        self.quitButton = customtkinter.CTkButton(self, text="Quit", height=50, command=self.quitButtonPressed)
        self.quitButton.grid(row=4, column=2)
        
        # Fetch Transfer case controller status every second
        self.transfercaseTimer = threading.Timer(5.0, self.getTransferCaseStatus).start()
        # getTransferCaseStatus(self)
        
        

    # Callback function when left seat button is pressed
    def leftSeatPressed(self):
        # print("left CLICK!!")
        
        # This is the current path of this .py file, used to find other resources in subfolders
        current_path = os.path.dirname(os.path.realpath(__file__))
        
        # Cycle through seat statuses
        global drvSeatStatus
        drvSeatStatus += 1
        # print("New drv seat status" + str(drvSeatStatus))
        
        # Reset if we went through all the statuses
        if(drvSeatStatus == 3):
            drvSeatStatus = 0;

            # Seat is now off, put icon
            self.drvSeatButton.configure(image=customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/leftSeatOff.png"), dark_image=Image.open(current_path + "/res/seats/leftSeatOff.png"), size=(180,220)))
        
        elif (drvSeatStatus == 1):
            # Seat is now cooling, put icon
            self.drvSeatButton.configure(image=customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/leftSeatCool.png"), dark_image=Image.open(current_path + "/res/seats/leftSeatCool.png"), size=(180,220)))
        
        elif (drvSeatStatus == 2):
            # Seat is now heating, put icon
            self.drvSeatButton.configure(image=customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/leftSeatHeat.png"), dark_image=Image.open(current_path + "/res/seats/leftSeatHeat.png"), size=(180,220)))
        
    # Callback function when right seat button is pressed
    def rightSeatPressed(self):
        # print("right CLICK!!")
        
        # This is the current path of this .py file, used to find other resources in subfolders
        current_path = os.path.dirname(os.path.realpath(__file__))
        
        # Cycle through seat statuses
        global passSeatStatus
        passSeatStatus += 1
        # print("New pass seat status" + str(passSeatStatus))
        
        # Reset if we went through all the statuses
        if(passSeatStatus == 3):
            passSeatStatus = 0;

            # Seat is now off, put icon
            self.passSeatButton.configure(image=customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/rightSeatOff.png"), dark_image=Image.open(current_path + "/res/seats/rightSeatOff.png"), size=(180,220)))
        
        elif (passSeatStatus == 1):
            # Seat is now cooling, put icon
            self.passSeatButton.configure(image=customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/rightSeatCool.png"), dark_image=Image.open(current_path + "/res/seats/rightSeatCool.png"), size=(180,220)))
        
        elif (passSeatStatus == 2):
            # Seat is now heating, put icon
            self.passSeatButton.configure(image=customtkinter.CTkImage(light_image=Image.open(current_path + "/res/seats/rightSeatHeat.png"), dark_image=Image.open(current_path + "/res/seats/rightSeatHeat.png"), size=(180,220)))

    # Callback function when Switch Theme button is pressed
    def switchThemePressed(self):
        global appearance_mode_status
        
        if(appearance_mode_status == 0): # We are light, switch to dark
            appearance_mode_status = 1
            customtkinter.set_appearance_mode("Dark")
            
        elif(appearance_mode_status == 1): # We are dark, switch to light
            appearance_mode_status = 0
            customtkinter.set_appearance_mode("Light")
            
    def getTransferCaseStatus(self): # 0 = Unknown, 1 = 2WD, 2 = 4WD_HIGH, 3 = 4WD_LOW
        global transferCaseStatus
        global current_path
    
        transferCaseStatus += 1 # TEMP
        # print("New status: " + str(transferCaseStatus))
    
        # modbus...figure out which icon based on answer from modbus
        if(transferCaseStatus == 0): # Unknown
            driveTrainImage = customtkinter.CTkImage(light_image=Image.open(current_path + "/res/drivetrain/missing_200_250.png"), dark_image=Image.open(current_path + "/res/drivetrain/missing_200_250.png"), size=(200,250))
        
        elif(transferCaseStatus == 1): # 2WD
            driveTrainImage = customtkinter.CTkImage(light_image=Image.open(current_path + "/res/drivetrain/2WD_200_250.png"), dark_image=Image.open(current_path + "/res/drivetrain/2WD_200_250.png"), size=(200,250))
        
        elif(transferCaseStatus == 2): # 4WD_HIGH
            driveTrainImage = customtkinter.CTkImage(light_image=Image.open(current_path + "/res/drivetrain/4HI_200_250.png"), dark_image=Image.open(current_path + "/res/drivetrain/4HI_200_250.png"), size=(200,250))
        
        elif(transferCaseStatus == 3): # 4WD_LOW
            driveTrainImage = customtkinter.CTkImage(light_image=Image.open(current_path + "/res/drivetrain/4LOW_200_250.png"), dark_image=Image.open(current_path + "/res/drivetrain/4LOW_200_250.png"), size=(200,250))
        
        self.drivetrainLabel.configure(image=driveTrainImage)
        
        # Re-schedule this timer function for next update
        self.transfercaseTimer = threading.Timer(5.0, self.getTransferCaseStatus).start()
    
    # Quit!      
    def quitButtonPressed(self):
        self.quit()

app = App()
app.mainloop()