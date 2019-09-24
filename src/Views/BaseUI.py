#!/usr/bin/env python

import PyQt5.QtGui as qtg

class BaseView:
    """
    This is the base class for all Views in this project. Contains properties that should be consistent across the
    entire application.
    """

    def __init__(self):
        # Set the default font for all child Views
        self._baseFont = qtg.QFont("Helvetica Neue", 36, qtg.QFont.Bold)
        self.appName = 'UAS Performance Tracker'

    def get_font(self)->qtg.QFont:
        """
        Get the current default font for all child Views
        :return: The current font
        """
        return self._baseFont

    def set_font(self, font: qtg.QFont):
        """
        Set the default font for all child Views
        :param font: The font we want to change to
        :return: None
        """
        self._baseFont = font

    def del_font(self):
        """
        Delete function for the default font
        :return:
        """
        del self._baseFont

    def get_appName(self):
        """
        Getter for the name of the application
        :return:
        """
        return self.appName

    # Set the property to get, set and delete the base font
    Font = property(get_font, set_font, del_font)
