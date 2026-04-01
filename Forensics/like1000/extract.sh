#!/bin/bash

# Loop from 1000 down to 1
for ((i=1000; i>=1; i--)); do
    # Check if the tar file exists
    if [ -f "$i.tar" ]; then
        echo "Extracting $i.tar..."
        # Extract the file
        tar -xf "$i.tar"
        # Optional: remove the old tar to keep the directory clean
        # rm "$i.tar"
    else
        echo "Finished or $i.tar not found."
        break
    fi
done

