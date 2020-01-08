window.onload = function(){
    this.console.log("hehe")
}


var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
        console.log(xhr.responseText);
    }
}
xhr.open('GET', 'http://127.0.0.1:8000/capteur/getCapteurs', true);
xhr.send(null);