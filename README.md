Quick example python to spin thru a BIG-IP and pull the Policy ID(s)

Then it iterates thru the results and shows the signatures and their Blocking state.

This has no real error handling - like if the password is not right or if the policy list is empty...

Added a couple new files:

policychangedetails.py - Outputs the last change of the selected policy
policyauditdetails.py - Pulls the audit log for the selected policy/policies
