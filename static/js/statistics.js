document.addEventListener('DOMContentLoaded', function() {
    loadData('weekly'); // Load weekly data by default
});

function loadData(dateRange, branchId = '') {
    fetch(`/statistics?range=${dateRange}&branch_id=${branchId}`)
        .then(response => response.json())
        .then(data => updateChart(data));
}

let currentChart = null; // To keep track of the current chart instance

function updateChart(data) {
    const ctx = document.getElementById('requestChart').getContext('2d');
    if (currentChart) {
        currentChart.destroy(); // Destroy the current chart instance before creating a new one
    }
    currentChart = new Chart(ctx, {
        type: 'bar', // Change to 'line' if preferred
        data: {
            labels: data.labels,
            datasets: [{
                label: '요청 수량',
                data: data.values,
                backgroundColor: 'rgba(78, 115, 223, 0.75)',
                borderColor: 'rgba(78, 115, 223, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function changeRange(range) {
    loadData(range);
    document.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`button[onclick="changeRange('${range}')"]`).classList.add('active');
}

function changeBranch(branchId) {
    const range = document.querySelector('button.active').getAttribute('onclick').match(/'(\w+)'/)[1];
    loadData(range, branchId);
}