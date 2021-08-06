import serial
import time
from pynput import keyboard
import json
import codecs
from pprint import pprint
import argparse


def ino_wrapper(func, device, scancodes):
    """
        A wrapper that takes care of all possible expections, expecially I/O ones.
        This wrapper has two main purposes:
            - avoiding the laptop<->arduino communication to stop because of bugs.
            - looking for exact expections origin to correct them and make the 
            communication more robust.

        Args
        ----
        func : function
            the function to wrap, namely on_press or on_release, which read the
            keyboard strokes.
        device : serial.serialposix.Serial
            the device to communicate with, namely an arduino board.
        scancodes : dict
            a dictionary of scancodes used by the communication protocol.

        Returns
        -------
        wrapped_func : function
            the wrapped function, doing the same thing, with extra arguments and
            expection handling to avoid communication protocol failures.
    """
    def wrapped_func(*args, **kwargs):
        try:
            func(*args, device=device, scancodes=scancodes, **kwargs)
        except Exception as e:  # looking for real exceptions to handle, temporary.
            print(f"EXCEPTION of type {type(e)} SKIPPED:", e)
    return wrapped_func


def on_press(key, device, scancodes, prt=print):
    """
        Takes care of keys being pressed.
        Send the appropriate scancode to the micro-controller interface.

        Args
        ----
        key : keyboard._xorg.KeyCode or Key enum.
            a key object given by the pynput.keyboad module, whenever a key is pressed.
        device : serial.serialposix.Serial
            the device to communicate with, namely an arduino board.
        scancodes : dict
            a dictionary of scancodes used by the communication protocol.
        prt : function, optional
            a print-like function. Might be void if no verbose.
    """
    # different treatment based on the key type.
    if isinstance(key, keyboard._xorg.KeyCode):
        scancode = scancodes[key.char.lower()]
        prt()
    else:
        scancode = scancodes[key.name.lower()]
        prt(f"{key.name.lower()}")

    # send 0xe0 if scancode is extended.
    if scancode.startswith("E0"):
        send_scancode(scancode[:2], device)
        send_scancode(scancode[2:], device)
    else:
        send_scancode(scancode, device)


def on_release(key, device, scancodes):
    """
        Takes care of keys being released.
        Send the appropriate scancode to the micro-controller interface.

        Args
        ----
        key : keyboard._xorg.KeyCode or Key enum.
            a key object given by the pynput.keyboad module, whenever a key is released.
        device : serial.serialposix.Serial
            the device to communicate with, namely an arduino board.
        scancodes : dict
            a dictionary of scancodes used by the communication protocol.
    """
    # different treatment based on the key type.
    if isinstance(key, keyboard._xorg.KeyCode):
        scancode = scancodes[key.char.lower()]
    else:
        scancode = scancodes[key.name.lower()]

    # send 0xe0 0xf0 if scancode is extended.
    if scancode.startswith("E0"):
        send_scancode(scancode[:2], device)
        send_scancode("F0", device)
        send_scancode(scancode[2:], device)
    else:
        send_scancode("F0", device)
        send_scancode(scancode, device)


def to_bin(number, nb_bits=8):
    """
        Converts an integer to binary with a given number of bits.

        Args
        ----
        number : int
            the number to convert to binary.
        nb_bits  : int, optional
            the number of bits.

        Returns:
        bin : str
            the string binary representation of the number, with 'nb_bits' bits.
    """
    return bin(number)[2:][::-1].ljust(nb_bits,'0')[::-1]


def send_scancode(scancode, device, prt=print):
    """
        Send a given scancode to the device.

        Args
        ----
        scancode : str
            a hex representation of the scancode. A scancode is here 8-bit, i.e. 2 characters.
        device : serial.serialposix.Serial
            the device to communicate with, namely an arduino board.
        prt : function, optional
            a print-like function. Might be void if no verbose.

        Returns:
        none
    """
    byte = int(scancode, 16)  # convert to hex.
    prt(f"\t{scancode} - ({byte:3d}, {hex(byte)}, {to_bin(byte)})", end=" -> ")
    written = device.write(bytes(chr(byte), "latin-1"))  # send to device.
    prt(f"{written = }")


def main():
    parser = argparse.ArgumentParser("An argument parser that allows control over the keyboard emulator.")

    parser.add_argument("--port", "-p", type=str, default="/dev/ttyACM0",
                        help="the port to communicate with the Arduino board (defaults to '/dev/ttyACM0').")
    parser.add_argument("--baudrate", "--rate", "-r", type=int, default=115200,
                        help="the baudrate of the communication (defaults to 115200 bauds).")
    parser.add_argument("--scancodes", "-s", default="res/scancodes_set2.json",
                        help="the location of the PS/2 protocol scancodes (defaults to 'res/scancodes_set2.json').")
    parser.add_argument("--encoding", "-e", default="utf-8-sig",
                        help="the encoding used in the .json scancodes file (defaults to 'utf-8-sig').")

    args = parser.parse_args()

    # connect to the arduino.
    arduino = serial.Serial(port=args.port, baudrate=args.baudrate, timeout=.1)

    # load the scancodes.
    with codecs.open(args.scancodes, 'r', args.encoding) as scancodes_file:
        scancodes = json.load(scancodes_file)
    
    # collect events until released.
    with keyboard.Listener(
            on_press=ino_wrapper(on_press, arduino, scancodes),
            on_release=ino_wrapper(on_release, arduino, scancodes)) as listener:
        print("PRESS <ctrl>c TO EXIT THIS API.")
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("clean exit")


