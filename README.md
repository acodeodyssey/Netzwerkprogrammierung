# Tusc
<h2> Netzwerkprogrammierung Abschlussprojekt </h2>
<h3> Overview </h3>
<h4>Tusc, short for Thin update scraper...</h4>
  This CLI-Application is designed for package-management of Thin-Clients. It's easy to use und doesn't come with any unwanted or       bloated features. At the Start of the programm it connects to an available server. Everything after the login is interactive.

<h3> Usage </h3>
<h4> Installation </h4>
Requiered: Python 3.6
Clone the repo and you are good to go, no need of installing any packages with pip.
<h4> Start a local server </h4>
Navigate to server in the repository und run in console:

    python server.py

<h5> Commands </h5>
List all connected Clients

    list

 
Show Client by Id

    show -the client id-
    
  In case you forget one of the commands
  

    help
If you want to kill it
 

    quit

<h4> Using the client </h4>
  Navigate to tusc/tusc in the repository und run in the console:
  

    python tusc.py

<h5> Commands </h5>
Update a specific package. If you misspelled the package nothing will happen
  

    update -name of package-
Upgrade every package, and install those you don't have
  

    upgrade
To exit the application just type
  

    quit

<h3> Upcoming Features </h3>
 

 - Configuration File to specify fallback-servers to minimize load on
   servers in working environment.   
 - Server Ui with great Diagrams etc    to visiualize the behaviour of
   clients

<h4> Security </h4>
  

 - Ssl encryption of communication between server and client

  

 - Checksum to validate packages
