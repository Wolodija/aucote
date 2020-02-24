#!/bin/bash

cd /opt/feeder/src || exit

exec python3 feeder.py
