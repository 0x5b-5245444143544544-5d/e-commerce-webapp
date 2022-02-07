# e-commerce-webapp
A flask-based e-commerce web application

## How do I run this?
1. Create a .env file and config.yml in project root directory, fill them up as necessary, use the docker-compose file to deploy a mariadb instance (/var/lib/mysql wasn't mapped to a folder on disk, so it will *not* persist reboots)
2. Install the prerequisites by running:
```
pip install -r requirements.txt
```
inside the `backend` folder.
3. Set the shell environment variable `FLASK_APP` as `backend` and then run `flask run` and the site should be served at `http://localhost:5000`
