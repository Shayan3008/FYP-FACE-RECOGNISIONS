// JS FILE CONTAINING ALL CODE REGARDING SOCKETS

const socket = new WebSocket("ws://127.0.0.1:8000/ws/admin")
const videos = document.querySelector(".videoPanel")
const file = document.querySelector(".file")
const hidden = document.querySelector(".hidden")
socket.onmessage = (event) => {
    event_obj = JSON.parse(event.data)
    id = event_obj.msg.toString()
    console.log(document.querySelector(".camera2"))
    if (event_obj.type === "Alert") {
        document.querySelector(".camera2").style.border = "4px solid red"
        hidden.style.display = "block"
    }
}