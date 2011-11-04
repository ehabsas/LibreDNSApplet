#!/usr/bin/env python2
#!/usr/bin/python
import sys, os, os.path
from distutils.core import setup
from glob import glob
VERSION=open(os.path.join(os.path.dirname(sys.argv[0]), 'VERSION'), 'r').read().strip()
## python2 setup.py install --root=/ #~ For ArchLinux Users
## python setup.py install --root=/
locales=map(lambda i: ('share/'+i,[''+i+'/liberdns.mo',]),glob('locale/*/LC_MESSAGES'))
data_files=[]
data_files.extend(locales)
setup (name='liberdns', version=VERSION,
      description='Liber Open DNS update tool',
      author='Ehab El-Gedawy',
      author_email='ehabsas@gmail.com',
      url='http://git.ojuba.org/',
      license='Waqf',
      py_modules = ['liberdns'],
      scripts=['liberdns-applet'],
      data_files=data_files
)


