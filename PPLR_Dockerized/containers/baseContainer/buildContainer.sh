docker rmi datasharing/base
docker build -t datasharing/base .\

# if you want to run the container in a command line, and mount the PQcrypto to a local folder, uncomment the line below
# docker run -it datasharing/base /bin/bash
