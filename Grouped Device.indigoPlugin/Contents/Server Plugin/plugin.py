"""
A Plugin which demonstrates creating a grouped device using the Device Factory method.
"""

try:
    import indigo
    # import pydevd
except ImportError:
    pass


class Plugin(indigo.PluginBase):
    """
    Placeholder
    """
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        """ Standard __init__ method for Indigo plugins. """
        self.debug = True
        self.debugLog("__init__ called")

        # try:
        #     pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True, suspend=False)
        # except:
        #     pass

    def action_control_device(self, action):
        """
        Called when a change is made to a device. Required.

        :param action:
        """
        self.debugLog(f"{action}")
        dev = indigo.devices[action.deviceId]
        match action.deviceAction:
            case indigo.kDeviceAction.SetBrightness:
                indigo.server.log(f'sent "{dev.name}" set brightness to {action.actionValue}')
            case indigo.kDeviceAction.TurnOff:
                indigo.server.log(f'sent "{dev.name}" off')
            case indigo.kDeviceAction.TurnOn:
                indigo.server.log(f'sent "{dev.name}" on')
            case indigo.kDeviceAction.RequestStatus:
                indigo.server.log(f'sent "{dev.name}" status request')
            case _:
                indigo.server.log(f"{action}")

    def action_control_sensor(self, action):
        """
        Called when a change is made to a device. Required.

        :param action:
        """
        self.debugLog(f"{action}")
        dev = indigo.devices[action.deviceId]
        match action.sensorAction:
            case indigo.kSensorAction.TurnOff:
                indigo.server.log(f'sent "{dev.name}" off')
            case indigo.kSensorAction.TurnOn:
                indigo.server.log(f'sent "{dev.name}" on')
            case indigo.kSensorAction.RequestStatus:
                indigo.server.log(f'sent "{dev.name}" status request')
            case _:
                indigo.server.log(f"{action}")

    def device_start_comm(self, dev):
        """
        Called after startup(). Called for each device. Optional.

        :param dev:
        """
        self.debugLog("device_start_comm called")

    def device_stop_comm(self, dev):
        """
        Called before shutdown(). Called for each device. Optional.

        :param dev:
        """
        self.debugLog("device_start_comm called")

    def startup(self):
        """ Called after __init__(). Optional. """
        self.debugLog("startup called")

    def shutdown(self):
        """ Called when plugin is disabled. Optional. """
        self.debugLog("shutdown called")

    # ##### Device Factory Config Methods #####
    def closed_device_factory_ui(self, values_dict, user_cancelled, dev_id_list):
        """
        Called when the device factory config UI is closed (called after validate_device_factory_ui() ). Optional.

        :param values_dict:
        :param user_cancelled:
        :param dev_id_list:
        """
        self.debugLog("closed_device_factory_ui called")

        return values_dict

    def get_device_factory_ui_values(self, dev_id_list):
        """
        Called when the device factory config UI is first opened. This method can be used to populate the dialog with
        whatever values are needed. Optional.

        :param dev_id_list:
        """
        self.debugLog("get_device_factory_ui_values called")

        values_dict = indigo.Dict()
        error_msg_dict = indigo.Dict()

        # Retrieve the 'my_name' parameter from storage (in device 1's props).
        if len(dev_id_list) > 0:
            dev = indigo.devices[dev_id_list[0]]
            values_dict['name'] = dev.pluginProps['name']

        return values_dict, error_msg_dict

    def validate_device_factory_ui(self, values_dict, dev_id_list):
        """
        Called when the device factory config UI 'save' button is clicked. Optional.

        :param values_dict:
        :param dev_id_list:
        """
        self.debugLog("validate_device_factory_ui called")
        name = values_dict['name']

        # If there are values in dev_id_list, then the group already exists.
        if len(dev_id_list) == 0:
            self.create_the_device_group(name)
        else:
            indigo.server.log("Device group already created.")

        return True, values_dict

    # ##### Device Config Methods #####
    def closed_device_config_ui(self, values_dict, user_cancelled, type_id, dev_id):
        """
        Called when the device factory config UI is closed (called after validate_device_config_ui() ). Optional. If
        something has changed, the device will be restarted by a call to device_start_comm().

        :param values_dict:
        :param user_cancelled:
        :param type_id:
        :param dev_id:
        """
        self.debugLog("closed_device_config_ui called")

        return values_dict

    def get_device_config_ui_values(self, values_dict, type_id, dev_id):
        """
        Called when any device config UI is opened. Optional.

        :param values_dict:
        :param type_id:
        :param dev_id:
        """
        self.debugLog("get_device_config_ui_values called")

        return values_dict

    def validate_device_config_ui(self, values_dict, type_id, dev_id):
        """
        Called when the device config UI 'save' button is clicked. Optional.

        :param values_dict:
        :param type_id:
        :param dev_id:
        """
        self.debugLog("validate_device_config_ui called")

        return values_dict

    def create_the_device_group(self, my_name):
        """
        Convenience method for device creation. This could also be done in closed_device_factory_ui() for example. Note
        that some device props are read only even when you create them from scratch (i.e., dev.version) and some will
        be ignored if you try to set them (i.e., dev.description, dev.errorState).

        :param my_name:
        """
        self.debugLog("create_the_device_group called")

        # Create the first device in the group.
        new_dev = indigo.device.create(protocol=indigo.kProtocol.Plugin, name=my_name, deviceTypeId="my_dimmer_device")
        new_dev.model = "Grouped Device"
        new_dev.subModel = "Dimmer"
        new_dev.name = f"{my_name} Dimmer"
        new_dev.replaceOnServer()

        # Add the group my_name setting to the props of device 1 for later use.
        new_props = new_dev.pluginProps
        new_props['name'] = my_name
        new_dev.replacePluginPropsOnServer(new_props)

        # Create the second device in the group. You can also add a state value
        # here if desired.
        new_dev = indigo.device.create(protocol=indigo.kProtocol.Plugin, name=my_name, deviceTypeId="my_sensor_device")
        new_dev.model = "Grouped Device"
        new_dev.subModel = "Temperature"
        new_dev.name = f"{my_name} Temperature"
        new_dev.replaceOnServer()
        new_dev.updateStateOnServer('state', value="Some value.")

        # You can also create devices that don't have corresponding device
        # parameters established in Devices.xml.
        new_dev = indigo.device.create(protocol=indigo.kProtocol.Plugin, name=my_name, deviceTypeId="my_lock_device")
        new_dev.model = "Grouped Device"
        new_dev.subModel = "Lock"
        new_dev.name = f"{my_name} Lock"
        new_dev.replaceOnServer()
