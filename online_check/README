This is a sample application that uses python-stdnum to see which number
formats are valid for a supplied number as can be seen online at:
  https://arthurdejong.org/python-stdnum/check/

Configuring the WSGI application in Apache.

- /path/to/wsgi is the directory containing the WSGI scripts
- /path/to/html is the directory containing the static files

The python-stdnum checkout is expected to be available in
/path/to/wsgi/python-stdnum.


WSGIDaemonProcess stdnum threads=5 maximum-requests=100 display-name=%{GROUP}
<Directory /path/to/wsgi>
  <Files stdnum.wsgi>
    WSGIProcessGroup stdnum
  </Files>
</Directory>
Alias /check /path/to/html
WSGIScriptAlias /check/stdnum.wsgi /path/to/wsgi/stdnum.wsgi
RewriteRule ^/check/$ /check/stdnum.wsgi/$1 [QSA,PT,L]
