@echo off
title AI&DST Quiz Public Tunnel (Cloudflare Powered)
color 0A
cls
echo ======================================================================
echo    AI & DST 2026 QUIZ PUBLIC TUNNEL (FOR DIFFERENT HOTSPOTS)
echo ======================================================================
echo.
echo  Powered by Cloudflare Global Tunnel (Never Expires, High Speed).
echo  Keep this window OPEN during the competition!
echo.
echo ======================================================================
echo.

if exist cloudflared.exe (
    cloudflared.exe tunnel --url http://127.0.0.1:5000
) else (
    ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:127.0.0.1:5000 serveo.net
)

pause
