#!/usr/bin/env python

"""
Initializes the display, and holds common color values.
"""

import os
import sys

import pygame

import local_debug

# The SunFounder 5" TFT
DEFAULT_SCREEN_SIZE = 800, 480

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
YELLOW = (255, 255, 0)


def display_init():
    """
    Initializes PyGame to run on the current screen.
    """

    size = DEFAULT_SCREEN_SIZE
    disp_no = os.getenv('DISPLAY')
    if not disp_no:
        # List of drivers:
        # https://wiki.libsdl.org/FAQUsingSDL
        drivers = ['fbcon', 'directfb', 'svgalib', 'directx', 'windib']
        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)

            try:
                pygame.display.init()
            except pygame.error:
                print('Driver: {0} failed.'.format(driver))
                continue

            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        size = DEFAULT_SCREEN_SIZE
        # NOTE - HWSURFACE and DOUBLEBUF cause problems...
        # DOUBLEBUF
        # https://stackoverflow.com/questions/6395923/any-way-to-speed-up-python-and-pygame
        # pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        # TODO - Use "convert" on text without ALPHA...
        # https://en.wikipedia.org/wiki/PyPy

    screen_mode = pygame.HWACCEL
    if local_debug.is_debug():
        screen_mode |= pygame.RESIZABLE
    else:
        screen_mode |= pygame.FULLSCREEN

    screen = pygame.display.set_mode(size, screen_mode)
    display_info = pygame.display.Info()

    print("hw={}, wm={}, blit_hw={}".format(display_info.hw, display_info.wm, display_info.blit_hw))

    size = display_info.current_w, display_info.current_h

    return screen, size
