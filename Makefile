all: local
deploy:
	appcfg.py -A bookings update app.yaml
local:
	dev_appserver.py --enable_sendmail True .
pip:
	pip install -t lib/ -r requirements.txt --upgrade
