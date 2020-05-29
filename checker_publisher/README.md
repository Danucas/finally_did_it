### Checker Publisher Django APP

### Apps

#### Publisher

Handles web static serving and REST API functions, is used to control user intranet requests and to store user credentials and media posting

##### Models

###### Channel

This model stores the Twitter API credentials to be used at posting your checker results to Social Media

###### Sended

This model stores all posting records for each user

#### Javascript files

[forms.js](static/scripts/forms.js)
Set listeners to the project requests flow:
- search a project by id
- get a task
- run check for that task

[init.js](static/scripts/init.js)
Set body height as the bar height

[popup.js](static/scripts/popup.js)
Sets the back, close and hidde behaviors

[save_corrections.js](static/scripts/save_corrections.js)
Draw the checker results in canvas and the send the base64 string to the server to be uploaded to twitter and the posted with the customized message

[scroll.js](static/scripts/scroll.js)
Mantain the right column at the top allways

[user.js](static/scripts/user.js)
Handle user authentication