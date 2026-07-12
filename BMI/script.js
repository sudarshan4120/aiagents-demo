document.getElementById('calculate-btn').addEventListener('click', calculateBMI);

document.getElementById('height').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        calculateBMI();
    }
});

document.getElementById('weight').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        calculateBMI();
    }
});

function calculateBMI() {
    const heightInput = document.getElementById('height').value;
    const weightInput = document.getElementById('weight').value;
    const errorMessage = document.getElementById('error-message');
    const resultContainer = document.getElementById('result');
    
    errorMessage.textContent = '';
    errorMessage.style.display = 'none';
    resultContainer.style.display = 'none';
    
    if (heightInput === '' || weightInput === '') {
        showError('Please enter both height and weight.');
        return;
    }
    
    const height = parseFloat(heightInput);
    const weight = parseFloat(weightInput);
    
    if (isNaN(height) || isNaN(weight)) {
        showError('Please enter valid numbers for height and weight.');
        return;
    }
    
    if (height <= 0 || weight <= 0) {
        showError('Height and weight must be positive numbers.');
        return;
    }
    
    const heightInMeters = height / 100;
    const bmi = weight / (heightInMeters * heightInMeters);
    const roundedBMI = Math.round(bmi * 10) / 10;
    
    const category = getCategory(roundedBMI);
    
    document.getElementById('bmi-value').textContent = roundedBMI.toFixed(1);
    document.getElementById('bmi-category').textContent = category;
    resultContainer.style.display = 'block';
}

function getCategory(bmi) {
    if (bmi < 18.5) {
        return 'Underweight';
    } else if (bmi >= 18.5 && bmi < 25) {
        return 'Normal';
    } else if (bmi >= 25 && bmi < 30) {
        return 'Overweight';
    } else {
        return 'Obese';
    }
}

function showError(message) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}
