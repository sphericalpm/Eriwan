var filename = "";

Dropzone.options.uploadDropzone = {
    paramName: "file",  // The name that will be used to transfer the file,
    maxFilesize: 20,   // MB
    autoProcessQueue: false,
    acceptedFiles: "audio/mpeg, .mp3",
    dictDefaultMessage: "Перетащите аудио файл в эту зону для загрузки",
    maxFiles: 1,
    accept: function (file, done) {
        console.log(file.name);
        filename = file.name;
        done();    // !Very important
    },
    init: function () {
        this.on("complete", function (file) {
            this.removeAllFiles(true);
        })


        var myDropzone = this,
            submitButton = document.querySelector("[type=submit]");

        submitButton.addEventListener('click', function (e) {
            var isValid = document.querySelector('#podcast-name').value!=''
            e.preventDefault();
            e.stopPropagation();
            if (isValid)
                myDropzone.processQueue();
            else alert('Введите имя подскаста!')
        });

        this.on('sendingmultiple', function (data, xhr, formData) {
            formData.append("warehouse", jQuery("#podcast-name").val());
        });
    }
};