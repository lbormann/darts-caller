ARG REF \
    REPOSITORY="lbormann/autodarts-caller"

FROM --platform=${BUILDPLATFORM} alpine:latest AS build

ARG REF \
    REPOSITORY \
    TARGETPLATFORM

WORKDIR /
RUN apk update && \
    apk add wget tar && \
    case ${TARGETPLATFORM} in \
        "linux/amd64")  DOWNLOAD_ARCH=""  ;; \
        "linux/arm64") DOWNLOAD_ARCH="-arm64"  ;; \
    esac && \
    ASSETNAME="autodarts-caller$DOWNLOAD_ARCH" && \
    wget "https://github.com/${REPOSITORY}/releases/download/${REF}/$ASSETNAME" && \
    mv $ASSETNAME autodarts-caller

FROM debian:bookworm-slim

ENV AUTODARTS_EMAIL= \
    AUTODARTS_PASSWORD= \
    AUTODARTS_BOARD_ID= \
    MEDIA_PATH='/usr/share/autodarts-caller/media' \
    MEDIA_PATH_SHARED='/usr/share/autodarts-caller/media-shared' \
    CALLER_VOLUME= \
    CALLER= \
    RANDOM_CALLER= \
    RANDOM_CALLER_EACH_LEG= \
    RANDOM_CALLER_LANGUAGE= \
    RANDOM_CALLER_GENDER= \
    CALL_CURRENT_PLAYER= \
    CALL_CURRENT_PLAYER_ALWAYS= \
    CALL_EVERY_DART= \
    CALL_EVERY_DART_SINGLE_FILES= \
    POSSIBLE_CHECKOUT_CALL= \
    POSSIBLE_CHECKOUT_CALL_SINGLE_FILES= \
    POSSIBLE_CHECKOUT_CALL_YOURSELF_ONLY= \
    AMBIENT_SOUNDS= \
    AMBIENT_SOUNDS_AFTER_CALLS= \
    DOWNLOADS= \
    DOWNLOADS_LANGUAGE= \
    DOWNLOADS_LIMIT= \
    DOWNLOADS_NAME= \
    BLACKLIST_PATH= \
    BACKGROUND_AUDIO_VOLUME= \
    WEB_CALLER= \
    WEB_CALLER_SCOREBOARD= \
    WEB_CALLER_PORT=5000 \
    HOST_PORT=8079\
    DEBUG= \
    CERT_CHECK= \
    MIXER_FREQUENCY= \
    MIXER_SIZE= \
    MIXER_CHANNELS= \
    MIXER_BUFFERSIZE=

WORKDIR /usr/bin/autodarts-caller
COPY --from=build /autodarts-caller* ./autodarts-caller
COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x autodarts-caller && \
    chmod +x entrypoint.sh
EXPOSE 5000 8079

CMD ./entrypoint.sh
