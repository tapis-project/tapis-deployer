# Automated Backup and Restoration

## Basic requirements
We need an automated backup process for MongoDB in Tapis V3. A Point In Time Recovery (PITR) feature is also desirable. In addition, the ability to self management of backups is also necessary feature. In order to do PITR or incremental backups MongoDB needs to be running as a replica set. We are running MongoDB as a single node replica set. Running the server as a replica set creates the opslog. The opslog records every operation applied to the server databases. This container addition to the Meta V3 pod accomplishes these goals.

## Configuration
Automated backup for MongoDb runs three cron jobs at different intervals for backing up MongoDB.

* The first cron job is daily at 3:30 am for a Full dump of MongoDB.
* The second cron job is an hourly incremental dump of the Opslog since the last Full dump.
* The third cron job is daily at 2:30 am to remove Full and Incremental backups older than 3 days.

The backup container is also an execution environment for running on demand backups and restorations.

The organization of tapis-deploy/meta/backup is as follows.

* burndown                                          #  stop automated backup container
* burnup                                               #  start automated backup container
* km                                                      #  pod runtime information
* mongo-backup-claim0-pvc.yaml        #  persistent claim store for backups and logs
* mongo-backup-deployment.yaml       #   deployment yaml for backup container
* README.md                                      #  this file
* pbm                                                    # dir of possible replacement candidate using Percona Backup for MongoDB

## Scripts list and function
* full_dump.sh           # full dump of configured MongoDb host. 
* full_restore.sh        # full restore
* incremental_dump.sh    # incremental dump of opslog  
* incremental_restore.sh # incremental restore of opslog 
* init_rs.js             # replica set initialization function for MongoDB
* init_rs.sh             # script used to check replica set 
* init_static_params.sh  # legacy static parameters 
* old_backup_removal.sh  # script used in cron for removing backups older than the specified setting in cron.
* script.sh              # initialization script that keeps backup container running.
* runtime_env            # runtime environment parameters captured to pass to cron.

## Usage
The most common usage scenario is restoration after a failure or disaster. The assumption is that the user is in the deployment environment that for the restoration, tapis-dev, tapis-stage or tapis-prod. The following steps will restore a full copy of the MongoDB server databases. This assumes a new MongoDB host container configured as a Single Node (SN) replica set has been deployed, empty and is running (see meta/mongo/README). By default the Backup container is wired to the MongoDB host in the pod for Meta and you are in the meta/backup directory. 

1. Use ./km find the pod indentifier information ie: pod/mongo-backup-7f594f95bb-cgwdz.
2. Using $> kubectl exec -it mongo-backup-7f594f95bb-cgwdz -- bash. Exec into the container. You will be in the scripts working directory. An ls -la will list the files for you.
3. The container has several tools installed, MongoDB database tools and a MongoDB client for shell based access to the targeted MongoDB server.
4. To restore the latest Full backup just run $> ./full_dump.sh without any parameters. It is possible to run an earlier full backup by specifying the backup directory to use. These directories can be found in /backup/DB_FULL_DUMP and are named by date. For information on translating the integer date tag on the directory to something human readable see meta/mongo/README. If errors occur it is generally due to the MongoDB server not running or not running in SN replica set mode. 
5. A mongo client can be used to validate restoration of the data.


# get pod info
./km

# get all the object for backup
k get all | grep mongo-backup

# logs for backup container
k logs -f mongo-backup-869b6b69c4-gkv9x

# describe for backup container
k describe pod  mongo-backup-cff69b988-cmfdp
