#!/bin/bash

echo ""
echo "=========================================="
echo "    JobTrack - AI Job Application Tracker"
echo "=========================================="
echo ""

# Function for setup
do_setup() {
    echo "============================================"
    echo "  AI MODE SETUP"
    echo "============================================"
    echo ""
    echo "Choose your AI mode:"
    echo ""
    echo "  [1] FREE - Basic keyword matching"
    echo "      No setup required, works offline"
    echo "      Good for: Quick ATS score estimates"
    echo ""
    echo "  [2] FREE + OLLAMA - Local AI (Recommended)"
    echo "      Requires: Ollama installed (free)"
    echo "      Good for: Full AI features, 100% free"
    echo "      Download: https://ollama.ai"
    echo ""
    echo "  [3] CLAUDE API - Best quality (Paid)"
    echo "      Requires: Anthropic API key"
    echo "      Good for: Best results, ~\$0.01/analysis"
    echo ""
    echo "============================================"
    echo ""
    echo "TIP: To change mode later, run: ./start.sh setup"
    echo ""
    
    read -p "Enter choice (1, 2, or 3): " MODE_CHOICE
    
    case "$MODE_CHOICE" in
        1)
            echo "JOBTRACK_AI_MODE=free" > .env
            echo ""
            echo "[OK] Free mode selected - basic keyword matching"
            echo ""
            ;;
        2)
            echo "JOBTRACK_AI_MODE=ollama" > .env
            echo ""
            echo "[OK] Ollama mode selected"
            echo ""
            echo "--------------------------------------------"
            echo "IMPORTANT - You need to install Ollama:"
            echo ""
            echo "  1. Download from: https://ollama.ai"
            echo "  2. Install and run Ollama"
            echo "  3. Open a NEW terminal and run:"
            echo "     ollama pull llama3.2"
            echo "  4. Wait for download to complete (~2GB)"
            echo "  5. Keep Ollama running in background"
            echo ""
            echo "If Ollama is not running, JobTrack will"
            echo "fall back to basic keyword matching."
            echo "--------------------------------------------"
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            echo ""
            echo "You need an Anthropic API key."
            echo "Get one at: https://console.anthropic.com/settings/keys"
            echo ""
            read -p "Paste your API key (starts with sk-ant-): " API_KEY
            
            if [ -n "$API_KEY" ]; then
                echo "JOBTRACK_AI_MODE=claude" > .env
                echo "ANTHROPIC_API_KEY=$API_KEY" >> .env
                echo ""
                echo "[OK] Claude mode configured!"
                echo ""
            else
                echo ""
                echo "[WARNING] No API key entered, falling back to free mode"
                echo "JOBTRACK_AI_MODE=free" > .env
                echo ""
            fi
            ;;
        *)
            echo ""
            echo "[INFO] Invalid choice, using free mode"
            echo "JOBTRACK_AI_MODE=free" > .env
            echo ""
            ;;
    esac
}

# Check if user wants to reconfigure
if [ "$1" = "setup" ] || [ "$1" = "config" ] || [ "$1" = "reset" ]; then
    do_setup
fi

# Check if this is first run
NEED_SETUP=0
if [ ! -f .env ]; then
    NEED_SETUP=1
elif ! grep -q "JOBTRACK_AI_MODE=" .env 2>/dev/null; then
    NEED_SETUP=1
fi

if [ "$NEED_SETUP" = "1" ]; then
    do_setup
fi

# Show current mode
echo ""
if [ -f .env ]; then
    MODE=$(grep "JOBTRACK_AI_MODE=" .env | cut -d'=' -f2)
    echo "Current AI Mode: $MODE"
fi
echo ""
echo "TIP: To change AI mode, run: ./start.sh setup"
echo ""

# Check if Python is installed
echo "[CHECK] Looking for Python..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "[ERROR] Python 3 is not installed."
    echo ""
    echo "Install it with:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu: sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi
python3 --version
echo "[OK] Python found!"

# Install dependencies if needed
if [ ! -f ".deps_installed" ]; then
    echo ""
    echo "[SETUP] Installing dependencies - this may take a minute..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERROR] Failed to install dependencies."
        echo ""
        exit 1
    fi
    touch .deps_installed
    echo ""
    echo "[OK] Dependencies installed!"
fi

echo ""
echo "=========================================="
echo "    Starting JobTrack..."
echo "=========================================="
echo ""
echo "Open your browser to: http://localhost:8000"
echo ""
echo "To stop: Press Ctrl+C"
echo "To change AI mode: Run \"./start.sh setup\""
echo "=========================================="
echo ""

# Start the server
python3 -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

echo ""
echo "Server stopped."