#!/bin/sh
cd "${0%/*}" || exit                                # Run from this directory
. ${WM_PROJECT_DIR:?}/bin/tools/CleanFunctions      # Tutorial clean functions
#------------------------------------------------------------------------------

cleanCase0

#------------------------------------------------------------------------------
# Set the known paths
SOURCE_DIR="./0.orig"   
DEST_DIR="./0"   

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Source directory '$SOURCE_DIR' does not exist."
    exit 1
fi

# Create the destination directory
mkdir -p "$DEST_DIR"

# Copy the entire contents of source to destination
cp -r "$SOURCE_DIR"/* "$DEST_DIR"

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "Contents of '$SOURCE_DIR' copied to '$DEST_DIR' successfully."
else
    echo "Failed to copy contents."
    exit 1
fi