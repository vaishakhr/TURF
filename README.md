# TURF
 The TURF algorithm that improves the bias of polynomial distribution estimators

Note:
This code heavily borrows from https://github.com/ludwigschmidt/ppoly_density
Our main contributions are in
1. ../src/newfuns.py 
2. Cell #4 of the two experiment files: ./experiments/turf_expts_d1.ipynb, ./experiments/turf_expts_d2.ipynb

Instructions:
1. Install Docker E.g. if using a Mac https://docs.docker.com/docker-for-mac/install/
2. Go to ./docker and run 
"docker build -t ppoly -f Dockerfile ."
3. Return to main folder and run:
"docker run -p 8800:8800 -v /TURF:/root/ppoly_density ppoly jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8800" (change /TURF to the corresponding path on your system)
4. Use the URL that is output by the terminal in a browser to access notebooks

IMPORTANT: 
If using a Mac with M1 chips some compatibility issues crop up when building the dockerfile.
To overcome this, run the following after installing the docker to set up the value of a docker environment variable. 
export DOCKER_DEFAULT_PLATFORM=linux/amd64

For troubleshooting:
To ssh into docker in case certain files are missing:
1. Find container name with
docker ps 
2. ssh with
docker exec -it <container name> /bin/bash
3. To kill docker
docker kill <container name>


