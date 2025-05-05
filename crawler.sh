#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <Seed File> <Number of Pages> <Max Hops> <Output Directory>"
    exit 1
fi

echo "Installing Dependencies..."
pip -q install --upgrade pip
pip -q install -r requirements.txt

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

echo "Crawling..."
start_time=$(date +%s)
python3 WikiScrape/main.py $1 $2 $3 $4
end_time=$(date +%s)
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "Python script failed with exit code $exit_code"
    exit $exit_code
fi

size=$(du -sh "$4" | cut -f1 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
count=$(ls -1 "$4" | wc -l | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
duration=$(echo "$end_time - $start_time" | bc)
throughput=$(echo "$count / $duration" | bc -l | xargs printf "%.2f")

echo "Finished in $duration seconds!"
echo "Collected $size of data across $count files"
echo "Scraping throughput: $throughput files per second"