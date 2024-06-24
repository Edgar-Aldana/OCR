const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById('snap');
const detectedTextDiv = document.getElementById('detected-text');
const translatedTextDiv = document.getElementById('translated-text');
const uploadedImage = document.getElementById('uploaded-image');

function showUploadForm() {
    document.getElementById('upload-form').style.display = 'block';
    document.getElementById('camera-form').style.display = 'none';
}

function showCamera() {
    document.getElementById('upload-form').style.display = 'none';
    document.getElementById('camera-form').style.display = 'block';
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } }).then(function(stream) {
            video.srcObject = stream;
            video.play();
        });
    }
}

snap.addEventListener("click", function() {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/png');
    uploadedImage.src = dataURL;

    fetch('/process_camera/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: dataURL })
    })
    .then(response => response.json())
    .then(data => {
        detectedTextDiv.innerText = data.extracted_text;
        translatedTextDiv.innerText = data.translated_text;
    });
});

function uploadImage() {
    const form = document.getElementById('upload-form-element');
    const formData = new FormData(form);

    fetch('/process_image/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        detectedTextDiv.innerText = data.extracted_text;
        translatedTextDiv.innerText = data.translated_text;
        uploadedImage.src = URL.createObjectURL(form.elements.file.files[0]);
    });
}
