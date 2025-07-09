async function uploadImage() {
  const input = document.getElementById('imageInput');
  const file = input.files[0];
  const loader = document.getElementById('loader');
  const predList = document.getElementById('predictions');

  predList.innerHTML = '';
  loader.style.display = 'block';

  if (!file) {
    alert("Please select an image first.");
    loader.style.display = 'none';
    return;
  }

  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();
    loader.style.display = 'none';

    result.predictions.forEach(pred => {
      const li = document.createElement('li');
      li.textContent = pred;
      predList.appendChild(li);
    });
  } catch (err) {
    loader.style.display = 'none';
    alert("Something went wrong. Try again.");
    console.error(err);
  }
}
