SHORT LINKS Project
==============

### What's included

 - Python
 - Django
 - Nginx
 - MySQL
 
### Docker
 - Create `.env` file and configure this file
     ```
     $ cp .env.dist .env
     ```
 - Start
     ``` 
     @dev:~$ bash init.sh
     ```
 - Build a new image and run containers
     ```
     @dev:~$ docker-compose up -d --build
     @prod:~$ docker-compose -f docker-compose.prod.yml up -d --build
     ```
 - Flush and migrate database
     ```
     @dev:~$ docker-compose exec web python manage.py flush --no-input
     @dev:~$ docker-compose exec web python manage.py migrate
     @prod:~$ docker-compose -f docker-compose.prod.yml exec web python manage.py flush --no-input
     @prod:~$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
     ```
 - Checking for errors in logs
     ```
     @dev:~$ docker-compose logs -f
     @prod:~$ docker-compose -f docker-compose.prod.yml logs -f
     ```
 - Stop containers and bind volumes with the -v flag
     ```
     @dev:~$ docker-compose down -v
     @prod:~$ docker-compose -f docker-compose.prod.yml down -v
     ```