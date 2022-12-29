# Amazon Reviews Scrapper
To use this program, you will have to setup some basic things before you can get started.

### Get Proxy
Amazon will block your ip address if you send multiple requets like a robot so we will have to get some proxies.

You can consider Soax or of you want free alternative you can look for those online. There are plenty of them available and only handful of them actually works.

So I am going to use free proxy from [webshare.io](https://www.webshare.io/), they give 10 free proxies and 1 GB of bandwidth for free!

### Step-1 
Create an account on [webshare.io](https://www.webshare.io/) and get your username and password.

### Step-2
 Download (or copy) all the ip addresses and their respective ports that you've been given.

### Step 3 
Replace all the ips with your ips in the script 
![](https://i.postimg.cc/3NJ6zr5C/image.png)

### Step 4 
You will have to use your username and password, so either set it as Environment variable on your system or use a variable

![](https://i.postimg.cc/d35PXDWw/image.png)

### Step 5
Install necessary requirements using this command:
```shell
pip install -r requirements.txt
```
### Step 6
You're almost there!! Just run the script by using the following command:
```shell
uvicorn main:app --reload
```

then visit the local url to use the application.


## Feedback and Contributions

If you have any feedback, please feel free to raise an issue and Contributions are welcomed.

