/*
 * Copyright 2014 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example.android.camera2video;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

import com.jcraft.jsch.JSchException;

import java.io.IOException;

/**
 * I pulled this code from the Google examples. This activity uses the Camera2VideoFragment
 * in order to take video from the camera. This implements the observer pattern which listens
 * to the signals from the Readloop class so we can control the camera and tell it to start and
 * stop recording. This class also calls the controls needed to transfer the video file to the
 * laptop once the recording has finished.
 *
 * @author Jonathan Westerfield
 * @version 1.0.3
 */
public class CameraActivity extends Activity implements Observer
{
    private Camera2VideoFragment cameraFrag;
    private NetConn conn;
    private final String TAG = "CameraActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        cameraFrag = Camera2VideoFragment.newInstance();
        conn = NetConn.getInstance();
        conn.getReadLoop().addObserver(this); // add the Camera fragment as an observer
        conn.startReadLoop();

        if (null == savedInstanceState) {
            getFragmentManager().beginTransaction()
                    .replace(R.id.container, cameraFrag)
                    .commit();

        }

    }

//    /**
//     * This is for when the phone gets rotated. When the phone rotates or changes orientation,
//     * application state is lost. This means that the network connectivity in the NetConn Singleton
//     * also gets lost. This function should save that NetConn instance and hopefully keep the
//     * connection open. This gets called when the application state is deleted.
//     * @param savedInstanceState The bundle that contains the application state.
//     */
//    @Override
//    protected void onSaveInstanceState(Bundle savedInstanceState)
//    {
//        super.onSaveInstanceState(savedInstanceState);
//        savedInstanceState.putSerializable("netconn", NetConn.getInstance());
//    }
//
//    /**
//     * This is for when the phone changes orientation. When the phone changes orientation,
//     * the application state is deleted. This leads to the NetConn class getting deleted. This
//     * function is called when the application is looking to reload the application state.
//     * @param savedInstanceState The bundle that contains the application state.
//     */
//    @Override
//    public void onRestoreInstanceState(Bundle savedInstanceState) {
//        super.onRestoreInstanceState(savedInstanceState);
//        // Restore UI state from the savedInstanceState.
//        // This bundle has also been passed to onCreate.
//        // TODO: figure out how to do a deep copy on this and set the Singleton to what was saved
////        NetConn.getInstance() = (NetConn) savedInstanceState.getSerializable("netconn");
//    }

    /**
     * The update function for this application. We need to listen for network signals so
     * we can start/stop recording and file transferring.
     * @param signal The signal type that was received from the laptop.
     * @param message The optional message that accompanied the signal.
     */
    public void update(Signal signal, String message)
    {
        try
        {
            switch(signal)
            {
                case START:
                    NetConn.getInstance().setPhoneID(message.trim()); // set the phone ID with the start message
                    cameraFrag.startRecordingVideo();
                    conn.sendMessage(Signal.START_ACKNOWLEDGE.toString());
                    break;
                case STOP:
                    cameraFrag.stopRecordingVideo();
                    conn.sendMessage(Signal.STOP_ACKNOWLEDGE.toString());
                    break;
                case START_FTP:
                    conn.sendMessage(Signal.START_FTP_ACKNOWLEDGE.toString());
                    conn.getFtpConn().setupConn();
                    conn.getFtpConn().setDestFilePath(message);
                    conn.getFtpConn().upload(); // Start the file transfer
                    break;
            }
        }
        catch(JSchException e)
        {
            String errMess = Integer.toString(e.getStackTrace()[0].getLineNumber()) + e.getMessage();
            Log.e(TAG, errMess);
        }
        catch (IOException e)
        {
            String errMess = Integer.toString(e.getStackTrace()[0].getLineNumber()) + e.getMessage();
            Log.e(TAG, errMess);
        }
    }
}
