let buttonSendMsg = document.getElementById("send__msg"),
	id = buttonSendMsg.value,
	dialog = document.getElementById("dialog"),
	options = {
	    year: 'numeric',
	    month: 'long',
	    day: 'numeric',
	    hour: 'numeric',
	    minute: 'numeric',
	    second: 'numeric'
	};

const url = "/send_msg",
	method = "post";


sendTextMsg = (id) => {
    let date = new Date();
    let textarea = document.getElementById("textarea"),
    	text = textarea.value;
    textarea.value = "";
    if (text === ""){
    	return
    }
	const requestXHR = new XMLHttpRequest();
	requestXHR.open(method, url, true);
	console.log(text)
	requestXHR.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	requestXHR.onreadystatechange = function(){
		if(requestXHR.readyState !== 4) return;
		if(requestXHR.status !== 200){
			alert(requestXHR.status + ': ' +requestXHR.statusText);		
		}
		else{
			answer = JSON.parse(requestXHR.responseText);
			console.log(answer);
			let divMessageFrom = document.createElement("div"),
				h5 = document.createElement("h5");
				p = document.createElement("p");
				h6 = document.createElement("h6");
			divMessageFrom.className = "message__from message__block";
			h5.innerHTML = answer["name"];
			p.innerHTML = answer["text"];
			h6.innerHTML = answer["time"];
			divMessageFrom.appendChild(h5);
			divMessageFrom.appendChild(p);
			divMessageFrom.appendChild(h6);
			dialog.appendChild(divMessageFrom);
		}
	}
	requestXHR.send("text="+text+"&id="+id+"&time="+date.toLocaleString("ru", options));
}	

buttonSendMsg.addEventListener('click', () => sendTextMsg(id));
