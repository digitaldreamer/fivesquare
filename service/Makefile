STATIC_DIR=static
HTML_DIR=../../html
BUILD_DIR=$(STATIC_DIR)/build
RJS=$(STATIC_DIR)/js/libs/r.js

CSS_NAME=styles
CSS_LESS=$(STATIC_DIR)/css/$(CSS_NAME).less
CSS_BUILD=$(BUILD_DIR)/$(CSS_NAME).css
CSS_MIN=$(BUILD_DIR)/$(CSS_NAME).min.css

JS_NAME=main
JS_FILE=$(STATIC_DIR)/js/build.js
JS_BUILD=$(BUILD_DIR)/$(JS_NAME).js
JS_MIN=$(BUILD_DIR)/$(JS_NAME).min.js

.PHONY: static

run:
	pserve development.ini --reload

resetdb:
	psql -U postgres -c 'drop database poseidon'
	psql -U postgres -c 'create database poseidon'
	psql -U postgres poseidon < poseidon.psql

build: static
	cp -Rf $(STATIC_DIR) $(HTML_DIR)

static: css js
css: less
js: require

less: builddir
	lessc $(CSS_LESS) $(CSS_BUILD)
	java -jar utils/yuicompressor-2.4.2.jar $(CSS_BUILD) -o $(CSS_MIN)

require: builddir
	node $(RJS) -o $(JS_FILE) optimize=none out=$(JS_BUILD)
	java -jar utils/yuicompressor-2.4.2.jar $(JS_BUILD) -o $(JS_MIN)

builddir:
	mkdir -p $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(HTML_DIR)/$(STATIC_DIR)

tailog:
	heroku logs --tail --app hinge-api-interview-juniper
