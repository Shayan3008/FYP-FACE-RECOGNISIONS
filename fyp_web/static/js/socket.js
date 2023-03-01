// JS FILE CONTAINING ALL CODE REGARDING SOCKETS

socket.onmessage = (event) => {
    event_obj = JSON.parse(event.data)
    console.log(event_obj)
    if(event_obj.type =="Alert" ){
    document.querySelector(".camera"+event_obj.msg).style.border = "4px solid red"
    hidden.style.display = "block"
    }
}