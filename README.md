# twitter - api by "TUSHAR MALAKAR"
- Twitter API Documentation:
- Distributed System and Cloud Computing


Purpose: a cloud API (Application Programming Interface) to provide services to users. Services like to create a tweet, read a tweet,            update a tweet, a delete tweet, comment on a tweet, like and dislike a tweet. In addition, “sign in” and “sign up” services to          create and log-in to authentication services. 

Programming Language: I used “python3.7.3” with “flask1.1.1” and “PyJWT1.7.1” to generate endpoints endpoints.   

Data base: I used NoSQL database, “Mongodb” to store user account and tweets. Database name is TWITTER. TWITTER database has two                    collection. For example:
           1.	Users Collection: to store all user account with username and password.
 

        2.	Tweet Collection: to store all tweet with the actual tweet and its owner, likes with liker name and actual like sign and               comments with commenter name and actual comment.
   

   I have two types to services: 
     1.	Public endpoints: where users do not need any authentication.
     
     2.	 Private endpoints: where users need to authenticate himself through “create_user” or “log_in” endpoints. Note: I am using “json       web token” as session cookie to provide authentication to authenticate a user.
     Public Endpoints: Endpoints which do not need authentication. In this API services, I have few endpoints do not need to                  authentication. For example:
     
public Endpoints:     
   1.	“create_user” endpoint to create a new user with a HTTP POST request to server where user need to send a JSON body with request.      This request will return, success message with a JWT session token or failure message with error message. 
   Note: user need to send this JWT session token to authenticate himself to use authenticated services.



   2.	“log-in” endpoint to login to an account with a HTTP GET request to server. User should have a valid account with a valid username    and a valid password to “log in.” This request will return, success message with a JWT session token or failure message with error      message.
   Note: user need to send this JWT session token to authenticate himself to use authenticated services.





   3.	“All_tweet” endpoint to view all tweets with a HHTP GET request to server. This will return all active tweets. 

Private Endpoints: To use these services user needs to add “session token” was return from “log in” or “sign up” to authenticate all         these services. For example:
   1.	“create_tweet” endpoint to create a new tweet with a HTTP POST request, in the tweet body requires a tweet and tweet owner. It        will return success message on successful creation of tweet or failure message on failure to create a tweet.  

   2.	“edit_my_tweet” endpoint to edit a tweet if she or he is the owner of the tweet with a HTTP POST request. In the body, “tweet ID”    and “ownership” of tweet is required. It will return success message on successful edition of tweet or failure message on failure to    edit a tweet.

   3.	“delete_my_tweet” endpoint to delete a tweet if she or he is the owner of the tweet with a HTTP POST request. In the body, “tweet    ID” and “ownership” of tweet is required. It will return success message on successful deletion of tweet or failure message on          failure to delete a tweet.

   4.	“my_tweet” endpoint to see all my tweets with a HTTP GET request to server. In this 

   request “owner name” is required. It will return success message on successful request with all tweets or failure message on failure.

   5.	“comment_on_tweet” endpoint to comment on a tweet with HTTP POST request. In the body “tweet ID”, commenter and comment are          required. It will return success message on successful comment addition on a tweet or failure message on failure.

   6.	“like_on_tweet” endpoint to like a tweet with HTTP POST request. In the json body “tweet id”, liker and actual like are required.    It will return success message on successful like addition on a tweet or failure message on failure.


   Please visit “https://github.com/TusharMalakar/twitter-api” to see the  code design.

# DEPLOY to KUBERNETES : https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app
1. install kubectl
   - gcloud components install kubectl
2. Set the PROJECT_ID environment variable to your GCP project ID.
    - export PROJECT_ID=[PROJECT_ID]
3. build the container image of this application and tag it for uploading
    - docker build -t gcr.io/${PROJECT_ID}/twitter:v1 .
4. verify that the build 
    - docker images
    
# upload the images
5. configure Docker command-line tool to authenticate to Container Registry
    - gcloud auth configure-docker
6. upload the image to your Container Registry using Docker cli
    - docker push gcr.io/${PROJECT_ID}/twitter:v1

# Create cluster to run the container image. e.g. cluster has VM 
7. Set your project ID
    - gcloud config set project $PROJECT_ID
8. Set your Compute Engine zone
    - gcloud config set compute/zone [COMPUTE_ENGINE_ZONE]
9. create a two-node cluster named twitter-cluster
    - gcloud container clusters create twitter-cluster --num-nodes=2
10. config the create clusters, it takes few minuites 
    - gcloud compute instances list

# Deploy application, Kubernetes represents applications as Pods
11. Run the following command to deploy twitter application
    - kubectl create deployment hello-web --image=gcr.io/${PROJECT_ID}/twitter:v1
12. see the Pod created by the Deployment
    - kubectl get pods

# Expose your application to the Internet
13. Expose external IP address to access the app
    - kubectl expose deployment twitter --type=LoadBalancer --port 80 --target-port 8080
14. find your extarnal adn cluster IP address
    - kubectl get service
    
# Scale up your application : add more replicas to your application's
15. add two additional replicas to your Deployment (for a total of three)
    - kubectl scale deployment twitter --replicas=3
16. config the replicas running on your cluster
    - kubectl get deployment twitter
