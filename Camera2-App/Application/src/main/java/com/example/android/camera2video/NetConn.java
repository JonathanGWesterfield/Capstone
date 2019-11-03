package com.example.android.camera2video;
import android.util.Log;

import java.io.*;

import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

/**
 * This class will allow for a single location for all network messages to flow through. This will
 * help us because we have 2 activities in use on the app. This class will be a singleton class
 * and will also use the Observer design pattern to notify the rest of the app that a network message
 * has been received.
 */
class NetConn implements Serializable
{
    private static NetConn instance = new NetConn();

    private String ipAddr;
    private int port;
    private String username;
    private String password;
    private String fromFTPPath;
    private String toFTPPath;

    private Socket socket;
    private BufferedWriter writer;
    private BufferedReader reader;
    private ReadLoop listener;
    private Thread listenerThread;
    private FTPConn ftpConn;

    static NetConn getInstance()
    {
        if(instance == null)
            instance = new NetConn();
        return instance;
    }

    /**
     * Empty Default Class constructor.
     */
    private NetConn()
    { /* Empty Default Constructor */ }

    /**
     * Class constructor.
     * @param ipAddr The IP address we are trying to connect to (the laptop).
     * @param port The port number that we must go through.
     */
    private NetConn(String ipAddr, int port)
    {
        this.ipAddr = ipAddr;
        this.port = port;
    }

    /**
     * Class constructor
     * @param ipAddr The IP address we are trying to connect to (the laptop).
     * @param port The port number that we must go through.
     * @param username The username of the user on the laptop.
     * @param password The password of the user on the laptop.
     */
    private NetConn(String ipAddr, int port, String username, String password)
    {
        this.ipAddr = ipAddr;
        this.port = port;
        this.username = username;
        this.password = password;
    }

    //region > Setters and getters for this class

    /**
     * Setter for this class instance IP address. This uses the builder pattern.
     * @param ip The IP address we are trying to connect to (the laptop).
     * @return The current instance of this class for the builder design pattern.
     */
    public NetConn setIPAddress(String ip)
    {
        this.ipAddr = ip;
        return this;
    }

    /**
     * Setter for this class instance port number. This uses the builder pattern.
     * @param port The port number that we must go through to establish a TCP connection.
     * @return The current instance of this class for the builder design pattern.
     */
    public NetConn setPortNumber(int port)
    {
        this.port = port;
        return this;
    }

    /**
     * Allows us to set the username needed to start the FTP process.
     * @param username The username of the user on the laptop.
     * @return The current instance of this class for the builder design pattern.
     */
    public NetConn setUsername(String username)
    {
        this.username = username;
        return this;
    }

    /**
     * Allows us to set the password needed to start the FTP process.
     * @param password The password of the user on the laptop.
     * @return The current instance of this class for the builder design pattern.
     */
    public NetConn setPassword(String password)
    {
        this.password = password;
        return this;
    }

    /**
     * Getter for the current IP Address.
     * @return The current IP address of the target.
     */
    public String getIpAddr()
    {
        return this.ipAddr;
    }

    /**
     * Getter for the currently set port number.
     * @return The current port number.
     */
    public int getPort()
    {
        return this.port;
    }

    /**
     * Getter for the reader once it is instanciated.
     * @return The buffered reader so we can start reading network messages.
     */
    public BufferedReader getReader()
    {
        return this.reader;
    }

    /**
     * Getter for the readloop so we can add a class as an observer.
     * @return Our instance of the readloop.
     */
    public ReadLoop getReadLoop()
    {
        return this.listener;
    }

    /**
     * Getter for the user to access the FTP connection functions like setting the source or
     * destination file locations.
     * @return The current instance of the FTPConn class.
     */
    public FTPConn getFtpConn()
    {
        return this.ftpConn;
    }

    //endregion

    /**
     * Is used to make sure the socket connection is currently connected and active.
     * @return True if the connection is live, false otherwise.
     */
    public boolean isAlive()
    {
        try
        {
            return this.socket.getInetAddress().isReachable(1000);
        }
        catch (IOException e)
        {
            return false;
        }
    }

