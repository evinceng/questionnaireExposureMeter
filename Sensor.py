# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 16:05:35 2018

@author: evin
@brief: Base class for each sensor, If necessary e new sensor that is going to be 
    connected will extend this class and have its own implmentations 
    for shapeDataforDB and parseData(if necessary)
"""
import json
from bottle import response
from datetime import datetime
import socket
import config
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dateutil.tz import tzlocal
from collections import OrderedDict

class Sensor():
    """
    Base class for each sensor, If necessary e new sensor that is going to be 
    connected will extend this class and have its own implmentations 
    for shapeDataforDB and parseData(if necessary)
    """
    
    sensorMessage=[]
    #sensorMessage.append(json.loads('{"tobiiEyeTracker":{"timeStamp":"30.12.2015 14:06:20.2412","leftPos":{"x":"-0,228793755914194","y":"11,5027813555582","z":"60,912982163767"},"rightPos":{"x":"5,89524352818696","y":"11,2245013358383","z":"61,0730322352786"},"leftGaze":{"x":"3,15812377150551","y":"17,3247499470179","z":"4,61986983600664"},"rightGaze":{"x":"-2,49937069615642","y":"17,3932511520527","z":"4,64480229580618"},"leftPupilDiameter":"2,645874","rightPupilDiameter":"2,622345"}}'))
    #sensorMessage.append(json.loads('{"tobiiEyeTracker":{"timeStamp":"30.12.2015 14:06:20.2442","leftPos":{"x":"-0,258863875351471","y":"11,5149518687205","z":"60,9095247803002"},"rightPos":{"x":"5,88168331298095","y":"11,2362714331765","z":"61,0613078775579"},"leftGaze":{"x":"2,38144559635971","y":"16,7283881083418","z":"4,40281135417063"},"rightGaze":{"x":"-3,55454772939922","y":"17,2529816540119","z":"4,59374825056375"},"leftPupilDiameter":"2,642151","rightPupilDiameter":"2,673187"}}'))
    
    def __init__(self, configSectionName):
        """
        Initilazes the necessary parameters and establishes DB connection
        """
        self.configSectionName = configSectionName
        self.halt = 0
        self.__receivedEventCounter = 0
        self.__initDBConnection()
    
    def setSessionStartTime(self, startTime):
        """
        The start time of the experiment is set when the start button is pressed
        """
        self.sessionStartTime = startTime
    
    def listenSocketFromDotNET(self):
        """
        The socket is listened for input, the input is parsed if necessary and
        shaped for db and data is written to both a logfile and DB
        """
        self.halt = 0
        self.sock = self.__initSocket()
        
        try:
            while True:
                # Wait for a connection
                print >>sys.stderr, "Server socket for incomming ", self.configSectionName, " data: waiting for a connection"
                connection, client_address = self.sock.accept()
                
#                print "sessionstarttime is ############"
#                print self.sessionStartTime
#                print "sessionstarttime is ###############"
                
                self.userPropsDict = self.createUserPropsDict()
                __timeStamp = self.sessionStartTime.strftime('%Y-%m-%d_%H%M%S')
                self.logFileName = self.configSectionName + "Log_" + __timeStamp + ".log"
                
                if not self.halt:
                    try:
                        while True:
                            if not self.halt:
                                print >>sys.stderr, "Server socket for incomming ", self.configSectionName, " data: connection from", client_address
                                self.__receivedEventCounter = self.__receivedEventCounter + 1
                                data = connection.recv(10000) # kinda ugly hack. If incomming message will be longer this will spill.
                            
                                if config.getConfig().getboolean(self.configSectionName, "IsDataHasToBeParsed"):
                                    __parsedData = self.parseData(self, data)
                                    data = __parsedData
                                self.sensorMessage.append(json.loads(data))
                                self.__writeToFile(data, "a")
                                self.__writeToDB(data)
                            
                                if data:
                                    print >>sys.stderr, "Server socket for incomming ", self.configSectionName, " data: sending data back to the client"
                                    connection.sendall(data)
                                else:
                                    print >>sys.stderr, "Server socket for incomming ", self.configSectionName, " data: no more data from", client_address
                                    break
                            else:
                                break
                    except Exception as e:
                        print("something's wrong with %s. Exception is %s" % (client_address, e))
                    finally:
                        # Clean up the connection
                        connection.shutdown(1)
                        connection.close()
                        print "Closing incomming ", self.configSectionName, " data socket connection."
                else:
                    break
        finally: 
            self.sock.close()
            print "Finished server socket for incomming ", self.configSectionName, " data thread"
                     
        print "Leaving listening method of ", self.configSectionName
    
    def respondTracker(self):
        """
        respond the web browser when the webpage is opened or refresh button is pressed
        """
        response.headers["Content-type"] = "application/json"
        data = {}
        
        data["receivedEventCounter"] = self.__receivedEventCounter        
        data[self.logFileName] = self.sensorMessage
        json_data = json.dumps(data)
        self.sensorMessage = []
        return json_data
    
    def stop(self):
        """
        halt flag is set and one last connect made locally
        in order get listen method out of loop 
        """
        self.halt = 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (config.getConfig().get(self.configSectionName, "Url"), config.getConfig().getint(self.configSectionName, "Port"))
        sock.connect(server_address)
        sock.close()
        
    def __initSocket(self):
        """
        The server socket is initialized
        """
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (config.getConfig().get(self.configSectionName, "Url"), config.getConfig().getint(self.configSectionName, "Port"))    
        print >>sys.stderr, "Server socket for incomming ", self.configSectionName, " data: starting up on %s port %s" % server_address
        sock.bind(server_address)   
        # Listen for incoming connections
        sock.listen(1)
        return sock
    
    def __initDBConnection(self):
        """
        Initializes mongoDB connection
        """
        dbSectionName = "MONGODB"
        __host = config.getConfig().get(dbSectionName, "Host")
        __port = config.getConfig().getint(dbSectionName, "Port")
        try: 
            client = MongoClient(host=__host, port=__port)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
            
        dbhost = client[config.getConfig().get(dbSectionName, "DBName")]
        #self.userCollection = dbhost[config.getConfig().get(dbSectionName, "UserCollection")]
        self.sensorCollection = dbhost[config.getConfig().get(self.configSectionName, "DBCollectionName")]
         
    def __writeToFile(self, data, mode):
        """ 
        Opens the file named logFileName in the specified @mode and writes the
        @data to it and closes the file.
    
        @param data (string): The data that will be written to the file
        @param mode (char): The mode to open the file
        """
        try:
            logFile = open(self.logFileName, mode)                        
            logFile.write(data)
        except IOError:
            print("Error while writing to file: ")
        finally:
            logFile.close()
            
    def __writeToDB(self, data):
        """
        Shapes the data for DB  and writes the shaped data combined with user information to the DB
        """
        #should be implemented for each sensor separately
        shapedDataDict = self.shapeDataForDB(data)
        
        #calculate relative time since the start of the session
        diff = shapedDataDict["timeStamp"] - self.userPropsDict["sessionStartTime"]
        self.userPropsDict["relativeTime"] = diff.total_seconds()
        
        #add user nd session related info infront of the sensor info
        #shapedDataDict.update(self.userPropsDict)
        concatedDict = OrderedDict(list(self.userPropsDict.items()) + list(shapedDataDict.items()))
        #save to DB
        self.sensorCollection.insert_one(concatedDict)
            
    def parseData(self, data):
        """
        Parses the data coming from the sensor
        If necessary each sensor should extend this class and implement this method separately
        """
        if config.getConfig().getboolean(self.configSectionName, "IsDataHasToBeParsed"):
            raise NotImplementedError("It seems that the data has to be parsed. Please override and implement parseData method!")
        else:
            raise NotImplementedError("It is declared that the data don\'t need to be parsed. Please check config file!")
            
    def shapeDataForDB(self, data):
        """
        Shapes the data coming form the sensor for DB
        Each sensor should extend this class and implement this method separately
        """
        raise NotImplementedError("The prepareDataForDB method should be overridden by every new sensor class inheriting Sensor class!")
        
    def createUserPropsDict(self):
        """
        Creates the user info dictionary
        """
        userPropsArr = []
        userPropsArr.append(("userName",sys.argv[1]))
        userPropsArr.append(("sessionStartTime", self.sessionStartTime))
        
        local_tz_name = datetime.now(tzlocal()).tzname()
        userPropsArr.append(("timeZoneName", local_tz_name))
        
        userPropsArr.append(("sessionID", sys.argv[1] + str(self.sessionStartTime)))
        
        userPropsArr.append(("relativeTime", 0))
        
        return OrderedDict(userPropsArr)
            