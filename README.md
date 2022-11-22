# List Signatures

## Introduction
Quick example python to spin thru a BIG-IP and pull the Policy ID(s)

Then it iterates thru the results and shows the signatures and their Blocking state.

This has no real error handling - like if the password is not right or if the policy list is empty...


## Added a couple new files:

policychangedetails.py - Outputs the last change of the selected policy
policyauditdetails.py - Pulls the audit log for the selected policy/policies

## November 22, 2022
Added a call to the signature data in the loop ... note that this greatly increases the run time since we need to call them each time.  Might be good to have the Whole Signature DB pulled and then use a JSON query to get it but for now, this works as a Proof of Concept

