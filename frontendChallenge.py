from tkinter import *
from backendChallenge import * # This will import everything in the backend file
from tkinter import messagebox
from tkinter import colorchooser 
from tkinter import filedialog
import time


""" USER INPUT """
def setUpHome():
    myHome = SmartHome()
    
    print("Welcome To SmartHome Setup!")
    
    # Allow the user to add five devices
    for i in range(5):
        print(f"\nAdding Device {i + 1}:")
        deviceCreated = False
        
        while not deviceCreated:
            deviceType = input("Enter device type (SmartPlug/SmartHeater): ").lower().strip()

            if deviceType == "smartplug":
                # Prompt for consumption rate for SmartPlug
                consumptionRate = input("Enter consumption rate for SmartPlug (0-150): ")
                if consumptionRate.isdigit():
                    consumptionRate = int(consumptionRate)
                    if 0 <= consumptionRate <= 150:
                        device = SmartPlug(consumptionRate)
                        deviceCreated = True
                    else:
                        print("Invalid consumption rate. Please enter a value between 0 and 150.")
                else:
                    print("Invalid input. Please enter a valid integer for consumption rate.")

            elif deviceType == "smartheater":
                # Prompt for option for SmartHeater
                option = input("Enter option for SmartHeater (0-5): ")
                if option.isdigit():
                    option = int(option)
                    if 0 <= option <= 5:
                        device = SmartHeater()
                        device.setOption(option)
                        deviceCreated = True
                    else:
                        print("Invalid option. Please enter a value between 0 and 5.")
                else:
                    print("Invalid input. Please enter a valid integer for option.")
            else:
                print("Invalid device type. Please enter 'SmartPlug' or 'SmartHeater'.")

        # Add the device to the SmartHome
        myHome.addDevices(device)
    return myHome

#setUpHome()


