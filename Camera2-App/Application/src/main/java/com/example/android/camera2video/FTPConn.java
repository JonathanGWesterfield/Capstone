package com.example.android.camera2video;

import android.util.Log;
import android.view.TextureView;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.IO;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.SftpException;
import com.jcraft.jsch.SftpProgressMonitor;

import org.apache.commons.net.ftp.FTP;
import org.apache.commons.net.ftp.FTPClient;

import java.io.File;
import java.io.IOException;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class FTPConn implements Observer
{
    String host, username, password, destFilePath;
    int port = 22;
    private final String TAG = "FTPConn";

    Channel channel;
    ChannelSftp sftp;


    //region > Class Constructors
    /**
     * Empty Constructor
     */
    public FTPConn()
    { /* Empty Constructor */ }

    /**
     * Class constructor.
     * @param host The ip address of the laptop we want to connect to.
     */
    public FTPConn(String host)
    {
        this.host = host;
    }

    /**
     * Class constructor
     * @param host The ip address of the laptop we want to connect to.
     * @param username The username for the laptop.
     * @param password The password for the laptop.
     */
    public FTPConn(String host, String username, String password, String destFilePath)
    {
        this.host = host;
        this.username = username;
        this.password = password;
        this.destFilePath = destFilePath;
    }
    //endregion

    //region > Builder Setters
    /**
     * Setter for the host we need to connect to.
     * @param host The ip address of the laptop we want to connect to.
     * @return The current instance of this class according to the builder design pattern
     */
    public FTPConn setHost(String host)
    {
        this.host = host;
        return this;
    }

    /**
     * Setter for the username so we can login to the laptop.
     * @param username The username of the user for the laptop.
     * @return The current instance of this class according to the builder design pattern
     */
    public FTPConn setUsername(String username)
    {
        this.username = username;
        return this;
    }

    /**
     * Setter for the password so we can login to the laptop.
     * @param password The password of the user needed to login to the laptop.
     * @return The current instance of this class according to the builder design pattern
     */
    public FTPConn setPassword(String password)
    {
        this.password = password;
        return this;
    }

    /**
     * Setter for the destination file path we need to send the video file to.
     * @param filePath The destination filepath
     * @return The current instance of this class according to the builder design pattern
     */
    public FTPConn setDestFilePath(String filePath)
    {
        this.destFilePath = filePath;
        return this;
    }
    //endregion

    //region > Getters
    /**
     * Getter for the host.
     * @return The currently set host.
     */
    public String getHost()
    {
        return this.host;
    }

    /**
     * Getter for the username.
     * @return The currently set username.
     */
    public String getUsername()
    {
        return this.username;
    }

    /**
     * Getter for the password.
     * @return The currently set password.
     */
    public String getPassword()
    {
        return this.password;
    }

    /**
     * Getter for the destination file path we want to send the file to.
     * @return The currently set destination file path.
     */
    public String getDestFilePath()
    {
        return this.destFilePath;
    }
    //endregion

    /**
     * A way to check if our connection to the host machine is alive.
     * @return True if it is alive, false otherwise.
     */
    public boolean isLive()
    {
        return this.sftp.isConnected();
    }

    /**
     * Creates the sftp connection to the host (the laptop).
     * @throws JSchException In case some connection issue happens or ssh isn't setup on the host.
     */
    public void setupConn() throws JSchException
    {
        JSch jsch = new JSch();
        Session session = jsch.getSession(this.username, this.host, this.port);
        session.setPassword(this.password);

//        java.util.Properties config = new java.util.Properties();
//        // Makes it MITM-vulnerable but there is no access to the internet in the field
//        config.put("StrictHostKeyChecking", "no");
        session.setConfig("StrictHostKeyChecking", "no");
//        session.setConfig(config);
        session.setTimeout(5000);
        session.setConfig("PreferredAuthentications", "password");
        session.connect();

        channel = session.openChannel("sftp");
        channel.connect();
        sftp = (ChannelSftp) channel;
    }

    /**
     * Allows us to close the sftp connection cleanly
     */
    public void closeConn()
    {
        sftp.disconnect();
        channel.disconnect();
    }

    /**
     * Sends the file to the destination folder on the host (the laptop)
     * @return True if it succeeded, false otherwise.
     * @throws SftpException
     */
    public boolean upload(String srcFilePath) throws InstantiationException
    {
        if(!sftp.isConnected() || sftp.isClosed())
            throw new InstantiationException("SFTP Connection not established!");

        try
        {
            sftp.cd(this.destFilePath);
            int mode = sftp.OVERWRITE;
            SftpProgressMonitor monitor = new MyProgressMonitor();

            sftp.put(srcFilePath, this.destFilePath, monitor, mode);
            closeConn();
            return true;
        }
        catch (SftpException e)
        {
            Log.d(TAG, e.getMessage());
            Log.d(TAG, "Failed to Transfer the file");
        }
        return false;
    }

    /**
     * Gets called when the file transfer is complete so we can send a signal to the laptop
     * to let it know that the file transfer is done and it can start analyzing the footage.
     * @param signal The signal type that was received from the laptop.
     * @param message The optional message that accompanied the signal.
     */
    @Override
    public void update(Signal signal, String message)
    {
        NetConn conn = NetConn.getInstance();
        try
        {
            conn.sendMessage(Signal.FTP_COMPLETED.toString());
        }
        catch (IOException e)
        {
            Log.d(TAG, "Sending FTP_COMPLETED signal failed!");
            Log.d(TAG, e.getMessage());
        }
    }
}


