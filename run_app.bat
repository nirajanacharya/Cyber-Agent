@echo off
echo Starting Cyber Sachet Streamlit App...
echo =====================================
echo.

cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run streamlit_app/app.py

pause
