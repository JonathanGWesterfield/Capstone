package com.example.android.camera2video;

import android.util.Log;

import com.jcraft.jsch.SftpProgressMonitor;

import java.util.ArrayList;
import java.util.Calendar;

/**
 * This class was created so that we could easily monitor when the SFTP file transfer started
 * and finished. This also implements the Observer in the Observer Pattern to let any observer
 * know when the file transfer was completed.
 *
 * This has been deprecated as its functions are no longer needed.
 *
 * @author Jonathan Westerfield
 * @version 1.0.3
 */
public class MyProgressMonitor implements SftpProgressMonitor, Observable
{
    private SftpProgressMonitor monitor;
    private ArrayList<Observer> observers;
    private final String TAG =  "ProgressMonitor";

    /**
     * Add an observer to tell them that the file transfer has finished.
     * @param observer The concrete observer to add.
     */
    @Override
    public void addObserver(Observer observer) {
        if(this.observers == null)
            this.observers = new ArrayList<>();
        this.observers.add(observer);
    }

    /**
     * Remove observers to satisfy the interface.
     * @param observer The concrete observer we want to remove.
     */
    @Override
    public void removeObserver(Observer observer) {
        if (this.observers == null)
            return;
        this.observers.remove(observer);
    }

    /**
     * Notify the observers that the file transfer has completed.
     * @param signal The signal received from the server.
     * @param message The optional message that accompanied the signal.
     */
    @Override
    public void notifyObservers(Signal signal, String message) {
        for(Observer observer : this.observers)
            observer.update(signal, message);
    }

    /**
     * Called at the beginning.
     * @param op No Idea
     * @param src Source file path.
     * @param dest Destination file path on the server.
     * @param max No Idea
     */
    public void init(int op, String src, String dest, long max)
    {
        Log.d(TAG, "File Transfer Started!");
    }

    /**
     * Called at the end of the file transfer
     */
    public void end()
    {
        Log.d(TAG, "File Transfer Complete!");
        notifyObservers(Signal.FTP_COMPLETED,
                Calendar.getInstance().getTime().toString().replaceAll(" ", "-"));
    }

    @Override public boolean count(long i)
    {
        return false;
    }
}
