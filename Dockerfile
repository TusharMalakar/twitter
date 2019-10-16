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
CMD ["main.py"]

#################################################################
# see all the container of a image
#docker ps

# create an image from cmd
#docker build -t twitter:latest .

#damon RUN (PUBLIC), IT will RUN in DOCKER VIRTUALLY
#docker run -it -d -p 5000:5000 twitter

#NB:: docker stop to stop the container
#docker stop <IMAGE-ID>

# running the image as /bin/sh
#docker run -it twitter /bin/sh

#To stop this container
# exit()

#see all the images
#docker images

#stop a container
#docker stop <container-ID>

#NB: To run an image from cmd
# docker run -it <image-name> /bin/sh

# force delete an images
# docker rmi -f <images-id>

##restart docker
#sudo service docker start

##Stop Docker
#sudo service docker stop

####Run a command in a running container####

# go inside a running image
#docker exec -it <IMAGE-ID> bash

# docker commit <container-id> <username>/<image-name>
# docker commit c4a2fca0e4d7 tusharnew/twiter

#docker push <username>/<image-name>
#docker push tusharnew/twiter

# docker pull tusharnew/flaskapp
# docker run -it -d <username>/<image-id>

################apparmor problem############
###############cant kill an images##########
# sudo aa-status
# sudo systemctl disable apparmor.service --now
# sudo service apparmor teardown
# sudo aa-status
