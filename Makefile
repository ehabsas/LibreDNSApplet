APPNAME=liberdns
APPVER?=$(shell cat ./VERSION)
DESTDIR?=/
datadir?=$(DESTDIR)/usr/share
docdir?=$(datadir)/doc/liberdns-applet-$(APPVER)
xdgdir?=$(DESTDIR)/etc/xdg
INSTALL=install

SOURCES=$(wildcard *.desktop.in)
TARGETS=${SOURCES:.in=}

all: $(TARGETS) icons

icons:
	for i in 96 72 64 48 36 32 24 22 16; do \
		convert -background none $(APPNAME).svg -resize $${i}x$${i} $(APPNAME)-$${i}.png; \
	done
pos:
	make -C po all

install: all
	## For ArchLinux Use, Toggle comment next tow lines
	#python2 setup.py install -O2 --root $(DESTDIR)
	#python setup.py install -O2 --root $(DESTDIR)
	$(INSTALL) -m 0777 -D setup.py Setup.py
	./Setup.py install -O2 --root $(DESTDIR)
	$(INSTALL) -d $(datadir)/applications/
	$(INSTALL) -d $(xdgdir)/autostart/
	$(INSTALL) -m 0644 $(APPNAME).desktop $(datadir)/applications/
	$(INSTALL) -m 0644 $(APPNAME)-autostart.desktop $(xdgdir)/autostart/
	$(INSTALL) -d $(datadir)/icons/hicolor/scalable/apps;
	$(INSTALL) -m 0644 -D $(APPNAME).svg $(datadir)/icons/hicolor/scalable/apps/
	for i in 96 72 64 48 36 32 24 22 16; do \
		$(INSTALL) -d $(datadir)/icons/hicolor/$${i}x$${i}/apps; \
		$(INSTALL) -m 0644 -D $(APPNAME)-$${i}.png $(datadir)/icons/hicolor/$${i}x$${i}/apps/$(APPNAME).png; \
	done
	$(INSTALL) -d $(docdir)
	for i in AUTHORS COPYING VERSION README LICENSE-ar LICENSE-en ARTISTS; do\
	  $(INSTALL) -m 0644 -D $${i} $(docdir)/$${i}; \
	done

uninstall:
	rm -f $(datadir)/applications/$(APPNAME).desktop
	rm -f $(xdgdir)/autostart/$(APPNAME)-autostart.desktop
	rm -f $(datadir)/icons/hicolor/scalable/apps/$(APPNAME).svg
	rm -rf $(docdir)
	rm -f $(DESTDIR)/usr/share/locale/ar/LC_MESSAGES/liberdns.mo
	rm -f $(DESTDIR)/usr/bin/liberdns-applet
	rm -f $(DESTDIR)/usr/lib/python2.7/site-packages/liberdns*
	for i in 96 72 64 48 36 32 24 22 16; do \
		rm -f $(datadir)/icons/hicolor/$${i}x$${i}/apps/$(APPNAME).png; \
	done
		
%.desktop: %.desktop.in pos
	intltool-merge -d po $< $@

clean:
	rm -f $(TARGETS)
	rm -f Setup.py
	rm -rf locale build
	rm -f po/*.mo
	for i in 96 72 64 48 36 32 24 22 16; do \
		rm -f $(APPNAME)-$${i}.png; \
	done

