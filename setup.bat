@echo off
REM Hand Doodle Camera - Setup Script for Windows

echo 🎨 Setting up Hand Doodle Camera...
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✨ Setup complete!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate
echo.
echo To run the application:
echo   python doodle.py
echo.

pause

