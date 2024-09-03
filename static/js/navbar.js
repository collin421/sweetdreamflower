// 햄버거 버튼 액션
document.querySelector('.custom-hamburger').addEventListener('click', function() {
    document.querySelector('.custom-sidebar').style.right = '0';
    document.querySelector('.custom-overlay').style.display = 'block';
});

document.querySelector('.close-btn').addEventListener('click', function() {
    document.querySelector('.custom-sidebar').style.right = '-250px';
    document.querySelector('.custom-overlay').style.display = 'none';
});

document.querySelector('.custom-overlay').addEventListener('click', function() {
    document.querySelector('.custom-sidebar').style.right = '-250px';
    this.style.display = 'none';
});

document.addEventListener('DOMContentLoaded', function () {
    // 현재 페이지의 URL을 파싱하여 path 변수에 저장
    const path = window.location.pathname;

    // 모든 메뉴 항목을 선택
    const menuItems = document.querySelectorAll('.custom-menu a, .custom-sidebar a');

    // 모든 메뉴 항목을 반복하면서, href 속성이 현재 path와 일치하는 항목을 찾음
    menuItems.forEach(function(item) {
        if (item.getAttribute('href') === path) {
            // 일치하는 항목에 'active' 클래스를 추가하여 하이라이트
            item.classList.add('active');
        } else {
            // 일치하지 않는 항목에서는 'active' 클래스 제거
            item.classList.remove('active');
        }
    });
});
