# mvc
Installed packages------------
conda install -c cogsci pygame


Preperation:

1. Connect tobii eyetracker sensor
2. Run tobii eyetracker dotnet app.
3. 
5. Press OK button 
6. Have following fields in config:
    [MONGODB]
    Host = localhost
    Port = 27017
    DBName = mediaExposureTry


7. Edit ActionUnit.py file according to needs(Necessary info can be found in the script file)
If not edited following actions will be observed.

Run:
1. Run the Mvc.py file through command line
    *by pressing 'Alt+D' in the folder
    *type 'cmd' in the selected folder path
    *python Mvc.py
2. Enter the username (for ex: evina)
3. Press the start button through exposuremeter
4. Observe sessionStarttime is displayed on the console
5. Observe "Message is first" is displayed on the console at first second (timeActionUnit)
6. Fill the pop up pre questionnaire (timeActionUnit)
7. Close the pre questionnaire window
8. Observe "Message is second" is displayed on the console at third second (timeActionUnit)
9. Press Stop button
10.Observe "Message is the session is going to be stopped." is displayed on the console (eventActionUnit)
11. Fill the pop up post questionnaire
12. Close the post questionnaire window
13. Close the exposuremeter app.