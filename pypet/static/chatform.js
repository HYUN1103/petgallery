// 폼 제출 이벤트를 감지하여 메시지를 처리
form.addEventListener('submit', function(e) {
    e.preventDefault(); // 폼의 기본 동작(페이지 새로고침)을 막음

    const user = userField.value; // 사용자 이름 필드에서 값 가져오기
    const message = document.getElementById('formMessage').value; // 메시지 입력 필드에서 값 가져오기

    if (message.trim() !== '') { // 메시지가 빈 문자열이 아닌 경우에만 실행
        const messageElement = document.createElement('p'); // 새 메시지를 담을 <p> 요소 생성
        messageElement.textContent = `${user}: ${message}`; // <p> 요소에 사용자 이름과 메시지 설정
        
        // 메시지를 메시지 박스의 맨 위에 추가
        messageBox.insertBefore(messageElement, messageBox.firstChild);

        // scrollTop을 계산하여 스크롤이 클라이언트 영역에 맞춰지도록 조정
        messageBox.scrollTop = messageBox.scrollHeight - messageBox.clientHeight;

        form.reset(); // 입력 필드를 초기화
    }
});
