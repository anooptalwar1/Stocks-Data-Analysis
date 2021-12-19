# Overview
SDA (Stock Data Analytics) 


# Authentication
SDA supports JWT based authentication programmatic access to APIs. 
Auuthentication and authorization has been handled through a custom middleware where user has to call first the /api/reporting/login, send username and password sent in the form of json in body.
User will receive access_token as a response, refresh_token and CSRF token will be received as cookie.
While performing an api call user is required to send access_token and CSRF token(X-CSRFTOKEN) in headers for token validation specially for post request.


# Authorization
Post user authentication, authorization check will be followed in same login call. Custom decorator @has_permission checks for the current roles and permissions assigned to a user.
For frontend to view/handle user permissions at UI level, frontend can call 'api/reporting/users/me' API call

AUTHORIZATION_PLACEHOLDER
