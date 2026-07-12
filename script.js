let display = document.getElementById('display');
let currentValue = '0';
let previousValue = '';
let operation = null;
let shouldResetDisplay = false;

function updateDisplay() {
    display.value = currentValue;
}

function appendNumber(number) {
    if (shouldResetDisplay) {
        currentValue = number;
        shouldResetDisplay = false;
    } else {
        if (currentValue === '0' && number !== '.') {
            currentValue = number;
        } else if (number === '.') {
            if (!currentValue.includes('.')) {
                currentValue += number;
            }
        } else {
            currentValue += number;
        }
    }
    updateDisplay();
}

function appendOperation(op) {
    if (operation !== null && !shouldResetDisplay) {
        calculate();
    }
    previousValue = currentValue;
    operation = op;
    shouldResetDisplay = true;
}

function calculate() {
    if (operation === null || shouldResetDisplay) {
        return;
    }
    
    let result;
    const prev = parseFloat(previousValue);
    const current = parseFloat(currentValue);
    
    switch (operation) {
        case '+':
            result = prev + current;
            break;
        case '-':
            result = prev - current;
            break;
        case '*':
            result = prev * current;
            break;
        case '/':
            result = current !== 0 ? prev / current : 0;
            break;
        default:
            return;
    }
    
    currentValue = result.toString();
    operation = null;
    shouldResetDisplay = true;
    updateDisplay();
}

function clearDisplay() {
    currentValue = '0';
    previousValue = '';
    operation = null;
    shouldResetDisplay = false;
    updateDisplay();
}
