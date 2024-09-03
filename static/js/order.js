document.addEventListener('DOMContentLoaded', function() {
    loadBranches();
    document.getElementById('addOrderItemBtn').addEventListener('click', addOrderItem);
    document.getElementById('removeOrderItemBtn').addEventListener('click', removeLastOrderItem);
    document.getElementById('orderForm').addEventListener('submit', function(event) {
        event.preventDefault();
        if (validateForm()) {
            this.submit();
        }
    });
    document.getElementById('orderForm').addEventListener('input', checkFormInputs);
});

document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('orderDate').value = today;

    loadBranches();
    document.getElementById('addOrderItemBtn').addEventListener('click', addOrderItem);
    document.getElementById('orderForm').addEventListener('submit', function(event) {
        event.preventDefault();
        if (validateForm()) {
            this.submit();
        }
    });
});

function loadBranches() {
    fetch('/api/branches')
    .then(response => response.json())
    .then(branches => {
        const branchSelect = document.getElementById('branchSelect');
        branchSelect.innerHTML = '<option disabled selected value="">지점을 선택해주세요</option>';
        
        branches.forEach(branch => {
            const option = new Option(branch.name, branch.id);
            branchSelect.appendChild(option);
        });

        branchSelect.addEventListener('change', () => updateEmailOptions(branches));
    })
    .catch(error => console.error('Error loading branches:', error));
}

let orderItemIndex = 1;

function addOrderItem() {
    fetch('/api/products')
        .then(response => response.json())
        .then(products => {
            const orderItemsDiv = document.getElementById('orderItems');
            const div = document.createElement('div');
            div.classList.add('orderItem', 'mb-3');

            const itemTitle = document.createElement('h5');
            itemTitle.innerText = `품목 ${orderItemIndex++}`;
            div.appendChild(itemTitle);

            const productSelect = document.createElement('select');
            productSelect.name = 'product_id[]';
            productSelect.classList.add('form-control', 'productSelect', 'mb-2');

            const defaultProductOption = new Option('품목을 선택해주세요', '');
            defaultProductOption.disabled = true;
            defaultProductOption.selected = true;
            productSelect.appendChild(defaultProductOption);

            products.forEach(product => {
                const optionValue = `${product.id}|${product.name}`;
                const option = new Option(product.name, optionValue);
                productSelect.appendChild(option);
            });

            productSelect.addEventListener('change', function() {
                loadColors(this, this.nextElementSibling);
                loadBudTypes(this, this.nextElementSibling.nextElementSibling);
            });

            const colorSelect = document.createElement('select');
            colorSelect.name = 'color[]';
            colorSelect.classList.add('form-control', 'colorSelect', 'mb-2');

            const defaultColorOption = new Option('색상을 선택해주세요', '');
            defaultColorOption.disabled = true;
            defaultColorOption.selected = true;
            colorSelect.appendChild(defaultColorOption);

            const budTypeSelect = document.createElement('select');
            budTypeSelect.name = 'bud_type[]';
            budTypeSelect.classList.add('form-control', 'budTypeSelect', 'mb-2');

            const defaultBudTypeOption = new Option('봉오리 타입을 선택해주세요', '');
            defaultBudTypeOption.disabled = true;
            defaultBudTypeOption.selected = true;
            budTypeSelect.appendChild(defaultBudTypeOption);

            const quantityInput = document.createElement('input');
            quantityInput.type = 'number';
            quantityInput.name = 'quantity[]';
            quantityInput.classList.add('form-control', 'quantityInput', 'mb-2');
            quantityInput.placeholder = "수량";
            quantityInput.min = 1;
            quantityInput.required = true;

            div.appendChild(productSelect);
            div.appendChild(colorSelect);
            div.appendChild(budTypeSelect);
            div.appendChild(quantityInput);
            orderItemsDiv.appendChild(div);

            loadColors(productSelect, colorSelect);
            loadBudTypes(productSelect, budTypeSelect);
        })
        .catch(error => console.error('Error loading products:', error));
}

function removeLastOrderItem() {
    const orderItemsDiv = document.getElementById('orderItems');
    const lastOrderItem = orderItemsDiv.lastElementChild;
    if (lastOrderItem) {
        orderItemsDiv.removeChild(lastOrderItem);
    }
}

function loadColors(productSelect, colorSelect) {
    const productName = productSelect.options[productSelect.selectedIndex].text;
    fetch(`/api/colors/${productName}`)
        .then(response => response.json())
        .then(colors => {
            colorSelect.innerHTML = '';
            const defaultColorOption = new Option('색상을 선택해주세요', '');
            defaultColorOption.disabled = true;
            defaultColorOption.selected = true;
            colorSelect.appendChild(defaultColorOption);

            colors.forEach(color => {
                const option = new Option(color, color);
                colorSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading colors:', error));
}

function loadBudTypes(productSelect, budTypeSelect) {
    const productName = productSelect.options[productSelect.selectedIndex].text;
    fetch(`/api/bud_types/${productName}`)
        .then(response => response.json())
        .then(budTypes => {
            budTypeSelect.innerHTML = '';
            const defaultBudTypeOption = new Option('봉오리 타입을 선택해주세요', '');
            defaultBudTypeOption.disabled = true;
            defaultBudTypeOption.selected = true;
            budTypeSelect.appendChild(defaultBudTypeOption);

            budTypes.forEach(budType => {
                const option = new Option(budType, budType);
                budTypeSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading bud types:', error));
}

function validateForm() {
    return true;
}

function checkFormInputs() {
    const orderDate = document.getElementById('orderDate').value;
    const branchSelect = document.getElementById('branchSelect').value;
    const specialNote = document.getElementById('specialNoteTextarea').value;
    const orderItems = document.querySelectorAll('#orderItems .orderItem');
    const submitOrderBtn = document.getElementById('submitOrderBtn');

    let allFilled = orderDate && branchSelect;

    if(orderItems.length > 0) {
        orderItems.forEach(item => {
            const productSelect = item.querySelector('.productSelect').value;
            const colorSelect = item.querySelector('.colorSelect').value;
            const budTypeSelect = item.querySelector('.budTypeSelect').value;
            const quantityInput = item.querySelector('.quantityInput').value;
            if(!productSelect || !colorSelect || !budTypeSelect || !quantityInput) {
                allFilled = false;
            }
        });
    } else {
        allFilled = false;
    }

    if (allFilled) {
        submitOrderBtn.disabled = false;
        submitOrderBtn.classList.add('btn-primary');
        submitOrderBtn.classList.remove('btn-light');
    } else {
        submitOrderBtn.disabled = true;
        submitOrderBtn.classList.remove('btn-primary');
        submitOrderBtn.classList.add('btn-light');
    }
}
