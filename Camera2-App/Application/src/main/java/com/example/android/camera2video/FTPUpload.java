package com.example.android.camera2video;

import android.util.Log;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.IO;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.SftpException;
import com.jcraft.jsch.SftpProgressMonitor;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.nio.file.DirectoryNotEmptyException;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Paths;

/**
 * This class is a class to house the function for transferring the video file to the laptop.
 * This function was originally carried out on the main thread. However, Donald's phone
 * (the Google Pixel 4) is a lot more finicky than Ismael's phone (the Samsung S10e). The Pixel
 * will throw an error message saying that frames were skipped on the main UI and the work
 * we are trying to do is too taxing for the main thread. To get around this, we are putting
 * the file transfer function into a separate thread so the main thread can still run while the
 * file is being uploaded. This thread will be called from the {@link FTPConn} class.
 *
 * @author Jonathan Westerfield
 * @version 1.0.0
 * @see FTPConn
 */
public class FTPUpload implements Runnable
{
    private String srcFilePath, destFilePath;
    private ChannelSftp sftp;
    private Session session;
    private String TAG = "FTPUpload";

    /**
     * Class constructor. Takes in the necessary file information to transfer the file as well
     * as an open SFTP connection to the laptop in order to actually transfer the file. Must
     * call the <code>run()</code> function to actually upload the file.
     * @param srcFilePath The file we need to transfer from the phone to the laptop.
     * @param destFilePath The folder on the target laptop where the file will be transferred.
     * @param sftp An open sftp connection to the laptop.
     * @param session The sessions representing the connection to the laptop. (I don't know if this is needed tbh).
     */
    public FTPUpload(String srcFilePath, String destFilePath, ChannelSftp sftp, Session session)
    {
        this.srcFilePath = srcFilePath;
        this.destFilePath = destFilePath;
        this.sftp = sftp;
        this.session = session;
    }

    /**
     * This function implements the run function for the {@link Runnable} interface. This function
     * will take the file stored at the specified file location, transfer it over SFTP to the
     * laptop and then delete the file once the transfer has finished.
     */
    @Override
    public void run()
    {
        if(sftp == null || session == null)
        {
            Log.d(TAG, "SFTP Connection not established! Can't transfer file!");
            return;
        }
        if(!sftp.isConnected() || sftp.isClosed())
        {
            Log.d(TAG, "SFTP Connection not established! Can't transfer file!");
            return;
        }
        try
        {
            File src = new File(this.srcFilePath);
            sftp.cd(this.destFilePath);
            int mode = sftp.OVERWRITE;
            SftpProgressMonitor monitor = new MyProgressMonitor();

//            sftp.put(this.srcFilePath, this.destFilePath, monitor, mode);
            sftp.put(new FileInputStream(src), src.getName(), ChannelSftp.OVERWRITE);

            // Tell the laptop we finished the transfer
            NetConn.getInstance().sendMessage(Signal.FTP_COMPLETED.toString());

            deleteVideo(); // delete video off phone so we can save storage
        }
        catch (FileNotFoundException e)
        {
            String errMess = "Line: " + Integer.toString(e.getStackTrace()[0].getLineNumber()) + ": " + e.getMessage();
            Log.d(TAG, errMess);
            Log.d(TAG, "Failed to Transfer the file");
        }
        catch (IOException e)
        {
            String errMess = "Line: " + Integer.toString(e.getStackTrace()[0].getLineNumber()) + ": " + e.getMessage();
            Log.d(TAG, errMess);
            Log.d(TAG, "Failed to Transfer the file");
        }
        catch (SftpException e)
        {
            String errMess = "Line: " + Integer.toString(e.getStackTrace()[0].getLineNumber()) + ": " + e.getMessage();
            Log.d(TAG, errMess);
            Log.d(TAG, "Failed to Transfer the file");
        }
        catch (Exception e)
        {
            String errMess = "Line: " + Integer.toString(e.getStackTrace()[0].getLineNumber()) + ": " + e.getMessage();
            Log.d(TAG, errMess);
            Log.d(TAG, "Failed to delete the file after transfer");
        }
    }

    /**
     * Deletes the file after it has been transferred to the phone so we can still
     * have storage on the phone after multiple recordings.
     */
    public void deleteVideo() throws Exception
    {
        File deleteFile = new File(this.srcFilePath);
        if(!deleteFile.getCanonicalFile().delete())
            throw new Exception("ERROR! Failed to delete the video file from the phone storage!");

        Log.d(TAG, "File successfully deleted");
    }

}
