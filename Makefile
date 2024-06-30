# Makefile to run Python script and then Tectonic

all: compile

python:
	python main.py -i songs/ -o src/ --verbose

latex:
	tectonic -X build

tex: latex

compile: python latex

.PHONY: all compile tex latex python