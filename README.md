# dns_lab

Under each of the 3 folders US, AS, and FS, please use command:

docker build -t userName/path:latest .

to build the .py file in corresponding folder onto Docker according to userName. After that, please build a Docker network using:

docker network create someNetworkName

and then uses docker run for each of the 3 images to run them in containers. Please use --network someNetworkName in this run command to run these images under the Docker network you have built. Besides, please use port 8080:8080, 9090:9090, and 53533:53533 for user server, Fibonacci server, and authoritative server, respectively.

After that, please first register the DNS of your Fibonacci server. You can use some HTTP tools (e.g., Postman on Google Chrome) to send an HTTP PUT message to http://localhost:9090. In this PUT message, please provide JSON object in the right format as below:

{
    "hostname": your hostname,
    "ip": your FS IP,
    "as_ip": your AS IP,
    "as_port": "53533"
}

Specially, both ip and as_ip in this JSON object should be the IP address of each container inside the Docker network you have created. You can use docker inspect someNetworkName to check these 2 IP addresses directly.

Then, if the DNS registration is successful, your registration information will be returned in the HTTP response 201. After that, you can refer to localhost:8080/fibonacci on the user server to test DNS query and fibonacci number retrieval. In this URL, hostname should be correctly registered on the authoritative server, fs_port should be 9090, and the as_ip and as_port should be the IP and port number of the authoritative server under your Docker network. If the URL is correct, the return message on your page is: (take number=30 as an example)

Fibonacci number generated. The result is: 832040
