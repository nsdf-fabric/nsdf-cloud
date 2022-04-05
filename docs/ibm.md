# IbmCloud setup

Links:

- https://github.com/IBM-Cloud/ibm-cloud-cli-release/issues/57


TODO...

### Prerequisites

install ibmcloudcli


### Credential Setup up in Vendor IAM & SSH Keys




## NSDF-Cloud Example: Create, List, Delete

Create new nodes:

```
alias nsdf-cloud="python3 -m nsdf-cloud"

ACCOUNT=TODO
nsdf-cloud $ACCOUNT create nodes test1 --num 1 
```

List of nodes:

```
nsdf-cloud $ACCOUNT get nodes test1 

# to get all nodes remove `test1`
```

Delete nodes:

```
nsdf-cloud $ACCOUNT delete nodes test1 

# to delete all nodes remove `test1`
```



### Other Useful with Vendor Tools
