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


function setupWebSocketConnection(protocol, host, port, onOpenHandle, onCloseHandle, onMessageHandle, maxReconnectAttempts = 3, reconnectInterval = 1000) {
    const socket = new WebSocket(`${protocol}://${host}:${port}`);

    socket.onopen = function() {
        console.log("Socket: connected!");
        onOpenHandle(socket);
    };

    socket.onclose = function(event) {
        console.log("Socket: disconnected!");
        onCloseHandle(socket, event);

        if (event.code !== 1000) {
            console.log(`Reconnecting in ${reconnectInterval / 1000} seconds...`);
            setTimeout(function() {
                return setupWebSocketConnection(protocol, host, port, onOpenHandle, onCloseHandle, onMessageHandle, maxReconnectAttempts, reconnectInterval);
            }, reconnectInterval);
        }
    };

    socket.onmessage = function(event) {
        try {
            let data = JSON.parse(event.data);
            onMessageHandle(socket, data);
        } catch (error) {
            console.error('Error parsing incoming JSON:', error);
        }
    };

    socket.onerror = function(error) {
        console.error('WebSocket error occurred:', error);
    };

    return socket;
}

