# elk

kinda sorta working elastic stack

## stern

Stern is a utility that streams all your kubernetes' pods logs to stdout. You can download and run it live and it's nice.

What these ymls do is run it inside a fluentd container so that it can send all the logs from your namespace to elasticsearch. 

See stern-fluentd.yml & stern-fluentd-config.yml. 

Currently you need to create a configmap with your kube config. Hopefully we can find a workaround to that later.
