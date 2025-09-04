# stepping-razor
MicroPython class for unipolar stepper motors such as 28BYJ-48. Also [a classic tune by Peter Tosh](https://youtu.be/watch?v=aLJFRgE4Ywk).

I was experimenting with a 28BYJ-48 stepper motor driven by a ULN2003 connected to an ESP32-C3. Found no existing module that I liked, so I made this one. Maybe it will help someone else.

The main feature, compared to other ULN2003-modules, is that this module considers the _current_ step position (active coils) before taking a _new_ step. Thus, _not_ trying to move the rotor from position 1 to position 3, 4 to 1, or such nonsense.

Default is **full drive stepping**, for more power. **Wave drive** is also supported. Drive type is determined by `first_step` when instantiating the class. 
- Wave drive: The four coils take turn being active one at a time, such as `[1,0,0,0]` to `[0,1,0,0]` to `[0,0,1,0]` to `[0,0,0,1]` to `[1,0,0,0]` and so on. Or the reverse order for counter-clockwise.
- Full drive: The four coils take turn being active two at a time, such as `[1,1,0,0]` to `[0,1,1,0]` to `[0,0,1,1]` to `[1,0,0,1]` to `[1,1,0,0]` and so on. Or the reverse order for counter-clockwise.

# Installation
`import-module steping-razor`

# Instantiation of class uln2003() as "my_stepper"

**Basic:** `my_stepper = uln2003(0, 1, 2, 21)` where the four INT's are your four pins going to `IN` ports on the ULN2003. _0,1,2,21 are convenient pins on an ESP32-C3 OLED version._

**Advanced:** `my_stepper = uln2003(in1=0, in2=1, in3=2, in4=21, first_step=[0,1,1,0], steps_per_rev=2048.0, delay_ms=3)` where
- `in1`...`in4` are the numbers of four pins going to `IN` ports on the ULN2003. _N.b! Just the pin **numbers**, not machine.Pin()._
- `first_step` is the step configuration, i.e. _active coils_ to start with. Full/Wave drive is determined by the pattern of 0/1 in this list.
- `steps_per_rev` is how many steps the motor needs to rotate 360 degrees
- `delay_ms` is the delay after taking a step. _Anti-proportional to speed. The rotor needs some time to move after each re-configuration of active coil(s)._

# Functions on "my_stepper"

## my_stepper.set_coils()
Activate the four coils according to a list. 

After instantiating `my_stepper`, no coils are active - i.e. the rotor can move freely until a step is taken. Example usages to set coils to...
- initial list: `my_stepper.set_coils()`
- first position: `my_stepper.set_coils([1,1,0,0])`
- free rotation: `my_stepper.set_coils([0,0,0,0])`

## my_stepper.step_once()
Take a single step 
- clockwise: `my_stepper.step_once(1)` _Any INT between 1 and infinity = 1 step._
- counter clockwise: `my_stepper.step_once(-1)` _Any INT between -1 and -infinity = 1 step._

## my_stepper.rotate_steps()
Rotate a number of steps. _Can be under `0` and over `steps_per_rev`._

## my_stepper.rotate_deg()
Rotate an angle in degrees. _Can be less than `0` and more than `360`._

## my_stepper.position_steps()
Get/set position to a number of steps from home. _Can be under `0` and over `steps_per_rev`._
- Get: `my_stepper.position_steps()`.
- Set: `my_stepper.position_steps(3000)`.

## my_stepper.position_deg()
Get/set position _to_ a number of degrees from home. _Can be less than `0` and more than `360`._
- Get: `my_stepper.position_deg()`
- Set: `my_stepper.position_deg(600)`

## my_stepper.step_count()
Get/set step counter INT to answer the question "where am I?". Mostly for internal use.

## my_stepper.set_home()
Set home at current position/step.

## my_stepper.invert_rotation()
Get/set inversion of rotation. Useful since "clockwise" may mean different things in different setups.
- Get: `my_stepper.invert_rotation()`
- Set: `my_stepper.invert_rotation(True)` _or False_

## my_stepper.delay_ms()
Get/set milliseconds delay between steps to control speed vs torque.
- Get: `my_stepper.delay_ms()`
- Set: `my_stepper.delay_ms(10)`

## my_stepper.steps_per_revolution()
Get/set how many steps the motor takes forone full revolution (360deg).
- Get: `my_stepper.steps_per_revolution()`
- Set: `my_stepper.steps_per_revolution(2048)` _Standard 28BYJ-48_

## my_stepper.get_drive_type()
Get drive type, `wave` or `full` depending on `first_step` list.