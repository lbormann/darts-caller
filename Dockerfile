ARG PYTHON_VERSION
FROM --platform=${TARGETPLATFORM} python:${PYTHON_VERSION}-slim-bookworm

ENV AUTODARTS_EMAIL='' \
    AUTODARTS_PASSWORD='' \
    AUTODARTS_BOARD_ID='' \
    AUTODARTS_MEDIA_PATH='/usr/share/autodarts-caller/media'

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update && \
    apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev python3-setuptools python3-dev python3-numpy && \
    pip3 install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000 8079

CMD [ "python", "./autodarts-caller.py", "-U", "${AUTODARTS_EMAIL}", "-P", "${AUTODARTS_PASSWORD}", "-B", "${AUTODARTS_BOARD_ID}", "-M", "${AUTODARTS_MEDIA_PATH}"]