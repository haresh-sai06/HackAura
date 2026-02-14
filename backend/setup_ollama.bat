@echo off
REM RAPID-100 Ollama Setup Script for Windows
REM Automates setup of Ollama and model creation

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║        RAPID-100 Emergency Triage - Ollama Setup          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Ollama is not installed!
    echo.
    echo 📥 Please install Ollama first:
    echo    1. Visit: https://ollama.ai
    echo    2. Download and install for Windows
    echo    3. Run: ollama serve (in another terminal)
    echo.
    pause
    exit /b 1
)

echo ✅ Ollama is installed
echo.

REM Check if Ollama server is running
echo 🔍 Checking if Ollama server is running...
ollama list >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Ollama server doesn't appear to be running
    echo.
    echo Start Ollama in another terminal:
    echo    ollama serve
    echo.
    pause
)

echo ✅ Ollama server is accessible
echo.

REM Navigate to backend directory
echo 📁 Navigating to backend directory...
cd /d "%~dp0"
echo 📍 Current directory: %cd%
echo.

REM Check if Modelfile exists
if not exist "Modelfile" (
    echo ❌ Modelfile not found!
    pause
    exit /b 1
)

echo ✅ Modelfile found
echo.

REM Create the rapid-triage model
echo 🤖 Creating RAPID-100 emergency triage model...
ollama create rapid-triage -f Modelfile

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to create model
    pause
    exit /b 1
)

echo ✅ Model created successfully!
echo.

REM Verify model
echo 📋 Verifying model...
ollama list | findstr "rapid-triage"
echo.

REM Install Python dependencies
echo 📦 Installing Python dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ Dependencies installed
) else (
    echo ⚠️  requirements.txt not found
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           ✅ Setup Complete!                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Next Steps:
echo.
echo 1. Ensure Ollama is running:
echo    ollama serve
echo.
echo 2. Start the backend:
echo    python main.py
echo.
echo 3. Run tests:
echo    python execute.py
echo.
echo 📖 For more details, see: OLLAMA_INTEGRATION.md
echo.
pause
