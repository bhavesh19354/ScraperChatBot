
# Scraper ChatBot Extension
Scraping Extension is a powerful Chrome extension that provides a seamless way to scrape web content and extract valuable information. With this extension, you can easily retrieve data from web pages and save it for further analysis or reference

## Features
- Ask questions to the question-answering system and receive responses.
- Scrape the content of the currently active tab and download it as text file.
- Display the user's questions and the bot's responses in a chat-like interface.
- Show timestamps for each message.
- Responsive design for a seamless user experience.

## Installation
1. Clone the repository or download the source code.
2. Open Chrome and navigate to `chrome://extensions`.
3. Enable Developer mode by toggling the switch in the top-right corner.
4. Click on "Load unpacked" and select the folder containing the extension's source code.
5. The extension will be added to Chrome, and its icon will appear in the browser's toolbar.

## Usage
1. Click on the extension icon in the toolbar to open the extension popup.
2. Then click the "Scrape Content" button to Scrape the data from the active web page and train the model on data.
3. A text file will be downloaded.
4. In the popup, enter your question in the input field and click the "Send" button.
5. The extension will send the question to the question-answering system and display the response in the chat interface.


## API Endpoints
- `/ask`: Accepts a GET request with a query parameter `ques` containing the user's question. Returns the bot's response as plain text.
- `/scrape`: Accepts a GET request with a query parameter `url` containing the URL of the page to scrape. Processes the page content and returns the results.
