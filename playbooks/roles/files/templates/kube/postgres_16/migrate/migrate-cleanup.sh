# clean up all migration related objects
kubectl delete configmap files-migrate-pg-11-to-16-sh-configmap
kubectl delete configmap files-migrate-pg-11-to-16-vars-configmap
kubectl delete -f files-migrate-pg-11-to-16.yml
kubectl delete -f files-migrate-check-pg-11-to-16.yml

kubectl delete -f ../service.yml
kubectl delete -f ../deploy.yml
kubectl delete -f ../pg-16-pvc.yml 
