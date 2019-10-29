package com.example.android.camera2video;

import org.apache.commons.net.ftp.FTP;
import org.junit.Test;

import static org.junit.Assert.*;

public class FTPConnTest {
    final String ipAddr = "10.236.35.41";

    final String username = "jgwesterfield";
    final String password = "Chrome11";

    final String destPath = "/Users/jgwesterfield/Desktop/drone-tracker-testDir/";

//    final String username = "testUser";
//    final String password = "test";

    @Test
    public void setHost() {
        FTPConn conn = new FTPConn().setHost(ipAddr);

        assertEquals(ipAddr, conn.getHost());
    }

    @Test
    public void setUsername() {
        FTPConn conn = new FTPConn().setUsername(username);
        assertEquals(username, conn.getUsername());
    }

    @Test
    public void setPassword() {
        FTPConn conn = new FTPConn().setPassword(password);
        assertEquals(password, conn.getPassword());
    }

    @Test
    public void setDestFilePath() {
        FTPConn conn = new FTPConn().setDestFilePath(destPath);
        assertEquals(destPath, conn.getDestFilePath());
    }

    @Test
    public void setupConn()
    {
        try
        {
            FTPConn conn = new FTPConn()
                    .setHost(ipAddr)
                    .setUsername(username)
                    .setPassword(password)
                    .setDestFilePath(destPath);

            conn.setupConn();

            assertEquals(true, conn.isLive());
        }
        catch(Exception e)
        {
            System.err.println(e.getMessage());
            fail();
        }
    }

    @Test
    public void upload()
    {
        final String testFilePath = "/sdcard/Pictures/TestFile.txt";
        try
        {
            FTPConn conn = new FTPConn()
                    .setHost(ipAddr)
                    .setUsername(username)
                    .setPassword(password)
                    .setDestFilePath(destPath);
            conn.setupConn();

            boolean succeded = conn.upload(testFilePath);
            assertEquals(true, succeded);
        }
        catch(Exception e)
        {
            System.err.println(e.getMessage());
            fail();
        }

    }
}