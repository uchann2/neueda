#Task: 
##Write a script, which will convert json files to xml files, encrypt and transfer it in a remote location. 

This repository include, two applications written in python. It works in client-sever model. It includes a docker-compose.yml file that will allow you to run both applications in a single docker brige network

##how to run

```bash
git clone https://github.com/uchann2/neueda.git
docker-compose -f docker-compose.yml up -d
```

Following docker compose file was only created to allow testing in a local environment. The two servcies in the file can still be segregated and run in different hosts (swarm cluster), as long as connectivity is there between hosts.

For the demonstration it will create a bridge network with static ips. 

###IMPORTANT: Please make sure to apply the same ip/port settings in the docker-compose.yml file, to be identical with app configurations, that can be found in ./config/receive_config.json and ./config/send_config.json.


```python
version: '3'
services:
  receive-data:
    build:
      context: ./
      dockerfile: Dockerfile.receive
    image: receive-data
    ports:
     - "5000:5000"
    networks:
            app_net:
                ipv4_address: 10.5.0.5
    volumes:
      - ./config/:/usr/src/app/config
      - ./received/:/usr/src/app/received
  send-data:
    build:
      context: ./
      dockerfile: Dockerfile.send
    image: send-data
    depends_on:
      - receive-data
    volumes:
      - ./config/:/usr/src/app/config
      - ./input/:/usr/src/app/input
      - ./xmls/:/usr/src/app/xmls
      - ./sent/:/usr/src/app/sent
    networks:
            app_net:
                ipv4_address: 10.5.0.10
networks:
    app_net:
        driver: bridge
        ipam:
          config:
            - subnet: 10.5.0.0/16
```

1. receive_app.py -> This is the server end of the application.Once run, It listens on a specified port for a tcp stream, in following format.

```python
"<file-name>|<length of data following>|<actual data>"
```

Upon the receipt of the data it saves the data to /usr/src/app/received location of the container. To ensure persistency of the received files and input files, these dependednt directories have been mounted using the bind volumes.

###IMPORTANT: Make sure the volume names in docker-compose.yml match with what is mentioned in ./config/receive_config.json ./config/send_config.json files

1. send_app.py -> This is the client end of the application.Once run, It will lokk for unprocessed files in input directory and send them to server ip and port specified in ./config/send_config.json. For this to work successfully given ip:port should be accessible from the container

```python
"<file-name>|<length of data following>|<actual data>"
```

Upon the receipt of the data it saves the data to /usr/src/app/received location of the container. To ensure persistency of the received files and input files, these dependednt directories have been mounted using the bind volumes.