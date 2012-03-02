$(document).ready(function(){
    var ws = new WebSocket($('body').attr('data-web-socket'));
    ws.onmessage = function (msg) {
        $('body').append($('<p>', {'text': msg.data}));
    };
    ws.onopen = function() {
        ws.send('connected');
    };
});
