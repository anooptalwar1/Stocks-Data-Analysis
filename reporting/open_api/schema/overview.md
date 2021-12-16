# Overview
SDA (Stock Data Analytics) 


# Authentication
SDA supports JWT based authentication programmatic access to APIs. 
Custom authentication has been used where user has to call first the /api/reporting/login and enter username and password sent in the form of json in body.
User will receive access_token as a response, refresh_token and CSRF Cookie will be received alongside.
While performing an api call user is required to send access_token and CSRF token(X-CSRFTOKEN) in headers for token validation specially for post request

# Authorization
AUTHORIZATION_PLACEHOLDER
