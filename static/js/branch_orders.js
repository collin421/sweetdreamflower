document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.order-input').forEach(function(input) {
        input.addEventListener('change', function() {
            const orderId = this.dataset.orderId;
            document.querySelector(`.update-order[data-order-id="${orderId}"]`).disabled = false;
        });
    });

    document.querySelectorAll('.update-order').forEach(function(button) {
        button.addEventListener('click', function() {
            const orderId = this.dataset.orderId;
            const product_name = document.querySelector(`[data-order-id="${orderId}"][data-field="product_name"]`).value;
            const color = document.querySelector(`[data-order-id="${orderId}"][data-field="color"]`).value;
            const quantity = document.querySelector(`[data-order-id="${orderId}"][data-field="quantity"]`).value;

            fetch('/update_order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    order_id: orderId,
                    product_name: product_name,
                    color: color,
                    quantity: quantity,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('주문이 성공적으로 업데이트되었습니다.');
                    button.disabled = true; // 성공적으로 업데이트된 후 버튼 비활성화
                } else {
                    alert('업데이트에 실패했습니다.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('오류가 발생했습니다.');
            });
        });
    });
});

document.querySelectorAll('.delete-order').forEach(function(button) {
    button.addEventListener('click', function() {
        const orderId = this.dataset.orderId;

        fetch('/delete_order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                order_id: orderId
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('주문이 성공적으로 삭제되었습니다.');
                // 삭제 후 페이지를 새로고침하거나 해당 행을 DOM에서 제거
                location.reload();
            } else {
                alert('삭제에 실패했습니다.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('오류가 발생했습니다.');
        });
    });
});