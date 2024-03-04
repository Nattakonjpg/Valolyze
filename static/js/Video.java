document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault(); // ป้องกันการส่งคำขอฟอร์มโดยปกติ
    uploadAndDisplayVideo(event);
});
