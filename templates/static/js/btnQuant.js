function process(step) {
  var quant = document.getElementById('quant');
  var newVal = parseInt(quant.value) + step;
  var maxVal = parseInt(quant.getAttribute('max'));
  var minVal = parseInt(quant.getAttribute('min'));

  if (newVal >= minVal && newVal <= maxVal) {
      quant.value = newVal;
  }
}

function process(change) {
  var quantInput = document.getElementById('quant');
  var newValue = parseInt(quantInput.value) + change;
  var maxAllowed = parseInt(quantInput.getAttribute('max'));
  newValue = Math.min(Math.max(newValue, 1), maxAllowed);  // Garante que o valor esteja dentro dos limites

  quantInput.value = newValue;
}