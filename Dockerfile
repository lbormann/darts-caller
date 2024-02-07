ARG PYTHON_VERSION \
    REF \
    REPOSITORY="lbormann/autodarts-caller"

FROM --platform=${BUILDPLATFORM} python:${PYTHON_VERSION}-slim-bookworm AS build

ARG PYTHON_VERSION \
    REF \
    REPOSITORY \
    TARGETPLATFORM

ENV AUTODARTS_EMAIL='' \
    AUTODARTS_PASSWORD='' \
    AUTODARTS_BOARD_ID='' \
    AUTODARTS_MEDIA_PATH='/usr/share/autodarts-caller/media'

WORKDIR /
RUN apt update && \
    apt install -y wget tar && \
    case ${TARGETPLATFORM} in \
        "linux/amd64")  DOWNLOAD_ARCH=""  ;; \
        "linux/arm64") DOWNLOAD_ARCH="-arm64"  ;; \
    esac && \
    wget "https://github.com/${REPOSITORY}/releases/download/${REF}/autodarts-caller$DOWNLOAD_ARCH"

FROM python:${PYTHON_VERSION}-slim-bookworm

WORKDIR /usr/share/autodarts-caller
COPY --from=build /autodarts-caller* ./autodarts-caller
EXPOSE 5000 8079

CMD [ "./autodarts-caller", "-U", "${AUTODARTS_EMAIL}", "-P", "${AUTODARTS_PASSWORD}", "-B", "${AUTODARTS_BOARD_ID}", "-M", "${AUTODARTS_MEDIA_PATH}"]
