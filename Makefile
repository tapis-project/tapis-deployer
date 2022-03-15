build-inputgen:
	docker build -t tapis/deployer-input-gen -f Dockerfile-inputgen .

build-deploygen:
	docker build -t tapis/deployer .

build: build-inputgen build-deploygen

push: build
	docker push tapis/deployer; docker push tapis/deployer-input-gen
