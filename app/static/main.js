var k = document.getElementById("url");
var btn = document.getElementById("submit");
k.addEventListener('input', action);

function action () {
	if (k.value){
		btn.className = "btn btn-outline-success my-4";
		k.disabled = false;
	}
	else{
		btn.className = "btn btn-outline-danger my-4 disabled";
		k.disabled = true;
	}
}