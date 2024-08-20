// DOM이 로드되었을 때 카드 불러오기
document.addEventListener('DOMContentLoaded', () => {
    loadCards(); // 페이지가 로드될 때 loadCards 함수를 호출하여 카드 목록을 불러옴
});
console.log($.fn.jquery);
// 카드 추가 모달 표시
function showAddCardModal() {
    $('#addCardModal').modal('show'); // '카드 추가' 모달을 표시
}

// 카드 추가 모달 취소 버튼
function cancelAddCard() {
    document.getElementById('addCardForm').reset(); // '카드 추가' 폼 초기화
    $('#addCardModal').modal('hide'); // '카드 추가' 모달을 숨김
}

// 카드 수정 모달 취소 버튼
function cancelEditCard() {
    document.getElementById('editCardForm').reset(); // '카드 수정' 폼 초기화
    $('#editCardModal').modal('hide'); // '카드 수정' 모달을 숨김
}

// 카드 추가 폼 제출 처리
document.getElementById('addCardForm').addEventListener('submit', function (e) {
    e.preventDefault(); // 폼 제출 기본 동작을 막음
    addCard(); // addCard 함수를 호출하여 카드 추가 처리
    $('#addCardModal').modal('hide'); // '카드 추가' 모달을 숨김
});

// 카드 수정 폼 제출 처리
document.getElementById('editCardForm').addEventListener('submit', function (e) {
    e.preventDefault(); // 폼 제출 기본 동작을 막음
    updateCard(); // updateCard 함수를 호출하여 카드 수정 처리
    $('#editCardModal').modal('hide'); // '카드 수정' 모달을 숨김
});

// 카드 추가 함수
function addCard() {
    const title = document.getElementById('cardTitle').value; // 입력된 카드 제목을 가져옴
    const text = document.getElementById('cardText').value; // 입력된 카드 내용을 가져옴
    const imageInput = document.getElementById('cardImage'); // 업로드된 이미지 파일을 가져옴
    const imageUrl = URL.createObjectURL(imageInput.files[0]); // 이미지의 Blob URL 생성
    const cardContainer = document.getElementById('cardContainer');
    const userId = cardContainer.dataset.userId; // 사용자 ID 가져오기
    const username = cardContainer.dataset.username; // 사용자 이름 가져오기

    const newCard = document.createElement('div'); // 새 div 요소 생성
    newCard.className = 'col'; // 클래스 설정
    newCard.dataset.id = userId; // 데이터 속성에 사용자 ID 설정
    newCard.dataset.userId = userId; // 사용자 ID 저장
    newCard.dataset.username = username; // 사용자 이름 저장
    newCard.innerHTML = `
        <div class="card h-100">
            <img src="${imageUrl}" class="card-img-top" alt="Card image"> <!-- 이미지 설정 -->
            <div class="card-body">
                <h5 class="card-title">${title}</h5> <!-- 카드 제목 설정 -->
                <p class="card-text">${text}</p> <!-- 카드 내용 설정 -->
                <p class="card-text">username: ${username}</p>
                <button class="btn btn-primary" onclick="showEditCardModal(this)">modify</button> <!-- 수정 버튼 -->
                <button class="btn btn-danger" onclick="deleteCard(this)">삭제</button> <!-- 삭제 버튼 -->
            </div>
        </div>
    `;

    document.getElementById('cardContainer').appendChild(newCard); // 새 카드 요소를 카드 컨테이너에 추가

    saveCard({ id: userId, title, text, imageUrl, username });  // 로컬 스토리지에 카드 정보 저장

    const formData = new FormData(document.getElementById('addCardForm')); // '카드 추가' 폼 데이터를 FormData 객체로 생성
    formData.append('user_id', userId); // 사용자 ID 추가
    formData.append('username', username); // 사용자 이름 추가
    formData.append('title', title);
    formData.append('text', text);
    formData.append('image', imageInput.files[0]);

    fetch('/card/add', {
        method: 'POST', // POST 요청
        body: formData // 폼 데이터를 요청 본문에 포함
    }).then(response => response.json()) // 응답을 JSON으로 파싱
    .then(data => {
        if (data.success) {
            loadCards(); // 카드가 성공적으로 추가되면 카드를 다시 불러옴
        } else {
            alert('Failed to add card'); // 실패 시 알림
        }
    }).catch(error => {
        console.error('Error:', error); // 에러 발생 시 콘솔에 출력
    });

    // 폼 초기화
    document.getElementById('addCardForm').reset(); // '카드 추가' 폼 초기화
}

