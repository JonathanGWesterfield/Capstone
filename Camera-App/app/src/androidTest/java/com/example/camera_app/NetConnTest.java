package com.example.camera_app;

import org.junit.Test;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

import static org.junit.Assert.*;

public class NetConnTest
{
    final String ipAddr = "127.0.0.1";
    final int portNum = 8000;

    @Test
    public void getInstance()
    {
        NetConn conn = NetConn.getInstance()
                .setIPAddress(ipAddr)
                .setPortNumber(portNum);

        assertEquals(ipAddr, conn.getIpAddr());
        assertEquals(portNum, conn.getPort());
    }

    @Test
    public void setIPAddress()
    {
        NetConn conn = NetConn.getInstance();
        conn.setIPAddress(ipAddr);

        assertEquals(ipAddr, conn.getIpAddr());
    }

    @Test
    public void setPortNumber()
    {
        NetConn conn = NetConn.getInstance();
        conn.setPortNumber(8000);

        assertEquals(portNum, conn.getPort());
    }

    @Test
    public void createConn()
    {
        try
        {
            NetConn conn = NetConn.getInstance()
                    .setIPAddress(ipAddr)
                    .setPortNumber(portNum);
            conn.createConn();
            assertEquals(true, conn.isAlive());

        }
        catch(Exception e)
        { /* Do Nothing */ }
    }

    @Test
    public void createConnThrowsInstantiationException()
    {
        boolean thrown = false;
        try
        {
            NetConn conn = NetConn.getInstance();
            conn.createConn();
        }
        catch(InstantiationException e)
        {
            thrown = true;
        }
        catch (IOException e)
        {
            // Do Nothing
        }
        finally
        {
            assertEquals(true, thrown);
        }
    }

    @Test
    public void sendMessage()
    {
        String message = "Yeeterino";
        try
        {
            // Setup stuff
            BufferedReader reader = readerHelper();

            NetConn conn = NetConn.getInstance()
                    .setPortNumber(portNum)
                    .setIPAddress(ipAddr);
            conn.createConn();
            conn.sendMessage(message);

            // Verify the message that was sent
            String receivedMessage = reader.readLine();

            assertEquals(message, receivedMessage);

        }
        catch(Exception e)
        { /* Do Nothing */ }
    }

    @Test
    public void readMessage()
    {

    }

    /**
     * Is used to create a buffered reader to read any messages that the NetConn class sent.
     * @return Reader to process incoming network calls.
     */
    public BufferedReader readerHelper()
    {
        try
        {
            InetAddress address = InetAddress.getByName(ipAddr);
            Socket sock = new Socket(address, portNum);
            InputStream is = sock.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            return new BufferedReader(isr);
        }
        catch(IOException e)
        {
            System.err.println("SOCKET READER COULD NOT BE CREATED");
        }
        return null;
    }
}