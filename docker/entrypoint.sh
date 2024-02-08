#!/bin/sh
args=""
if [ -n "$AUTODARTS_EMAIL" ]; then
  args="$args -U $AUTODARTS_EMAIL"
fi
if [ -n "$AUTODARTS_PASSWORD" ]; then
  args="$args -P $AUTODARTS_PASSWORD"
fi
if [ -n "$AUTODARTS_BOARD_ID" ]; then
  args="$args -B $AUTODARTS_BOARD_ID"
fi
if [ -n "$MEDIA_PATH" ]; then
  args="$args -M $MEDIA_PATH"
fi
if [ -n "$MEDIA_PATH_SHARED" ]; then
  args="$args -MS $MEDIA_PATH_SHARED"
fi
if [ -n "$CALLER_VOLUME" ]; then
  args="$args -V $CALLER_VOLUME"
fi
if [ -n "$CALLER" ]; then
  args="$args -C $CALLER"
fi
if [ -n "$RANDOM_CALLER" ]; then
  args="$args -R $RANDOM_CALLER"
fi
if [ -n "$RANDOM_CALLER_EACH_LEG" ]; then
  args="$args -L $RANDOM_CALLER_EACH_LEG"
fi
if [ -n "$RANDOM_CALLER_LANGUAGE" ]; then
  args="$args -RL $RANDOM_CALLER_LANGUAGE"
fi
if [ -n "$RANDOM_CALLER_GENDER" ]; then
  args="$args -RG $RANDOM_CALLER_GENDER"
fi
if [ -n "$CALL_CURRENT_PLAYER" ]; then
  args="$args -CCP $CALL_CURRENT_PLAYER"
fi
if [ -n "$CALL_CURRENT_PLAYER_ALWAYS" ]; then
  args="$args -CCP $CALL_CURRENT_PLAYER_ALWAYS"
fi
if [ -n "$CALL_EVERY_DART" ]; then
  args="$args -E $CALL_EVERY_DART"
fi
if [ -n "$CALL_EVERY_DART_SINGLE_FILES" ]; then
  args="$args -ESF $CALL_EVERY_DART_SINGLE_FILES"
fi
if [ -n "$POSSIBLE_CHECKOUT_CALL" ]; then
  args="$args -PCC $POSSIBLE_CHECKOUT_CALL"
fi
if [ -n "$POSSIBLE_CHECKOUT_CALL_SINGLE_FILES" ]; then
  args="$args -PCCSF $POSSIBLE_CHECKOUT_CALL_SINGLE_FILES"
fi
if [ -n "$POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY" ]; then
  args="$args -PCCYO $POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY"
fi
if [ -n "$AMBIENT_SOUNDS" ]; then
  args="$args -A $AMBIENT_SOUNDS"
fi
if [ -n "$AMBIENT_SOUNDS_AFTER_CALLS" ]; then
  args="$args -AAC $AMBIENT_SOUNDS_AFTER_CALLS"
fi
if [ -n "$DOWNLOADS" ]; then
  args="$args -DL $DOWNLOADS"
fi
if [ -n "$DOWNLOADS_LANGUAGE" ]; then
  args="$args -DLLA $DOWNLOADS_LANGUAGE"
fi
if [ -n "$DOWNLOADS_LIMIT" ]; then
  args="$args -DLL $DOWNLOADS_LIMIT"
fi
if [ -n "$DOWNLOADS_NAME" ]; then
  args="$args -DLN $DOWNLOADS_NAME"
fi
if [ -n "$BLACKLIST_PATH" ]; then
  args="$args -BLP $BLACKLIST_PATH"
fi
if [ -n "$BACKGROUND_AUDIO_VOLUME" ]; then
 args="$args -BAV $BACKGROUND_AUDIO_VOLUME"
fi
if [ -n "$WEB_CALLER" ]; then
  args="$args -WEB $WEB_CALLER"
fi
if [ -n "$WEB_CALLER_SCOREBOARD" ]; then
  args="$args -WEBSB $WEB_CALLER_SCOREBOARD"
fi
if [ -n "$WEB_CALLER_PORT" ]; then
  args="$args -WEBP $WEB_CALLER_PORT"
fi
if [ -n "$HOST_PORT" ]; then
  args="$args -HP $HOST_PORT"
fi
if [ -n "$DEBUG" ]; then
  args="$args -DEB $DEBUG"
fi
if [ -n "$CERT_CHECK" ]; then
  args="$args -DEB $CERT_CHECK"
fi
if [ -n "$MIXER_FREQUENCY" ]; then
  args="$args -MIF $MIXER_FREQUENCY"
fi
if [ -n "$MIXER_SIZE" ]; then
  args="$args -MIS $MIXER_SIZE"
fi
if [ -n "$MIXER_CHANNELS" ]; then
  args="$args -MIC $MIXER_CHANNELS"
fi
if [ -n "$MIXER_BUFFERSIZE" ]; then
  args="$args -MIB $MIXER_BUFFERSIZE"
fi

./autodarts-caller $args