// 카드 삭제 함수
function deleteCard(button) {
    const card = button.closest('.col'); // 클릭된 버튼에서 가장 가까운 카드 요소를 찾음
    const cardId = card.dataset.id; 
    removeCardFromStorage(cardId); // 로컬 스토리지에서 해당 카드 정보 제거
    card.remove(); // 카드 요소를 DOM에서 제거

    fetch(`/card/delete/${cardId}`, { // 서버에 카드 삭제 요청
        method: 'DELETE' // DELETE 요청
    }).then(response => response.json()) // 응답을 JSON으로 파싱
    .then(data => {
        if (data.success) {
            card.remove(); // 카드가 성공적으로 삭제되면 해당 카드 요소 제거
        } else {
            alert('Failed to delete card'); // 실패 시 알림
        }
    }).catch(error => {
        console.error('Error:', error); // 에러 발생 시 콘솔에 출력
    });
}

// 카드 수정 모달 표시 함수
function showEditCardModal(button) {
    const cardBody = button.closest('.card-body'); // 클릭된 버튼에서 가장 가까운 카드 본문 요소를 찾음
    const card = button.closest('.col'); // 클릭된 버튼에서 가장 가까운 카드 요소를 찾음
    const id = card.dataset.id; // 카드 ID
    const title = cardBody.querySelector('.card-title').textContent; // 카드 제목
    const text = cardBody.querySelector('.card-text').textContent; // 카드 내용

    document.getElementById('editCardTitle').value = title; // '카드 수정' 모달의 제목 입력 필드에 기존 카드 제목 설정
    document.getElementById('editCardText').value = text; // '카드 수정' 모달의 내용 입력 필드에 기존 카드 내용 설정
    document.getElementById('editCardForm').dataset.id = id; // '카드 수정' 폼 데이터 속성에 카드 ID 설정

    $('#editCardModal').modal('show'); // '카드 수정' 모달을 표시
}

// 카드 수정 함수
function updateCard() {
    const id = document.getElementById('editCardForm').dataset.id; // '카드 수정' 폼 데이터 속성에서 카드 ID 가져옴
    const title = document.getElementById('editCardTitle').value; // '카드 수정' 모달의 제목 입력 필드에서 새로운 제목 가져옴
    const text = document.getElementById('editCardText').value; // '카드 수정' 모달의 내용 입력 필드에서 새로운 내용 가져옴
    const imageInput = document.getElementById('editCardImage'); // '카드 수정' 모달의 이미지 입력 필드
    const card = document.querySelector(`#cardContainer [data-id="${id}"]`); // 카드 컨테이너에서 해당 카드 요소 찾음
    const cardBody = card.querySelector('.card-body'); // 카드 본문 요소 찾음

    let imageUrl = card.querySelector('.card-img-top').src; // 기존 이미지 URL 기본값

    if (title) cardBody.querySelector('.card-title').textContent = title; // 제목이 있으면 카드 제목 업데이트
    if (text) cardBody.querySelector('.card-text').textContent = text; // 내용이 있으면 카드 내용 업데이트

    if (imageInput.files && imageInput.files.length > 0) { // 새로운 이미지 파일이 업로드되었는지 확인
        imageUrl = URL.createObjectURL(imageInput.files[0]); // 이미지의 Blob URL 생성
        card.querySelector('.card-img-top').src = imageUrl; // 카드 이미지 업데이트
    }

    updateCardInStorage({ id, title, text, imageUrl }); // 로컬 스토리지에서 카드 정보 업데이트

    // 서버에 카드 수정 요청
    const formData = new FormData();
    formData.append('id', id);
    formData.append('title', title);
    formData.append('text', text);
    if (imageInput.files && imageInput.files.length > 0) {
        formData.append('image', imageInput.files[0]);
    }

    fetch(`/card/update/${id}`, {
        method: 'PUT', // PUT 요청
        body: formData // 폼 데이터를 요청 본문에 포함
    }).then(response => response.json()) // 응답을 JSON으로 파싱
    .then(data => {
        if (data.success) {
            loadCards(); // 카드가 성공적으로 수정되면 카드를 다시 불러옴
        } else {
            alert('Failed to update card'); // 실패 시 알림
        }
    }).catch(error => {
        console.error('Error:', error); // 에러 발생 시 콘솔에 출력
    });
}

// 카드 저장 함수
function saveCard(card) {
    let cards = JSON.parse(localStorage.getItem('cards')) || []; // 로컬 스토리지에서 기존 카드 목록 불러옴
    cards.push(card); // 새 카드 추가
    localStorage.setItem('cards', JSON.stringify(cards)); // 업데이트된 카드 목록을 로컬 스토리지에 저장
}

// 카드 삭제 함수 (스토리지에서 제거)
function removeCardFromStorage(id) {
    let cards = JSON.parse(localStorage.getItem('cards')) || []; // 로컬 스토리지에서 기존 카드 목록 불러옴
    cards = cards.filter(card => card.id !== id); // 해당 카드 ID와 일치하지 않는 카드들로 필터링
    localStorage.setItem('cards', JSON.stringify(cards)); // 업데이트된 카드 목록을 로컬 스토리지에 저장
}

