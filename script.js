var slider = document.getElementById("range1");
var output = document.getElementById("range1_value");

slider.oninput = function() {
    output.innerHTML = slider.value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {}
    };
    xhttlp.open("GET". "http://172.17.21.24:5000/set_speed?speed=" + slider.value, true);
    xhttp.send();
}