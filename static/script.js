function uploadImage() {
  const fileInput = document.getElementById('imageInput');
  const file = fileInput.files[0];
  const analyzeButton = document.querySelector('button');
  const resultDiv = document.getElementById('result');
  const swatch = document.getElementById('colorSwatch');

  if (!file) {
    alert("Please select an image.");
    return;
  }

  resultDiv.innerText = "Analyzing...";
  swatch.style.backgroundColor = "transparent";
  analyzeButton.disabled = true;

  const formData = new FormData();
  formData.append('image', file);

  // Show preview
  const reader = new FileReader();
  reader.onload = function(e) {
    document.getElementById('preview').src = e.target.result;
  };
  reader.readAsDataURL(file);

  fetch('/analyze', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    analyzeButton.disabled = false;

    if (data.error) {
      resultDiv.innerText = data.error;
      return;
    }

    // Show result
    resultDiv.innerHTML = `<strong>Dominant Color:</strong><br>
                           RGB(${data.r}, ${data.g}, ${data.b})<br>
                           HEX: ${data.hex}`;

    swatch.style.backgroundColor = data.hex;
    swatch.style.display = "block";

    // Also set body background
    document.body.style.background = `linear-gradient(135deg, ${data.hex}, #ffffff)`;
  })
  .catch(err => {
    analyzeButton.disabled = false;
    resultDiv.innerText = "Error analyzing image.";
    console.error(err);
  });
}
