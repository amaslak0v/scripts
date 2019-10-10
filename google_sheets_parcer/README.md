****
#### Script resources_parser.py executes following steps:


1. Downloads git@github.com:amaslakou/saas-app-deployment.git.
2. Parse files from to_check_folders value (list of folders), and gets metrics from all selected folders, and imports it to CSV.
3. Updates Google Sheet with metrics for all environments.

#### Requirements:
- python 3.7
- imported libs
- access to git@github.com:*maslakou/saas******.git (~/.ssh keys configured)
- client_secrets_service_account.json file.
    - Register in Google Cloud Platform and create project.
    - Create service account in GCP.(Place it in same folder as script, and rename as client_secrets_service_account.json)
    - Add API's in API's & Services tab in GCP - Google sheets API, Google Drive API
    - Create Google Spreadsheet, and add write access to created service account.