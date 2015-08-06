ROOT_DIR=$(CURDIR)
DOCS_DIR=$(ROOT_DIR)/docs
DOCS_BUILD_DIR=$(ROOT_DIR)/docs/_build

.PHONY: static docs

run:
	pserve development.ini --reload

build: docs

docs: clean
	cd $(DOCS_DIR); make html

clean:
	rm -rf $(DOCS_BUILD_DIR)

tailog:
	heroku logs --tail --app hinge-api-interview-juniper
