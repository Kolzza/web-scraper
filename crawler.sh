#!/bin/bash

echo "Installing Dependencies..."
pip -q install --upgrade pip
pip -q install -r requirements.txt

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <Seed File> <Number of Pages> <Max Hops> <Output Directory>"
    exit 1
fi

if [ -f "$1" ]; then
    echo "Reading Seed URLs from $1..."
else
    echo "Seed File $1 does not exist."
    exit 1
fi

if [ ! -d "$4" ]; then
    echo "Output directory not found!"
    echo "Creating $4/"
    mkdir -p $4
fi

echo "Starting Crawler..."
python3 WikiScrape/main.py $1 $2 $3 $4
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "Python script failed with exit code $exit_code"
    exit $exit_code
fi

echo "Completed!"