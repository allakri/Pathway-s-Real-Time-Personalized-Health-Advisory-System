from pathway import Pathway
from google.oauth2.service_account import Credentials

# Path to your service account JSON key
SERVICE_ACCOUNT_FILE = 'path/to/your/credentials.json'

# Authenticate using the service account credentials
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

# Initialize Pathway with the credentials
pathway = Pathway(credentials)

# Example to read from Google Drive (use the shared object ID)
# Replace object_id with the ID of the file or folder you want to interact with
object_id = "YOUR_SHARED_OBJECT_ID"

# Reading from Google Drive
table = pathway.io.gdrive.read(
    object_id=object_id,
    service_user_credentials_file=SERVICE_ACCOUNT_FILE
)

# Execute the pathway
pathway.run()

