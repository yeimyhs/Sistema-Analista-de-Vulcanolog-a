const ws = new WebSocket('ws://' + window.location.host + '/ws/realtimestobspy/');

ws.onmessage = function(e) {
    var djangoData = JSON.parse(e.data);
    console.log(djangoData.value.data);
    document.querySelector('#app').innerText = djangoData.value;
}