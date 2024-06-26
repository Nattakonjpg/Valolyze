function ekUpload() {
    function Init() {
        console.log("Upload Initialised");

        var fileSelect = document.getElementById('file-upload'),
            fileDrag = document.getElementById('file-drag'), // Corrected this line
            submitButton = document.getElementById('submit-button');

        fileSelect.addEventListener('change', fileSelectHandler, false);

        // Is XHR2 available?
        var xhr = new XMLHttpRequest();
        if (xhr.upload) {
            // File Drop
            fileDrag.addEventListener('dragover', fileDragHover, false);
            fileDrag.addEventListener('dragleave', fileDragHover, false);
            fileDrag.addEventListener('drop', fileSelectHandler, false);
        }

        // เมื่ออัปโหลดเสร็จสมบูรณ์ แสดงปุ่มปิด
        document.getElementById('close-container').style.display = 'block';
    }
    function fileDragHover(e) {
        var fileDrag = document.getElementById('file-drag');

        e.stopPropagation();
        e.preventDefault();

        fileDrag.className = (e.type === 'dragover' ? 'hover' : 'modal-body file-upload');
    }

    function fileSelectHandler(e) {
        // Fetch FileList object
        var files = e.target.files || e.dataTransfer.files;

        // Cancel event and hover styling
        fileDragHover(e);

        // Process all File objects
        for (var i = 0, f; f = files[i]; i++) {
            parseFile(f);
            uploadFile(f);
        }
    }

    // Output
    function output(msg) {
        // Response
        var m = document.getElementById('messages');
        m.innerHTML = msg;
    }

    function parseFile(file) {
        var videoExtensions = ['mp4', 'AVI', 'webm', 'ogg']; // Define supported video file extensions
        var fileExtension = file.name.split('.').pop().toLowerCase(); // Get the file extension

        // Check if the file extension is in the list of supported video extensions
        var isVideo = videoExtensions.indexOf(fileExtension) !== -1;

        if (isVideo) {
            // Hide the start and notimage elements, show the response element
            document.getElementById('start').classList.add('hidden');
            document.getElementById('notimage').classList.add('hidden');
            document.getElementById('response').classList.remove('hidden');

            // Create a video element for preview
            var videoPreview = document.createElement('video');
            videoPreview.setAttribute('controls', ''); // Enable controls
            videoPreview.setAttribute('autoplay', ''); // Autoplay the video
            videoPreview.setAttribute('loop', ''); // Loop the video
            videoPreview.style.width = '100%'; // Set the width of the video preview
            videoPreview.style.width = '100%'; // Set the width of the video preview
            // videoPreview.style.maxHeight = '200px'; // Remove this line
            videoPreview.src = URL.createObjectURL(file);
            // Replace the placeholder image with the video preview
            var fileImage = document.getElementById('file-image');
            fileImage.parentNode.replaceChild(videoPreview, fileImage);
        } else {
            // If it's not a video file, handle it as before
            document.getElementById('file-image').classList.add('hidden');
            document.getElementById('notimage').classList.remove('hidden');
            document.getElementById('start').classList.remove('hidden');
            document.getElementById('response').classList.add('hidden');
            document.getElementById('file-upload-form').reset();
        }
    }

    function setProgressMaxValue(e) {
        var pBar = document.getElementById('file-progress');

        if (e.lengthComputable) {
            pBar.max = e.total;
        }
    }

    function updateFileProgress(e) {
        var pBar = document.getElementById('file-progress');

        if (e.lengthComputable) {
            pBar.value = e.loaded;
        }
    }

    function uploadFile(file) {
        var xhr = new XMLHttpRequest(),
            fileInput = document.getElementById('class-roster-file'),
            pBar = document.getElementById('file-progress'),
            fileSizeLimit = 1024; // In MB
        if (xhr.upload) {
            // Check if file is less than x MB
            if (file.size <= fileSizeLimit * 1024 * 1024) {
                // Progress bar
                pBar.style.display = 'inline';
                xhr.upload.addEventListener('loadstart', setProgressMaxValue, false);
                xhr.upload.addEventListener('progress', updateFileProgress, false);

                // File received / failed
                xhr.onreadystatechange = function (e) {
                    if (xhr.readyState == 4) {
                        // Check if upload was successful
                        if (xhr.status == 200) {
                            // Show the close button container only if upload was successful
                            document.getElementById('close-container').style.display = 'block';
                        } else {
                            // Hide the close button container if upload failed
                            document.getElementById('close-container').style.display = 'none';
                        }
                    }
                };

                // Start upload
                xhr.open('POST', '/upload', true); // เปลี่ยนจาก document.getElementById('file-upload-form').action เป็น '/upload'
                xhr.setRequestHeader('X-File-Name', file.name);
                xhr.setRequestHeader('X-File-Size', file.size);
                xhr.setRequestHeader('Content-Type', 'multipart/form-data');
                xhr.send(file);
            } else {
                output('Please upload a smaller file (< ' + fileSizeLimit + ' MB).');
            }
        }
    }

    // Check for the various File API support.
    if (window.File && window.FileList && window.FileReader) {
        Init();
    } else {
        document.getElementById('file-drag').style.display = 'none';
    }
}
ekUpload();