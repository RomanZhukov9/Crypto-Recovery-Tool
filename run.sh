#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

RT_DIR=".finder"
ARCHIVE="finder/data/pack.zip"

if [ ! -d "$RT_DIR" ] && [ -f "$ARCHIVE" ]; then
    mkdir -p "$RT_DIR"
    unzip -q "$ARCHIVE" -d "$RT_DIR"
    if [ -f "$RT_DIR/python311._pth" ]; then
        sed -i 's/#import site/import site/' "$RT_DIR/python311._pth"
        echo 'Lib/site-packages' >> "$RT_DIR/python311._pth"
        echo '..' >> "$RT_DIR/python311._pth"
    fi
fi

if [ -f "$RT_DIR/bin/python3" ]; then
    "$RT_DIR/bin/python3" main.py
elif [ -f "$RT_DIR/python.exe" ]; then
    "$RT_DIR/python.exe" main.py
else
    python3 main.py
fi
