# talkitover2
To run this, you need to have
talkitover_app.py
and then following folders at the same level as talkitover_app.py
/static
/templates
The templates folder should include home - bootstrap 2020m05.html and home - original pre-2020m05.html
The static folder should include functions.js, image2.jpg and styling.css
A live version can be found at http://talkitovertest.pythonanywhere.com/

## Prerequisites
You will need the following prerequisites for this repository:

- An IDE such as Visual Studio Code - https://code.visualstudio.com/download
- Python 3.7.* installed on your machine (has to be 64 bit)- https://www.python.org/downloads/windows/
- Git installed on your machine - https://git-scm.com/download
- Windows 10 SDK - https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/

To get this project working on your machine, do the following:
1. Clone the repository on your machine in your development workspace using the following command: 
```
git clone https://github.com/SanjayRedScarf/talkitover2.git'.
```
2. Next, open a CLI of your choice and run the following commands one by one:
```	
	pip install flask
	pip install cython
	pip install chatterbot==1.0.4
	pip install pytz
```
3. You should now be able to run the following command: 
```
python talkitover2_app.py
```

