#!/bin/sh
xvfb-run \
    --server-args="-screen 0 1920x1080x24" \
    --error-file=/dev/stdout \
    python3 twitter-archiver/twitter-archiver.py
