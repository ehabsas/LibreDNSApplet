# -*- coding: utf-8 -*-
"""
Liber DNS update tool
Copyright © 2009-2011, ojuba.org <core@ojuba.org>

    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/license"
"""
import sys, os, os.path
import locale, gettext
import urllib2, urlparse
import pynotify
import gtk
import glib
import time
bus, bus_name, bus_object=None,None,None
try:
  import dbus
  import dbus.service
  #import gobject # for gobject.MainLoop() if no gtk is to be used
  from dbus.mainloop.glib import DBusGMainLoop
  dbus_loop = DBusGMainLoop(set_as_default=True)
  bus = dbus.SessionBus()
except ImportError: pass

exedir=os.path.dirname(sys.argv[0])
ld=os.path.join(exedir,'..','share','locale')
if not os.path.isdir(ld): ld=os.path.join(exedir, 'locale')
gettext.install('liberdns', ld, unicode=0)

class AboutDLG(gtk.AboutDialog):
  VERSION = "0.1.4"
  DOC_DIR = os.path.join(exedir, '..', 'share', 'doc', 'liberdns-applet-%s' %VERSION)
  AUTHORS_fn = os.path.join(DOC_DIR, 'AUTHORS')
  LICENSE_fn = os.path.join(DOC_DIR, 'COPYING')
  ARTISTS_fn = os.path.join(DOC_DIR, 'ARTISTS')
  if not os.path.isfile(AUTHORS_fn): AUTHORS_fn = os.path.join(exedir, 'AUTHORS')
  if not os.path.isfile(LICENSE_fn): LICENSE_fn = os.path.join(exedir, 'COPYING')
  if not os.path.isfile(ARTISTS_fn): ARTISTS_fn = os.path.join(exedir, 'ARTISTS')
  if os.path.isfile(AUTHORS_fn):
    AUTHORS=open(AUTHORS_fn, 'r').read().strip().split('\n')
    ARTISTS=open(ARTISTS_fn, 'r').read().strip().split('\n')
    LICENSE=open(LICENSE_fn, 'r').read().strip()
  else: 
    AUTHORS=["Ehab El-Gedawy <ehabsas@gmail.com>"]
    ARTISTS=["Zakaria Aikido <zakariaox@gmail.com>", "Ahmed Mohamedy <profseeer@gmail.com>", "Saif Al-islam Albakry <albakry.linux@yahoo.com>"]
    LICENSE="""
    Released under terms on Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://www.ojuba.org/wiki/doku.php/waqf/license"

    """
  def __init__(self):
    gtk.AboutDialog.__init__(self)
    self.set_default_response(gtk.RESPONSE_CLOSE)
    self.connect('delete-event', lambda w, *a: w.hide() or True)
    self.connect('response', lambda w, *a: w.hide() or True)
    try: self.set_program_name("liberdns-applet")
    except: pass
    self.set_name(_("Liber DNS Applet"))
    self.set_version(self.VERSION)
    self.set_copyright(_("Copyright (c) 2008-2011 Ojuba team <core@ojuba.org>"))
    self.set_comments(_("Update Open DNS service address"))
    self.set_license(self.LICENSE)
    self.set_website("http://git.ojuba.org/cgit/LibreDNSApplet")
    self.set_website_label(_("LibreDNSApplet"))
    self.set_authors(self.AUTHORS) #["Ehab El-Gedawy <ehabsas@gmail.com>"])
    self.set_logo_icon_name('liberdns')
    self.set_artists(self.ARTISTS)
    #self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    #	about_dlg.set_documenters(documenters)
    #	about_dlg.set_translator_credits(translator_credits)
    #self.set_logo(logo)

