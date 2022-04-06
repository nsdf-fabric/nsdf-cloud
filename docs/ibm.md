# IBM Cloud setup

Links:

- https://www.ibm.com/cloud/cli
- https://github.com/IBM-Cloud/ibm-cloud-cli-release/issues/57
- https://cloud.ibm.com/docs/vpc?topic=vpc-infrastructure-cli-plugin-vpc-reference


TODO...

### Prerequisites

Follow the installation instructions for IBM Cloud CLI from https://www.ibm.com/cloud/cli

```
ibmcloud login
```

```
ibmcloud plugin install vpc-infrastructure
```

The "vpc-infrastructure" plugin adds the is subcommand which allows to control VPC resources.

E.g., to list instances use:
```
ibmcloud si instances
```


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
