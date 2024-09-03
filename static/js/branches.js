$(document).ready(function() {
    // URL에서 탭 정보를 추출하여 해당 탭을 활성화
    var urlParams = new URLSearchParams(window.location.search);
    var tab = urlParams.get('tab');
    
    if (tab) {
        $('.nav-tabs a[href="#' + tab + '"]').tab('show');
    }
});

// 수정하기
function editBranch(branchId) {
    var nameCell = document.getElementById('name_' + branchId);
    var nameValue = nameCell.innerText;

    nameCell.innerHTML = `<input type="text" id="inputName_${branchId}" value="${nameValue}" class="form-control">`;

    var actionCell = document.getElementById('action_' + branchId);
    actionCell.innerHTML = `<button onclick="saveBranch(${branchId})" class="btn btn-success btn-sm" style="margin-right: 5px;">저장</button>` +
                           `<button onclick="cancelEdit(${branchId}, '${nameValue}')" class="btn btn-secondary btn-sm">취소</button>`;
}


function saveBranch(branchId) {
    var newName = document.getElementById('inputName_' + branchId).value.trim();

    // 이름이 입력되었는지 확인
    if (!newName) {
        alert('지점 이름을 입력해주세요.');
        return;
    }

    // 서버에 업데이트 요청을 전송
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/edit_branch/" + branchId, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function() {
        if (xhr.status === 200) {
            // 성공적으로 데이터 업데이트 후 UI를 업데이트
            resetToViewMode(branchId, newName);
        } else {
            alert('수정에 실패했습니다.');
        }
    };
    xhr.send(`name=${encodeURIComponent(newName)}`);
}

function resetToViewMode(branchId, newName) {
    var nameCell = document.getElementById('name_' + branchId);
    nameCell.innerText = newName;

    var actionCell = document.getElementById('action_' + branchId);
    actionCell.innerHTML = `<button onclick="editBranch(${branchId})" class="btn btn-warning btn-sm" style="margin-right: 5px;">수정</button>` +
        `<form method="post" style="display: inline;"><input type="hidden" name="delete" value="${branchId}"><button type="submit" class="btn btn-danger btn-sm">삭제</button></form>`;
}

function cancelEdit(branchId, nameValue) {
    var nameCell = document.getElementById('name_' + branchId);
    nameCell.innerText = nameValue;

    var actionCell = document.getElementById('action_' + branchId);
    actionCell.innerHTML = `<button onclick="editBranch(${branchId})" class="btn btn-warning btn-sm" style="margin-right: 5px;">수정</button>` +
        `<form method="post" style="display: inline;"><input type="hidden" name="delete" value="${branchId}"><button type="submit" class="btn btn-danger btn-sm">삭제</button></form>`;
}
