# This is a simple/manual example of how to use 3-legged oauth2 approach for the following:
# 1. Have a user authenticate on Indeed's identity servers.
# 2. Process redirect url with authorization code query parameter.
# 3. Exchange the authorization code for Indeed API OAuth token.
# 4. Make a simple API call and print the response to the console.

from requests_oauthlib import OAuth2Session

# App registration id and secret. These are provided by Indeed once you register your app.
client_id = "get-this-from-indeed"
client_secret = "get-this-from-indeed"

# URLs
# This can be any URL in practice, you don't even have to be the owners/host/anything but 
# idealy this would point back to a route/endpoint on your web application which could then 
# programatically parse the URL query parameters, i.e. the authorization code.
redirect_url = "send-users-here-after-authenticating"
# This URL points to the identity service from Indeed. This is found in the Indeed API 
# documentation.
authorization_base_url = "https://secure.indeed.com/oauth/v2/authorize"
# Once the redirect returns with the authorization code, use that with this endpoint to 
# exchange it for an OAuth token. This is found in the Indeed documentation.
token_request_url = "https://apis.indeed.com/oauth/v2/tokens"
# This is a protected resource on the Indeed API. This is found in the Indeed documentation
user_info_endpoint = "https://secure.indeed.com/v2/api/userinfo"

# Program
# Step 0: Create oauthlib-requests session object. You can read more about this object wrapper here
# https://requests-oauthlib.readthedocs.io/en/latest/api.html?highlight=session%20object%5C#oauth-2-0-session
# and here 
# http://man.hubwiz.com/docset/Requests.docset/Contents/Resources/Documents/user/advanced.html?highlight=session#session-objects
session = OAuth2Session(client_id, redirect_uri=redirect_url)

# Step 1: Form the authorization URL
authorization_url = session.authorization_url(authorization_base_url)

# Step 2: Send the user to Indeed's identity servers using authorization url
print(f"Send the user to Indeed by clicking this link: {authorization_url}")

# Step 3: Process the redirect url to extract OAuth token
redirect_response = input("Paste the full redirect URL here:")
token = session.fetch_token(
    token_url=token_request_url,
    client_id=client_id,
    client_secret=client_secret,
    authorization_response=redirect_response
    )

# Step 4: Make a request for a protected resource
response = session.get(user_info_endpoint)
if response.ok:
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    print("\nResponse from Indeed Request:\n{}".format("-"*30,))
    pp.pprint(response.json())
else:
    print(f"response returned error {response.status_code}: {response.reason}")
    