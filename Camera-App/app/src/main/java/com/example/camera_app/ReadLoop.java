package com.example.camera_app;

import android.widget.MultiAutoCompleteTextView;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;

public class ReadLoop implements Runnable, Observable
{
//    private Thread t;
    private BufferedReader reader;
    private ArrayList<Observer> subscribers;

    //region > Observable Interface Functions
    /**
     * Implements the addObserver function in the Observable interface. Adds objects that
     * need to be updated of the status from this loop.
     * @param sub The object that needs to subscribe to the messages on this loop.
     */
    public void addObserver(Observer sub)
    {
        this.subscribers.add(sub);
    }

    /**
     * Allows for observers to remove themselves from the event feed. This isn't really needed
     * for this application but I'm going to stick to the Observer Design Pattern dammit.
     * @param sub The observer (subscriber) that wants to be removed from updates.
     */
    public void removeObserver(Observer sub)
    {
        this.subscribers.remove(sub);
    }

    /**
     * Is used to remove all of the observers when this thread needs to be closed.
     */
    public void removeAllObservers()
    {
        this.subscribers.clear();
    }

    /**
     * Goes through all observers in our subscriber list and calls their update functions
     * to notify them of a network signal that came through. It is up to the observer to
     * do with that information what they will.
     * @param signal The signal received from the server.
     * @param message The optional message that accompanied the signal.
     */
    public void notifyObservers(Signal signal, String message)
    {
        for(Observer observer : this.subscribers)
            observer.update(signal, message);
    }
    //endregion

    public ReadLoop(BufferedReader reader)
    {
        this.reader = reader;
        this.subscribers = new ArrayList<>();
    }

    //region > Getter Functions

    /**
     * Allows us to get the number of subscribers current subscribed to this observable instance.
     * @return
     */
    public int getNumObservers()
    {
        return this.subscribers.size();
    }
    //endregion

//    /**
//     * Gets this instances thread object so that it can interrupt it
//     * @return The thread of this class
//     */
//    public Thread getThread()
//    {
//        return this.t;
//    }

    /**
     * Parses the message received by the server and pulls out the Signal type
     * that the server sent.
     * @param message The full message that we need to parse.
     * @return The Signal type to send to the rest of the app.
     */
    public Signal parseSignal(String message)
    {
        // Network Message format: SIGNAL-MESSAGE
        // split on the '-' character. The first token is the signal type
        String[] splitMessage = message.split("-");

        //Signals: START, STOP, START_ACKNOWLEDGE, STOP_ACKNOWLEDGE, FTP_STARTED, FTP_COMPLETED
        if(splitMessage[0].equalsIgnoreCase("START"))
            return Signal.START;

        if (splitMessage[0].equalsIgnoreCase("STOP"))
            return Signal.STOP;

        // If the signal isn't start or stop, it's illegal
        return Signal.ILLEGAL;
    }

    /**
     * Parses the message recieved by the server and pulls out the message sent after the signal
     * @param message The raw message recieved from the server.
     * @return The message attached to the server signal.
     */
    public String parseMessage(String message)
    {
        // Network Message format: SIGNAL-MESSAGE
        // split on the '-' character. The first token is the signal type
        String[] splitMessage = message.split("-");

        return splitMessage[1];
    }

    /** Starts the thread */
    public void run()
    {
        String message = "";

        try
        {
            while(!Thread.interrupted() && (message = this.reader.readLine()) != null)
            {
                System.out.println("Starting network reading");

                notifyObservers(parseSignal(message), parseMessage(message));
                Thread.sleep(1000); // this is going to poll for new messages every second
            }
        }
        catch (IOException e)
        {
            // TODO: THROW AN ERROR HERE ON THE PHONE SCREEN
            System.err.println(e.getMessage());
            e.printStackTrace();
        }
        catch (InterruptedException e)
        {
            // TODO: THROW AN ERROR HERE ON THE PHONE SCREEN
            System.err.println(e.getMessage());
            e.printStackTrace();
        }

        // Cleanup
        removeAllObservers();
        System.out.println("Thread has stopped");
        NetConn.getInstance().closeConn();
        return;
    }
}
