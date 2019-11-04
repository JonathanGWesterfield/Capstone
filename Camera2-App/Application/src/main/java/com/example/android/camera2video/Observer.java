package com.example.android.camera2video;

/**
 * Is paired with the Observable class. Follows the Observer design pattern. Any class that
 * wants to subscribe to the received network signals so it can react to them accordingly.
 *
 * @author Jonathan Westerfield
 * @version 1.0.0
 */
public interface Observer
{
    /**
     * The update function in the observer pattern.
     * @param signal The signal type that was received from the laptop.
     * @param message The optional message that accompanied the signal.
     */
    void update(Signal signal, String message);
}
