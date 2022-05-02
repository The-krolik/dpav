===========
What is Direct Python Audio/Video?
===========

Direct Python Audio/Video is a library wrapping certain functionalities of Pygame that aims to give users a very simple, no-nonsense, direct feeling experience with basic audio and video manipulation. This library features the ability to craft basic waveforms and play them, as well as manipulate pixels in an image using 24-bit hex color codes, using no more than a few calls from our library. We abstract away technical aspects of interfacing with audio and video devices such as the need to maintain an event loop, in favor of straightforward calls that feel intuitive and beginner friendly.


===========
Installation
===========

This library may be installed by:

Cloning the repository:

>>> git clone https://github.com/The-krolik/dpav

Then navigating to the cloned dpav folder and running:

>>> pip install dpav



===========
Audio Class
===========

The Audio class is intended to provide basic sound capabilities focused around playing a constant tone for a desired duration in seconds. It supports playing one sound at a time with a waveform: sin, square, noise, saw, or triangle.

To get started, there are three basic steps to play a tone:
  1. Create an Audio class object
  2. Call the play_sound method with a frequency and duration (in seconds)
  3. Use the wait_for_sound_end. This maintains the process


.. code-block::
   :caption: Playing a sound
   
    mySound = dpp.Audio()
    frequency = 261
    duration = 1
    
    mySound.play_sound(frequency, duration)
    mySound.wait_for_sound_end()
..

If using audio alongside the Window class or within a while loop, the wait_for_sound_end method is unnecessary.

.. code-block::
   :caption: Using the play_sound inside a while loop
   
    mySound = dpp.Audio()
    frequency = 261
    duration = 1

    while window.is_open():
        mySound.play_sound(frequency, duration)
..


The utility function get_note_from_string takes a music note, such as "C", as a string and returns the frequency


.. code-block::
   :caption: Using the utility function: get_note_from_string
   
    mySound = dpp.Audio()
    frequency = dpp.get_note_from_string("C", 0)
    duration = 1
    
    mySound.play_sound(frequency, duration)
    mySound.wait_for_sound_end()
..
=============
VBuffer Class
=============

The VBuffer class operates as a 2-dimensional array of hex color values. This is the main data structure used for visualization within the Window class.


***************
Initialization
***************

.. code-block::
   :caption: VBuffer initialization with dimensions 1920x1080
   
    vbuffer = dpp.VBuffer((1920,1080))
       
..

.. code-block::
   :caption: VBuffer initialization with numpy array
   
    arr = np.zeros((1920,1080))
    vbuffer = dpp.VBuffer(arr)
       
..

.. code-block::
   :caption: VBuffer default initializaion provides dimensions 800x600
   
    vbuffer = dpp.VBuffer()
       
..


************
Modification
************

.. code-block::
   :caption: Changing color of pixel to red at location: x=30, y=50
   
   red = 0xFF0000
   vbuffer[30,50] = red
       
..

.. code-block::
   :caption: Changing row 30 to red
   
   red = 0xFF0000
   vbuffer[30,:] = red
..

.. code-block::
   :caption: Fill vbuffer object with color red
   
   red = 0xFF0000
   vbuffer.fill(red)
..


.. code-block::
   :caption: Clear vbuffer object with color red
   
   vbuffer.clear()
..





=============
Window Class
=============

The Window class is an abstraction of the PyGame library’s display and event handling. It is closely tied to the VBuffer class, using VBuffer objects as the primary data structure to hold the current image to display. An understanding of the VBuffer class may not be required for simple projects, such as those with static displays, but is recommended nonetheless, especially for more complicated use cases. Currently, only one window may be active at a time.


-------------
Display
-------------



**************
Initialization
**************

Only one instance of the window class is needed throughout the lifetime of the program. Initialization of the object may be done in one of three ways, based upon the argument passed, or lack thereof. Passing a VBuffer object is the preferred method of initialization, however a 2-dimensional numpy array is also accepted, which will create the VBuffer for you. If neither are provided, the Window will create a default VBuffer with dimensions: (800,600).


.. code-block::
   :caption: VBuffer initialization
   
    vbuffer = dpp.VBuffer((1920,1080))
    window = dpp.Window(vbuffer)
       
..


.. code-block::
   :caption: Numpy array initialization
   
    vbuffer = numpy.zeros((1920,1080))
    window = dpp.Window(arr)
       
..

.. code-block::
   :caption: Default initialization
   
    window = dpp.Window()
..


***************
Opening the Window
***************

  1. Call open function
  2. Construct while loop with is_open function



.. code-block::

    window.open()
    while window.is_open():
    ### your code here
..


The open function creates and opens the display. The is_open call maintains and updates the status of all events, as well as the display, on every call. The loop structure is required, as the display will become inactive otherwise.


***************
Scaling
***************

The window may be scaled up or down in one of three ways:

  1. Provide a scale value to Window on initialization
  2. Call the set_scale function with the scale value
  3. Directly modify the scale member
  
    
The default scale value is 1.0. Reducing this value will reduce the size of the display, increasing it will increase the size of the display. 

This feature can be useful. Such as: 
creating a virtual canvas of dimensions (50,50). Scaling this up by a factor of 13 will provide display dimensions of (650,650), making it much easier to visualize any changes made.



-------------
Events
-------------

Capturing events are the way which users utilize registered mouse clicks and key presses. Users have two ways to interface with these events

***************
Eventq List
***************

The eventsq list will be most often used, as this structure is best for expressions that only need to register once per key press / mouse click. This list is updated on every iteration of the window loop, removing old events and adding new ones that have been registered. These events may be used by simply checking if a specific event is in the list.

Example of what may be held in the eventq after one iteration:

.. code-block::
   :caption: Held in the eventq after one iteration example:
   
    ["a", "l_shift"]
       
..

***************
Events Dictionary
***************

The events dictionary holds String:Boolean key:value pairs. The key indicates the event to check for, and value is a Boolean indicating if a key or the mouse is currently pressed. It is ideal for continuous expression calls while a key/mouse is held down. It is not recommended to utilize this interface unless incorporated with custom handling when only one expression call is required for an event trigger.

.. code-block::
   :caption: Constantly printing to standard out while left-shift is held down
   
    while window.is_open():
        if window.events["l_shift"]:
            print("Left Shift is pressed DOWN!")
       
..


***************
Mouse Position
***************

Obtaining the current position of the mouse is done by calling the get_mouse_pos function. This will return a tuple of coordinates: (x , y). These coordinates are with respect to both the window, and the underlying VBuffer data structure.

.. code-block::
   :caption: Setting pixel at mouse location to red
   
    if "mouse" in window.eventq:
        red = 0xFF0000
        pos = window.get_mouse_pos() #get mouse position
        window.vbuffer[pos[0], pos[1]] = red # set pixel at mouse (x,y) to red
        print(f"Color at {pos} changed to Red")
..