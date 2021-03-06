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

import collections
import colorsys
import datetime
import logging
import math

from dateutil import relativedelta, tz
from PIL import Image, ImageDraw, ImageFont

from .resources import RESOURCES

NOW = RESOURCES / 'now'
LOG = logging.getLogger('now')
TIMEZONES = (
    # (name, tz)
    ("Auckland", tz.gettz("Pacific/Auckland")),
    ("Berlin", tz.gettz("Europe/Berlin")),
    ("Brisbane", tz.gettz("Australia/Brisbane")),
    ("Chicago", tz.gettz("America/Chicago")),
    ("Denver", tz.gettz("America/Denver")),
    ("L.A.", tz.gettz("America/Los_Angeles")),
    ("London", tz.gettz("Europe/London")),
    ("Moscow", tz.gettz("Europe/Moscow")),
    ("New York", tz.gettz("America/New_York")),
    ("Paris", tz.gettz("Europe/Paris")),
    ("Perth", tz.gettz("Australia/Perth")),
    ("Seoul", tz.gettz("Asia/Seoul")),
    ("Shanghai", tz.gettz("Asia/Shanghai")),
    ("Tokyo", tz.gettz("Asia/Tokyo")),
    ("Urumqi", tz.gettz("Asia/Urumqi")),
    ("Kolkata", tz.gettz("Asia/Kolkata")),
)


def create_colour_circle(size: int) -> Image.Image:
    # This function is the slow way to generate the colour circle used to tint the globe image.
    # In the actual function, a cached version is loaded instead
    LOG.info('Generating colour circle of size %dx%d', size, size)

    im = Image.new('RGB', (size, size), (0, 0, 0))

    for y in range(im.height):
        for x in range(im.width):
            # Get radius at this point
            radius = math.sqrt(
                pow(x - (im.width / 2), 2) +
                pow(y - (im.height / 2), 2)
            )

            radius /= size

            radius = min(radius, 0.5) * 2

            # Get angle at this point
            angle = math.atan2(
                (im.width / 2) - x,
                y - (im.height / 2),
            ) / (2 * math.pi)

            # Center to hour
            angle -= (0.5 / 12)

            if angle < 0.0:
                angle += 1.0

            radius = pow(radius, 3)

            r, g, b = colorsys.hsv_to_rgb(angle, radius, 0.5 + (radius / 2))
            r, g, b = (int(x * 255) for x in (r, g, b))

            im.putpixel((x, y), (r, g, b))

    return im


def generate(time: datetime.datetime) -> Image.Image:
    LOG.info('Loading outer ring')
    with Image.open(NOW / 'outer_ring.png') as outer_ring:
        outer_ring = outer_ring.convert('RGBA')

        utc = time.astimezone(tz.UTC)

        # Paste the globe in the middle
        LOG.info('Loading globe')
        with Image.open(NOW / 'globe.png') as globe:
            globe = globe.convert('RGBA')

            # Rotate by hours
            globe = globe.rotate(-15 * (utc.hour - 11.5))

            # Load the cached colour circle
            # To do the slow but cacheless method, replace this with:
            #   with create_colour_circle(globe.width) as colour_circle:
            LOG.info('Loading colour circle')
            with Image.open(NOW / 'colour_circle.png') as colour_circle:
                colour_circle = colour_circle.convert('RGB').resize(globe.size, Image.ANTIALIAS)

                # Paste in middle
                LOG.info('Pasting globe')
                outer_ring.paste(colour_circle, (
                    round((outer_ring.width - globe.width) / 2),
                    round((outer_ring.height - globe.height) / 2),
                ), mask=globe)

        # Collect up timezones
        LOG.info('Aggregating timezones')
        timezones = collections.defaultdict(list)

        for name, timezone in TIMEZONES:
            local_time = time.astimezone(timezone)
            timezones[local_time.hour].append(name)

        # Load font
        LOG.info('Loading font')
        font = ImageFont.truetype(str(RESOURCES / 'NotoSans-Bold.ttf'), 48)

        # Create text for each timezone segment
        for hour, timezones in timezones.items():
            LOG.info('Drawing hour %d', hour)
            with Image.new("RGBA", outer_ring.size, (0, 0, 0, 0)) as im:
                draw = ImageDraw.Draw(im)

                # Draw each timezone for this hour
                for offset, timezone in enumerate(timezones):
                    offset_y = (offset * font.size * 1.2) + int(im.height * 0.075)
                    offset_x = round(im.width / 2)

                    r, g, b = colorsys.hsv_to_rgb(hour / 24, 1.0, 1.0)
                    r, g, b = (int(x * 255) for x in (r, g, b))

                    draw.text(
                        (offset_x, offset_y),
                        text=timezone,
                        fill=(r, g, b, 255),
                        font=font,
                        anchor="ms",
                    )

                # Rotate by hour
                im = im.rotate(-15 * (hour - 11.5))

                # Paste in middle
                LOG.info('Pasting hour %d', hour)
                outer_ring.paste(im, (
                    round((outer_ring.width - im.width) / 2),
                    round((outer_ring.height - im.height) / 2),
                ), mask=im)

        # Return a copy to make sure the original file is closed
        LOG.info('Resizing output')
        return outer_ring.resize((1024, 1024), Image.ANTIALIAS)
