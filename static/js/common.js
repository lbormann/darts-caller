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




function setupWebSocketConnection(host, port, onOpenHandle, onCloseHandle, onMessageHandle, maxReconnectAttempts = 3, reconnectInterval = 1000) {
    let socket;

    function connect() {
        socket = new WebSocket(`ws://${host}:${port}`);

        socket.onopen = function() {
            console.log("Socket: connected!");
            onOpenHandle(socket);
        };

        socket.onclose = function(event) {
            console.log("Socket: disconnected!");
            onCloseHandle(socket, event);

            if (event.code !== 1000 && maxReconnectAttempts > 0) {
                console.log(`Reconnecting in ${reconnectInterval / 1000} seconds...`);
                setTimeout(connect, reconnectInterval);
                maxReconnectAttempts--;
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
    }

    connect();

    return socket;
}


// function setupWebSocketConnection(host, port, onOpenHandle, onCloseHandle, onMessageHandle) {
//     const socket = new WebSocket(`ws://${host}:${port}`);

//     socket.onopen = function() {
//         console.log("Socket: connected!");
//         onOpenHandle(socket);
//     };

//     socket.onclose = function(event) {
//         console.log("Socket: disconnected!");
//         onCloseHandle(socket);

//         console.log('Code: ' + event.code + ', Reason: ' + event.reason + ', Clean: ' + event.wasClean);
//         setTimeout(() => setupWebSocketConnection(host, port, onOpenHandle, onCloseHandle, onMessageHandle), 1000);
//     };

//     socket.onmessage = function(event) {
//         let data = JSON.parse(event.data);
//         onMessageHandle(socket, data); 
//     };

//     socket.onerror = function(error) {
//         console.error('WebSocket-Fehler aufgetreten: ', error);
//     };

//     // return socket;
// }

