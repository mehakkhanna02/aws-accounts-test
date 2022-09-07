# Welcome to Itoc AWS Account Configuration 
# [CLICK HERE FOR LATEST CONFIG FILES]( https://github.com/itoc/aws-accounts/releases/tag/latest)
This repository is designed to hold all AWS accounts that Itoc works on.


This repository uses branch protection to ensure you use signed commits and requires the build to pass. [Setting up signed commits](https://wiki.aws.itoc.com.au/xwiki/bin/view/Managed%20Services/Standard%20Processes/GitHub%20-%20Using%20GPG%20and%20SSH/)

## How this repository works
This repository takes the client configuration from the `clients` directory and generates a consistent CLI and Browser configuration.
The `build.py` file also applies some validation to ensure that we have consistency across the profiles. 
The latest build will have artifacts that has the resultant configurations included.

## Notes for client configuration
* All account names are lower case
* If you are specifying a role outside our `ItocBilling`, `ItocReadOnly`, `ItocAdmin` roles please add a color by adding the following line to the `roles` dictionary. `"the_nonstandard_rolename": {"color": "000000"}`
* If the client normally uses a region not `ap-southeast-2` please add a region line to the account definition eg `"region": "us-east-1",` NOTE: You can only specify 1 region per account. If you need to use multiple regions please use the region switcher or duplicate the account object.
* If the role contains `admin` in the name we add `!` to the end to ensure the browser plugin won't auto assume that role

