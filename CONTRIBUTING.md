# CONTRIBUTING

## How to add a new client
1. Generate a new client json file based on the `template.json` file in the `clients` folder. This file should be all lower case and named after the clients name. Requirements are below.
    * No spaces
    * All lower case
    * Ensure that ALL Itoc roles are added. We should deploy the `ItocReadOnly` where possible
    * For multi region accounts please specify the primary region
    * `roles` are an array even if there is only 1 role that we will assume
2. Create a PR to allow the build to run validating the configuration

## How to add a new account to an existing client
1. Open existing client file. 
2. Add new account to the list of accounts in the file.
3. Create a PR to allow the build to run validating the configuration
