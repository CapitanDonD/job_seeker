# Job Seeker

This script will allow you to quickly find vacancies in the profession of a programmer in different programming languages.

### How to install

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

The program requires a SuperJob key to work. It can be obtained
on this site - [api.superjob.ru](https://api.superjob.ru/info/), go to the site, register your application
the key will appear, copy it. Then,
in the folder with the program, create a file called ".env". It needs
paste this:
```
SECRET_KEY="your token"
```

### How to run
To run the program itself, you need to write the following command on the command line:
```
python main.py 
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
