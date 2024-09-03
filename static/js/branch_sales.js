document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.sales-input').forEach(function(input) {
        input.addEventListener('change', function() {
            const saleId = this.dataset.saleId;
            document.querySelector(`.update-sale[data-sale-id="${saleId}"]`).disabled = false;
        });
    });

    document.querySelectorAll('.update-sale').forEach(function(button) {
        button.addEventListener('click', function() {
            const saleId = this.dataset.saleId;
            const salesCardSweetdream = parseFloat(document.querySelector(`[data-sale-id="${saleId}"][data-field="sales_card_sweetdream"]`).value);
            const salesCardGlory = parseFloat(document.querySelector(`[data-sale-id="${saleId}"][data-field="sales_card_glory"]`).value);
            const salesCash = parseFloat(document.querySelector(`[data-sale-id="${saleId}"][data-field="sales_cash"]`).value);
            const salesZeropay = parseFloat(document.querySelector(`[data-sale-id="${saleId}"][data-field="sales_zeropay"]`).value);
            const salesTransfer = parseFloat(document.querySelector(`[data-sale-id="${saleId}"][data-field="sales_transfer"]`).value);

            fetch('/update_sale', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    sale_id: saleId,
                    sales_card_sweetdream: salesCardSweetdream,
                    sales_card_glory: salesCardGlory,
                    sales_cash: salesCash,
                    sales_zeropay: salesZeropay,
                    sales_transfer: salesTransfer
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('매출이 성공적으로 업데이트되었습니다.');
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

    document.querySelectorAll('.delete-sale').forEach(function(button) {
        button.addEventListener('click', function() {
            const saleId = this.dataset.saleId;

            fetch('/delete_sale', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    sale_id: saleId
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('매출이 성공적으로 삭제되었습니다.');
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
});
