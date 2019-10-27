package com.example.camera_app;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.graphics.SurfaceTexture;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.util.Log;
import android.util.Size;

import java.util.*;

import java.util.concurrent.TimeUnit;

public class Camera extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        getSupportActionBar().hide();
        AppCompatDelegate.setCompatVectorFromResourcesEnabled(true);
//        if (null == savedInstanceState) {
//            getFragmentManager().beginTransaction()
//                    .replace(R.id.container, CameraFragment.newInstance())
//                    .commit();
    }

    /**
     * This is to help us return the connection activity in case the user needs to
     * reset some of the preferences.
     */
    public void returnToPrevActivity()
    {
        Intent mainIntent = new Intent();
//        mainIntent.putExtra("updated_score", this.currScore);
        setResult(RESULT_OK, mainIntent);
        finish();
    }



}
