package com.example.camera_app;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.karumi.dexter.Dexter;
import com.karumi.dexter.MultiplePermissionsReport;
import com.karumi.dexter.PermissionToken;
import com.karumi.dexter.listener.PermissionRequest;
import com.karumi.dexter.listener.multi.MultiplePermissionsListener;

import java.io.IOException;
import java.net.UnknownHostException;
import java.util.List;


/**
 * This main activity will then redirect to the camera activity once a tcp connection has
 * been established between the phone and the laptop.
 */
public class MainActivity extends AppCompatActivity
{
    static final int REQUEST_VIDEO_CAPTURE = 1;

    String ipaddr;
    int port;
    Button btnConnect;
    TextView tbIPAddr;
    TextView tbPortNum;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        init();
    }

    public void init()
    {
        this.btnConnect = (Button) findViewById(R.id.btnConnect);
        this.tbIPAddr = (TextView) findViewById(R.id.tbIPAddress);
        this.tbPortNum = (TextView) findViewById(R.id.tbPortNum);
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

        NetConn conn = NetConn.getInstance()
                .setIPAddress(this.ipaddr)
                .setPortNumber(this.port);

        switchToCameraActivity();


//        try
//        {
//            conn.createConn();
//        }
//        catch (UnknownHostException e)
//        {
//            Log.e("ERROR", e.getMessage());
//            showFailedConnectionAlert(view, "Unknown Host Exception", e.getMessage());
//
//        }
//        catch (InstantiationException e)
//        {
//            Log.e("ERROR", e.getMessage());
//            showFailedConnectionAlert(view, "Instantiation Exception", e.getMessage());
//        }
//        catch (IOException e)
//        {
//            Log.e("ERROR", e.getMessage());
//            showFailedConnectionAlert(view, "IOException", e.getMessage());
//        }
    }

    public void switchToCameraActivity()
    {
        Intent cameraIntent = new Intent(this, Camera.class);
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

    // TODO: CREATE ALERTS FOR ERROR MESSAGE AND WHEN THINGS START
}
