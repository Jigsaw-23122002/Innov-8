//Selector
const $ = (selector) => document.querySelector(selector);

//Chat
const chat = $('#chat');

//Options
const options = $('#options'),
						button_options = $('#button-options'),
						close_options = $('#close-options');

button_options.addEventListener('click', () => {
	options.classList.toggle('active');
});

close_options.addEventListener('click', () => {
	options.classList.remove('active');
});

//Dark Mode
const toggle = $('#input-dark');

toggle.addEventListener('change', function(){
	this.checked ? chat.classList.add('dark') : chat.classList.remove('dark');
});

//Colors
const blue = $('#color-blue'),
						red = $('#color-red'),
						green = $('#color-green'),
						purple = $('#color-purple');

blue.addEventListener('click', () => {
	delete chat.dataset.color;
});
red.addEventListener('click', () => {
	chat.dataset.color = 'red';
});
green.addEventListener('click', () => {
	chat.dataset.color = 'green';
});
purple.addEventListener('click', () => {
	chat.dataset.color = 'purple';
});

//Messages
const messages = $('#messages'),
						input = $('#input-message'),
						send = $('#send-text');

//Send messages
input.addEventListener('keypress', function(ev){
	if(ev.key === 'Enter' && input.value){
		ev.preventDefault();
		const msg = input.value;
		sendMessage(msg);
	};
});

send.addEventListener('click', () => {
	const msg = input.value;
	if(msg) sendMessage(msg);
});

const sendMessage = (msg) => {
	//Create message
	const block = document.createElement('div');
							block.setAttribute('class', 'msg-text owner');
	const message = document.createElement('span');
							message.setAttribute('class', 'text');
							message.innerText = String(msg);
	
	//Append message
	block.appendChild(message);
	messages.appendChild(block);
	messages.scrollTo(0, 99999);
	
	//Clear input
	input.value = '';
	input.focus();
};