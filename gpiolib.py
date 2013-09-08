import os
from gpio_SysInit import *

class GPIO(object):
    """Control and monitor GPIOs using sysfs interface."""
    global conf_params
    conf_params = gpio_SysInit()
    gpio_class = conf_params.GPIOFS_PATH
    print gpio_class + "\n"
    off_value = 1

    '''def __init__(self, id, direction="in", value=off_value):'''
    def __init__(self, id, direction="out", value=off_value):
        self.id = id
        self.path = self.gpio_class + "gpio" + str(self.id)

        if not os.path.isdir(self.path):
            with open(self.gpio_class + "export", 'w') as fexport:
                fexport.write(str(self.id))

        # must set direction before setting value
	'''
        self.set_direction(direction)
        if direction == 'out':
            self.set_value(value)
	'''

    def set_direction(self, dir):
        if dir not in ('in', 'out'):
            raise ValueError("direction should be either 'in' or 'out'")
        with open(os.path.join(self.path, "direction"), 'w') as fdir:
            fdir.write(dir)


    def get_direction(self):
        with open(os.path.join(self.path, "direction"), 'r') as fdir:
            return fdir.read()


    def set_value(self, value):
        value = int(value)
        if value not in (0, 1):
            raise ValueError("Value should be 0|1")
        #if self.get_direction() == 'in':
            #raise IOError("Set direction to output before setting value")
        with open(os.path.join(self.path, "value"), 'w') as fvalue:
            fvalue.write(str(value))


    def get_value(self):
        with open(os.path.join(self.path, "value"), 'r') as fvalue:
            return int(fvalue.read())


    def off(self):
        self.set_value(self.off_value)


    def on(self):
        self.set_value(not self.off_value)


    def toggle(self):
        self.on() if self.is_off() else self.off()


    def is_off(self):
        return True if self.get_value() == self.off_value else False


    def is_on(self):
        return not self.is_off()


    def __str__(self):
        return self.path + " is " + ("off" if self.is_off() else "on")
        

class LED(GPIO):
    """Control an LED via sysfs interface."""
    def __init__(self, id):
        """Initialize an LED connected to a GPIO."""
        super(LED, self).__init__(id, 'out')
    def __str__(self):
        return "LED is " + ("off" if self.is_off() else "on")


class Button(GPIO):
    """Monitor a Button via sysfs interface."""

    def __init__(self, id):
        """Initialize a Button connected to a GPIO."""
        super(Button, self).__init__(id, 'in')
        self.pressed_value = not self.off_value


    def __str__(self):
        return "Button is " + ("pressed" if self.is_pressed() else "not pressed")


    def detect_press(self):
        """Blocking call to wait for button push."""
        while True:
            if self.is_pressed():
                break
        return True


    def is_pressed(self):
        return True if self.get_value() == self.pressed_value else False
