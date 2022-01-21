# backup 

These backup scripts use s3cmd and credentials to move the backup file off of this local system. Therefore, s3cmd must be installed and credentials (usually ~/.s3cfg file) must be present.

## pgbackup-sk 

Here is an example of a script that will do a `pg_dump` of the sk postgres database. You can customize it to backup your database, but a couple warnings:

- you might have to customize the `pg_dump` command user,password,db,etc to get it to work
- run the `kubectl ... pg_dump` manually first to make sure it works
- a backup is no good until you test the restore step!



