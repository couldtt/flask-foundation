init:
	pip3 install virtualenv
	virtualenv --python=python3 env/ && source env/bin/activate
	pip3 install -r requirements.txt

