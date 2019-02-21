docker build --no-cache -t fairhealth/ppdml ./

@echo off
set /p upload="Upload to docker hub? [Y/n]: "
IF /I "%upload%" NEQ "n" (
    docker push fairhealth/ppdml
)