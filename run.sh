#!/bin/bash

PYTHON_SCRIPT="gather.py"
TICKER_FILE="ticker.txt"

while IFS= read -r ticker; do
    if [[ -z "$ticker" ]]; then
        continue 
    fi

    echo "Processing ticker: $ticker"
    python3 "$PYTHON_SCRIPT" "$ticker"

    echo "Done with $ticker"
    echo "=============================="
    
done < "$TICKER_FILE"