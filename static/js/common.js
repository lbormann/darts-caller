function showFullscreenOverlay(text) {
    if (document.querySelector('.fullscreen-overlay')) return;
    const overlay = document.createElement('div');
    overlay.className = 'fullscreen-overlay';
    overlay.innerText = text;
    document.body.appendChild(overlay);
}

function setupWebSocketConnection(host, port, onOpenHandle, onCloseHandle, onMessageHandle) {
    const socket = new WebSocket(`ws://${host}:${port}`);

    socket.onopen = function() {
        console.log("Socket: connected!");
        onOpenHandle();
    };

    socket.onclose = function() {
        console.log("Socket: disconnected!");
        onCloseHandle();
        setTimeout(() => setupWebSocketConnection(host, port, onmessagehandle), 1000);
    };

    socket.onmessage = function(event) {
        let data = JSON.parse(event.data);
        onMessageHandle(data); 
    };
}

function getRandomInterval(min, max) {
    return Math.random() * (max - min) + min;
}