@echo off
:restart
echo Starting bot...
python bot.py
echo Bot crashed with exit code %ERRORLEVEL%
echo Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto restart
