#!/usr/bin/env python

import PyQt5.QtGui as qtg

class BaseView:
    """
    This is the base class for all Views in this project. Contains properties that should be consistent across the
    entire application.
    """

    def __init__(self):
        # Set the default font for all child Views
        self.__titleFont = qtg.QFont("Helvetica Neue", 36, qtg.QFont.Bold)
        self.__mediumFont = qtg.QFont("Helvetica Neue", 24, qtg.QFont.Bold)
        self.__regularFont = qtg.QFont("Helvetica Neue", 14)
        self.__appName = 'UAS Performance Tracker'
        self.__teamMembers = ['Jonathan Westerfield', 'Hayley Eckert', 'Donald Elrod', 'Ismael Rodriguez', 'Ariana Boroujerdi']

    def getStrTeamMembers(self) -> str:
        """
        Allows us the get a string of the team members for the project to use in other parts of the application.
        :return: All of the team members in a string Ex: 'Jonathan Westerfield, Hayley Eckert, ..."
        """
        return ', '.join(self.__teamMembers)

    # region > Title Font Property
    @property
    def TitleFont(self) -> qtg.QFont:
        """
        Get the current default title font for all child Views
        :return: The current title font
        """
        return self.__titleFont

    @TitleFont.setter
    def set_font(self, font: qtg.QFont):
        """
        Set the default font for all child Views
        :param font: The font we want to change to
        :return: None
        """
        self.__titleFont = font

    @TitleFont.deleter
    def del_font(self):
        """
        Delete function for the default font
        :return:
        """
        del self.__titleFont
    # endregion

    #region > Regular Font Property
    @property
    def RegularFont(self) -> qtg.QFont:
        """
        Get the current default normal font for all child Views
        :return: The current normal font
        """
        return self.__regularFont

    @RegularFont.setter
    def set_regularFont(self, font: qtg.QFont):
        """
        Set the default normal font for all child Views
        :param font: The font we want to change to
        :return: None
        """
        self.__regularFont = font

    @RegularFont.deleter
    def del_regularFont(self):
        """
        Delete function for the default font
        :return:
        """
        del self.__regularFont
    #endregion

    #region > Medium Font Property
    @property
    def MediumFont(self):
        """
        Get the current default medium font for all child Views
        :return: The current Medium Font
        """
        return self.__mediumFont

    @MediumFont.setter
    def set_MediumFont(self, font: qtg.QFont):
        """
        Set the default normal font for all child Views.
        :param font: The font we want to change to
        :return: None
        """
        self.__mediumFont = font

    @MediumFont.deleter
    def del_MediumFont(self):
        """
        Deleter for the medium font.
        :return: None
        """
        del self.__mediumFont
    #endregion

    def get_appName(self) -> str:
        """
        Getter for the name of the application
        :return: The name of the application
        """
        return self.__appName

