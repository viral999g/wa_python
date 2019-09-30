<h1>Python Profile Management</h1>

<b>Socket url : </b> ws://localhost:9011/ <br>
<b>Profiles folder : </b> ./Profiles/ (No need to create it)<br> 
<b>Profiles list file : </b> ./profiles.txt (No need to create it)<br> 

<h2>Socket messages :</h2>

<h3>1: Create/Open profile</h3>
<b>Send : </b> ["create_profile", url_to_open , profile_id (String)] (Stringify)
Python will create a profile in the folder 'Profiles' of the current directory if not created before and open the url.

<h3>2: Update status of a single profile</h3>
<b>Send from that profile: </b> ["Presence", mobile_no, profile_id, status (0 = Offline, 1= Online)] (Stringify)
Python will update the 'profile.txt' file and send the status update to the dashboard if it's connected with timestamp like this [mobile_no, profile_id, status, ts].

<h3>3: Get users list</h3>
<b>Send from that profile: </b> ["get_user_list", url (To check the status of all the profiles)] (Stringify)
Python will send the list of profiles and its info from the file 'profiles.txt'. Python will also start all the profiles with the url given to initiate status update and keep all the profiles open for 1 minute. All the profiles will send the status update using 2nd form of socket message and update the dashboard about the status and also update the file.
<br><br><br>

<p>* Please change the command to open google-chrome in function create_profile() and open_all_profiles() according to your OS *</p>
