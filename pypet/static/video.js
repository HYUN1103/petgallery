// 주어진 페이지 ID로 스크롤 이동 (부드럽게)
function scrollToPage(pageId) {
    document.getElementById(pageId).scrollIntoView({ behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', () => {
    loadMedia(); // 페이지가 로드될 때 미디어 로드


    const videoElements = document.querySelectorAll('video'); // 페이지 내 모든 비디오 요소를 선택

    // 각 비디오 요소에 대해 이벤트 리스너 추가
    videoElements.forEach(video => {
        video.addEventListener('waiting', function() {
            document.getElementById('loadingSpinner').style.display = 'block'; // 버퍼링 시작 시 로딩 스피너 표시
        });

        video.addEventListener('playing', function() {
            document.getElementById('loadingSpinner').style.display = 'none'; // 재생 시작 시 로딩 스피너 숨기기
        });

        video.addEventListener('canplay', function() {
            document.getElementById('loadingSpinner').style.display = 'none'; // 비디오가 재생 가능해지면 로딩 스피너 숨기기
        });
    });  
    
});



// 동영상 추가 모달 열기
function showAddVideoModal() {
    $('#addVideoModal').modal('show');
}

// 동영상 추가 모달 취소 버튼
function cancelAddVideo() {
    document.getElementById('addVideoForm').reset();
    $('#addVideoModal').modal('hide');
}

// 동영상 수정 모달 취소 버튼
function cancelEditVideo() {
    document.getElementById('editVideoForm').reset(); // '수정' 폼 초기화
    $('#editVideoModal').modal('hide');
}

// 동영상 수정 모달 열기
function showEditVideoModal(button) {
    const cardBody = button.closest('.card-body'); // 클릭된 버튼에서 가장 가까운 카드 본문 요소를 찾음
    const card = button.closest('.col'); // 클릭된 버튼에서 가장 가까운 카드 요소를 찾음
    
    const id = card.dataset.id; // 카드 ID
    const title = cardBody.querySelector('.card-title').textContent; // 카드 제목
    const text = cardBody.querySelector('.card-text').textContent; // 카드 내용

    document.getElementById('editVideoId').value = id; // '카드 수정' 모달의 숨겨진 입력 필드에 카드 ID 설정
    document.getElementById('editVideoTitle').value = title; // '카드 수정' 모달의 제목 입력 필드에 기존 카드 제목 설정
    document.getElementById('editVideocontent').value = text; // '카드 수정' 모달의 내용 입력 필드에 기존 카드 내용 설정

    $('#editVideoModal').modal('show');
}

// 동영상 추가 및 카드 표시
function appendVideoCard(video) {
    var cardHtml = `
    <div class="col" data-id="${video.id}">
        <div class="card h-100">
            <video class="card-img-top" controls>
                <source src="${video.file}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div class="card-body">
                <h5 class="card-title">${video.title}</h5>
                <p class="card-text">${video.content}</p>
                <button class="btn btn-warning" onclick="showEditVideoModal(this)">Edit</button> <!-- 수정 버튼 추가 -->
                <button class="btn btn-danger" onclick="deleteVideo(this)(${video.id})">Delete</button> <!-- 삭제 버튼 추가 -->
            </div>
        </div>
    </div>`;

    $('#videoCardContainer').append(cardHtml); // 동영상 카드를 컨테이너에 추가
}

// 동영상 추가 폼 제출 이벤트 처리
$('#addVideoForm').on('submit', function (e) {
    e.preventDefault(); // 폼 기본 제출 동작 방지

    var videoTitle = $('#videoTitle').val(); // 제목 가져오기
    var videocontent = $('#videocontent').val(); // 설명 가져오기
    var videoFile = $('#videoFile')[0].files[0]; // 파일 가져오기
    var username = $('#videoCardContainer').data('username'); // 사용자 이름 가져오기

    var formData = new FormData();
    formData.append('title', videoTitle);
    formData.append('content', videocontent);
    formData.append('video', videoFile);
    formData.append('username', username); // 사용자 이름 추가

    fetch('/media/add', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            loadMedia(); // 카드가 성공적으로 추가되면 카드를 다시 불러옴
            $('#addVideoModal').modal('hide'); // 모달 닫기
            this.reset(); // 폼 초기화
        } else {
            alert('Failed to add video');
        }
    }).catch(error => {
        console.error('Error:', error);
    });
});

// 동영상 수정 폼 제출 이벤트 처리
$('#editVideoForm').on('submit', function (e) {
    e.preventDefault(); // 폼 기본 제출 동작 방지

    var videoId = document.getElementById('editVideoId').value; // 수정할 동영상 ID 가져오기]
    var videoTitle = $('#editVideoTitle').val(); // 제목 가져오기
    var videocontent = $('#editVideocontent').val(); // 설명 가져오기



    var formData = new FormData();
    formData.append('title', videoTitle);
    formData.append('content', videocontent);
    formData.append('video', document.getElementById('editVideoFile').files[0]); // 새로 선택된 동영상 파일 추가
    console.log(document.getElementById('editVideoFile').files);
    formData.append('id', videoId);


    fetch(`/media/update/${videoId}`, {
        method: 'POST', // 서버에 수정 요청
        body: formData // formDate 객체 전송
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadMedia(); // 미디어를 다시 로드하여 변경 사항 반영
            $('#editVideoModal').modal('hide'); // 모달 닫기
        } else {
            alert('Failed to update video'); // 실패시 알림
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// 동영상 삭제 함수
function deleteVideo(videoId) {
    fetch(`/media/delete/${videoId}`, {
        method: 'DELETE'
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            loadMedia(); // 동영상 삭제 후 목록 갱신
        } else {
            alert('Failed to delete video');
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}

// 서버에서 미디어 로드 함수
function loadMedia() {
    fetch('/media/list', {
        method: 'GET'
    }).then(response => response.json())
    .then(media => {
        document.getElementById('videoCardContainer').innerHTML = ''; // 미디어 컨테이너 초기화
        media.forEach(item => {
            const newMedia = document.createElement('div'); // 새 div 요소 생성
            newMedia.className = 'col'; // 클래스 설정
            newMedia.dataset.id = item.id; // 데이터 속성에 미디어 ID 설정
            if (item.username === $('#videoCardContainer').data('username')) {
                newMedia.innerHTML = `
                <div class="card h-100">
                    <video controls class="card-img-top">
                        <source src="${item.video_url}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <div class="card-body">
                        <h5 class="card-title">${item.title}</h5>
                        <p class="card-text">${item.content}</p>
                        <button class="btn btn-primary" onclick="showEditVideoModal(this)">Edit</button>
                        <button class="btn btn-danger" onclick="deleteVideo(${item.id})">Delete</button>
                    </div>
                </div>
                `;
            } else {
                newMedia.innerHTML = `
                <div class="card h-100">
                    <video controls class="card-img-top">
                        <source src="${item.video_url}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <div class="card-body">
                        <h5 class="card-title">${item.title}</h5>
                        <p class="card-text">${item.content}</p>
                    </div>
                </div>
                `;
            }
            document.getElementById('videoCardContainer').appendChild(newMedia); // 미디어 컨테이너에 새 미디어 추가
        });
    }).catch(error => {
        console.error('Error:', error); // 에러 발생 시 콘솔에 출력
    });
}

