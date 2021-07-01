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

import datetime


def calculate_phase(now: datetime.datetime = None) -> float:
    now = now or datetime.datetime.utcnow()

    # https://en.wikipedia.org/wiki/Linar_phase#Calculating_phase
    total_seconds = (now - datetime.datetime(1999, 8, 11).replace(tzinfo=now.tzinfo)).total_seconds()
    total_days = total_seconds / (60 * 60 * 24)
    PHASE_LENGTH = 29.530588853
    phase = (total_days % PHASE_LENGTH) / PHASE_LENGTH
    return phase


def phase_emoji(now: datetime.datetime = None):
    return chr(0x1F311 + round(calculate_phase(now=now) * 8))
