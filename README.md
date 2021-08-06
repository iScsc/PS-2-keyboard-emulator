# A PS/2 keyboard emulator.
In this directory, some code is provided to emulate a PS/2 keyboard using an arduino board an python code. Please refer to the below Table Of Content (TOC) for more details about this document.  
In case of any issue, please open an issue on the repo or contact us at `supaerocsclub@gmail.com`.


## Table Of Content.
- [1  ](https://github.com/Supaero-Computer-Science-Club/PS-2-keyboard-emulator/tree/main/#1-the-hardware-toc) The Hardware.
- [2  ](https://github.com/Supaero-Computer-Science-Club/PS-2-keyboard-emulator/tree/main/#2-the-software-toc) The Software.
- [3  ](https://github.com/Supaero-Computer-Science-Club/PS-2-keyboard-emulator/tree/main/#3-run-the-code-toc) Run the code.

## 1 The Hardware. [[toc](https://github.com/Supaero-Computer-Science-Club/PS-2-keyboard-emulator/tree/main/#table-of-content)]
The hardware part is fairly simple here and involves not swapping wire coming from the arduino board.

+5V and ground could provide power to shift register, to go from serial data to parallel data as briefly mentionned [here](https://www.youtube.com/watch?v=7aXbh9VUB3U&t=1826s). They really should go the opposite direction in the real PS/2 keyboard setup, but the arduino already have access to power, so, be careful with these two lines.

clock and data lines are supposed to be connected to some interface between the keyboard and the host CPU.

Apart from this, hardware is pretty free :-)

## 2 The software. [[toc](https://github.com/Supaero-Computer-Science-Club/PS-2-keyboard-emulator/tree/main/#table-of-content)]
The software part of the emulator is split into two parts:
- first, key strokes are read by the python script, converted to valid PS/2 scancodes and sent to the arduino via the serial port.
- next, the arduino receives the scancodes, i.e. bytes, coming from the laptop's keyboard. The board then sends logic signal through its ports to whatever device is connected to it. The arduino board uses 4 lines to simulate the working of a PS/2 keyboard. There are two lines for power supply, i.e. +5V (red) and GND (brown), and two lines for clock (white) and serial data (purple). Only device-to-host protocol is implemented for now, i.e. 11-bit protocol (more information [here](http://www.burtonsys.com/ps2_chapweske.htm)).

## 3 Run the code. [[toc](https://github.com/Supaero-Computer-Science-Club/PS-2-keyboard-emulator/tree/main/#table-of-content)]
**Prerequisites**: install the `pynput` python module and make sure one is inside a python environment where `pynput` is active.  
Once the hardware is setup, one can run the code by following the steps below:
- upload the arduino side: `arduino --board arduino:avr:mega:cpu=atmega2560 --port <board_port> --upload src/arduino_side/arduino_side.ino`
- run the emulator: `python src/laptop_side.py`  

or run `make emulate` or `make`.  
One can look at the *parameters* section of the [makefile](makefile) and change any parameters by adding `PARAM_NAME=value` to the `make` command above.  
`device` and `host` also are available `make` *targets* and allow to run only part of the protocol.  
If one does not know the port name, please refer to the notes below.

Notes:
- the user might want to change the arduino's side parameters to his convenience, namely to adapt to slightly different hardware setups. This changes can be done in `src/arduino_side/arduino_side.ino` between lines 1 and 5, using the `#define` statements.
- the `src/laptop_side.py` script comes with some arguments the one can change. Please run `python src/laptop_side.py -h` for more details about them and their uses.
- to fully use the `makefile`, one might need to known the device port name. Simply connect the arduino to the host computer and run `./getports` which should spit out the ports where the devices are connected, and thus a usable port for the emulator protocol.
