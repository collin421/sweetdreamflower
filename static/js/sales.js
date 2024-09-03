document.addEventListener('DOMContentLoaded', function() {
    loadBranches();
    const saleDate = document.getElementById('saleDate');
    const branchSelect = document.getElementById('branchSelect');
    const submitButton = document.getElementById('submitSalesButton');

    branchSelect.addEventListener('change', function() {
        updateSubmitButtonState();
    });

    [saleDate, branchSelect].forEach(item => {
        item.addEventListener('change', updateSubmitButtonState);
    });

    updateSubmitButtonState();
});

function loadBranches() {
    fetch('/api/branches')
        .then(response => response.json())
        .then(branches => {
            const branchSelect = document.getElementById('branchSelect');
            branchSelect.innerHTML = '<option disabled selected value="">지점 선택</option>';
            branches.forEach(branch => {
                const option = new Option(branch.name, branch.id);
                branchSelect.add(option);
            });
        })
        .catch(error => console.log('Error loading branches:', error));
}

function updateSubmitButtonState() {
    const saleDate = document.getElementById('saleDate').value;
    const branchId = document.getElementById('branchSelect').value;
    const submitButton = document.getElementById('submitSalesButton');
    submitButton.disabled = !saleDate || !branchId;
}

document.getElementById('salesForm').addEventListener('submit', function(event) {
    ['sales_card_sweetdream', 'sales_card_glory', 'sales_cash', 'sales_zeropay', 'sales_transfer'].forEach(inputId => {
        const inputElement = document.getElementById(inputId);
        if (inputElement && inputElement.value === '') {
            inputElement.value = '0';
        }
    });
});