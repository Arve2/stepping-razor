from machine import Pin
from time import sleep_ms

class uln2003:
    
    #Initiator
    def __init__(self, in1:int, in2:int, in3:int, in4:int, first_step:list=[1,1,0,0], steps_per_rev:float=2048.0, delay_ms:int=3):
        self._uln_pins = [Pin(in1, Pin.OUT), Pin(in2, Pin.OUT), Pin(in3, Pin.OUT), Pin(in4, Pin.OUT)] #Init coil output pins
        if first_step in ([1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]): #Wave drive, less current
            self._drive_type = 'wave'
        elif first_step in ([1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]): #Full step drive, more power
            self._drive_type = 'full'
        else:
            raise ValueError(f"Unsupported drive type: {first_step}. Must be a Wave or Single step sequence.")
        self._step = first_step #Initial pin configuration. Default first coil active.
        self._steps_per_revolution = steps_per_rev #How many steps per one revolutin. Default 2048 for 28BYJ-48.
        self._delay_ms = delay_ms #Delay between steps. Default 3ms. Shorter time --> faster but weaker.
        self._home = 0
        self._step_counter = 0
        self._invert_rotation = True #True/False depending on wiring connection.
    
    #Set coils to a step configuration list. Defaults to self._step. Can be [0,0,0,0] to release all coils
    def set_coils(self, step:list=None):
        if step is None:
            step = self._step #Default to self
        #print(step)
        for i in range(len(self._uln_pins)):
            self._uln_pins[i].value(step[i])
        sleep_ms(self._delay_ms) #Wait for mechanical delay (not really neccessary for 0 steps).
        self._step = step #Update self with new position
        
    #Take a single step, CW or CCW, by changing where the number(s) 1 are in the step configuration list
    def step_once(self, n:int=1):                   #n is only to control direction. E.g. 0.0...999 --> 1 step CW, -999...-0.1 --> 1 step CCW.
        if n < 0:                                   #Limit n (steps) to only -1, or +1.
            n = -1
        else:
            n = 1
        if self._invert_rotation:                   #Handle inversion of CW/CCW
            n = -n
        next_step = self._step[n:] + self._step[:n] #'Move' the active coil(s) left/right in the step configuration list
        self.set_coils(next_step)                   #Apply next step to coils and self
        self._step_counter += n                     #Update step counter.
    
    #Rotate some steps (can be less than 0 and more than self._steps_per_revolution)
    def rotate_steps(self, steps:int=0):
        steps = int(steps)
        print(f"About to take {steps} steps.")
        for i in range(0,abs(steps)):
            self.step_once(steps)
    
    #Rotate some angle (can be less than 0 and more than 360).
    def rotate_deg(self, deg:float=0.0):
        steps = int(deg * self._steps_per_revolution / 360)
        print(f"{self._steps_per_revolution} / 360deg ~ {steps} steps.")
        self.rotate_steps(steps)
    
    #Get/set a number of steps from home (can be less than 0 and more than self._steps_per_revolution)
    def position_steps(self, target:int=None):
        if target is None:
            return (self._step_counter - self._home)
        target = int(target)
        diff = target - self._step_counter #Just to get a positive/negative value for step_once()
        print(f"About to take {diff} steps to position {target}.")
        while abs(self._step_counter - target) > 0.5: #Step until position is within 0.5 steps from target.
            self.step_once(diff)
    
    #Get/set an angle compared to home, including small rounding errors. (can be less than 0 and more than 360)
    def position_deg(self, target_deg:float=None):
        if target_deg is None: #If get: Answer with current position compared to home
            return (self._step_counter - self._home) / (self._steps_per_revolution / 360)
        target_step = int(target_deg * self._steps_per_revolution / 360) #Translate from deg to step and round to int
        print(f"{target_deg} * {self._steps_per_revolution} / 360 ~ {target_step} steps.")
        self.position_steps(target_step)
    
    #Get/set step counter
    def step_count(self, steps:int=None):
        if steps is None:
            return self._step_counter
        else:
            self._step_counter = steps
    
    #Set home at current position 
    def set_home(self):
        self._step_counter = 0
            
    #Get/set rotation (CW/CCW)
    def invert_rotation(self, flip:bool=None):
        if flip is None:
            return self._invert_rotation
        else:
            self._invert_rotation = flip
    
    #Get/set milliseconds delay between steps
    def delay_ms(self, ms:int=None):
        if ms is None:
            return self._delay_ms
        else:
            self._delay_ms = ms
    
    #Get/set steps per revolution
    def steps_per_revolution(self, steps:int=None):
        if steps is None:
            return self._steps_per_revolution
        else:
            self._steps_per_revolution = steps
    
    #Get drive type
    def get_drive_type(self):
        return self._drive_type
