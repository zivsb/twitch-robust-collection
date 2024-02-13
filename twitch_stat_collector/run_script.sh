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
        TRACE_FILE="${RATE}mbps.trace"s
        CURRENT_DIR="${BASE_DIR}/${CATEGORY_NAME}/${RATE}Mbps"
        mkdir -p $CURRENT_DIR

        # Initialize a counter for successful iterations
        successful_iterations=0

        # Initialize an index for fetching URLs
        i=0

        # While loop to ensure 5 successful data collections
        while [ $successful_iterations -lt $TOTAL_ITERATIONS ]
        do
            TIMESTAMP=$(date +%Y%m%dT%H%M%S)
            echo "Attempting category: $CATEGORY_NAME, try: $i, rate: ${RATE}Mbps, successful so far: $successful_iterations"

            TWITCH_URL=$(python3 get_url.py $CATEGORY_NAME $i)
            echo "Obtained Twitch URL: $TWITCH_URL"

            PCAP_FILE="${CURRENT_DIR}/pcap_try${i}_${TIMESTAMP}.pcap"
            tcpdump -w $PCAP_FILE -i any & 
            TCPDUMP_PID=$!

            mm-link $TRACE_FILE $TRACE_FILE -- python3 script.py $TWITCH_URL $CATEGORY_NAME $i $CURRENT_DIR $TIMESTAMP | tee temp_output.txt

            if tail -n 1 temp_output.txt | grep -q 'SKIPPING STREAM'; then
                echo "Stream was age-restricted, skipping..."
                # Do not increment successful_iterations
            else
                echo "Stream completed successfully."
                let successful_iterations++
            fi

            rm temp_output.txt
            kill $TCPDUMP_PID

            ELAPSED_TIME=$(($SECONDS / 60))
            echo "Progress: Category $CATEGORY_NAME, Rate $RATE Mbps - $successful_iterations collected, Total time taken: $ELAPSED_TIME minutes."

            # Increment the index for the next URL
            let i++
        done
    done
done
