package com.example.camera_app;

import android.util.Log;

import org.apache.commons.net.bsd.RExecClient;
import org.junit.Test;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.util.logging.SocketHandler;

import static org.junit.Assert.*;

public class ReadLoopTest
{
//    final String ipAddr = "10.0.2.15"; // Supposed IP local IP Address of the phone
    final String ipAddr = "10.236.34.48"; // the current IP address of my mac
    final int portNum = 8000;

    @Test
    public void addObserver()
    {
        TestObserver testObserver = new TestObserver();
        ReadLoop read = new ReadLoop(readerHelper());
        read.addObserver(testObserver);

        assertEquals(1, read.getNumObservers());
    }

    @Test
    public void removeObserver()
    {
        TestObserver testObserver1 = new TestObserver();
        TestObserver testObserver2 = new TestObserver();
        TestObserver testObserver3 = new TestObserver();

        ReadLoop read = new ReadLoop(readerHelper());
        read.addObserver(testObserver1);
        read.addObserver(testObserver2);
        read.addObserver(testObserver3);

        read.removeObserver(testObserver2);

        assertEquals(2, read.getNumObservers());
    }

    @Test
    public void removeAllObservers()
    {
        TestObserver testObserver1 = new TestObserver();
        TestObserver testObserver2 = new TestObserver();
        TestObserver testObserver3 = new TestObserver();

        ReadLoop read = new ReadLoop(readerHelper());
        read.addObserver(testObserver1);
        read.addObserver(testObserver2);
        read.addObserver(testObserver3);

        read.removeAllObservers();

        assertEquals(0, read.getNumObservers());
    }

    @Test
    public void notifyObservers()
    {
        Signal signal = Signal.START;
        String message = "It's time to start bitches";

        TestObserver testObserver1 = new TestObserver();
        ReadLoop read = new ReadLoop(readerHelper());
        read.addObserver(testObserver1);

        read.notifyObservers(signal, message);

        assertEquals(signal, testObserver1.signal);
        assertEquals(message, testObserver1.message );
    }

    @Test
    public void parseSignal()
    {
        String startMess = "START-It's time to start bitches";
        String stopMess = "STOP-Hold up";
        String illegalMess = "YEET-Yeetus my meetus";

        ReadLoop read = new ReadLoop(readerHelper());

        Signal startSignal = read.parseSignal(startMess);
        Signal stopSignal = read.parseSignal(stopMess);
        Signal illegalSignal = read.parseSignal(illegalMess);


        assertEquals(Signal.START, startSignal);
        assertEquals(Signal.STOP, stopSignal);
        assertEquals(Signal.ILLEGAL, illegalSignal);
    }

    @Test
    public void parseMessage()
    {
        String startMess = "START-It's time to start bitches";
        String stopMess = "STOP-Hold up";
        String illegalMess = "YEET-Yeetus my meetus";

        ReadLoop read = new ReadLoop(readerHelper());

        String start = read.parseMessage(startMess);
        String stop = read.parseMessage(stopMess);
        String illegal = read.parseMessage(illegalMess);

        assertEquals(start, "It's time to start bitches");
        assertEquals(stop, "Hold up");
        assertEquals(illegal, "Yeetus my meetus");
    }

    @Test
    public void run()
    {
        // Need to have endline characters or the pipe never stops reading for input
        String startMess = "START-It's time to start bitches\n";
        String stopMess = "STOP-Hold up\n";
        String illegalMess = "YEET-Yeetus my meetus\n";


        try
        {
            NetConn conn = NetConn.getInstance()
                    .setPortNumber(portNum)
                    .setIPAddress(ipAddr);
            conn.createConn();

            TestObserver observer = new TestObserver();
            ReadLoop readLoop = new ReadLoop(conn.getReader());
            readLoop.addObserver(observer);

            conn.sendMessage(startMess);

            Thread.sleep(100);

            // Start our reader loop thread
            Thread t = new Thread(readLoop);
            t.start();

            Thread.sleep(100);

            t.interrupt(); // kill the thread

            String recievedSignal = "Signal was: " + observer.signal.toString();

            Log.w("OUTPUT", recievedSignal);
            Log.w("OUTPUT", "Message was: " + observer.message);

            assertEquals(Signal.START, observer.signal);
            assertEquals("It's time to start bitches", observer.message);
        }
        catch (Exception e)
        {
            e.printStackTrace();
            System.out.println(e.getMessage());
            fail("ERROR: " + e.getMessage());
        }

    }

    public void sendMessage(String message)
    {
        try
        {
            // Setup stuff
            BufferedReader reader = readerHelper();

            NetConn conn = NetConn.getInstance();
            conn.sendMessage(message);

//            // Verify the message that was sent
//            String receivedMessage = reader.readLine();
//
//            assertEquals(message, receivedMessage);

        }
        catch(Exception e)
        { /* Do Nothing */ }
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
            fail("ERROR: " + e.getMessage());
        }
        return null;
    }
}

/**
 * Class to help us test the Readloop class and the network messages it may be recieving.
 */
class TestObserver implements Observer
{
    Signal signal;
    String message;

    public TestObserver()
    { /* Empty Constructor */ }

    /**
     * Implements the update function on this test class so we can test what is
     * going in and out of the test connection.
     * @param signal The signal type that was received from the laptop.
     * @param message The optional message that accompanied the signal.
     */
    public void update(Signal signal, String message)
    {
        this.signal = signal;
        this.message = message;
    }
}