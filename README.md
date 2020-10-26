# Commands


## Generate requirements/base.txt
```
docker-compose run --rm pip-compile
```

## Generate requirements/tools.txt
```
docker-compose run --rm pip-compile requirements/tools.in -o requirements/tools.txt
```


##  Auto genereate migration 
```
docker-compose run app db migrate -m "Initial migration."
```

## Apply migration
```
docker-compose run app db upgrade
```

## Change permission of migration (only for Linux)
```
sudo chown -R $USER migrations
```