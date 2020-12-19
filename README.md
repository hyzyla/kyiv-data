# Commands



## Generate requirements/base.txt
```
docker-compose run --rm pip-compile requirements/base.in -o requirements/base.txt
```

## Generate requirements/tools.txt
```
docker-compose run --rm pip-compile requirements/tools.in -o requirements/tools.txt
```


## Generate requirements/prod.txt
```
docker-compose run --rm pip-compile requirements/prod.in -o requirements/prod.txt
```


##  Auto generate migration 
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

## Deploy
```
git push dokku main:master
```

