# Chameleon setup

Links:

- [https://chi.uc.chameleoncloud.org/](https://chi.uc.chameleoncloud.org/)
- [https://chi.tacc.chameleoncloud.org](https://chi.tacc.chameleoncloud.org/)

Generate an ssh key:

```
if [ ! -f ~/.ssh/id_nsdf ] ; then
  ssh-keygen -t rsa -f ~/.ssh/id_nsdf -N ""
fi
```

 and import the public key to:

- https://chi.uc.chameleoncloud.org/project/key_pairs
- https://chi.tacc.chameleoncloud.org/project/key_pairs

with the folloing values:

- Key pair name: `id_nsdf`

- Key type: `SSH key`

- Public key: *paste the content of ~/.ssh/id_nsdf.pub*

## Update your vault file

Then add some items to your `~/.nsdf/vault/vault.yml` file (change values as needed; for example you may need to change `OS_PROJECT_ID`, `OS_PROJECT_NAME`, `OS_USERNAME`, `OS_PASSWORD`):

```
ec2-chameleon-tacc:
  description: chameleon computing service
  resources: many Service Unit (SU)
  class: ChameleonEC2
  cloud-url: https://chi.tacc.chameleoncloud.org
  node-type: compute_haswell
  num: 1
  image-name: 'CC-Ubuntu20.04'
  network-name: 'sharednet1'
  lease-days: 7
  env:
    OS_AUTH_URL: https://chi.tacc.chameleoncloud.org:5000/v3
    OS_INTERFACE: public
    OS_PROTOCOL: openid
    OS_IDENTITY_PROVIDER: chameleon
    OS_DISCOVERY_ENDPOINT: https://auth.chameleoncloud.org/auth/realms/chameleon/.well-known/openid-configuration
    OS_CLIENT_ID: keystone-tacc-prod
    OS_ACCESS_TOKEN_TYPE: access_token
    OS_CLIENT_SECRET: none
    OS_REGION_NAME: CHI@TACC
    OS_PROJECT_DOMAIN_NAME: chameleon
    OS_AUTH_TYPE: v3oidcpassword
    OS_PROJECT_ID: 2c45428ad4584b52b336ba4ac62472fb
    OS_PROJECT_NAME: CHI-210923
    OS_USERNAME: XXXXX@YYYYY.edu
    OS_PASSWORD: ZZZZZ
  ssh-key-name: id_nsdf
  ssh-key-filename: ~/.ssh/id_nsdf
  ssh-username: cc

ec2-chameleon-uc:
  class: ChameleonEC2
  node-type: compute_skylake
  num: 1
  image-name: 'CC-Ubuntu20.04'
  network-name: 'sharednet1'
  lease-days: 7
  env:
    OS_AUTH_URL: https://chi.uc.chameleoncloud.org:5000/v3
    OS_INTERFACE: public
    OS_PROTOCOL: openid
    OS_IDENTITY_PROVIDER: chameleon
    OS_DISCOVERY_ENDPOINT: https://auth.chameleoncloud.org/auth/realms/chameleon/.well-known/openid-configuration
    OS_CLIENT_ID: keystone-uc-prod
    OS_ACCESS_TOKEN_TYPE: access_token
    OS_CLIENT_SECRET: none
    OS_REGION_NAME: CHI@UC
    OS_PROJECT_DOMAIN_NAME: chameleon
    OS_AUTH_TYPE: v3oidcpassword
    OS_PROJECT_ID: 1b52ee31654449d589f010446827f89c
    OS_PROJECT_NAME: CHI-210923
    OS_USERNAME: XXXXX@YYYYY.edu
    OS_PASSWORD: ZZZZZZ
  ssh-key-name: id_nsdf
  ssh-key-filename: ~/.ssh/id_nsdf
  ssh-username: cc
```

Note: using *token credentials* does not work as confirmed by the Chameleon help center . The only work around is t use clear username/password that can be changed here [Log in to Chameleon](https://auth.chameleoncloud.org/auth/realms/chameleon/account/password) This seems to be related to some problems of the `python-chi` package.

## Examples

Create new nodes, for example on `ec2-chameleon-tacc`:

```
alias nsdf-cloud="python3 -m nsdf-cloud"


ACCOUNT=ec2-chameleon-tacc
nsdf-cloud $ACCOUNT create nodes test1 \
  --num 1 \
  --node-type compute_haswell
```

> You could get the *NOT_ENOUGH_RESOURCES* error message. Python code will retry to get the lease.

List of nodes:

```
nsdf-cloud $ACCOUNT get nodes test1 
```

Delete nodes:

```
nsdf-cloud $ACCOUNT delete nodes test1 
```
