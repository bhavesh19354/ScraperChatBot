document.addEventListener('DOMContentLoaded', function () {
    var sendBtn = document.getElementById('send_button');

    sendBtn.addEventListener('click', function () {
        console.log("clicked");
        var ques = document.getElementById('msg_input').value;
        var newTabUrl = 'http://localhost:8000/ask?ques=' + encodeURIComponent(ques);
        showUserMessage(ques);
        document.getElementById('msg_input').value = ""
        fetch(newTabUrl)
            .then(function (response) {
                return response.text();
            })
            .then(function (text) {
                showBotMessage(text);
            })
            .catch(function (error) {
                console.error('Error:', error);
                showBotMessage("Error");
            });
        
    });
    

    var scrapeBtn = document.getElementById("scrapeBtn");

    scrapeBtn.addEventListener("click", function () {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            var tab = tabs[0];
            var url = tab.url;

            chrome.tabs.create({ url: "http://localhost:8000/scrape?url=" + encodeURIComponent(url) });
        });
    });
 
    function getCurrentTimestamp() {
        return new Date();
    }

    
    function renderMessageToScreen(args) {
        
        let displayDate = (args.time || getCurrentTimestamp()).toLocaleString('en-IN', {
            month: 'short',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
        });
        let messagesContainer = document.querySelector('.messages');

        
        let message = document.createElement('li');
        message.classList.add('message', args.message_side);

        let avatar = document.createElement('div');
        avatar.classList.add('avatar');

        let textWrapper = document.createElement('div');
        textWrapper.classList.add('text_wrapper');

        let text = document.createElement('div');
        text.classList.add('text');
        text.textContent = args.text;

        let timestamp = document.createElement('div');
        timestamp.classList.add('timestamp');
        timestamp.textContent = displayDate;

        textWrapper.appendChild(text);
        textWrapper.appendChild(timestamp);

        message.appendChild(avatar);
        message.appendChild(textWrapper);

       
        messagesContainer.appendChild(message);

        setTimeout(function () {
            message.classList.add('appeared');
        }, 0);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }


   
    function showUserMessage(message, datetime) {
        renderMessageToScreen({
            text: message,
            time: datetime,
            message_side: 'right',
        });
    }

    
    function showBotMessage(message, datetime) {
        renderMessageToScreen({
            text: message,
            time: datetime,
            message_side: 'left',
        });
    }

});
