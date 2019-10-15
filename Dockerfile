# load the base docker image
FROM alpine:latest

#install python3 and pip3 inside the alpine image
RUN apk add --no-cache python3-dev && pip3 install --upgrade pip

#copy the source code and libraries inside the alpine image
#creating a app_directory inside my image
WORKDIR /app
#copy everything inside the app_dir of image
COPY . /app
#run pip cmd to install all libraies form requirements.txt
RUN pip3 --no-cache-dir install -r requirements.txt

#Expose a port
EXPOSE 5000

#Now build the EXECUTABLE IMAGE using python CMD
# python3 app.py
ENTRYPOINT ["python3"]
CMD ["app.py"]

#################################################################
# see all the container of a image
#docker ps

#non-damon mode RUN (locally)
#docker run -it flaskapp

#damon RUN (PUBLIC), IT will RUN in DOCKER VIRTUALLY
#docker run -it -d -p 5000:5000 flaskapp

#NB:: docker stop to stop the container
#docker stop <IMAGE-ID>

# running the image as /bin/sh
#docker run -it flaskapp /bin/sh

#To stop this container
# exit()

# create an image from cmd
#docker build -t flaskapp:latest .

#see all the images
#docker images

#run a CONTAINER from the Image (LOCALLY)
#docker run -it flaskapp

#run a CONTAINER from the Image (PUBLICLY)
#docker run -it -d -p 5999: 5000 flaskapp

#How many container is running
#docker ps

#stop a container
#docker stop <container-ID>

#NB: To run an image from cmd
# docker run -it <image-name> /bin/sh


####################################  Whenever we run a IMAGE, It generate a NEW Container ##########################################

#$ docker images                     // To view install images
#$ docker rmi <IMAGE_NAME>           // To remove an installed image
#
#$ docker ps -a                      // To view all docker containers
#$ docker stop <CONTAINER_NAME>      // To stop a docker container
#$ docker rm <CONTAINER_NAME>        // To remove a docker container
#
#$ docker exec -it <CONTAINER_NAME> bash    // Execute into container and run bash

##Reload the systemctl daemon
#sudo systemctl daemon-reload

##restart docker
#sudo service docker start

##Stop Docker
#sudo service docker stop

####Run a command in a running container####

# go inside a running image
#docker exec -it <IMAGE-ID> bash

# docker commit <container-id> <username>/<image-name>
# docker commit c4a2fca0e4d7 tusharnew/flaskapp

#docker push <username>/<image-name>
#docker push tusharnew/flaskapp

# docker pull tusharnew/flaskapp
# docker run -it -d <username>/<image-id>
