#!/bin/bash


# -----------------------------------------
# ARGUMENTS

# Required:
autodarts_email="TODO"
autodarts_password="TODO"
autodarts_board_id="TODO"
media_path="TODO"

# Optional:

# ------------------------------------------







# DO NOT CHANGE ANYTHING BY THIS LINE!

python3 -U \
          "$autodarts_email" \
          -P \
          "$autodarts_password" \
          -B \
          "$autodarts_board_id" \
          -M \
          "$media_path"