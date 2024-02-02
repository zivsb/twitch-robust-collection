#!/bin/bash

# List of valid data shaping rates in Mbps
DATA_RATES=("1" "3" "5")

# List of category names
# Categories: 5 each for: MOBA, RPG, IRL
CATEGORY_NAMES=(
    "league-of-legends" "smite" "dota-2" "brawl-stars" "pokemon-unite"
    "fortnite" "palworld" "enshrouded" "escape-from-tarkov" "roblox" "world-of-warcraft" "final-fantasy-xiv-online" "genshin-impact" "new-world" "minecraft"
    "just-chatting" "special-events" "sports-1" "pools-hot-tubs-and-beaches" "asmr" "travel-and-outdoors"
)

# Base directory for captures
BASE_DIR="captures"

# Create base directory if it doesn't exist
mkdir -p $BASE_DIR

# Total iterations per rate per category
TOTAL_ITERATIONS=5

# Reset SECONDS at the start
SECONDS=0

# Loop to run the main part for each category
for CATEGORY_NAME in "${CATEGORY_NAMES[@]}"
do
    # Loop for each data rate
    for RATE in "${DATA_RATES[@]}"
    do
        # Directory for current category and rate
        CURRENT_DIR="${BASE_DIR}/${CATEGORY_NAME}/${RATE}Mbps"
        # Create directory for current category and rate
        mkdir -p $CURRENT_DIR

        # Inner loop for iterations 0, 1, 2, 3, and 4
        for i in {0..4}
        do
            # Current timestamp for file naming
            TIMESTAMP=$(date +%Y%m%dT%H%M%S)
            echo "Starting category: $CATEGORY_NAME, iteration: $i, rate: ${RATE}Mbps"

            # Get the ith most popular Twitch URL for the category
            TWITCH_URL=$(python3 get_url.py $CATEGORY_NAME $i)
            echo "Obtained Twitch URL: $TWITCH_URL"

            # Packet capture file path
            PCAP_FILE="${CURRENT_DIR}/pcap_iter${i}_${TIMESTAMP}.pcap"
            
            # Start packet capture in the background
            tcpdump -w $PCAP_FILE -i any & 
            TCPDUMP_PID=$!

            # Run mm-link with the selected trace file and execute the Python script with category
            mm-link $TRACE_FILE $TRACE_FILE -- python3 script.py $TWITCH_URL $CATEGORY_NAME $i $CURRENT_DIR $TIMESTAMP

            # Stop the packet capture
            kill $TCPDUMP_PID

            # Update progress
            let COMPLETED=i+1
            let REMAINING=TOTAL_ITERATIONS-COMPLETED
            ELAPSED_TIME=$(($SECONDS / 60))
            echo "Progress: Category $CATEGORY_NAME, Rate $RATE Mbps - $COMPLETED completed, $REMAINING remaining. Total time taken: $ELAPSED_TIME minutes."
        done
    done
done
