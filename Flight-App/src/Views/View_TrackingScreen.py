import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from Controllers.PhoneController import PhoneControl
from datetime import datetime

class TrackingWindow(qtw.QWidget):
    """
    The view for the tracking view page that is shown when the user presses the "Start Tracking" button on the home page.
    Allows the user to enter in flight information and begin tracking the drone.

    :ivar __btnConfirm: The class property for the 'Confirm' button.
    :ivar __btnClear: The class property for the 'Clear' button.
    :ivar __btnStart: The class property for the 'Start Tracking' button.
    :ivar __btnStop: The class property for the 'Stop Tracking' button.
    """
    # Initialize signals. Use for switching between views.
    sigReturnHome = qtc.pyqtSignal()
    sigStopTracking = qtc.pyqtSignal()
    sigFlightInfoConfirmed = qtc.pyqtSignal(str, str, str)

    def __init__(self, phoneControl: PhoneControl) -> None:
        """
        Class Constructor
        """
        qtw.QWidget.__init__(self)
        self.setFixedSize(550, 550)
        self.phoneControl = phoneControl
        self.startedTracking = False
        self.initView()

    def initView(self) -> None:
        """
         Initializes and lays out all of the controls and elements on the view.

         :return: None
         """
        # Set up window
        self.setWindowTitle('Tracking Screen')

        # Initialize titles
        title = self.setTitle()
        sectionTitle = self.setSubTitle("Flight Information")
        self.status = self.setStatusLabel("Flight Status: Not Tracking")

        # Initialize textboxes
        pilot = self.setPilot()  # Setup the pilot textbox
        instructor = self.setInstructor()  # Setup the instructor textbox
        instructions = self.setFlightInstructions()  # Setup the flight Instructions text editor

        # Initialize labels and start/stop, clear/confirm, home buttons
        clrConfirm = self.setClrConfirmBtns()
        startStop = self.setStartAndStopBtns()
        homeBtn = qtw.QPushButton('Return to Home')

        # Attach functionality to stop and home buttons
        homeBtn.clicked.connect(self.returnHome)
        self.BtnStart.clicked.connect(self.startTracking)
        self.BtnStop.clicked.connect(self.stopTracking)

        # Initialize and attach functionality to clear, confirm buttons
        confirmBtn = self.BtnConfirm
        confirmBtn.clicked.connect(self.confirmValues)
        clearBtn = self.BtnClear
        clearBtn.clicked.connect(self.clearValues)

        # Spacer to make the view more pleasing and less squished
        verticalSpacer = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)

        # Layout the elements
        vLayout = qtw.QVBoxLayout()
        vLayout.addLayout(title)
        vLayout.addWidget(sectionTitle)
        vLayout.addLayout(pilot)
        vLayout.addLayout(instructor)
        vLayout.addLayout(instructions)
        vLayout.addLayout(clrConfirm)
        vLayout.addSpacerItem(verticalSpacer)
        vLayout.addWidget(self.status)
        vLayout.addLayout(startStop)
        vLayout.addWidget(homeBtn)

        # Attach the layout to the screen
        self.setLayout(vLayout)

    def returnHome(self) -> None:
        """
        Sends a signal to the main controller that the Return Home button was pushed.

        :return: none
        """
        self.sigReturnHome.emit()

    def startTracking(self) -> None:
        """
        Sends a signal to the main controller that the Start Tracking button was pushed.

        :return: none
        """
        if self.startedTracking is False:
            try:
                self.phoneControl.startRecording()
                self.startTrackingTime = datetime.now()
                msgBox = qtw.QMessageBox()
                msgBox.setText(
                    "Tracking started!")
                msgBox.exec()
                self.startedTracking = True
                self.status.setText("Flight Status: Tracking in Progress")
            except Exception as e:
                msgBox = qtw.QMessageBox()
                msgBox.setText(str(e))
                msgBox.exec()
        else:
            msgBox = qtw.QMessageBox()
            msgBox.setText(
                "Tracking has already been started.")
            msgBox.exec()

    def stopTracking(self) -> None:
        """
        Sends a signal to the main controller that the Stop Tracking button was pushed.

        :return: none
        """
        try:
            self.phoneControl.stopRecording()

            duration = datetime.now() - self.startTrackingTime
            maxTime = 600 # max time in seconds

            if duration.total_seconds() > maxTime:
                buttonReply = qtw.QMessageBox.question(self,
                                                       'Tracking Time Notification', "You have tracked for longer than "
                                                                                     "the maximum allowed time of "
                                                                                     "10 minutes. \n \n"
                                                                                     "Do you want to record a new run? "
                                                                                     "If so, press yes. \n"
                                                                                     "If you wish to analyze the first "
                                                                                     "10 minutes of this run instead, "
                                                                                     "press no. ",
                                                   qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.No)
                if buttonReply == qtw.QMessageBox.Yes:
                    self.status.setText("Flight Status: Tracking Halted.")
                    self.phoneControl.stopRecording()
                    self.startedTracking = False
                else:
                    msgBox = qtw.QMessageBox()
                    msgBox.setText(
                        "Tracking stopped! \nPlease wait while file transfer is initiated."
                        "\n You will be redirected shortly.")
                    msgBox.exec()
                    self.sigStopTracking.emit()
                    self.status.setText("Flight Status: Tracking Completed")

            else:
                msgBox = qtw.QMessageBox()
                msgBox.setText(
                    "Tracking stopped! \n"
                    "Please wait while file transfer is initiated.\n "
                    "You will be redirected shortly.")
                msgBox.exec()
                self.sigStopTracking.emit()
                self.status.setText("Flight Status: Tracking Completed")

        except Exception as e:
            msgBox = qtw.QMessageBox()
            msgBox.setText(str(e))
            msgBox.exec()

    def setTitle(self) -> qtw.QVBoxLayout:
        """
        Sets up the title with the application title on top and the name of the screen just below it.

        :return: Layout with the application title and screen title labels
        """
        lblTitle = qtw.QLabel("UAS Performance Tracker")
        lblTitle.setFont(qtg.QFont("Helvetica Neue", 36, qtg.QFont.Bold))
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        lblTitle2 = qtw.QLabel('Tracking View')
        lblTitle2.setFont(qtg.QFont("Helvetica Neue", 24, qtg.QFont.Bold))
        lblTitle2.setAlignment(qtc.Qt.AlignCenter)

        vbox = qtw.QVBoxLayout()
        vbox.addWidget(lblTitle)
        vbox.addWidget(lblTitle2)

        return vbox

    def setSubTitle(self, text) -> qtw.QLabel:
        """
        Sets up a subtitle label for the window

        :return: Subtitle of the application taken from the "text" parameter
        """
        lblTitle = qtw.QLabel(text)
        lblTitle.setFont(qtg.QFont("Helvetica Neue", 16, qtg.QFont.Bold))
        lblTitle.setAlignment(qtc.Qt.AlignLeft)

        return lblTitle

    def setStatusLabel(self, text) -> qtw.QLabel:
        """
        Sets up a status label for the window

        :return: Label of the application taken from the "text" parameter
        """
        lblTitle = qtw.QLabel(text)
        lblTitle.setFont(qtg.QFont("Helvetica Neue", 12, qtg.QFont.Bold))
        lblTitle.setAlignment(qtc.Qt.AlignCenter)

        return lblTitle

    def confirmValues(self) -> None:
        """
         Confirms the values in the textboxes by displaying a pop up message of the values.

         :return: None
         """
        pilotName = self.TBPilot.text()
        instructorName = self.TBInstructor.text()
        instructions = self.TEInstructions.toPlainText()
        self.sigFlightInfoConfirmed.emit(pilotName, instructorName, instructions)

        msgBox = qtw.QMessageBox()
        msgBox.setText(
            "Pilot Name: \n" + pilotName + "\nInstructor Name: \n" + instructorName + "\nInstructions: \n" + instructions)
        msgBox.exec()

    def clearValues(self) -> None:
        """
         Clears the values in the text boxes.

         :return: None
         """
        # TODO: Change cursor location out of text box so all boxes can clear at the same time
        self.TBPilot.setText('')
        qtw.QApplication.processEvents()
        self.TBInstructor.setText('')
        qtw.QApplication.processEvents()
        self.TEInstructions.clear()
        qtw.QApplication.processEvents()

    def setPilot(self) -> qtw.QVBoxLayout:
        """
        Sets up the Pilot label and the textbox that will be used to set the pilot flying during this
        session.

        :return: Returns a vertical layout with the pilot label over the pilot textbox
        """
        self.__lblPilot = qtw.QLabel('Pilot: ')
        self.__lblPilot.setAlignment(qtc.Qt.AlignLeft)

        self.__tbPilot = qtw.QLineEdit('')
        self.__tbPilot.setPlaceholderText('Pilot Name Here')
        self.__tbPilot.resize(280, 40)
        self.__tbPilot.setAlignment(qtc.Qt.AlignLeft)

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
        self.__lblInstr.setAlignment(qtc.Qt.AlignLeft)

        self.__tbInstr = qtw.QLineEdit()
        self.__tbInstr.setPlaceholderText('Instructor Name Here')
        self.__tbInstr.resize(280, 40)
        self.__tbInstr.setAlignment(qtc.Qt.AlignLeft)

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
        lblInstr = self.setSubTitle('Flight Instructions')

        self.__teInstr = qtw.QPlainTextEdit('')
        self.__teInstr.setPlaceholderText('Add Flight Instructions Here')

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
        lblTimerTitle.setAlignment(qtc.Qt.AlignCenter)

        self.__lblTimer = qtw.QLabel('00:00:00')
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
        space1 = qtw.QSpacerItem(100, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
        space2 = qtw.QSpacerItem(100, 40, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)

        buttonBox = qtw.QHBoxLayout()
        buttonBox.addSpacerItem(space1)
        buttonBox.addWidget(self.__btnStart)
        buttonBox.addWidget(self.__btnStop)
        buttonBox.addSpacerItem(space2)

        return buttonBox

    # region > Class Properties to attach functionality to in child classes

    # region > Pilot Textbox Property
    @property
    def TBPilot(self) -> qtw.QLineEdit:
        """
        Getter for the Pilot Textbox so we can attach functionality to it

        :return: The pilot textbox
        """
        return self.__tbPilot

    @TBPilot.setter
    def set_TBPilot(self, tb: qtw.QLineEdit) -> None:
        """
        Setter for the Pilot Textbox

        :param tb: Textbox we want to replace the current one with
        :return: None
        """
        self.__tbPilot = tb

    @TBPilot.deleter
    def del_TBPilot(self) -> None:
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
    def set_LblPilot(self, lbl: qtw.QLabel) -> None:
        """
        Setter for the pilot label

        :param lbl:  Label we want to replace the current one with
        :return: None
        """
        self.__lblPilot = lbl

    @LblPilot.deleter
    def del_LblPilot(self) -> None:
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
    def set_TBInstructor(self, tb: qtw.QLineEdit) -> None:
        """
        Setter for the instructor textbox

        :param tb: The textbox we want to replace the current one with
        :return: None
        """
        self.__tbInstr = tb

    @TBInstructor.deleter
    def del_TBInstructor(self) -> None:
        """
        Deleter for the instructor textbox

        :return: None
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
    def set_LblInstructor(self, lbl: qtw.QLabel) -> None:
        """
        Setter for the instructor label

        :param lbl: The label we want to replace the current one with
        :return: None
        """
        self.__lblInstr = lbl

    @LblInstructor.deleter
    def del_LblInstructor(self) -> None:
        """
        Deleter for the instructor label

        :return: None
        """
        del self.__lblInstr

    # endregion

    # region > Instructions TextEditBox Property
    @property
    def TEInstructions(self) -> qtw.QPlainTextEdit:
        """
        Getter for the instructions text edit box

        :return: Reference to the instructions text edit box
        """
        return self.__teInstr

    @TEInstructions.setter
    def set_TEInstructions(self, te: qtw.QPlainTextEdit) -> None:
        """
        Setter for the instructions text edit box

        :param te: The Text edit box we want to replace the current one with.
        :return: None
        """
        self.__teInstr = te

    @TEInstructions.deleter
    def del_TEInstructions(self) -> None:
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
    def set_BtnClear(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the clear button.

        :param btn: The button we want to replace the current one with.
        :return: None
        """
        self.__btnClear = btn

    @BtnClear.deleter
    def del_BtnClear(self) -> None:
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
    def set_BtnConfirm(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the confirm button.

        :param btn: The button we want to replace the current one with.
        :return: None
        """
        self.__btnConfirm = btn

    @BtnConfirm.deleter
    def del_BtnConfirm(self) -> None:
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
    def set_LblTimer(self, lbl: qtw.QLabel) -> None:
        """
        Setter for the LblTimer property.

        :param lbl: The label we want to replace the current one with.
        :return: None
        """
        self.__lblTimer = lbl

    @LblTimer.deleter
    def del_LblTimer(self) -> None:
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
    def set_BtnStart(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the start button.

        :param btn: Button we want to replace the current one with.
        :return: None
        """
        self.__btnStart = btn

    @BtnStart.deleter
    def del_BtnStart(self) -> None:
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
    def set_BtnStop(self, btn: qtw.QPushButton) -> None:
        """
        Setter for the stop button.

        :param btn: Button we want to replace the current one with.
        :return: None
        """
        self.__btnStop = btn

    @BtnStop.deleter
    def del_BtnStop(self) -> None:
        """
        Deleter for the stop button.
        
        :return: None
        """
        del self.__btnStop
    # endregion

    # endregion