// 카드 수정 함수 (스토리지 업데이트)
function updateCardInStorage(updatedCard) {
    let cards = JSON.parse(localStorage.getItem('cards')) || []; // 로컬 스토리지에서 기존 카드 목록 불러옴
    cards = cards.map(card => card.id === updatedCard.id ? updatedCard : card); // 해당 카드 ID와 일치하는 카드를 업데이트
    localStorage.setItem('cards', JSON.stringify(cards)); // 업데이트된 카드 목록을 로컬 스토리지에 저장
}

// 카드 로드 함수 (스토리지에서 불러오기)
function loadCards() {
    localStorage.clear();
    fetch('/card/list', {
        method: 'GET'
    }).then(response => response.json())
        .then(card => {
            document.getElementById('cardContainer').innerHTML = ''; // 컨테이너 초기화
            card.forEach(item => {
                const newCard = document.createElement('div'); // 새 div 요소 생성
                newCard.className = 'col'; // 클래스 설정
                newCard.dataset.id = item.id; // 데이터 속성에 미디어 ID 설정
                if (item.login_user == item.username) {
                    newCard.innerHTML = `
                            <div class="card h-100">
                                <img src="${item.image_url}" class="card-img-top" alt="Card image"> <!-- 이미지 설정 -->
                                <div class="card-body">
                                    <h5 class="card-title">${item.title}</h5> <!-- 카드 제목 설정 -->
                                    <p class="card-text">${item.text}</p> <!-- 카드 내용 설정 -->
                                    <p class="card-text">Uploaded by: ${item.username}</p> <!-- 추가 -->
                                    <button class="btn btn-primary" onclick="showEditCardModal(this)">수정</button> <!-- 수정 버튼 -->
                                    <button class="btn btn-danger" onclick="deleteCard(this)">삭제</button> <!-- 삭제 버튼 -->
                                </div>
                            </div>
                    `;
                } else {
                    newCard.innerHTML = `
                    <div class="card h-100">
                        <img src="${item.image_url}" class="card-img-top" alt="Card image"> <!-- 이미지 설정 -->
                        <div class="card-body">
                            <h5 class="card-title">${item.title}</h5> <!-- 카드 제목 설정 -->
                            <p class="card-text">${item.text}</p> <!-- 카드 내용 설정 -->
                            <p class="card-text">Uploaded by: ${item.username}</p> <!-- 추가 -->
                        </div>
                    </div>
                    `;
                }
                document.getElementById('cardContainer').appendChild(newCard); // 미디어 컨테이너에 새 미디어 추가
            });
        }).catch(error => {
            console.error('Error:', error);
        });

    // fetch('/card/list', {
    //     method: 'GET'
    // }).then(response => response.json())
    // .then(data => {
    //     if (data.success) {
    //         loadCards(); // 카드가 성공적으로 추가되면 카드를 다시 불러옴
    //     } else {
    //         alert('Failed to add card'); // 실패 시 알림
    //     }
    // }).catch(error => {
    //     console.error('Error:', error); // 에러 발생 시 콘솔에 출력
    // });

    // document.getElementById('cardContainer').innerHTML = ''; // 기존 카드를 초기화
    // let cards = JSON.parse(localStorage.getItem('cards')) || []; // 로컬 스토리지에서 카드 목록 불러옴
    // cards.forEach(card => { // 각 카드에 대해 새로운 카드 요소를 생성
    //     const newCard = document.createElement('div'); // 새 div 요소 생성
    //     newCard.className = 'col'; // 클래스 설정
    //     newCard.dataset.id = card.id; // 데이터 속성에 카드 ID 설정
    //     newCard.innerHTML = `
    //         <div class="card h-100">
    //             <img src="${card.imageUrl}" class="card-img-top" alt="Card image"> <!-- 이미지 설정 -->
    //             <div class="card-body">
    //                 <h5 class="card-title">${card.title}</h5> <!-- 카드 제목 설정 -->
    //                 <p class="card-text">${card.text}</p> <!-- 카드 내용 설정 -->
    //                 <p class="card-text">Uploaded by: ${card.username}</p> <!-- 추가 -->
    //                 <button class="btn btn-primary" onclick="showEditCardModal(this)">수정</button> <!-- 수정 버튼 -->
    //                 <button class="btn btn-danger" onclick="deleteCard(this)">삭제</button> <!-- 삭제 버튼 -->
    //             </div>
    //         </div>
    //     `;
    //     document.getElementById('cardContainer').appendChild(newCard); // 카드 컨테이너에 새 카드 추가
    // });
}
