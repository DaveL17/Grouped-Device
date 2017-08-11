#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = True
        self.debugLog(u"__init__ called")

    def startup(self):
        """ Called after __init__(). Optional."""
        self.debugLog(u"startup called")
        
    def deviceStartComm(self, dev):
        """ Called after startup(). Called for each device. Optional. """
        self.debugLog(u"deviceStartComm called")
    
    def deviceStopComm(self, dev):
        """ Called before shutdown(). Called for each device. Optional."""
        self.debugLog(u"deviceStartComm called")

    def shutdown(self):
        """ Called when plugin is disabled. """
        self.debugLog(u"shutdown called")

    # ##### Device Factory Config Methods #####
    def getDeviceFactoryUiValues(self, devIdList):
        """ Called when the device factory config UI is first opened. This
        method can be used to populate the dialog with whatever values are
        needed. Optional. """
        self.debugLog(u"getDeviceFactoryUiValues called")
                
        valuesDict = indigo.Dict()
        errorMsgDict = indigo.Dict()
        
        # Retrieve the 'name' parameter from storage (in device 1's props).
        if len(devIdList) > 0:
            dev = indigo.devices[devIdList[0]]
            valuesDict['name'] = dev.pluginProps['name']
        
        return (valuesDict, errorMsgDict)
        
    def validateDeviceFactoryUi(self, valuesDict, devIdList):
        """ Called when the device factory config UI 'save' button is clicked.
        Optional. """
        self.debugLog(u"validateDeviceFactoryUi called")
        name = valuesDict['name']

        # If there are values in devIdList, then the group already exists.
        if len(devIdList) == 0:
            self.createTheDeviceGroup(name)
        else:
            indigo.server.log("Device group already created.")
            
        return (True, valuesDict)

    def closedDeviceFactoryUi(self, valuesDict, userCancelled, devIdList):
        """ Called when the device factory config UI is closed (called after
        validateDeviceFactoryUi(). Optional. """
        self.debugLog(u"closedDeviceFactoryUi called")
        
        return valuesDict

    # ##### Device Config Methods #####
    def getDeviceConfigUiValues(self, valuesDict, typeId, devId):
        """ Called when any device config UI is opened. Optional."""
        self.debugLog(u"getDeviceConfigUiValues called")
        
        return (valuesDict)

    def validateDeviceConfigUi(self, valuesDict, typeID, devId):
        """ Called when the device config UI 'save' button is clicked. Optional. """
        self.debugLog(u"validateDeviceConfigUi called")

        return (True, valuesDict)
        
    def closedDeviceConfigUi(self, valuesDict, userCancelled, typeId, devId):
        """ Called when the device factory config UI is closed (called after
        validateDeviceConfigUi(). Optional. If something has changed, the
        device will be restarted by a call to deviceStartComm(). """
        self.debugLog(u"closedDeviceConfigUi called")

        return (True, valuesDict)
        
    def createTheDeviceGroup(self, name):
        """ Convenience method for device creation. This could also be done in
        closedDeviceFactoryUi() for example. Note that some device props are
        read only even when you create them from scratch (i.e., dev.version)
        and some will be ignored if you try to set them (i.e., dev.description,
        dev.errorState). """
        self.debugLog(u"createTheDeviceGroup called")
        
        # Create the first device in the group.
        newdev = indigo.device.create(indigo.kProtocol.Plugin, deviceTypeId="Device1")
        newdev.model = "Device 1 Model"
        newdev.subModel = "Sub Model 1"
        newdev.name = u"{0} Device 1".format(name)
        newdev.replaceOnServer()

        # Add the group name setting to the props of device 1 for later use.
        newprops = newdev.pluginProps
        newprops['name'] = name
        newdev.replacePluginPropsOnServer(newprops)
        
        # Create the second device in the group. You can also add a state value
        # here if desired.
        newdev = indigo.device.create(indigo.kProtocol.Plugin, deviceTypeId="Device2")
        newdev.model = "Device 2 Model"
        newdev.subModel = "Sub Model 2"
        newdev.name = u"{0} Device 2".format(name)
        newdev.replaceOnServer()
        newdev.updateStateOnServer('state', value="Some value.")
    
        # You can also create devices that don't have corresponding device
        # parameters established in Devices.xml.
        newdev = indigo.device.create(indigo.kProtocol.Plugin, deviceTypeId="Device3")
        newdev.model = "Device 3 Model"
        newdev.subModel = "Sub Model 3"
        newdev.name = u"{0} Device 3".format(name)
        newdev.replaceOnServer()
