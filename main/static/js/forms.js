let login_section = document.getElementsByClassName('login__section')[0],
	register_section = document.getElementsByClassName('register__section')[0],
	login = document.getElementById('login'),
	register = document.getElementById('register'),
	close_reg = document.getElementById('close__reg'),
	close_login = document.getElementById('close__login'),
	content_section = document.getElementsByClassName("content__section")[0];


login.addEventListener('click', function(){
	login_section.style.display = "block";
	content_section.style.display = "none";
	register_section.style.display = "none";
})


register.addEventListener('click', function(){
	register_section.style.display = "block";
	content_section.style.display = "none";
	login_section.style.display = "none";
})


close_reg.addEventListener('click', function(){
	content_section.style.display = "block";
	register_section.style.display = "none";
})

close_login.addEventListener('click', function(){
	content_section.style.display = "block";
	login_section.style.display = "none";
})