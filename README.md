# product_service_parser  

This repository contains a server that parses out product/service recommendations from a document with AI  

## Requirements  

1. Make a .env file with the same fields as those in the .env.sample file
Bash:
```
nano .env
```
2. Add an OpenAI API key, a username for yourself and a password.  
3. Python 3.9+ (this was built on version 3.11)
4. Install the dependencies. Run ```pip install requirements.txt``` in git bash, and if errors are encountered, try ```pip install --upgrade pip``` or just installing the dependencies mannually using ```pip install [package_name]```. There are 4 packages in total. (BeautifulSoup, OpenAI, PyPDF2, dotenv)

## Running the server  
Bash:
```
python main.py
```

## Uploading documents and getting products back  
1. When running locally, navigate to the localhost url (It will be displayed in console, and look something like 'http://127.0.0.1:5000')  
2. Enter your username, password, and upload a file, and press 'Upload'.
3. Your page will reload






