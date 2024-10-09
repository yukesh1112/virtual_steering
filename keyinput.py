import ctypes

# Dictionary for virtual key codes
keys = {
    "w": 0x11,
    "a": 0x1E,
    "s": 0x1F,
    "d": 0x20,
}

# Pointer type for extra info
PUL = ctypes.POINTER(ctypes.c_ulong)

# Structure for keyboard input
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),      # Virtual key code (not used here, set to 0)
                ("wScan", ctypes.c_ushort),    # Scan code (we'll use this)
                ("dwFlags", ctypes.c_ulong),   # Flags (press or release)
                ("time", ctypes.c_ulong),      # Timestamp (not used, set to 0)
                ("dwExtraInfo", PUL)]          # Extra information (pointer to ulong)

# Structure for hardware input (not used)
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

# Structure for mouse input (not used)
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

# Union structure for input (Keyboard, Mouse, Hardware)
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

# Main input structure
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Function to press a key
def press_key(key):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, keys[key], 0x0008, 0, ctypes.pointer(extra))  # 0x0008 is KEYEVENTF_SCANCODE for key press
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Function to release a key
def release_key(key):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, keys[key], 0x0008 | 0x0002, 0, ctypes.pointer(extra))  # 0x0002 is KEYEVENTF_KEYUP for key release
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
