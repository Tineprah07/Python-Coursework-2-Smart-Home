
""" INHERITANCE """

# Super Class 
class Device:
    def __init__(self):
        self.switchedOn = False

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def getSwitchOn(self):
        return self.switchedOn


""" TASK 1 """
# Sub Class
class SmartPlug(Device):
    def __init__(self, consumptionRate):
        super().__init__()
        self.deviceType = "SmartPlug"
        self.consumptionRate = consumptionRate

    def getConsumptionRate(self):
        return self.consumptionRate

    def setConsumptionRate(self, newRate):
        if 0 <= newRate <= 150:
            self.consumptionRate = newRate
        else:
            print(f"Rate: {newRate} - Invalid Consumption Rate.")

    def __str__(self):
        if self.switchedOn:
            status = "ON"
        else:
            status = "OFF"
             
        output = f"Smart Plug Status : {status} , Consumption Rate : {self.consumptionRate}"
        return output
    
def testSmartPlug():
    mySmart = SmartPlug(45)
    mySmart.toggleSwitch()
    print(f"Plug Switched On: {mySmart.getSwitchOn()}")
    print(f"Original Consumption Rate: {mySmart.getConsumptionRate()}")
    mySmart.setConsumptionRate(52)  # Setting a new valid consumption rate
    print(f"New Consumption Rate: {mySmart.getConsumptionRate()}")
    print(mySmart)
    

""" TASK 2 """
# Sub Class
class SmartHeater(Device):
    def __init__(self):
        super().__init__()
        self.deviceType = "SmartHeater" 
        self.option = 0

    def getOption(self):
        return self.option

    def setOption(self, newOption):
        if 0 <= newOption <= 5:
            self.option = newOption
        else:
            print("Invalid option.")

    def __str__(self):
        if self.switchedOn:
            status = "ON "
        else:
            status = "OFF"
            
        output = f"Heater Status: {status}"
        output += f", Heater is set to: {self.option}"
        return output

def testSmartHeater():
    myHeater = SmartHeater()
    myHeater.toggleSwitch()
    print(f"Heater Switched On: {myHeater.getSwitchOn()}")
    print(f"Current Option: {myHeater.getOption()}")
    myHeater.setOption(4)
    print(f"New Option: {myHeater.getOption()}")
    
    print(myHeater)


""" TASK 3 """ 
class SmartHome:
    def __init__(self):
        self.devices = []

    def getDevices(self):
        return self.devices

    def getDeviceAt(self, index):
        if 0 <= index < len(self.devices):
            return self.devices[index]
        else:
            print("Error: Index out of range.")

    def removeDeviceAt(self, index):
        if 0 <= index < len(self.devices):
            del self.devices[index]
        else:
            print("Error: Index out of range.")

    def addDevices(self, device):
        self.devices.append(device)

    def toggleSwitch(self, index):
        if 0 <= index < len(self.devices):
            self.devices[index].toggleSwitch()
        else:
            print("Error: Index out of range.")

    def turnOnAll(self):
        for device in self.devices:
            device.switchedOn = True

    def turnOffAll(self):
        for device in self.devices:
            device.switchedOn = False

    def __str__(self):
        result = "Smart Home Devices:\n"
        index = 1
        for device in self.devices:
            result += f"Device {index} : {device}\n"
            index += 1
        return result


def testSmartHome():
    myHome = SmartHome()
    plug1 = SmartPlug(45)
    plug2 = SmartPlug(45)
    myHeater = SmartHeater()

    plug1.toggleSwitch()  # Turning on the first plug
    plug1.setConsumptionRate(150)
    plug2.setConsumptionRate(25)
    myHeater.setOption(3)

    myHome.addDevices(plug1)
    myHome.addDevices(plug2)
    myHome.addDevices(myHeater)

    myHome.toggleSwitch(1)
    print(myHome)

    myHome.turnOnAll()
    print("Smart Home status after turning all devices on:")
    print(myHome)

    myHome.removeDeviceAt(0)
    print("Smart Home status after removing the first device:")
    print(myHome)

#testSmartPlug()
#testSmartHeater()
#testSmartHome()
