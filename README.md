# azure-audit

These basic scripts audit the following information from your Azure environment

- All active users (note: the 'jobTitle' field must be present). For me in my environment I only need to audit active users and this filters out test users / others. Modify line 15 of user_list.py as necessary.

- All devices within Defender ATP and their onboarding status.

- All devices with their encryption state.

- All directory roles with their members. Any role without a member is omitted. This is set on line 14 of directory_roles.py.

## Requirements

1. Clone repository to desired location

2. Create your virtual environment and install 'requirements.txt' with `pip install -r /path-to-requirements.txt`

3. Create an App Registration within Auzre. Use the 'Desktop Application' option. Reference [here](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app "here")
	- The following API permissions are used:
	
		- BitlockerKey.ReadBasic.All (Application)
		- Device.Read.All (Application)
		- DeviceManagementConfiguration.Read.All (Application)
		- Directory.Read.All (Application)
		- User.Read.All (Application)
		- Machine.Read.All (Application)


4. Create your .env with the following:
	
	1. AZURE_CLIENT_ID
	2. AZURE_TENANT_ID
	3. AZURE_CLIENT_SECRET
	
5. Run main.py - multiple csv files will be placed in the project root directory


#### Current TODOs
NONE

### Recent TODOs Finished
1. Added Pagination
