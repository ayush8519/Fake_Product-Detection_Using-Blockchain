@echo off
echo Starting Ethereum local blockchain (Ganache)...
cd /d "%~dp0"
ganache-cli --port 7545 --networkId 5777
pause
