PACKAGE_NAME=lcg-info
.PHONY: configure install clean

all: configure

prepare:
	mkdir -p build

configure:
	@echo "No configuration required, use either 'make install' or 'make rpm'."

compile:
	@echo "No compiling required, use either 'make install' or 'make rpm'."

install: 
	@echo installing...
	@mkdir -p $(prefix)/bin
	@mkdir -p $(prefix)/man/man1
	@install -m 0755 src/lcg-info $(prefix)/bin/lcg-info
	@install -m 0644 src/lcg-info.1 $(prefix)/man/man1/lcg-info.1

dist: prepare
	@tar --gzip -cf build/$(PACKAGE_NAME).src.tgz src Makefile lcg-info.spec

rpm: dist
	@rpmbuild -ta build/$(PACKAGE_NAME).src.tgz

clean:
	rm -f *~
	rm -rf build
