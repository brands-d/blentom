.PHONY: all clean build

all: clean build

clean:
	rm -rf build/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +

build:
	python3 build.py