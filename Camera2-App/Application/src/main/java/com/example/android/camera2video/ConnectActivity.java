package com.example.android.camera2video;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.net.UnknownHostException;

public class ConnectActivity extends Activity
{
    String ipaddr, username, password;
    int port;

    Button btnConnect;
    TextView tbIPAddr;
    TextView tbPortNum;
    TextView tbUsername;
    TextView tbPassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connect);
        init();

        // Allows us to run network functions on the main thread
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
    }

    /**
     * Initializes the view and associates all of the view controls with class members
     * in this class.
     */
    public void init()
    {
        this.btnConnect = (Button) findViewById(R.id.btnConnect);
        this.tbIPAddr = (TextView) findViewById(R.id.tbIPAddress);
        this.tbPortNum = (TextView) findViewById(R.id.tbPortNum);
        this.tbUsername = (TextView) findViewById(R.id.tbUsername);
        this.tbPassword = (TextView) findViewById(R.id.tbPassword);
    }

    /**
     * Handles the click event for the connect button. Once clicked, the phone should take
     * the IP address in the IP address textbox and store the connection info for the laptop.
     * Then the phone should open a TCP connection to the laptop to receive control signals.
     */
    public void btnConnClk(View view)
    {
        this.ipaddr = this.tbIPAddr.getText().toString();
        this.port = Integer.parseInt(this.tbPortNum.getText().toString());
        this.username = this.tbUsername.getText().toString();
        this.password = this.tbPassword.getText().toString();

        try
        {
            // Setup the connection
            NetConn conn = NetConn.getInstance()
                    .setIPAddress(this.ipaddr)
                    .setPortNumber(this.port)
                    .setUsername(this.username)
                    .setPassword(this.password);

            conn.createConn();
            conn.createFTPConn();

            switchToCameraActivity();
        }
        catch (UnknownHostException e)
        {
            Log.e("ERROR", e.getMessage());
            showFailedConnectionAlert(view, "Unknown Host Exception", e.getMessage());

        }
        catch (InstantiationException e)
        {
            Log.e("ERROR", e.getMessage());
            showFailedConnectionAlert(view, "Instantiation Exception", e.getMessage());
        }
        catch (IOException e)
        {
            Log.e("ERROR", e.getMessage());
            showFailedConnectionAlert(view, "IOException", e.getMessage());
        }
    }

    public void switchToCameraActivity()
    {
        Intent cameraIntent = new Intent(this, CameraActivity.class);
        startActivity(cameraIntent);
    }

    public void showFailedConnectionAlert(View view, String title, String message)
    {
        this.tbIPAddr.setText("");
        this.tbPortNum.setText("");

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle(title)
                .setMessage(message)
                .setNeutralButton("OK", null);

        AlertDialog dialog = builder.create();
        dialog.show();
    }
}
