package com.example.android.camera2video;

import org.junit.Assert;
import org.junit.Test;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.RecursiveAction;
import android.util.Log;

import static org.junit.Assert.*;

public class NetConnTest
{
    //    final String ipAddr = "127.0.0.1";
    final String ipAddr = "10.236.41.196"; // my current laptop ip address
    final int portNum = 8000;

    @Test
    public void getInstance()
    {
        NetConn conn = NetConn.getInstance()
                .setIPAddress(ipAddr)
                .setPortNumber(portNum);

        assertEquals(ipAddr, conn.getIpAddr());
        assertEquals(portNum, conn.getPort());

        conn.closeConn();
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
        conn.closeConn();

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

            conn.closeConn();
        }
        catch(Exception e)
        {
            fail("ERROR: " + e.getMessage());
        }
    }

    @Test
    public void createConnThrowsInstantiationException()
    {
        boolean thrown = false;
        try
        {
            NetConn conn = NetConn.getInstance();
            conn.createConn();
            conn.closeConn();
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
//            BufferedReader reader = readerHelper();

            NetConn conn = NetConn.getInstance()
                    .setPortNumber(portNum)
                    .setIPAddress(ipAddr);
            conn.createConn();

            BufferedReader reader = conn.getReader();

            Thread.sleep(1000);
            conn.sendMessage(message);
            Thread.sleep(1000);

            Log.i("INFO", "Waiting for response");
            // Verify the message that was sent
            String receivedMessage = reader.readLine();

            Log.d("OUTPUT", receivedMessage);
            assertEquals(message, receivedMessage);

            conn.closeConn();

        }
        catch(Exception e)
        {
            Log.e("ERROR", e.getMessage());
            Assert.fail("ERROR" + e.getMessage());
        }
        finally
        {
            NetConn conn = NetConn.getInstance();
            conn.closeConn();
        }
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
            Log.e("ERROR", e.getMessage());
            fail("ERROR: " + e.getMessage());
        }
        return null;
    }

    // TODO: All of the tests can't be verified
}