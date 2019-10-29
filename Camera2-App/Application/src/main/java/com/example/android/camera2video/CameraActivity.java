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

import java.io.IOException;

public class CameraActivity extends Activity implements Observer
{
    Camera2VideoFragment cameraFrag;
    NetConn conn;

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
                    cameraFrag.startRecordingVideo();
                    conn.sendMessage(Signal.START_ACKNOWLEDGE.toString());
                    break;
                case STOP:
                    cameraFrag.stopRecordingVideo();
                    conn.sendMessage(Signal.STOP_ACKNOWLEDGE.toString());
                    break;
                case START_FTP:
                    // TODO: PUT THE FILE TRANSFER FUNCTION CALL HERE
                    conn.sendMessage(Signal.START_FTP_ACKNOWLEDGE.toString());
                    break;
            }
        }
        catch (IOException e)
        {
            Log.e("ERROR", e.getMessage());
        }
    }

    // TODO: FIX THE CALLEDFROMWRONGTHREADEXCEPTION using this 'https://stackoverflow.com/questions/5161951/android-only-the-original-thread-that-created-a-view-hierarchy-can-touch-its-vi'
}
