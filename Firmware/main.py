import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import MatrixScanner
from kmk.keys import KC
from kmk.modules.rotary_encoder import RotaryEncoderHandler
from kmk.modules.layers import Layers
from kmk.extensions.display import Display, SSD1306, TextEntry

keyboard = KMKKeyboard()

layers = Layers()
keyboard.modules.append(layers)

keyboard.matrix = MatrixScanner(
    column_pins=[board.GP26, board.GP27, board.GP28],
    row_pins=[board.GP29, board.GP6, board.GP7],
    value_when_pressed=False,
)

# ALT   TAB   SPACE ( rotary encoder)
# SHIFT   W    CTRL
# A      S      D
keyboard.keymap = [
    [
        KC.A, KC.S, KC.D,        # bottom row
        KC.LSFT, KC.W, KC.LCTL,  # middle row
        KC.LALT, KC.TAB, KC.SPC  # top row
    ]
]

encoder = RotaryEncoderHandler(pin_a=board.GP2, pin_b=board.GP1)
encoder.rotation_cw = KC.VOLU
encoder.rotation_ccw = KC.VOLD
keyboard.modules.append(encoder)

i2c_bus = busio.I2C(board.GP3, board.GP4)
display_driver = SSD1306(i2c=i2c_bus)

display = Display(
    display=display_driver,
    entries=[
        TextEntry(text="Pressed:", x=0, y=0),
        TextEntry(text="---", x=60, y=0, name="pressed"),
    ],
    brightness=1,
)

keyboard.extensions.append(display)


def before_hid_send(kbd):
    pressed = kbd.keys_pressed
    if pressed:
        try:
            name = pressed[0].__repr__()
        except:
            name = "KEY"
        try:
            display.update_entry("pressed", name)
        except:
            pass
    else:
        try:
            display.update_entry("pressed", "---")
        except:
            pass

keyboard.before_hid_send = before_hid_send


if __name__ == '__main__':
    keyboard.go()
