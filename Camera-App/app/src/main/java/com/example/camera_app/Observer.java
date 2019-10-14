package com.example.camera_app;

/**
 * Is paired with the Observable class. Follows the Observer design pattern. Any class that
 * wants to subscribe to the received network signals so it can react to them accordingly.
 */
public interface Observer
{
    /**
     * The update function in the observer pattern.
     * @param signal The signal type that was received from the laptop.
     * @param message The optional message that accompanied the signal.
     */
    public void update(Signal signal, String message);


}
