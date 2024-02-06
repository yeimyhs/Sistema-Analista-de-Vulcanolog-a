    const ws = new WebSocket('ws://' + window.location.host + ':8003/ws/realtimestobspy/');

    ws.onmessage = function(e) {
        var djangoData = JSON.parse(e.data);
        console.log(djangoData.value);
        console.log(djangoData.time);
        document.querySelector('#app').innerText = djangoData.value;
        document.querySelector('#app2').innerText = djangoData.time;
    }