class ConfigDlg(gtk.Dialog):
  def __init__(self, applet):
    gtk.Dialog.__init__(self)
    self.applet=applet
    #self.set_size_request(300,200)
    self.set_resizable(False)
    self.connect('delete-event', lambda w,*a: w.hide() or True)
    self.connect('response', lambda w,*a: w.hide() or True)
    self.set_title(_('Liber DNS Update Preferences'))
    self.add_button(_('Cancel'), gtk.RESPONSE_CANCEL)
    self.add_button(_('Save'), gtk.RESPONSE_OK)
    vb=gtk.VBox()
    self.get_content_area().add(vb)
    hb = gtk.HBox()
    vb.pack_start(hb, False, False, 2)
    self.auto_start = b = gtk.CheckButton(_("Auto start"))
    hb.pack_start(b, False, False, 2)
    self.Unote = b = gtk.CheckButton(_("Show notifications"))
    hb.pack_start(b, False, False, 2)
    hb = gtk.HBox()
    vb.pack_start(hb, False, False, 2)
    hb.pack_start(gtk.Label(_('User name:')), False, False, 2)
    self.Uname = e = gtk.Entry()
    hb.pack_end(e, False, False, 2)
    hb = gtk.HBox()
    vb.pack_start(hb, False, False, 2)
    hb.pack_start(gtk.Label(_('Password:')), False, False, 2)
    self.Upawd = e = gtk.Entry()
    e.set_visibility(False)
    hb.pack_end(e, False, False, 2)
    hb = gtk.HBox()
    vb.pack_start(hb, False, False, 2)
    hb.pack_start(gtk.Label(_('Nerwork Name:')), False, False, 2)
    self.Unetw = e = gtk.Entry()
    hb.pack_end(e, False, False, 2)
    hb = gtk.HBox()
    vb.pack_start(hb, False, False, 2)
    hb.pack_start(gtk.Label(_('Time:')), False, False, 2)
    hb.pack_start(gtk.HBox(), True, True, 2)
    self.Utime = b = gtk.SpinButton(gtk.Adjustment(5, 5, 90, 5, 5))
    hb.pack_end(gtk.Label(_('Minutes')), False, False, 2)
    hb.pack_end(b, False, False, 2)
    
  def run(self, *a, **kw):
    self.auto_start.set_active(not os.path.exists(self.applet.skip_auto_fn))
    self.Uname.set_text(self.applet.conf['Uname'])
    self.Upawd.set_text(self.applet.conf['Upawd'])
    self.Unetw.set_text(self.applet.conf['Unetw'])
    self.Utime.set_value(self.applet.conf['Utime'])
    self.Unote.set_active(self.applet.conf['Unote'])
    return gtk.Dialog.run(self, *a, **kw)
    
