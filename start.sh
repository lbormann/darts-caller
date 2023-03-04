#!/bin/bash


# -----------------------------------------
# ARGUMENTS

# Required:
autodarts_email="TODO"
autodarts_password="TODO"
autodarts_board_id="TODO"
media_path="TODO"


# TODO (dev)
# Optional:
# media_path_shared=
# caller_volume
# caller
# random_caller
# random_caller_each_leg
# call_current_player
# call_every_dart
# call_every_dart_single_files
# possible_checkout_call
# possible_checkout_call_single_files
# ambient_sounds
# ambient_sounds_after_calls
# downloads
# downloads_limit
# downloads_path
# background_audio_volume
# host_port



# ------------------------------------------



# String erstellen
opts=""

# Bedingte Anweisungen, um den String basierend auf den Variablen zu erstellen
if [ -n "$name" ]; then
  opts="$opts -MS \"$name\""
fi

if [ -n "$age" ]; then
  opts="$opts Alter: $age,"
fi

if [ -n "$city" ]; then
  opts="$opts Stadt: $city,"
fi

# Entfernen des letzten Kommas aus dem String
# opts="${opts%,}"

echo "Optional arguments: $opts"



# DO NOT CHANGE ANYTHING BY THIS LINE!

python3 autodarts-caller.py -U "$autodarts_email" -P "$autodarts_password" -B "$autodarts_board_id" -M "$media_path""$opts"