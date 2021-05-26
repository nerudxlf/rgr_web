const requestUrl = '/send_msg',
    xhr = new XMLHttpRequest();


xhr.open('POST', requestUrl, true);
xhr.responseType = 'json';
xhr.send();

xhr.onload = function(){
    if(xhr.status !== 200){
        alert('Ошибка');
    }else{
        const obj = xhr.response;
        console.log(obj);
    }
}