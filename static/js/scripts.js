$(document).ready(function() {
    var urlParams = new URLSearchParams(window.location.search);
    var tab = urlParams.get('tab');
    
    if (tab) {
        $('.nav-tabs a[href="#' + tab + '"]').tab('show');
    }
});

function editProduct(productId) {
    console.log(`Editing product with ID: ${productId}`); // 동작 확인을 위한 로그
    var nameCell = document.getElementById('name_' + productId);
    var colorCell = document.getElementById('color_' + productId);
    var nameValue = nameCell.innerText;
    var colorValue = colorCell.innerText;

    // 텍스트 필드로 변환
    nameCell.innerHTML = `<input type="text" id="inputName_${productId}" value="${nameValue}" class="form-control">`;
    colorCell.innerHTML = `<input type="text" id="inputColor_${productId}" value="${colorValue}" class="form-control">`;

    // 수정 버튼을 저장 버튼으로 변경
    var actionCell = document.getElementById('action_' + productId);
    actionCell.innerHTML = `<button onclick="saveProduct(${productId})" class="btn btn-success btn-sm">저장</button>`;
}

function saveProduct(productId) {
    console.log(`Saving product with ID: ${productId}`); // 동작 확인을 위한 로그
    var newName = document.getElementById('inputName_' + productId).value.trim();
    var newColor = document.getElementById('inputColor_' + productId).value.trim();

    // 필드 검증
    if (!newName || !newColor) {
        alert('제품 이름과 색상을 모두 입력해주세요.');
        return;
    }

    // AJAX 요청 설정
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/edit_product/" + productId, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function() {
        if (xhr.status == 200) {
            // 페이지에서 직접 텍스트 업데이트
            document.getElementById('name_' + productId).innerText = newName;
            document.getElementById('color_' + productId).innerText = newColor;

            // 저장 버튼을 다시 수정 버튼으로 변경하고 삭제 버튼도 유지
            var actionCell = document.getElementById('action_' + productId);
            actionCell.innerHTML = `
                <button onclick="editProduct(${productId})" class="btn btn-warning btn-sm">수정</button>
                <form method="post" style="display: inline;">
                    <input type="hidden" name="delete" value="${productId}">
                    <button type="submit" class="btn btn-danger btn-sm">삭제</button>
                </form>
            `;
        } else {
            alert('수정에 실패했습니다.');
        }
    };
    xhr.send(`name=${encodeURIComponent(newName)}&color=${encodeURIComponent(newColor)}`);
}

function editBranche(brancheId) {
    console.log(`Editing branch with ID: ${brancheId}`); // 동작 확인을 위한 로그
    var nameCell = document.getElementById('name_' + brancheId);
    var emailCell = document.getElementById('email_' + brancheId);
    var nameValue = nameCell.innerText;
    var emailValue = emailCell.innerText;

    nameCell.innerHTML = `<input type="text" id="inputName_${brancheId}" value="${nameValue}" class="form-control">`;
    emailCell.innerHTML = `<input type="text" id="inputEmail_${brancheId}" value="${emailValue}" class="form-control">`;

    var actionCell = document.getElementById('action_' + brancheId);
    actionCell.innerHTML = `<button onclick="saveBranche(${brancheId})" class="btn btn-success btn-sm">저장</button>`;
}

function saveBranche(brancheId) {
    console.log(`Saving branch with ID: ${brancheId}`); // 동작 확인을 위한 로그
    var newName = document.getElementById('inputName_' + brancheId).value.trim();
    var newEmail = document.getElementById('inputEmail_' + brancheId).value.trim();

    if (!newName || !newEmail) {
        alert('지점 이름과 이메일을 모두 입력해주세요.');
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/edit_branche/" + brancheId, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function() {
        console.log(`Response for product ID ${productId}:`, xhr.responseText); // 응답 로그
        
        if (xhr.status == 200) {
            document.getElementById('name_' + brancheId).innerText = newName;
            document.getElementById('email_' + brancheId).innerText = newEmail;

            var actionCell = document.getElementById('action_' + brancheId);
            actionCell.innerHTML = `
                <button onclick="editBranche(${brancheId})" class="btn btn-warning btn-sm">수정</button>
                <form method="post" style="display: inline;">
                    <input type="hidden" name="delete" value="${brancheId}">
                    <button type="submit" class="btn btn-danger btn-sm">삭제</button>
                </form>
            `;
        } else {
            console.error('Failed to save product:', xhr.status, xhr.statusText); // 실패 로그
            alert('수정에 실패했습니다.');
        }
    };
    xhr.send(`name=${encodeURIComponent(newName)}&email=${encodeURIComponent(newEmail)}`);
}