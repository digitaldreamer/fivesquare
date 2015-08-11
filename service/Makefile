ROOT_DIR=$(CURDIR)
DOCS_DIR=$(ROOT_DIR)/docs
DOCS_BUILD_DIR=$(ROOT_DIR)/docs/_build

.PHONY: static docs

run:
	pserve development.ini --reload

build: docs

docs: clean
	cd $(DOCS_DIR); make html

ubuntu:
	sudo apt-get install -y libffi-dev
	sudo apt-get install -y ntp
	sudo apt-get install -y vim
	sudo apt-get install -y htop
	sudo apt-get install -y build-essential
	sudo apt-get install -y git
	sudo apt-get install -y bash-completion
	sudo apt-get install -y python-dev
	sudo apt-get install -y python-setuptools
	sudo apt-get install -y libpq-dev
	sudo apt-get install -y mongodb
	sudo apt-get install -y redis-server
	sudo easy_install virtualenv

redis:
	redis-cli -h pub-redis-19387.us-east-1-3.6.ec2.redislabs.com -p 19387 -a 'hinge'

clean:
	rm -rf $(DOCS_BUILD_DIR)

tailog:
	heroku logs --tail --app hinge-api-interview-juniper
