docker build --no-cache -t fairhealth/basetrain ./

printf "Upload to Docker Hub?\nOptions [Y/n]: "
read uploadChoice
if [ $uploadChoice != "n" ]; then
    docker push fairhealth/basetrain
fi
