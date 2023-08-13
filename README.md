# spotter
Use Spotify API to fetch data and store it on a SQL server.

## Set up with Docker Compose:
- Create environment file 
Modify env_template with your Spotify API info and the MYSQL settings you wish to use, then rename or copy to '.env'.

- Run docker compose
~~~
sudo docker-compose
~~~
This will set up the the database and auto-populate recommendations for the current day and the last 4 days.
If you wish to start with a blank database.

- Populate with recommendations.
Optionally you can pre-populate the database to contain recommendations. 
~~~
sudo docker-compose run fetch
~~~
Running this command wil fetch todays recommendations
~~~
sudo docker-compose run fetch python fetch 5
~~~
Adding 'python fetch 5' will fetch todays recommendations and a number of preceding days for a total of 5 days.
Adjust the trailing number as you see fit. 

- Schedule
...