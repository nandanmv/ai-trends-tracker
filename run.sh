#!/bin/bash
# Launch the AI Trends Tracker
set -e

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$APP_DIR"

# Check yt-dlp
if ! command -v yt-dlp &>/dev/null; then
  echo "yt-dlp not found. Install with: brew install yt-dlp"
  exit 1
fi

# Check streamlit
if ! python3 -c "import streamlit" &>/dev/null; then
  echo "Installing streamlit..."
  pip3 install streamlit --break-system-packages -q
fi

echo "Starting AI Trends Tracker..."
python3 -m streamlit run "$APP_DIR/app.py" \
  --server.port 8501 \
  --server.headless false \
  --browser.gatherUsageStats false
