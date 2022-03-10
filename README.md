# azure-audit

These basic scripts audit the following information from your Azure environment

- All active users (note: the 'jobTitle' field must be present). For me in my environment I only need to audit active users and this filters out test users / others. Modify line 66 as necessary.

- All devices within Defender ATP and their onboarding status.

- All devices with their encryption state.

- All directory roles with their members. Any role without a member is omitted. This is set on line 27.

## Requirements

1. Clone repository to desired location

2. Create your virtual environment and install 'requirements.txt' with `pip install -r /path-to-requirements.txt`

3. Create an App Registration within Auzre. Use the 'Desktop Application' option. Reference [here](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app "here")
	- The following API permissions are used:
	
		- BitlockerKey.ReadBasic.All (Delegated)
		- Device.Read.All (Delegated)
		- DeviceManagementConfiguration.Read.All (Delegated)
		- Directory.Read.All (Delegated)
		- Directory.Read.All (Application)
		- User.Read (Delegated)
		- User.Read.All (Delegated)
		- Machine.Read.All (Application)


4. Create your .env with the following:
	
	1. SECRET (Application secret)
	2. TENANTID (Tenant ID of your Azure tenant)
	3. APPID (Application ID for your Registered Application)
	
5. Run main.py - multiple csv files will be placed in the project root directory


#### Current TODOs
1. Use Graph API pagination instead of 'top' call. Currently will only grab top 999 users.
