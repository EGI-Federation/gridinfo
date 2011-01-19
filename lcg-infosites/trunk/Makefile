PACKAGE_NAME=lcg-infosites
####################################################################
# Distribution Makefile
####################################################################

.PHONY: configure install clean

all: compile

####################################################################
# Prepare
####################################################################

prepare: 
	@mkdir -p build

####################################################################
# Configure
####################################################################

configure: 
	@echo "No configuration required, use either 'make install' or 'make rpm'."

####################################################################
# Compile
####################################################################

compile: prepare
	@echo "No compile required, use either 'make install' or 'make rpm'."

####################################################################
# Install
####################################################################

install: compile
	@echo installing ...
	@mkdir -p $(prefix)/bin/
	@mkdir -p $(prefix)/man/man1
	@install -m 0755 src/lcg-infosites   $(prefix)/bin/lcg-infosites
	@install -m 0644 man/lcg-infosites.1 $(prefix)/man/man1/lcg-infosites.1

####################################################################
# Documentation
####################################################################

doc: 
	@echo "No documentation required, use either 'make install' or 'make rpm'."
####################################################################
# Install Doc
####################################################################

install-doc: doc
	@echo installing  docs...


####################################################################
# Build Distribution
####################################################################

dist: prepare 
	@tar --gzip -cf build/$(PACKAGE_NAME).src.tgz *

rpm: dist
	@rpmbuild -ta build/$(PACKAGE_NAME).src.tgz 

clean::
	rm -f *~ test/*~ etc/*~ doc/*~ src/*~ $(PACKAGE_NAME).src.tgz 
	rm -rf build