    /**
     * Creates this classes instance of the FTP connection. Any action to get to the FTP connection
     * must come through this NetConn singleton instance.
     * @throws InstantiationException Thrown if port number, ip address, username or password is not set
     */
    public void createFTPConn() throws InstantiationException
    {
        // A port number of 0 means it wasn't set
        if(this.port == 0 || this.ipAddr == null || this.username == null || this.password == null)
            throw new InstantiationException(
                    "IP Address, Port Number, Username, and Password must be set before a connection can be established!!!");

        ftpConn = new FTPConn()
                .setHost(this.ipAddr)
                .setUsername(this.username)
                .setPassword(this.password);
    }

    /**
     * Uses the class IP Address and port number to establish a connection with the the target
     * address (the laptop).
     * @throws InstantiationException Is thrown if the target IP address or port number haven't been set.
     * @throws UnknownHostException Is thrown if the host IP address can't be found.
     * @throws IOException Is thrown if the socket connection cannot be established.
     */
    public void createConn() throws InstantiationException, UnknownHostException, IOException
    {
        // A port number of 0 means it wasn't set
        if(this.port == 0 || this.ipAddr == null)
            throw new InstantiationException(
                    "IP Address and Port Number must be set before a connection can be established!!!");

        InetAddress address = InetAddress.getByName(this.ipAddr);
        this.socket = new Socket(address, this.port);

        // Create the network readers and writers
        createWriter();
        createReader();

        // Create the listener so we can spawn a new listener thread
        this.listener = new ReadLoop(this.reader);
    }

    public void startReadLoop()
    {
        // Start our reader loop thread
        Thread t = new Thread(this.listener);
        t.start();
    }

    /**
     * Creates the input stream reader to read incoming network messages.
     * @throws IOException Throws when there is an issue with the network stream.
     */
    public void createReader() throws IOException
    {
        if (this.socket == null)
            throw new NullPointerException("ERROR! The socket has not been created!!");
        InputStream is = this.socket.getInputStream();
        InputStreamReader isr = new InputStreamReader(is);
        this.reader = new BufferedReader(isr);
    }

    /**
     * Creates the output stream writer to write messages to the other side of the network connection
     * (the laptop).
     * @throws IOException Throws when there is an issue with the network stream.
     */
    public void createWriter() throws IOException
    {
        if (this.socket == null)
            throw new NullPointerException("ERROR! The socket has not been created!!");
        OutputStream os = this.socket.getOutputStream();
        OutputStreamWriter osw = new OutputStreamWriter(os);
        this.writer = new BufferedWriter(osw);
    }

    /**
     * Sends a passed in message to the other side of the connection (the laptop).
     * @param message The message we want to send across the connection.
     * @throws IOException Is thrown when the message fails to send for some reason.
     */
    public boolean sendMessage(String message) throws IOException
    {
        if (this.writer == null)
            throw new NullPointerException("ERROR! The Writer has not been initialized!!");

        // TODO: MAKE THIS INTO A THREADED FUNCTION

        // Need an newline character or else the pipe won't close
        String endMessage = message + "\n";
        String logMessage = "Sent message to the server: " + endMessage;
        this.writer.write(endMessage);
        this.writer.flush();
        Log.i("NetConn", logMessage);

        return true;
    }

    /** Starts the listener thread so that we can read messages from the server while
     * doing other things.
     */
    public void startListener()
    {
        this.listenerThread = new Thread(this.listener);
        this.listenerThread.start();
        System.out.println("Started listening to the server (laptop)");
        // TODO: PUT AN ALERT HERE THAT WE ARE NOW LISTENING TO THE LAPTOP
    }

    /**
     * Allows us to subscribe to the listener so that we can get updates from the laptop
     * while the rest of the app is running.
     * @param observer The object that needs to listen to the server.
     */
    public void suscribeToListener(Observer observer)
    {
        if (this.listener == null)
            this.listener = new ReadLoop(this.reader);
        this.listener.addObserver(observer);
    }

    /**
     * Used to close the connection if that is needed. Basically closes the connection and
     * deletes the class. Do not call this unless the connection needs to be completely reset.
     */
    public void closeConn()
    {
        try
        {
            if(this.listenerThread != null)
                this.listenerThread.interrupt(); // kill the listener thread
            if(this.socket != null)
                this.socket.close();

            this.instance = null; // delete this connection instance.
        }
        catch (IOException e)
        {
            // Since the connection is being closed, it doesn't really matter if an exception is thrown.
            e.printStackTrace();
        }
    }
}
