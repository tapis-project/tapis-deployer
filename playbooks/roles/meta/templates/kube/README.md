# Meta V3 Service

# Modules
## api
The API module contains the definition files for the Restheart service container and the Meta V3 Securty container. These two containers work as a pipeline to access the MongoDb data server on the back end.

See the README in the api directory

## mongo
The Mongo module contains the definition files for the MongoDb server running as a single node replica set. This gives us access to an operations log (oplog) and transactions for our server. Incremental backups require the oplog to achieve Point In Time Recovery (PITR).

See the README in the mongo directory

## backup
The backup and restore module allows us to run a parallel container that is responsible for scheduled backups and gives us the ability to restore a database that has been corrupted or lost. Incremental backup and restore is a finer grained method for getting backups and restorations tuned to a small window of time and smaller in size than a full backup. Incrementals require a full back/restoration as a base.

See the README in the backup directory

## mongo-exporter
This module holds the implementation of the mongo exporter. This container is able to run a query against the mongodb to extract time based metrics by prometheus. The prometheus exporter allows grafana to present the information in our metrics dashboard.

See the README in the backup directory

## Meta runtime information
Use the _**km**_ script to get runtime information about the modules in **Meta**.

## Starting and stopping containers
TODO

