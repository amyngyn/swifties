.PHONY: all debug

all:
	FLASK_APP=swifties python -m flask run

debug:
	FLASK_DEBUG=1 $(MAKE) all
