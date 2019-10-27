package com.example.camera_app;

/**
 * The interface that is required for any class that want to use this to send network signals
 * to the classes that need it. Uses the Observer design pattern.
 */
public interface Observable
{
    /**
     * Adds a new observer to notify when there is a network signal received.
     * @param observer The concrete observer to add.
     */
    void addObserver(Observer observer);

    /**
     * Removes the specified observer from the subscriber list.
     * @param observer The concrete observer we want to remove.
     */
    void removeObserver(Observer observer);

    /**
     * The function that will call the observers update() method and send the signal
     * and message for that observer to work with it.
     * @param signal The signal received from the server.
     * @param message The optional message that accompanied the signal.
     */
    void notifyObservers(Signal signal, String message);
}
