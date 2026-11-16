"""Approved-character cut-outs (extracted by extract_characters.py from the approved sheets). Heights in metres."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(HERE, '..', '_work', 'chars')
HEIGHT = {'emeka': 1.85, 'sam': 1.76, 'asha': 1.63}
_c = {}


def get(name):
    if name not in _c:
        _c[name] = Image.open(os.path.join(CH, name + '.png')).convert('RGBA')
    return _c[name]


def who(name):
    return name.split('_')[0]


def place(R, name, x, z, y=0.0, flip=False, shadow=True, op=0.34, tag=None):
    n = who(name)
    return R.billboard(get(name), x, z, HEIGHT[n], y=y, flip=flip, shadow=shadow, shadow_op=op, tag=tag or n)
