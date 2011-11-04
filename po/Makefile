POTFILE=$(shell cat POTFILES.in)
SOURCES=$(addprefix ../, $(POTFILE))
POFILES=$(wildcard *.po)
MOFILES=$(patsubst %.po,%.mo,$(POFILES))

all: liberdns.pot $(MOFILES)

liberdns.pot: $(SOURCES)
	echo $(SOURCES)
	intltool-update -g liberdns -p

%.mo: %.po
	msgfmt $*.po -o $*.mo
	mkdir -p ../locale/$*/LC_MESSAGES/ || :
	cp $*.mo ../locale/$*/LC_MESSAGES/liberdns.mo

%.po: liberdns.pot
	intltool-update -g liberdns -d $*

