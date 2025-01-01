from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

# Replace this with the correct path to your downloaded Secure Connect Bundle
cloud_config = {
    'secure_connect_bundle': r'C:\proj\astra\secure-connect-social-media-engagement.zip'  # Make sure to use raw string (r'') to handle the backslashes correctly
}

# Replace this with the correct path to your Application Token JSON file
with open(r"C:\proj\astra\Social_Media_Engagement-token.json") as f:  # Correct file path for the token JSON
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# Test the connection and fetch the release version from Cassandra
row = session.execute("SELECT release_version FROM system.local").one()
if row:
    print(row[0])  # This will print the database version if the connection works
else:
    print("An error occurred.")

rows = session.execute("SELECT * FROM social_data.posts LIMIT 10")

for row in rows:
    print(row)
