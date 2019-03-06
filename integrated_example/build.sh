docker rmi fairhealth/ppdml
docker build --no-cache -t fairhealth/ppdml ./

printf "Upload to Docker Hub?\nOptions [Y/n]: "
read uploadChoice
if [ $uploadChoice != "n" ]; then
    docker push fairhealth/ppdml
fi