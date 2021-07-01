# -*- coding: utf-8 -*-


# MIT License

# Copyright (c) 2021 Devon (Gorialis) R, Jamie Sinclair [jamsinclair/open-anki-jlpt-decks]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import colorsys
import random
import typing
import math
import logging

from PIL import Image


LOG = logging.getLogger('fractal')


def generate_fractal(
        width: int = 1024, height: int = 1024,
        colour: typing.Tuple[float, float, float] = None,
        c: complex = None
) -> Image.Image:
    im = Image.new('RGB', (width, height), (0, 0, 0))
    colour = colour or colorsys.hsv_to_rgb(random.random(), 1.0, 1.0)
    c = c or complex((random.random() - 0.5) * 2, (random.random() - 0.5) * 2)
    colour = tuple(int(x * 255) for x in colour)

    # Create fractal mix layer
    LOG.info('Creating fractal mix layer.')
    with Image.new('L', (width, height), 0) as mix_layer:
        for y in range(mix_layer.height):
            for x in range(mix_layer.width):
                # Map to coordinate space
                z = complex(((x / mix_layer.width) - 0.5) * 4, ((y / mix_layer.height) - 0.5) * 4)
                value = 0

                # Calculate fractal
                for iteration in range(100):
                    z = (z ** 2) + c  # Julia fractal
                    if abs(z) > 4:
                        value = ((iteration / 100) * 0.8) + 0.2
                        break

                mix_layer.putpixel((x, y), int(value * 255))

        LOG.info('Finished creating fractal mix layer.')

        # Mix with colour
        with Image.new('RGB', (width, height), colour) as fill:
            LOG.info('Pasting with mix layer.')
            im.paste(fill, (0, 0), mask=mix_layer)

    return im
