// JS FILE CONTAINING ALL INFO ABOUT NETWORKS REQUESTS


// Code to send input file and upload data
document.querySelector(".click").onclick = (e) => { //Send Input Image to Server
    if (file.files.length > 0) {
        const form = new FormData()
        form.append("input", file.files[0])
        $.ajax(
            {
                url: "/survallence/image/",
                type: "POST",
                data: form,
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                contentType: false,
                processData: false,
                success: (getData) => {
                    localStorage.setItem("input_path1", getData)
                    videos.style.display = "flex"
                    hidden.style.display = "none"
                    sendVideoFromCamera("")
                }
            });

    }
}


const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const getVideoBlob = async () => {
    const response = await fetch(window.location.origin + "/static/test8.mp4")
    const blob = await response.blob()
    return new File([blob], "video1.mp4", { type: "video/mp4" })
}


const sendVideoFromCamera = async (camera) => {
    const form = new FormData()
    const file = await getVideoBlob()
    form.append("vid", file)
    form.append("input", localStorage.getItem("input_path1"))
    $.ajax(
        {
            url: "/survallence/video/",
            type: "POST",
            data: form,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            contentType: false,
            processData: false,
            success: function (getData) {
                console.log(getData)
            }
        });
}
