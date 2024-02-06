function showFullscreenOverlay(text) {
    if (document.querySelector('.fullscreen-overlay')) return;
    const overlay = document.createElement('div');
    overlay.className = 'fullscreen-overlay';
    overlay.innerText = text;
    document.body.appendChild(overlay);
}

function getRandomInterval(min, max) {
    return Math.random() * (max - min) + min;
}




function setupWebSocketConnection(host, port, onOpenHandle, onCloseHandle, onMessageHandle) {
    const socket = new WebSocket(`ws://${host}:${port}`);

    socket.onopen = function() {
        console.log("Socket: connected!");
        onOpenHandle(socket);
    };

    socket.onclose = function(event) {
        console.log("Socket: disconnected!");
        onCloseHandle(socket);

        if (event.wasClean) {
            console.log('Verbindung geschlossen sauber.');
        } else {
            console.log('Verbindung unerwartet geschlossen.');
        }
        console.log('Code: ' + event.code + ', Grund: ' + event.reason);

        setTimeout(() => setupWebSocketConnection(host, port, onOpenHandle, onCloseHandle, onMessageHandle), 1000);
    };

    socket.onmessage = function(event) {
        let data = JSON.parse(event.data);
        onMessageHandle(socket, data); 
    };

    socket.onerror = function(error) {
        console.error('WebSocket-Fehler aufgetreten: ', error);
    };

    return socket;
}