class applet(object):
  skip_auto_fn=os.path.expanduser('~/.liberdns-up-applet-skip-auto')
  def __init__(self):
    self.conf_dlg = None
    self.conf = {}
    self.load_conf()
    self.TIMER_ID=None
    self.first_update=True
    self.about_dlg = AboutDLG()
    self.statusicon = gtk.StatusIcon()
    self.statusicon.set_visible(False)
    self.statusicon.connect('popup-menu',self.popup_cb)
    self.statusicon.set_title(_("Liber DNS Update"))
    #self.statusicon.set_tooltip(_("liberdns Update"))
    #self.statusicon.set_from_file(os.path.join('/home/ehab/oj/liberdns','liberdns.svg'))
    self.statusicon.set_from_icon_name('liberdns')
    self.statusicon.set_visible(True)
    pynotify.init('Liber DNS Update')
    self.notifycaps = pynotify.get_server_caps ()
    self.notify=pynotify.Notification(_("Liber DNS Update"))
    self.notify.set_property('icon-name', 'liberdns')
    self.notify.set_property('summary', _("Liber DNS Update....") )
    self.notify.set_hint('resident', True)
    self.notify.set_timeout(5000)
    #notify.set_hint('transient', True)
    self.init_menu()
    self.start_timer_cb()
  
  def start_timer_cb(self, *a):
    if self.first_update:
      self.TIMER_ID = glib.timeout_add_seconds(5, self.timer_cb)
      return True
    if self.TIMER_ID:
      glib.source_remove(self.TIMER_ID)
      self.TIMER_ID=None
    SEC = int(self.conf['Utime'])*60
    self.TIMER_ID = glib.timeout_add_seconds(SEC, self.timer_cb)
      
  def timer_cb(self, *a):
    if self.first_update:
      self.first_update=False
      if self.TIMER_ID: glib.source_remove(self.TIMER_ID)
      self.start_timer_cb()
    self.update_cb()
    return True
    
  def popup_cb(self, s, button, time):
    self.menu.popup(None, None, gtk.status_icon_position_menu, button, time, s)

  def init_menu(self):
    self.menu = gtk.Menu()
    i = gtk.ImageMenuItem(_('Update Now'))
    i.set_always_show_image(True)
    i.connect('activate', self.update_cb)
    self.menu.add(i)
    i = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
    i.set_always_show_image(True)
    i.connect('activate', self.config_cb)
    self.menu.add(i)
    self.menu.add(gtk.SeparatorMenuItem())
    i = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
    i.set_always_show_image(True)
    i.connect('activate', lambda a: self.about_dlg.run())
    self.menu.add(i)
    i = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    i.set_always_show_image(True)
    i.connect('activate', gtk.main_quit)
    self.menu.add(i)
    self.menu.show_all()
  
  def update_cb(self, *a):
    self.menu.get_children()[0].hide()
    self.statusicon.set_blinking(True)
    if self.conf['Uname'] and self.conf['Upawd'] and self.conf['Unetw']:
      b = self.update_dns(self.conf['Uname'], self.conf['Upawd'], self.conf['Unetw'])
      if not b: b = _('Liber NDS update Failed!') # Must not reach this!
    else:
      b = _('Set your Configuration frist')
      if self.TIMER_ID: glib.source_remove(self.TIMER_ID)
      self.TIMER_ID=None
    self.statusicon.set_blinking(True)
    print 'Liber DNS Update, Last stat: %s \033[91m%s\033[0m' %(time.ctime(), b)
    if self.conf['Unote']: self.show_note(b)
    self.menu.get_children()[0].show()
    self.statusicon.set_blinking(False)
    
  def show_note(self, body):
    self.notify.set_property('body', '''%s: %s\n\t\t%s''' % (_('Last stat'), time.ctime(), body))
    self.notify.show()
    
  def config_cb(self, *a):
    if self.conf_dlg==None:
      self.conf_dlg=ConfigDlg(self)
      self.conf_dlg.show_all()
    r=self.conf_dlg.run()
    if r==gtk.RESPONSE_OK:
      #self.save_auto_start()
      self.save_conf()
  
  def save_conf(self):
    self.conf['Unote']=self.conf_dlg.Unote.get_active()
    self.conf['Uname']=self.conf_dlg.Uname.get_text()
    self.conf['Upawd']=self.conf_dlg.Upawd.get_text()
    self.conf['Unetw']=self.conf_dlg.Unetw.get_text()
    self.conf['Utime']=int(self.conf_dlg.Utime.get_value())
    #print "** saving conf", self.conf
    fn=os.path.expanduser('~/.liberdns-up.rc')
    s='\n'.join(map(lambda k: "%s=%s" % (k,str(self.conf[k])), self.conf.keys()))
    try: open(fn,'wt').write(s)
    except OSError: pass
    self.start_timer_cb()
    self.save_auto_start()
    
  def save_auto_start(self):
    b=self.conf_dlg.auto_start.get_active()
    #print b
    if b and os.path.exists(self.skip_auto_fn):
      try: os.unlink(self.skip_auto_fn)
      except OSError: pass
    elif not b:
      open(self.skip_auto_fn,'wt').close()
  
  def load_conf(self):
    s=''
    fn=os.path.expanduser('~/.liberdns-up.rc')
    if os.path.exists(fn):
      try: s=open(fn,'rt').read()
      except OSError: pass
    self.parse_conf(s)
    try: self.conf['Utime']=float(self.conf['Utime'])
    except ValueError:self.conf['Utime']=5
    self.conf['Unote'] = self.conf['Unote']=='True'
    #print "** Loading conf", self.conf
    
  def parse_conf(self, s):
    self.default_conf()
    l1=map(lambda k: k.split('=',1), filter(lambda j: j,map(lambda i: i.strip(),s.splitlines())) )
    l2=map(lambda a: (a[0].strip(),a[1].strip()),filter(lambda j: len(j)==2,l1))
    r=dict(l2)
    self.conf.update(dict(l2))
    return len(l1)==len(l2)

  def default_conf(self):
    self.conf = {}
    self.conf['Unote'] = 'True'
    self.conf['Uname'] = ''
    self.conf['Upawd'] = ''
    self.conf['Unetw'] = ''
    self.conf['Utime'] = 5
       
  def update_dns_old(self, uname, passwd, network):
    url = 'https://%s:%s@updates.opendns.com/nic/update?hostname=%s' %(uname, passwd, network)
    try: r = urllib.urlopen(url).read()
    except IOError, e: r = None
    return r

  def update_dns(self, uname, passwd, network):
    url = 'https://updates.opendns.com/nic/update?hostname=%s' %network
    r = self.request(url, uname, passwd)
    return r
    
  def request(self, url, username, password):
    p = urlparse.urlparse(url)
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, p.hostname, username, password)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    try: response = urllib2.urlopen(url)
    except urllib2.URLError, e: return e
    except urllib2.HTTPError, e: return e
    return response.read()

def init_dbus():
  global bus_name, bus_object, app
  if not bus: return
  class Manager(dbus.service.Object):
    def __init__(self, bus, path):
          dbus.service.Object.__init__(self,bus,path)
    
    @dbus.service.method("org.ojuba.LiberDNS")
    def Show_pref(self):
      return app.config_cb()
    @dbus.service.method("org.ojuba.LiberDNS", in_signature='', out_signature='s')
    def Version(self):
      return "0.1"
  r=bus.request_name('org.ojuba.LiberDNS', flags=0x4)
  if r!=1:
    print "Another process own LiberDNS Service, Exiting... "
    trials=0; appletbus=False
    while(appletbus==False and trials<20):
      print ".",
      try:
        appletbus=bus.get_object("org.ojuba.LiberDNS","/Manager"); break
      except:
        appletbus=False
      time.sleep(1); trials+=1
    print "*"
    if appletbus: exit(appletbus.Show_pref())
    exit(-1)
  bus_name = dbus.service.BusName("org.ojuba.LiberDNS", bus)
  bus_object = Manager(bus, '/Manager')

def main():
  global app
  init_dbus()
  app=applet()
  gtk.window_set_default_icon_name('liberdns')
  gtk.main()

if __name__ == "__main__":
  fn=os.path.expanduser('~/.liberdns-up-applet-skip-auto')
  if '--auto' in sys.argv and os.path.exists(fn): exit(0)
  main()