""" GUI """    
""" TASK 4, TASK 5 AND CHALLENGE s""" 
class SmartHomeSystem: 
    
    def __init__(self, smartHome):
        self.smartHome = smartHome
        self.win = Tk()
        self.win.title("My Smart Home System")
        #self.win.geometry("700x350")
        self.win.config(background="white")
        self.mainFrame = Frame(self.win)
        self.mainFrame.grid(row=0,column=0, padx=10, pady=10)
        self.mainFrame.config(background="white")
        self.fontStyle = ("Calibri", 12)
        self.buttonColour = "lightgreen"
        self.buttons = []
       
    def createWidget(self):
        self.deleteWidgets()
        
        onButton = Button(self.mainFrame, text="Turn On All", width=25, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=self.allOn)
        onButton.grid(row=0, column=0, padx=(40, 0), pady=(0, 10)) 
        
        offButton = Button(self.mainFrame, text="Turn Off All", width=25, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=self.allOff)
        offButton.grid(row=0, column=1, padx=30, pady=(0, 10))
        
        addButton = Button(self.mainFrame, text="Add", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1,command=self.addNewWin)
        addButton.grid(row=20, column=0, padx=(40, 0), pady=(10, 0))  
        
        accessibilityButton = Button(self.mainFrame, text="App Settings", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1,command=self.accessibility)
        accessibilityButton.grid(row=20, column=1, padx=(0, 0), pady=(10, 0))
        
        # Time
        self.clockLabel = Label(self.mainFrame, text="", font=self.fontStyle, bg="white")
        self.clockLabel.grid(row=0, column=2, padx=(50,0), pady=(0,10))
        self.updateClock()
        
        # Add a new button to the GUI for setting automatic on/off time
        autoButton = Button(self.mainFrame, text="Set Auto On/Off Time (Seconds)", width=35, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=self.setAutoOnOffTime)
        autoButton.grid(row=22, column=0, columnspan=2, pady=10)
        
        # Load the images for Smart Plug and Smart Heater
        smartPlugIcon = PhotoImage(file="images/smart-plug.png").subsample(15, 15)
        smartHeaterIcon = PhotoImage(file="images/smartheater1.png").subsample(15, 15)
        
        # Display devices
        devices = self.smartHome.getDevices()
        index = 1
        for i in range(len(devices)):
            device = devices[i]
            label = Label(self.mainFrame, text=str(device), font=self.fontStyle, borderwidth=1)
            label.config(background="white")
            label.grid(row=index, column=0, columnspan=2, padx=(0,240), pady=(0, 5))
            self.buttons.append(label)  
            
            # Toggle button
            toggleButton = Button(self.mainFrame, text="Toggle", width=15, font=self.fontStyle, bg=self.buttonColour, borderwidth=1,command=lambda status=i: self.toggleWidget(status))
            toggleButton.grid(row=index, column=1, padx=(0,100), pady=5)
            self.buttons.append(toggleButton)
            
            # Edit button
            editButton = Button(self.mainFrame, text="Edit", width=8, font=self.fontStyle, bg=self.buttonColour, borderwidth=1,command=lambda edit=i: self.editNewWin(edit))
            editButton.grid(row=index, column=1, padx=(150, 0), pady=5)  
            self.buttons.append(editButton)
            
            # Delete button
            deleteButton = Button(self.mainFrame, text="Delete", width=10, font=self.fontStyle, bg=self.buttonColour, borderwidth=1,command=lambda delete=i: self.deleteDevice(delete))
            deleteButton.grid(row=index, column=2, padx=(50,0), pady=5)
            self.buttons.append(deleteButton)

            # Display device icon based on device type
            if device.deviceType == "SmartPlug":
                icon = smartPlugIcon
            elif device.deviceType == "SmartHeater":
                icon = smartHeaterIcon

            # Display the icon
            iconLabel = Label(self.mainFrame, image=icon)
            iconLabel.config(background="white")
            iconLabel.grid(row=index, column=0, padx=(0,350), pady=(0,10))
            iconLabel.image = [smartHeaterIcon,smartPlugIcon]
            self.buttons.append(iconLabel)
            
            index += 1
            
         # Add Load and Save buttons
        loadButton = Button(self.mainFrame, text="Load", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=self.loadDevicesFromFile)
        loadButton.grid(row=21, column=0, padx=(40, 0), pady=10)

        saveButton = Button(self.mainFrame, text="Save", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=self.saveDevicesToFile)
        saveButton.grid(row=21, column=1, padx=(0, 0), pady=10)

    def addLogo(self):
        # Load the image
        logoImage = PhotoImage(file="images/smart-home.png")

        # Set the window icon
        self.win.iconphoto(True, logoImage)
        
    def allOn(self):
        self.smartHome.turnOnAll()
        self.createWidget()  # Refresh widgets after turnOn
        
    def allOff(self):
        self.smartHome.turnOffAll()
        self.createWidget()  # Refresh widgets after turnOff
        
    def deleteDevice(self,index):
        self.smartHome.removeDeviceAt(index)
        self.createWidget()  # Refresh widgets after deletion
    
    # This destroys the old when the new is created
    def deleteWidgets(self):
        for widget in self.buttons:
            widget.destroy()
    
    def toggleWidget(self,index):
        self.smartHome.toggleSwitch(index)
        self.createWidget()
    
    # New Window For Adding Devices    
    def addNewWin(self):
        self.newWinAdd = Toplevel(self.win)
        self.newWinAdd.title("Add Device")
        mainFrameAdd = Frame(self.newWinAdd)
        mainFrameAdd.grid(row=0, column=0, padx=10, pady=10)
        
        # Display device icon
        smartHeaterIcon = PhotoImage(file="images/smart-plug.png").subsample(10, 10)
        myLabel = Label(mainFrameAdd, image=smartHeaterIcon)
        myLabel.image = smartHeaterIcon
        myLabel.grid(row=1,column=4,pady=(0,10))
        
        smartPlugIcon = PhotoImage(file="images/smartheater1.png").subsample(10, 10)
        myLabel = Label(mainFrameAdd, image=smartPlugIcon)
        myLabel.image = smartPlugIcon
        myLabel.grid(row=2,column=4,pady=(0,10))
        
        # Label and option menu to select device type
        deviceType = Label(mainFrameAdd, text="Select Device Type:", font=self.fontStyle)
        deviceType.grid(row=0, column=0, padx=10, pady=10)
        
        deviceTypeVar = StringVar(mainFrameAdd)
        deviceTypeVar.set("Smart Plug")  # Default option
        optionMenu = OptionMenu(mainFrameAdd, deviceTypeVar, "Smart Plug", "Smart Heater")
        optionMenu.config(background=self.buttonColour)
        optionMenu.grid(row=0, column=1, padx=10, pady=10)
        
        consumptionRateLabel = Label(mainFrameAdd, text="Enter Consumption Rate (0-150):", font=self.fontStyle)
        consumptionRateLabel.grid(row=1, column=0, padx=10, pady=10)
        
        consumptionRateSpinbox = Spinbox(mainFrameAdd, from_=0, to=150, font=self.fontStyle)
        consumptionRateSpinbox.grid(row=1, column=1, padx=10, pady=10)
        
        optionLabel = Label(mainFrameAdd, text="Enter Option (0-5):", font=self.fontStyle)
        optionLabel.grid(row=2, column=0, padx=10, pady=10)
        
        optionSpinbox = Spinbox(mainFrameAdd, from_=0, to=5, font=self.fontStyle)
        optionSpinbox.grid(row=2, column=1, padx=10, pady=10)
        
        addButton = Button(mainFrameAdd, text="Add Device", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=lambda: self.addDevice(deviceTypeVar.get(), consumptionRateSpinbox.get(), optionSpinbox.get()))
        addButton.grid(row=3, column=0, columnspan=2, pady=10)

    def addDevice(self, deviceType, consumptionRate, option):
        if deviceType == "Smart Plug":
            if consumptionRate.isdigit():
                consumptionRate = int(consumptionRate)
                if 0 <= consumptionRate <= 150:
                    device = SmartPlug(consumptionRate)
                    self.smartHome.addDevices(device)
                    self.createWidget()  # Refresh widgets after adding
                    self.newWinAdd.destroy()
                else:
                    messagebox.showerror("Error", "Invalid consumption rate. Please enter a value between 0 and 150.")
            else:
                messagebox.showerror("Error", "Invalid input. Please enter a valid integer for consumption rate.")
        elif deviceType == "Smart Heater":
            if option.isdigit():
                option = int(option)
                if 0 <= option <= 5:
                    device = SmartHeater()
                    device.setOption(option)
                    self.smartHome.addDevices(device)
                    self.createWidget()  # Refresh widgets after adding
                    self.newWinAdd.destroy()
                else:
                    messagebox.showerror("Error", "Invalid option. Please enter a value between 0 and 5.")
            else:
                messagebox.showerror("Error", "Invalid input. Please enter a valid integer for option.")
        else:
            messagebox.showerror("Error", "Invalid device type.")       
    
    # New Windows For Editing Devices
    def editNewWin(self, index):
        self.editWin = Toplevel(self.win)
        self.editWin.title("Edit Device")
        self.mainFrameEdit = Frame(self.editWin)
        self.mainFrameEdit.grid(row=0, column=0, padx=10, pady=10)
        
        device = self.smartHome.getDeviceAt(index)

        if device.deviceType == "SmartPlug":
            consumptionRateLabel = Label(self.mainFrameEdit, text="Enter New Consumption Rate (0-150):", font=self.fontStyle)
            consumptionRateLabel.grid(row=0, column=0, padx=10, pady=10)
            
            consumptionRateSpinbox = Spinbox(self.mainFrameEdit, from_=0, to=150, font=self.fontStyle)
            consumptionRateSpinbox.grid(row=0, column=1, padx=10, pady=10)
            
            updateButton = Button(self.mainFrameEdit, text="Update Device", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=lambda: self.updateConsumptionRate(index, consumptionRateSpinbox.get()))
            updateButton.grid(row=1, column=0, columnspan=2, pady=10)
            
            smartPlugIcon = PhotoImage(file="smart-plug.png").subsample(10, 10)
            myLabel = Label(self.mainFrameEdit, image=smartPlugIcon)
            myLabel.image = smartPlugIcon
            myLabel.grid(row=0,column=4,pady=(0,10))
            
        elif device.deviceType == "SmartHeater":
            optionLabel = Label(self.mainFrameEdit, text="Enter New Option (0-5):", font=self.fontStyle)
            optionLabel.grid(row=0, column=0, padx=10, pady=10)
            
            optionSpinbox = Spinbox(self.mainFrameEdit, from_=0, to=5, font=self.fontStyle)
            optionSpinbox.grid(row=0, column=1, padx=10, pady=10)
            
            updateButton = Button(self.mainFrameEdit, text="Update Device", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=lambda: self.updateOption(index, optionSpinbox.get()))
            updateButton.grid(row=1, column=0, columnspan=2, pady=10)

            smartHeaterIcon = PhotoImage(file="images/smartheater1.png").subsample(10, 10)
            myLabel = Label(self.mainFrameEdit, image=smartHeaterIcon)
            myLabel.image = smartHeaterIcon
            myLabel.grid(row=0,column=4,pady=(0,10))

    def updateConsumptionRate(self, index, newConsumptionRate):
        device = self.smartHome.getDeviceAt(index)

        if newConsumptionRate.isdigit():
            newConsumptionRate = int(newConsumptionRate)
            if 0 <= newConsumptionRate <= 150:
                device.setConsumptionRate(newConsumptionRate)
                self.createWidget()
                self.editWin.destroy()
            else:
                messagebox.showerror("Error", "Invalid consumption rate. Please enter a value between 0 and 150.")
        else:
            messagebox.showerror("Error", "Invalid input. Please enter a valid integer for consumption rate.")

    def updateOption(self, index, newOption):
        device = self.smartHome.getDeviceAt(index)

        if newOption.isdigit():
            newOption = int(newOption)
            if 0 <= newOption <= 5:
                device.setOption(newOption)
                self.createWidget()
                self.editWin.destroy()
            else:
                messagebox.showerror("Error", "Invalid option. Please enter a value between 0 and 5.")
        else:
            messagebox.showerror("Error", "Invalid input. Please enter a valid integer for option.")

    # Setting New Windows
    def accessibility(self):
        self.newWinAccess = Toplevel(self.win)
        self.newWinAccess.title("Add Device")
        mainFrameSettings = Frame(self.newWinAccess)
        mainFrameSettings.grid(row=0, column=0, padx=10, pady=10)
        
        # Background color setting
        bgColorLabel = Label(mainFrameSettings, text="Background Color:", font=self.fontStyle)
        bgColorLabel.grid(row=1, column=0, padx=10, pady=10)
        bgColorButton = Button(mainFrameSettings, text="Choose Color", bg=self.buttonColour, font=self.fontStyle, command=self.chooseBgColor)
        bgColorButton.grid(row=1, column=1, padx=10, pady=10)
        
        # Dark/Light mode button
        modeButton = Button(mainFrameSettings, text="Dark Mode / Light Mode", width=25, bg=self.buttonColour, font=self.fontStyle, command=self.mode)
        modeButton.grid(row=2, column=1, padx=10, pady=10)
            
    def chooseBgColor(self):
        color = colorchooser.askcolor() # Own Notes : The [1] is used to access the second element of the tuple returned by the colorchooser.askcolor() function.
        if color[1]:
            self.win.config(bg=color[1])
            self.mainFrame.config(bg=color[1])
            
    def mode(self):
        currentBg = self.win.cget('bg') # Retrive current colour
        if currentBg == 'white':
            newBg = 'black'
        else:
            newBg = 'white'
        self.win.config(bg=newBg)
        self.mainFrame.config(bg=newBg)
    
    # Time    
    def updateClock(self):
        currentTime = time.strftime("%H:%M:%S")
        self.clockLabel.config(text=currentTime)
        self.win.after(1000, self.updateClock) # 1000 milliseconds is equivalent to 1 second.

    def turnOnAuto(self):
        self.smartHome.turnOnAll()
        self.win.after(20000, self.turnOffAuto) # Turns on every 30 seconds(20000 milliseconds = 30 seconds)
        self.createWidget()

    def turnOffAuto(self):
        self.smartHome.turnOffAll()
        self.win.after(20000, self.turnOnAuto)
        self.createWidget()

    # Implement a function to handle the automatic on/off functionality
    def setAutoOnOffTime(self):
        self.autoWin = Toplevel(self.win)
        self.autoWin.title("Set Auto On/Off Time (Seconds)")
        mainFrameAuto = Frame(self.autoWin)
        mainFrameAuto.grid(row=0, column=0, padx=10, pady=10)

        onSecondsLabel = Label(mainFrameAuto, text="Turn On After (Seconds):", font=self.fontStyle)
        onSecondsLabel.grid(row=0, column=0, padx=10, pady=5)
        self.onSecondsVar = StringVar()
        onSecondsSpinbox = Spinbox(mainFrameAuto, from_=0, to=86400, textvariable=self.onSecondsVar, font=self.fontStyle)
        onSecondsSpinbox.grid(row=0, column=1, padx=10, pady=5)

        offSecondsLabel = Label(mainFrameAuto, text="Turn Off After (Seconds):", font=self.fontStyle)
        offSecondsLabel.grid(row=1, column=0, padx=10, pady=5)
        self.offSecondsVar = StringVar()
        offSecondsSpinbox = Spinbox(mainFrameAuto, from_=0, to=86400, textvariable=self.offSecondsVar, font=self.fontStyle)
        offSecondsSpinbox.grid(row=1, column=1, padx=10, pady=5)

        setButton = Button(mainFrameAuto, text="Set", width=10, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=self.setAutoOnOff)
        setButton.grid(row=2, column=0, columnspan=2, pady=10)

    # Implement functionality to read the time from the SpinBox and turn devices on/off automatically
    def setAutoOnOff(self):
        onSeconds = self.onSecondsVar.get()
        offSeconds = self.offSecondsVar.get()
        
        if onSeconds.isdigit() and offSeconds.isdigit():
            onSeconds = int(onSeconds)
            offSeconds = int(offSeconds)
            # Check if values are valid
            if onSeconds >= 0 and offSeconds >= 0:
                # Schedule the on event
                self.win.after(onSeconds * 1000, self.turnOnAuto)
                
                # Schedule the off event after the on event
                self.win.after((onSeconds + offSeconds) * 1000, self.turnOffAuto)
                self.autoWin.destroy()

                messagebox.showinfo("Auto On/Off Time Set", f"Devices will turn on after {onSeconds} seconds and off after {offSeconds} seconds.")
            else:
                messagebox.showerror("Invalid Input", "Please enter non-negative values for on and off seconds.")
        else:
            messagebox.showerror("Invalid Input", "Please enter valid integer values for on and off seconds.")       
        
    def run(self):
        self.createWidget()
        self.turnOffAuto()
        self.addLogo()
        self.win.mainloop()
        
    def loadDevicesFromFile(self):
        filePath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]) # Opens a file dialog window that allows the user to select a file
        #  Checks if a file has been selected by the user
        if filePath:
            file = open(filePath, 'r')
            lines = file.readlines()
            file.close()
            
            # Clear existing devices
            self.smartHome.devices = []

            # Read devices from the file and add them to the smart home
            for line in lines:
                data = line.strip().split(',')
                if data[0] == "SmartPlug":
                    device = SmartPlug(int(data[1]))
                elif data[0] == "SmartHeater":
                    device = SmartHeater()
                    device.setOption(int(data[1]))
                self.smartHome.addDevices(device)
            self.createWidget()  # Refresh widgets after loading

    def saveDevicesToFile(self):
        filePath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filePath:
            file = open(filePath, 'w')

            # Write each device's information to the file
            for device in self.smartHome.getDevices():
                if device.deviceType == "SmartPlug":
                    file.write(f"SmartPlug,{device.consumptionRate}\n")
                elif device.deviceType == "SmartHeater":
                    file.write(f"SmartHeater,{device.option}\n")
            file.close()
            
def main():
    # Create SmartHome object
    smartHome = setUpHome()
    
    # Create SmartHomeSystem object and pass SmartHome object to it
    mySystem = SmartHomeSystem(smartHome)
    
    # Run the SmartHomeSystem
    mySystem.run()
    
main()