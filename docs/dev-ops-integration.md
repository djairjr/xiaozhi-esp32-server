# Full module source code deployment automatic upgrade method

This tutorial is for fans of full-module source code deployment, how to automatically pull the source code, automatically compile, and automatically start port operation through automatic commands. Upgrade system for maximum efficiency.

The test platform of this project, `https://2662r3426b.vicp.fun`, has used this method since its opening with good results.

For tutorials, please refer to the video tutorial released by Bilibili blogger `Bile labs`: ["Open source Xiaozhi server xiaozhi-server automatic update and the latest version of MCP access point configuration nanny tutorial"] (https://www.bilibili.com/video/BV15H37zHE7Q)

# Start condition
- Your computer/server is a linux operating system
- You have gone through the entire process
- You like to keep up with the latest features, but you find manual deployment a bit troublesome every time. You are looking forward to an automatic update method.

The second condition must be met, because some of the files involved in this tutorial, such as JDK, Node.js environment, Conda environment, etc., require you to run through the entire process. If you have not run through it, when I talk about a certain file, you may not know what it means.

# Tutorial effect
- Solve the problem of being unable to pull the latest project source code in China
- Automatically pull code and compile front-end files
- Automatically pull code and compile java files, automatically kill port 8002, and automatically start port 8002
- Automatically pull python code, automatically kill port 8000, and automatically start port 8000

# The first step is to select your project directory

For example, I planned my project directory to be a new blank directory. If you don’t want to make mistakes, you can do the same as me.
```
/home/system/xiaozhi
```

# The second step is to clone this project
At this moment, you need to execute the first sentence and pull the source code. This command is applicable to domestic network servers and computers, and there is no need to bypass the firewall.

```
cd /home/system/xiaozhi
git clone https://ghproxy.net/https://github.com/xinnan-tech/xiaozhi-esp32-server.git
```

After execution, your project directory will have an additional folder `xiaozhi-esp32-server`, which is the source code of the project.

# The third step is to copy the basic files

If you have gone through the entire process before, you will be familiar with the funasr model file `xiaozhi-server/models/SenseVoiceSmall/model.pt` and your private configuration file `xiaozhi-server/data/.config.yaml`.

At this point you need to copy the `model.pt` file to a new directory. You can do this
```
#Create the required directories
mkdir -p /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/data/

cp Your original .config.yaml full path /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/data/.config.yaml
cp The full path of your original model.pt /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/models/SenseVoiceSmall/model.pt
```

# Step 4: Create three automatic compilation files

## 4.1 Automatically compile mananger-web module
In the `/home/system/xiaozhi/` directory, create a file named `update_8001.sh` with the following content

```
cd /home/system/xiaozhi/xiaozhi-esp32-server
git fetch --all
git reset --hard
git pull origin main


cd /home/system/xiaozhi/xiaozhi-esp32-server/main/manager-web
npm install
npm run build
rm -rf /home/system/xiaozhi/manager-web
mv /home/system/xiaozhi/xiaozhi-esp32-server/main/manager-web/dist /home/system/xiaozhi/manager-web
```

After saving, execute the authorization command
```
chmod 777 update_8001.sh
```
After execution, continue below

## 4.2 Automatically compile and run the manager-api module
In the `/home/system/xiaozhi/` directory, create a file named `update_8002.sh` with the following content

```
cd /home/system/xiaozhi/xiaozhi-esp32-server
git pull origin main


cd /home/system/xiaozhi/xiaozhi-esp32-server/main/manager-api
rm -rf target
mvn clean package -Dmaven.test.skip=true
cd /home/system/xiaozhi/

# Find the process ID occupying port 8002
PID=$(sudo netstat -tulnp | grep 8002 | awk '{print $7}' | cut -d'/' -f1)

rm -rf /home/system/xiaozhi/xiaozhi-esp32-api.jar
mv /home/system/xiaozhi/xiaozhi-esp32-server/main/manager-api/target/xiaozhi-esp32-api.jar /home/system/xiaozhi/xiaozhi-esp32-api.jar

# Check if the process number is found
if [ -z "$PID" ]; then
echo "The process occupying port 8002 was not found"
else
echo "Find the process occupying port 8002, the process number is: $PID"
# Kill the process
  kill -9 $PID
  kill -9 $PID
echo "Killed process $PID"
fi

nohup java -jar xiaozhi-esp32-api.jar --spring.profiles.active=dev &

tail tail -f nohup.out
```

After saving, execute the authorization command
```
chmod 777 update_8002.sh
```
After execution, continue below

## 4.3 Automatically compile and run Python projects
In the `/home/system/xiaozhi/` directory, create a file named `update_8000.sh` with the following content

```
cd /home/system/xiaozhi/xiaozhi-esp32-server
git pull origin main

# Find the process ID occupying port 8000
PID=$(sudo netstat -tulnp | grep 8000 | awk '{print $7}' | cut -d'/' -f1)

# Check if the process number is found
if [ -z "$PID" ]; then
echo "No process occupying port 8000 was found"
else
echo "Find the process occupying port 8000, the process number is: $PID"
# Kill the process
  kill -9 $PID
  kill -9 $PID
echo "Killed process $PID"
fi
cd main/xiaozhi-server
#Initialize conda environment
source ~/.bashrc
conda activate xiaozhi-esp32-server
pip install -r requirements.txt
nohup python app.py >/dev/null &
tail -f /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/tmp/server.log
```

After saving, execute the authorization command
```
chmod 777 update_8000.sh
```
After execution, continue below

# Daily updates

After the above scripts are created, for daily updates, we only need to execute the following commands in order to automatically update and start

```
cd /home/system/xiaozhi
# Update and start the Java program
./update_8001.sh
# Update web program
./update_8002.sh
# Update and start the python program
./update_8000.sh


# If you want to view the java log later, execute the following command
tail -f nohup.out
# If you want to view the python log later, execute the following command
tail -f /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/tmp/server.log
```

# Notes
The test platform `https://2662r3426b.vicp.fun` uses nginx as a reverse proxy. Detailed configuration of nginx.conf can be found [refer here](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues/791)

## FAQ

### 1. Why don’t you see port 8001?
Answer: 8001 is the port used by the development environment to run the front end. If you are deploying on a server, it is not recommended to use `npm run serve` to start port 8001 to run the front end. Instead, compile it into an html file like this tutorial, and then use nginx to manage access.

### 2. Do I need to update manual SQL statements for each update?
Answer: No, because the project uses **Liquibase** to manage the database version and will automatically execute new sql scripts.