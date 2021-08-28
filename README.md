# Quote


## Features

* As a normal user : 
    * Read all posts in application
    * Search in posts with categories and tags

* As logged in user :
    * Create, delete and deactivate your posts
    * Edit your posts (you can't change the image and post's category)
    * Like or dislike posts 


## How install and run ?
##### Clone the repository :
```bash
$ git clone https://github.com/Saeedahmadi7714/quote.git
$ cd quote
```
##### Create a virtualenv and activate it:
 ```bash
$ python3 -m venv venv
$ . venv/bin/activate.
```
##### Or on Windows cmd : 
 ```bash
> py -3 -m venv venv
> venv\Scripts\activate.bat
```
##### Install the app :
```bash
$ pip3 install -e .
```
#####  Export environment variables and run flask on local host :
```bash
$ export FLASK_APP=quote
$ export FLASK_ENV=development
$ flask run
```
##### Or on Windows cmd : 
```bash
> set FLASK_APP=quote
> set FLASK_ENV=development
> flask run
```
Open http://127.0.0.1:5000 in your browser. 
