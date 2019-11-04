package com.example.android.camera2video;

/**
 * Enumeration for different signals that can be handled by this app.
 *
 * @author Jonathan Westerfield
 * @version 1.0.0
 */
public enum Signal
{
    /**
     * Signal to tell the camera to start recording video.
     */
    START,

    /**
     * Signal to tell the camera to stop recording video.
     */
    STOP,

    /**
     * Signal to tell the laptop that this phone acknowledges the signal to start recording video.
     */
    START_ACKNOWLEDGE,

    /**
     * Signal to tell the laptop that this phone acknowledges the signal to stop recording video.
     */
    STOP_ACKNOWLEDGE,

    /**
     * Signal to tell the phone to start transferring the recorded video file to the laptop for analysis.
     */
    START_FTP,

    /**
     * Signal to tell the laptop that this phone acknowledges the signal to start transferring the
     * recorded video file to the laptop.
     */
    START_FTP_ACKNOWLEDGE,

    /**
     * Signal to tell the laptop that the file transfer of moving the video file to the laptop
     * finished and was successful.
     */
    FTP_COMPLETED,

    /**
     * A signal for this application to recognize that a signal that came from the laptop was
     * not a recognized signal and is therefore illegal.
     */
    ILLEGAL,

    /**
     * This is a signal in case there was no signal sent from the laptop. SHOULD NEVER BE USED.
     */
    NULL
}
