# PythonAnywhere Deploy Guide

This project is ready to deploy on PythonAnywhere from GitHub.

## 1. Create the web app

In PythonAnywhere dashboard:

1. Open `Web`
2. Click `Add a new web app`
3. Choose `Manual configuration`
4. Select `Python 3.10` or the closest available version

## 2. Open a Bash console and clone the repo

```bash
cd ~
git clone https://github.com/kaushalahirwar21/timepass.git
cd timepass
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

## 3. Set environment variables

In the Bash console, replace the values with your real domain and secret key:

```bash
echo 'export DJANGO_SECRET_KEY="replace-with-a-strong-secret-key"' >> ~/.bashrc
echo 'export DJANGO_DEBUG="False"' >> ~/.bashrc
echo 'export DJANGO_ALLOWED_HOSTS="choudharytravels.pythonanywhere.com"' >> ~/.bashrc
echo 'export DJANGO_CSRF_TRUSTED_ORIGINS="https://choudharytravels.pythonanywhere.com"' >> ~/.bashrc
echo 'export DJANGO_TIME_ZONE="Asia/Kolkata"' >> ~/.bashrc
source ~/.bashrc
```

If your PythonAnywhere username is different, use:

```bash
echo 'export DJANGO_ALLOWED_HOSTS="yourusername.pythonanywhere.com"' >> ~/.bashrc
echo 'export DJANGO_CSRF_TRUSTED_ORIGINS="https://yourusername.pythonanywhere.com"' >> ~/.bashrc
source ~/.bashrc
```

## 4. Configure the WSGI file

In PythonAnywhere `Web` tab, open the WSGI configuration file and make sure it contains the project path and virtualenv path for this repo.

Use this structure:

```python
import os
import sys

path = '/home/yourusername/timepass'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Also set the virtualenv in the `Web` tab to:

```text
/home/yourusername/timepass/.venv
```

## 5. Static and media mapping

In the `Web` tab add:

- URL: `/static/`
- Directory: `/home/yourusername/timepass/staticfiles`

Optional media mapping:

- URL: `/media/`
- Directory: `/home/yourusername/timepass/media`

## 6. Reload

Click `Reload` in the `Web` tab.

## 7. Update after new commits

Each time you push changes to GitHub, run:

```bash
cd ~/timepass
source .venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then reload the web app from the `Web` tab.
