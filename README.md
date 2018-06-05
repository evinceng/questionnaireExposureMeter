
#Installed packages------------
-Note that I installed them via conda install scripts,
-I will provide the pip install version but note that it is not tested, you may google for that

conda install -c conda-forge tk #this should be installed already in standard library
conda install -c conda-forge bottle / pip install bottle
conda install -c conda-forge apscheduler / pip install apscheduler
conda install -c conda-forge pydispatcher / pip install PyDispatcher
conda install -c cogsci pygame / pip install Pygame
conda install -c conda-forge python-utils / pip install python-utils

#MongoDB-----------------------
-Mongodb server is running at localhost for now (Installation is available at 04-Installations folder)
-I personally prefer to have visual of data I have in DB, so I installed studio 3t (Installation is available at 04-Installations folder)
-Note that some GUI for mongodb (ex:MongoDB compass) assuming all timestamps are in UTC;
 so when displaying I see a two hour difference but you can see the correct timestamp in sessionID as a string
-Create a folder for storing DB mine is "C:\Users\evin\Documents\MongoDB"
-To start a local server open cmd, type in following commands according to the location of mongo installation
 and the folder you created in the previous step

cd C:\Program Files\MongoDB\Server\3.6\bin
mongod.exe --dbpath "C:\Users\evin\Documents\MongoDB"

-Then it will start waiting connections

#TOBII---------------------------
-Note that TOBII sensor should be plugged in to a USB 2.0 for installing, in my experience using USB 3.0 works after installation
-To use TOBII sensor run the "InstallationGuide.exe" in the "04-Installations\Tobii\SW\InstallationGuide" folder.
-double click "LucamiTobiiLoggerForwarder.exe" file in the "04-Installations\LucamiTobiiLoggerForwarder\bin\Debug" folder 


#Preperation:

1. Connect tobii eyetracker sensor; if you are going to use it
2. Run tobii eyetracker dotnet app.
3. Have following fields in config: Change the values according to your needs 
  (note that the keys are referred in the scripts harcoded, so please don't change them)
  
    [SERVER]
    IP = 127.0.0.1
    Port = 8080
    EmptyDataRoute = /emptyData

    [MONGODB]
    Host = localhost
    Port = 27017
    DBName = mediaExposureTry

    [QUESTIONNAIRE]
    DBCollectionName = questionnaire
    FinalAnswersCollectionName = finalAnswersQuest

    [TOBII]
    Url = localhost
    Port = 10003
    HostRoute = /tobiiEyetracker
    IsLocalFileLogging = True
    IsDataHasToBeParsed = False
    DBCollectionName = tobiiQuestionnaire


7. Edit ActionUnit.py file according to needs(Necessary info can be found in the script file)
If not edited following actions will be observed.

#Run:
1. Run the Mvc.py file through command line
    *by pressing 'Alt+D' in the folder
    *type 'cmd' in the selected folder path
    *python Mvc.py
2.  Enter the username (for ex: evina)
3.  Press the start button through exposuremeter
4.  Observe sessionStarttime is displayed on the console
5.  The prequestionnaire will be displayed after 0.5 seconds the start button is pressed
6.  Fill the pop up pre questionnaire (timeActionUnit)
7.  Close the pre questionnaire window
8.  Observe "Message is first" is displayed on the console at first second (timeActionUnit)
9.  Observe "Message is second" is displayed on the console at third second (timeActionUnit)
10. Press "Connect" button on the dot net application that you opened in preperation step 1
11. Press "Disconnect" button when you are done
12. If you added new sensors do the necessary actions 
13. Press Stop button when you are done
14. Observe "Message is the session is going to be stopped." is displayed on the console (eventActionUnit)
15. Fill the pop up post questionnaire
16. Close the post questionnaire window
17. Close the exposuremeter app.
18. Please restart the exposure meter for a new session(for scheduler)


#Adding a new sensor class---------------
-There is an example Tobii class inheriting Sensor class. So Tobii.py should be inspected while adding a new sensor,
 and I will be explaining situations on the basis of Tobii sensor
-Note that every sensor is assumed to communicate via sockets.
-There is a Sensor.py class file for the common parts of all sensors
-Note that there are two methods unimplemented in Sensor.py; "parseData" and "shapeDataForDB"
-These methods should be implemeted by inheriting the Sensor class if needed by every sensor
-"parseData" is needed to make data coming from the sensor easy to process 
(in the case of Tobii it was not needed, and it may not be needed for any sensor)
-"shapeDataForDB" is used for having flat data and other computations. 
For ex: Tobii had everything in string format and "," for double values, so these issues are resolved in this method

#Initialize new sensor-------------------
-After a new class is created by inheriting Sensor class, put necessary configurations in the config.ini file (simply copy paste TOBII section and change as you wish)
-Initialize it in Model.py in "__init__" method by calling initNewSensorName  method that you created
-Please refer to "initTobiiEyeTracker" method. The new sensor should be initialiazed in the same way:
 by creating a new thread to run all the sensors in parallel
-Start the the sensor method in "start" method.
-Please note that you have to set the "startTime" first and then call "startListening" method
-Stop the sensor in "stop" method by calling the sensor's "stopListening" method

#ActionUnit----------------------------
-Please have a look at ActionUnit.py file
-Sound files are preferred in .ogg file extension, 
(if you have mp3 files or some other files you can simply convert them thorugh a website like "https://convertio.co/mp3-converter/")
-I used "https://www.texttomp3.online/" (Samantha for voice) for generating audio files