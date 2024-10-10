from tkinter import *
from backend import *

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


class SmartHomeSystem:
    
    def __init__(self, smartHome):
        self.smartHome = smartHome
        self.win = Tk()
        self.win.title("My Smart Home System")
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
        onButton.grid(row=0, column=0, padx=(0, 100), pady=(0, 10)) 
        
        offButton = Button(self.mainFrame, text="Turn Off All", width=25, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=self.allOff)
        offButton.grid(row=0, column=1, padx=30, pady=(0, 10))
        
        addButton = Button(self.mainFrame, text="Add", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1,command=self.addNewWin)
        addButton.grid(row=20, column=0, padx=(0, 100), pady=(10, 0))  
        
        devices = self.smartHome.getDevices()
        index = 1
        for i in range(len(devices)):
            device = devices[i]
            label = Label(self.mainFrame, text=str(device), bg="white", font=self.fontStyle, borderwidth=1)
            label.grid(row=index, column=0, columnspan=2, pady=(0, 5), sticky="w")
            self.buttons.append(label)  
            
            toggleButton = Button(self.mainFrame, text="Toggle", width=15, font=self.fontStyle, bg=self.buttonColour, borderwidth=1,command=lambda status=i: self.toggleWidget(status))
            toggleButton.grid(row=index, column=1, padx=(0,80), pady=5)
            self.buttons.append(toggleButton)
            
            editButton = Button(self.mainFrame, text="Edit", width=8, font=self.fontStyle, bg=self.buttonColour, borderwidth=1,command=lambda edit=i: self.editNewWin(edit))
            editButton.grid(row=index, column=1, padx=(130, 0), pady=5)  
            self.buttons.append(editButton)
            
            deleteButton = Button(self.mainFrame, text="Delete", width=10, font=self.fontStyle, bg=self.buttonColour, borderwidth=1,command=lambda delete=i: self.deleteDevice(delete))
            deleteButton.grid(row=index, column=2, pady=5)
            self.buttons.append(deleteButton)

            index += 1

    def allOn(self):
        self.smartHome.turnOnAll()
        self.createWidget()
        
    def allOff(self):
        self.smartHome.turnOffAll()
        self.createWidget()
        
    def deleteDevice(self,index):
        self.smartHome.removeDeviceAt(index)
        self.createWidget()
    
    def deleteWidgets(self):
        for widget in self.buttons:
            widget.destroy()
    
    def toggleWidget(self,index):
        self.smartHome.toggleSwitch(index)
        self.createWidget()
        
    def run(self):
        self.createWidget()
        self.win.mainloop()
        
    def addNewWin(self):
        self.newWinAdd = Toplevel(self.win)
        self.newWinAdd.title("Add Device")
        mainFrame = Frame(self.newWinAdd)
        mainFrame.grid(row=0, column=0, padx=10, pady=10)
        
        deviceType = Label(mainFrame, text="Select Device Type:", font=self.fontStyle)
        deviceType.grid(row=0, column=0, padx=10, pady=10)
        
        deviceTypeVar = StringVar(mainFrame)
        deviceTypeVar.set("Smart Plug")  # Default option
        optionMenu = OptionMenu(mainFrame, deviceTypeVar, "Smart Plug", "Smart Heater")
        optionMenu.grid(row=0, column=1, padx=10, pady=10)
        
        consumptionRateLabel = Label(mainFrame, text="Enter Consumption Rate (0-150):", font=self.fontStyle)
        consumptionRateLabel.grid(row=1, column=0, padx=10, pady=10)
        
        consumptionRateEntry = Entry(mainFrame, font=self.fontStyle)
        consumptionRateEntry.grid(row=1, column=1, padx=10, pady=10)
        
        optionLabel = Label(mainFrame, text="Enter Option (0-5):", font=self.fontStyle)
        optionLabel.grid(row=2, column=0, padx=10, pady=10)
        
        optionEntry = Entry(mainFrame, font=self.fontStyle)
        optionEntry.grid(row=2, column=1, padx=10, pady=10)
        
        addButton = Button(mainFrame, text="Add Device", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=lambda: self.addDevice(deviceTypeVar.get(), consumptionRateEntry.get(), optionEntry.get()))
        addButton.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Create error label
        self.errorLabelAdd = Label(mainFrame, text="", fg="red", font=self.fontStyle)
        self.errorLabelAdd.grid(row=4, column=0, columnspan=2, pady=10)

    def addDevice(self, deviceType, consumptionRate, option):
        if deviceType == "Smart Plug":
            if consumptionRate.isdigit():
                consumptionRate = int(consumptionRate)
                if 0 <= consumptionRate <= 150:
                    device = SmartPlug(consumptionRate)
                    self.smartHome.addDevices(device)
                    self.createWidget()
                    self.newWinAdd.destroy()
                else:
                    self.errorLabelAdd.config(text="Invalid consumption rate. Please enter a value between 0 and 150.")
            else:
                self.errorLabelAdd.config(text="Invalid input for consumption rate. Please enter a valid integer.")
                
        elif deviceType == "Smart Heater":
            if option.isdigit():
                option = int(option)
                if 0 <= option <= 5:
                    device = SmartHeater()
                    device.setOption(option)
                    self.smartHome.addDevices(device)
                    self.createWidget()
                    self.newWinAdd.destroy()
                else:
                    self.errorLabelAdd.config(text="Invalid option. Please enter a value between 0 and 5.")
            else:
                self.errorLabelAdd.config(text="Invalid input for option. Please enter a valid integer.")
        else:
            self.errorLabelAdd.config(text="Invalid device type.")
        
 
    def editNewWin(self, index):
        self.editWin = Toplevel(self.win)
        self.editWin.title("Edit Device")
        self.mainFrameEdit = Frame(self.editWin)
        self.mainFrameEdit.grid(row=0, column=0, padx=10, pady=10)

        device = self.smartHome.getDeviceAt(index)

        if device.deviceType == "SmartPlug":
            consumptionRate = Label(self.mainFrameEdit, text="Enter New Consumption Rate (0-150):", font=self.fontStyle)
            consumptionRate.grid(row=0, column=0, padx=10, pady=10)
            
            consumptionRateEntry = Entry(self.mainFrameEdit, font=self.fontStyle)
            consumptionRateEntry.grid(row=0, column=1, padx=10, pady=10)
            
            updateButton = Button(self.mainFrameEdit, text="Update Device", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=lambda: self.updateConsumptionRate(index, consumptionRateEntry.get()))
            updateButton.grid(row=1, column=0, columnspan=2, pady=10)
            
        elif device.deviceType == "SmartHeater":
            optionLabel = Label(self.mainFrameEdit, text="Enter New Option (0-5):", font=self.fontStyle)
            optionLabel.grid(row=0, column=0, padx=10, pady=10)
            
            optionEntry = Entry(self.mainFrameEdit, font=self.fontStyle)
            optionEntry.grid(row=0, column=1, padx=10, pady=10)
            
            updateButton = Button(self.mainFrameEdit, text="Update Device", width=20, font=self.fontStyle, bg=self.buttonColour, borderwidth=1, command=lambda: self.updateOption(index, optionEntry.get()))
            updateButton.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Create error label
        self.errorLabelEdit = Label(self.editWin, text="", fg="red", font=self.fontStyle)
        self.errorLabelEdit.grid(row=2, column=0, columnspan=2, pady=10)

    def updateConsumptionRate(self, index, newConsumptionRate):
        device = self.smartHome.getDeviceAt(index)

        if newConsumptionRate.isdigit():
            newConsumptionRate = int(newConsumptionRate)
            if 0 <= newConsumptionRate <= 150:
                device.setConsumptionRate(newConsumptionRate)
                self.createWidget()
                self.editWin.destroy()
            else:
                self.errorLabelEdit.config(text="Invalid consumption rate. Please enter a value between 0 and 150.")
        else:
            self.errorLabelEdit.config(text="Invalid input. Please enter a valid integer for consumption rate.")

    def updateOption(self, index, newOption):
        device = self.smartHome.getDeviceAt(index)

        if newOption.isdigit():
            newOption = int(newOption)
            if 0 <= newOption <= 5:
                device.setOption(newOption)
                self.createWidget()
                self.editWin.destroy()
            else:
                self.errorLabelEdit.config(text="Invalid option. Please enter a value between 0 and 5.")
        else:
            self.errorLabelEdit.config(text="Invalid input. Please enter a valid integer for option.")

def main():
    # Create SmartHome object
    smartHome = setUpHome()
    
    # Create SmartHomeSystem object and pass SmartHome object to it
    mySystem = SmartHomeSystem(smartHome)
    
    # Run the SmartHomeSystem
    mySystem.run()
    
main()