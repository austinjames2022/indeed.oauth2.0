# This is a simple/manual example of how to connect to Indeeds API:
# 1. Have a user authenticate on Indeed's identity servers.
# 2. Copy authorization code from redirect url.
# 3. Exchange the authorization code for Indeed API OAuth token.
# 4. Make a simple API call and print the response to the console.

from requests_oauthlib import OAuth2Session

# Our application's credentials. Indeed provides these after app is registered
client_id = "get-this-from-indeed"
client_secret = "get-this-from-indeed"

# Our application's redirect url
redirect_url = "send-users-here-after-authenticating"

# Indeed identity verification
authorization_base_url = "https://secure.indeed.com/oauth/v2/authorize"

# Exchange authorization code for token Indeed API endpoint
token_request_url = "https://apis.indeed.com/oauth/v2/tokens"

# Protected Indeed API endpoint
user_info_endpoint = "https://secure.indeed.com/v2/api/userinfo"

# Use requests-oauthlib to create an OAuth2Session object
session = OAuth2Session(client_id, redirect_uri=redirect_url)

# Use requests-oauthlib to create the authorization link
authorization_url = session.authorization_url(authorization_base_url)

# Follow link to verify identity with Indeed
print(f"Send the user to Indeed by clicking this link: {authorization_url}")

# Parse redirect url
redirect_response = input("Paste the full redirect URL here:")

# Create OAuth2 token via fetch_token method, see requests-oauthlib docs for more info
token = session.fetch_token(
    token_url=token_request_url,
    client_id=client_id,
    client_secret=client_secret,
    authorization_response=redirect_response
    )

# Make an HTTP request to a protected resource
response = session.get(user_info_endpoint)

# Use conditional to print response or error message
if response.ok:
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    print("\nResponse from Indeed Request:\n{}".format("-"*30,))
    pp.pprint(response.json())
else:
    print(f"response returned error {response.status_code}: {response.reason}")
    