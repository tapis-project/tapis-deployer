# Image: tapis/deployer

FROM tapis/deployer-input-gen

WORKDIR /deploygen
ENTRYPOINT ["python3", "tapis-api-generator.py"]