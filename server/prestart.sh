#! /usr/bin/env bash

echo "install additional packeges"

pip install --upgrade pip && \
pip install --no-cache-dir -r requirements.txt
