# Meta V3 Service

## Containers
These containers work as a pipeline unit for requests to MongoDb data. The restheart-security container takes care of validating jwt tokens and checking the permissions on available databases and collections. 

### restheart
This is the backend Restful api that handles most connections to MongoDb.


### restheart-security
This container proxies requests to restheart acting as a security filter allowing access to mongodb resources.

## Starting and stopping containers
TODO

