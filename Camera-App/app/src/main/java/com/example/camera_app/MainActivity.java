package com.example.camera_app;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;

/**
 * This main activity will then redirect to the camera activity once a tcp connection has
 * been established between the phone and the laptop.
 */
public class MainActivity extends AppCompatActivity {

    String ipaddr;
    int port;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    /**
     * Handles the click event for the connect button. Once clicked, the phone should take
     * the IP address in the IP address textbox and store the connection info for the laptop.
     * Then the phone should open a TCP connection to the laptop to receive control signals.
     */
    public void btnConnClk(View view)
    {

    }
}
