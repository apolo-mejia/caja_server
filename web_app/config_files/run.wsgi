import sys
sys.path.insert(0, "/var/www/html/web_app")

activate_this = '/home/pi/.local/share/virtualenvs/web_app-y4PcvRiq/bin/activate_this.py'
with open(activate_this) as file_:
  exec(file_.read(),dict(__file__=activate_this))

from index import app as application

