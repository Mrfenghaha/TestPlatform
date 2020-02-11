function showCustomer() {
	var xmlhttp;
    var input = document.getElementById("input").value;
	if (window.XMLHttpRequest) {
		// IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
		xmlhttp = new XMLHttpRequest();
	}
	else {
		// IE6, IE5 浏览器执行代码
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
    xmlhttp.open("POST", "/api/all_pairs/pairs/get_pairs", true);
	xmlhttp.setRequestHeader("Content-type", "application/json");
	xmlhttp.send(JSON.stringify({
		"input": input
	}));
	xmlhttp.onreadystatechange = function () {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			document.getElementById("status").innerHTML = "Request Successful";
			var response = JSON.parse(xmlhttp.responseText);
            if (response.success === "false"){
                document.getElementById("result").innerHTML = response.error_message;
            }
            else{
                document.getElementById("result").innerHTML = "Pairs:" + response.data.ouput;
            }
		}
		else if (xmlhttp.readyState == 4 && xmlhttp.status != 200) {
			document.getElementById("status").innerHTML = "Request Fail Code:" + xmlhttp.status;
			document.getElementById("result").innerHTML = "";
		}
    }
}