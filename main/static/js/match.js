
let like = document.getElementById('like'),
    skip = document.getElementById('skip'),
    dislike = document.getElementById('dislike'),
    name = document.getElementById('name'),
    age = document.getElementById('age'),
    about = document.getElementById('about'),
    src_msg = document.getElementById('img__user');

const url = '/match';

send_msg = (msg, value) => {
    const requestXHR = new XMLHttpRequest();
    requestXHR.open('post', url, true);
    requestXHR.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    requestXHR.onreadystatechange = function () {
        if(requestXHR.readyState!==4) return;
        if(requestXHR.status!==200){
            name.innerHTML = "Люди закончились";
            age.innerHTML = "";
            about.innerHTML = ""
            like.value = 0;
            skip.value = 0;
            dislike.value = 0;
            src_msg.src = "static/img/err_photo/no_avatar.png";
        }
        else{
            answer = JSON.parse(requestXHR.responseText)
            console.log(answer);
            let name_surname = answer['name'] + " " + answer['surname'];
            name.innerHTML = name_surname;
            age.innerHTML = "Возраст: " + answer['age'];
            about.innerHTML = "Инфо: " + answer['about'];
            like.value = answer['id'];
            skip.value = answer['id'];
            dislike.value = answer['id'];
            src_msg.src = "static/"+answer['img'];
        }
    };
    requestXHR.send("value="+msg+"&id="+value);
}


like.addEventListener('click', () =>  send_msg("like", like.value));

skip.addEventListener('click', () => send_msg("skip", skip.value));

dislike.addEventListener('click', () => send_msg("dislike", dislike.value));

