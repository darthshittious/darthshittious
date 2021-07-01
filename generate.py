# =*- coding: utf-8 -*-


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

import datetime
import logging
import logging.handlers
import pathlib
import sys

from dateutil import relativedelta, tz
from dateutil.tz import UTC

from readme import fractal, lunar_phase, now
from readme.templates import get_template


OUTPUT_RESOURCES = pathlib.Path('generated')
OUTPUT_README = pathlib.Path('README.md')

UTC_NOW = datetime.datetime.utcnow().replace(tzinfo=tz.UTC)

LOGGER: logging.Logger = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOG_FORMAT: logging.Formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
LOG_STREAM: logging.Handler = logging.StreamHandler(stream=sys.stdout)
LOG_STREAM.setFormatter(LOG_FORMAT)
LOGGER.addHandler(LOG_STREAM)

LOG = logging.getLogger('generate')


# generate now.png
LOG.info('Generating %s', OUTPUT_RESOURCES / 'now.png')
with open(OUTPUT_RESOURCES / 'now.png', 'wb') as output:
    with now.generate(UTC_NOW) as im:
        im.save(output, format='png')

# Generate fractal
LOG.info('Generating %s', OUTPUT_RESOURCES / 'fractal.png')
with open(OUTPUT_RESOURCES / 'fractal.png', 'wb') as output:
    with fractal.generate_fractal() as im:
        im.save(output, format='png')

# Get lunar phase
LOG.info('Getting lunar phase')
phase = lunar_phase.calculate_phase(UTC_NOW)
phase_emoji = lunar_phase.phase_emoji(UTC_NOW)

# Generate README.md
LOG.info('Generating %s', OUTPUT_README)
with open(OUTPUT_README, 'w', encoding='utf-8') as output:
    # Hour for the world clock
    hour = UTC_NOW.hour % 12
    if hour == 0:
        hour = 12

    hour_emoji = chr(0x1F54F + hour)

    # Year percentage bar
    current_year = UTC_NOW.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    next_year = current_year.replace(year=current_year.year + 1)
    current_seconds = (UTC_NOW - current_year).total_seconds()
    total_seconds = (next_year - current_year).total_seconds()

    year_percentage = (current_seconds / total_seconds)
    filled_blocks = int(year_percentage * 20)

    percentage_bar = ''.join((['\N{FULL BLOCK}'] * filled_blocks) + (['\N{LOWER ONE EIGHTH BLOCK}'] * (20 - filled_blocks)))

    output.write(get_template('README.md').render(
        hour_emoji=hour_emoji,
        now=UTC_NOW,
        percentage_bar=percentage_bar,
        phase=phase,
        phase_emoji=phase_emoji,
        year_percentage=year_percentage,
    ))
