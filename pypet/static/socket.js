document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    console.log('11111');
    console.log('location message:', {'socket': location.port});
    console.log('message:', {'doc': document.domain});
    console.log('ddd:', {'document': document});
    console.log(socket);

    document.querySelector('#messageForm').onsubmit = function () {
        var userName = document.getElementById('formUser');
        var userMessage = document.getElementById('formMessage');

        let userInfo = userName.value;
        let messageInfo = userMessage.value;

        console.log('Sending message:', {'user': userInfo, 'message': messageInfo});  // 메시지 보내기 전 로그

        // 메시지 데이터 보내기 : 클라이언트에서 서버로 메세지 보내는 역할
        socket.emit('message', {'user': userInfo, 'message': messageInfo});
        console.log(socket);

        // 메시지 입력 내용 초기화
        userMessage.value = "";

        return false;
    };

    // 서버로부터 메시지를 받을 때 화면에 표시
    // 서버가 보낸 것을 클라이언트가 받는 부분
    socket.on('message', function(data) {
        console.log('Received message from server:', data);  // 서버로부터 메시지 받기 후 로그

        var messageBox = document.getElementById('messageBox');
        var newMessage = document.createElement('p');
        newMessage.textContent = data.user + ": " + data.message;
        messageBox.appendChild(newMessage);
    });
});