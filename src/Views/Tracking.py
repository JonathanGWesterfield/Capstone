#!/usr/bin/env python
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from src.Views.BaseUI import BaseView

class TrackingView(BaseView):
    """
    This is the screen view that allows the user to input the pilot and instructor information,
    and start tracking the drone. This is just a view so the functionality in the controls need
    to be implemented in a child controller class.
    """

    def __init__(self):
        """
        Class Constructor
        """
        super().__init__()
        self.initView()

    def initView(self):
        """
        Initializes and lays out all of the controls and elements on the view.
        :return: None
        """
        title = self.setTitle() # Setup the title label

        pilot = self.setPilot() # Setup the pilot textbox

        instructor = self.setInstructor() # Setup the instructor textbox

        instructions = self.setFlightInstructions() # Setup the flight Instructions text editor

        clrConfirm = self.setClrConfirmBtns()

        # Spacer to make the view more pleasing and less squished
        verticalSpacer = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)

        timer = self.setTimerLabel() # Get the label for the timer

        startStop = self.setStartAndStopBtns()


        vLayout = qtw.QVBoxLayout()
        vLayout.addWidget(title)
        vLayout.addLayout(pilot)
        vLayout.addLayout(instructor)
        vLayout.addLayout(instructions)
        vLayout.addLayout(clrConfirm)
        vLayout.addSpacerItem(verticalSpacer)
        vLayout.addLayout(timer)
        vLayout.addLayout(startStop)

        # Attach the layout to the screen
        self.window = qtw.QWidget()
        self.window.setLayout(vLayout)

    def setTitle(self) -> qtw.QLabel:
        """
        Sets up the title label for the window
        :return: Title of the application taken from the base class
        """
        lblTitle = qtw.QLabel(self.get_appName())
        lblTitle.setFont(self.TitleFont)
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        return lblTitle

    def setPilot(self) -> qtw.QVBoxLayout:
        """
        Sets up the Pilot label and the textbox that will be used to set the pilot flying during this
        session.
        :return: Returns a vertical layout with the pilot label over the pilot textbox
        """
        self.__lblPilot = qtw.QLabel('Pilot: ')
        self.__lblPilot.setFont(self.RegularFont)
        self.__lblPilot.setAlignment(qtc.Qt.AlignCenter)

        self.__tbPilot = qtw.QLineEdit()
        self.__tbPilot.resize(280,40)
        self.__tbPilot.setAlignment(qtc.Qt.AlignCenter)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.__lblPilot)
        vbox.addWidget(self.__tbPilot)

        return vbox

    def setInstructor(self) -> qtw.QVBoxLayout:
        """
        Sets up the instructor label and the textbox that will be used to set the instructor flying during this
        session.
        :return: Returns a vertical layout with the instructor label over the instructor textbox
        """
        self.__lblInstr = qtw.QLabel('Instructor: ')
        self.__lblInstr.setFont(self.RegularFont)
        self.__lblInstr.setAlignment(qtc.Qt.AlignCenter)

        self.__tbInstr = qtw.QLineEdit()
        self.__tbInstr.resize(280, 40)
        self.__tbInstr.setAlignment(qtc.Qt.AlignCenter)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.__lblInstr)
        vbox.addWidget(self.__tbInstr)

        return vbox

    def setFlightInstructions(self) -> qtw.QVBoxLayout:
        """
        Sets the textbox that will allow the instructor to type in the flight instructions for the pilot
        to try to match.
        :return: A vertical layout with the Instructions label on top of the text box
        """
        lblInstr = qtw.QLabel('Flight Instructions')
        lblInstr.setFont(self.RegularFont)
        lblInstr.setAlignment(qtc.Qt.AlignCenter)

        self.__teInstr = qtw.QPlainTextEdit('Add Flight Instructions Here')

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(lblInstr)
        vbox.addWidget(self.__teInstr)

        return vbox

    def setClrConfirmBtns(self) -> qtw.QHBoxLayout:
        """
        Sets the buttons for clearing and confirming the pilot, instructor, and flight instruction information.
        :return: The confirmation button
        """
        self.__btnClear = qtw.QPushButton('Clear')
        self.__btnConfirm = qtw.QPushButton('Confirm')
        space1 = qtw.QSpacerItem(100, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        space2 = qtw.QSpacerItem(100, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)

        hbox = qtw.QHBoxLayout()
        hbox.addSpacerItem(space1)
        hbox.addWidget(self.__btnClear)
        hbox.addWidget(self.__btnConfirm)
        hbox.addSpacerItem(space2)

        return hbox

    def setTimerLabel(self) -> qtw.QVBoxLayout:
        """
        Sets the label that will continuously update and display the time that the application has been
        actively tracking. Need to attach a QTimer() to it.
        :return: The label that will contain the timer.
        """
        lblTimerTitle = qtw.QLabel('Time Spent Tracking Drone:')
        lblTimerTitle.setFont(self.RegularFont)
        lblTimerTitle.setAlignment(qtc.Qt.AlignCenter)

        self.__lblTimer = qtw.QLabel('00:00:00')
        self.__lblTimer.setFont(self.RegularFont)
        self.__lblTimer.setAlignment(qtc.Qt.AlignCenter)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(lblTimerTitle)
        vbox.addWidget(self.__lblTimer)

        return vbox

    def setStartAndStopBtns(self) -> qtw.QHBoxLayout:
        """
        Sets up the start and stop buttons for tracking the drones.
        :return:
        """

        self.__btnStart = qtw.QPushButton('Start Tracking')
        self.__btnStop = qtw.QPushButton('Stop Tracking')

        buttonBox = qtw.QHBoxLayout()
        buttonBox.addWidget(self.__btnStart)
        buttonBox.addWidget(self.__btnStop)

        return buttonBox

    def showWindow(self):
        """
        Takes all of the elements from the view and displays the window.
        :return: None
        """
        self.window.show()
        # self.app.exec_()

    #region > Class Properties to attach functionality to in child classes

    # region > Pilot Textbox Property
    @property
    def TBPilot(self) -> qtw.QLineEdit:
        """
        Getter for the Pilot Textbox so we can attach functionality to it
        :return: The pilot textbox
        """
        return self.__tbPilot

    @TBPilot.setter
    def set_TBPilot(self, tb: qtw.QLineEdit):
        """
        Setter for the Pilot Textbox
        :param tb: Textbox we want to replace the current one with
        :return: None
        """
        self.__tbPilot = tb

    @TBPilot.deleter
    def del_TBPilot(self):
        """
        Deleter for the pilot textbox
        :return: None
        """
        del self.__tbPilot

    # endregion

    # region > Pilot Label Property
    @property
    def LblPilot(self) -> qtw.QLabel:
        """
        Getter for the Pilot label so we can attach functionality to it
        :return: The pilot label
        """
        return self.__lblPilot

    @LblPilot.setter
    def set_LblPilot(self, lbl: qtw.QLabel):
        """
        Setter for the pilot label
        :param lbl:  Label we want to replace the current one with
        :return: None
        """
        self.__lblPilot = lbl

    @LblPilot.deleter
    def del_LblPilot(self):
        """
        Deleter for the pilot label
        :return: None
        """
        del self.__lblPilot

    # endregion

    # region > Instructor TextBox Property
    @property
    def TBInstructor(self) -> qtw.QLineEdit:
        """
        Getter for the Instructor textbox so we can attach functionality to it later.
        :return: The instructor textbox
        """
        return self.__tbInstr

    @TBInstructor.setter
    def set_TBInstructor(self, tb: qtw.QLineEdit):
        """
        Setter for the instructor textbox
        :param tb: The textbox we want to replace the current one with
        :return: None
        """
        self.__tbInstr = tb

    @TBInstructor.deleter
    def del_TBInstructor(self):
        """
        Deleter for the instructor textbox
        :return:
        """
        del self.__tbInstr

    # endregion

    # region > Instructor Label Property
    @property
    def LblInstructor(self) -> qtw.QLabel:
        """
        Getter for the Instructor label so we can attach functionality to it later.
        :return: The instructor label
        """
        return self.__lblInstr

    @LblInstructor.setter
    def set_LblInstructor(self, lbl: qtw.QLabel):
        """
        Setter for the instructor label
        :param lbl: The label we want to replace the current one with
        :return: None
        """
        self.__lblInstr = lbl

    @LblInstructor.deleter
    def del_LblInstructor(self):
        """
        Deleter for the instructor label
        :return: None
        """
        del self.__lblInstr

    # endregion

    #region > Instructions TextEditBox Property
    @property
    def TEInstructions(self) -> qtw.QPlainTextEdit:
        """
        Getter for the instructions text edit box
        :return: Reference to the instructions text edit box
        """
        return self.__teInstr

    @TEInstructions.setter
    def set_TEInstructions(self, te: qtw.QPlainTextEdit):
        """
        Setter for the instructions text edit box
        :param te: The Text edit box we want to replace the current one with.
        :return: None
        """
        self.__teInstr = te

    @TEInstructions.deleter
    def del_TEInstructions(self):
        """
        Deleter for the Instructions Text edit box
        :return: None
        """
        del self.__teInstr
    # endregion

    # region > Clear Button Property
    @property
    def BtnClear(self) -> qtw.QPushButton:
        """
        Getter for the Clear button so we can attach functionality to it later.
        :return: Reference to the clear button
        """
        return self.__btnClear

    @BtnClear.setter
    def set_BtnClear(self, btn: qtw.QPushButton):
        """
        Setter for the clear button.
        :param btn: The button we want to replace the current one with.
        :return: None
        """
        self.__btnClear = btn

    @BtnClear.deleter
    def del_BtnClear(self):
        """
        Deleter for the clear button.
        :return: None
        """
        del self.__btnClear

    # endregion

    # region > Confirmation Button Property
    @property
    def BtnConfirm(self) -> qtw.QPushButton:
        """
        Getter for the Confirm button so we can attach functionality to it later.
        :return: Reference to the confirm button
        """
        return self.__btnConfirm

    @BtnConfirm.setter
    def set_BtnConfirm(self, btn: qtw.QPushButton):
        """
        Setter for the confirm button.
        :param btn: The button we want to replace the current one with.
        :return: None
        """
        self.__btnConfirm = btn

    @BtnConfirm.deleter
    def del_BtnConfirm(self):
        """
        Deleter for the confirm button.
        :return: None
        """
        del self.__btnConfirm

    # endregion

    # region > Timer Label Property
    @property
    def LblTimer(self) -> qtw.QLabel:
        """
        Getter property for the timer label. We need to attach a QTimer to it so it can count the time the
        application has been tracking the drone.
        :return: The timer label
        """
        return self.__lblTimer

    @LblTimer.setter
    def set_LblTimer(self, lbl: qtw.QLabel):
        """
        Setter for the LblTimer property.
        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblTimer = lbl

    @LblTimer.deleter
    def del_LblTimer(self):
        """
        Deleter for the timer label.
        :return: None
        """
        del self.__lblTimer

    # endregion

    # region > Start Button Property
    @property
    def BtnStart(self) -> qtw.QPushButton:
        """
        Getter for the Start button
        :return: Reference to the start button
        """
        return self.__btnStart

    @BtnStart.setter
    def set_BtnStart(self, btn: qtw.QPushButton):
        """
        Setter for the start button.
        :param btn: Button we want to replace the current one with.
        :return: None
        """
        self.__btnStart = btn

    @BtnStart.deleter
    def del_BtnStart(self):
        """
        Deleter for the start button.
        :return: None
        """
        del self.__btnStart

    # endregion

    # region > Stop Button Property
    @property
    def BtnStop(self) -> qtw.QPushButton:
        """
        Getter for the Stop button
        :return: Reference to the stop button
        """
        return self.__btnStop

    @BtnStop.setter
    def set_BtnStop(self, btn: qtw.QPushButton):
        """
        Setter for the stop button.
        :param btn: Button we want to replace the current one with.
        :return: None
        """
        self.__btnStop = btn

    @BtnStop.deleter
    def del_BtnStop(self):
        """
        Deleter for the stop button.
        :return: None
        """
        del self.__btnStop
    # endregion

    #endregion



app = qtw.QApplication([])


ui = TrackingView()
ui.showWindow()

app.exec()


