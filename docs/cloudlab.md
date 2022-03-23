## CloudLab setup

Links:

- https://groups.google.com/forum/#!forum/cloudlab-users
- [CloudLab - Show Profile](https://www.cloudlab.us/show-profile.php?uuid=bdca59db-aa6a-11e9-8677-e4434b2381fc)
- [CloudLab - Login](https://www.cloudlab.us/user-dashboard.php)
- 

You need the `portal-tools` python package:

```
git -c http.sslVerify=false clone  \
   https://gitlab.flux.utah.edu/stoller/portal-tools.git 

pushd portal-tools 
python3 setup.py install --user 
popd 
rm -Rf portal-tools
```

Login into the [CloudLab Portal](https://www.cloudlab.us/login.php)

## Generate ssh key

Generate an ssh key:

```
if [ ! -f ~/.ssh/id_nsdf ] ; then
  ssh-keygen -t rsa -f ~/.ssh/id_nsdf -N ""
fi
```

Go to [Manage SSH keys](https://www.cloudlab.us/ssh-keys.php) and add your `id_nsdf.pub` key content.

## Download PEM file

Click on your username and *download credentials*; you should get a `cloudlab.pem` file that you need to add to your `~/.ssh` directory.

To remove the passphrase from the PEM  file (this is needed from programmatically creation of VMs):

```
pushd ~/.ssh
mv cloudlab.pem cloudlab.pem.source

# this is the private key
openssl rsa  -in cloudlab.pem.source >  cloudlab.pem 
# *** ENTER your CloudLab password ***

# this is the certificate (APPEND mode)
openssl x509 -in cloudlab.pem.source >> cloudlab.pem 

popd
```

## Create new profile

Create a new profile with name `nsdf-profile`:

```
"""NSDF Variable number of nodes in a lan. . 

Instructions:
see http://docs.cloudlab.us/
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab
from geni.rspec.igext import AddressPool

pc = portal.Context()
request = pc.makeRequestRSpec()


pc.defineParameter("nodeCount", "Number of Nodes", portal.ParameterType.INTEGER, 4,longDescription="If you specify more then one node, we will create a lan for you.")
params = pc.bindParameters()
pc.verifyParameters()

nodeCount=params.nodeCount

lan = request.LAN("lan")

# Request 1 routable ip addresses for MetalLB
addressPool = AddressPool('addressPool', int(1))
request.addResource(addressPool)

for I in range(nodeCount):
    name = "node{}".format(I+1)
    node = request.RawPC(name) # request.XenVM(name)
    node.component_manager_id = "urn:publicid:IDN+utah.cloudlab.us+authority+cm"
    node.hardware_type="m400" # 8 cores at 2.4Ghz 6 GB Ram, 120GB SATA3

    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD"
    iface = node.addInterface("eth1")

    # this breaks ssh -i ...?
    #iface.addAddress(pg.IPv4Address( "192.168.1.{}".format(I+1), "255.255.255.0"))

    lan.addInterface(iface)

    bs = node.Blockstore(name + "-bs", "/mnt/data")
    bs.size = "100GB"

pc.printRequestRSpec(request)
```

## Update your vault file

Add one item to your `~/.nsdf/vault/vault.yml` file (change values as needed; for example you may need to change the `project-name`, `profile-name`,`ssh-username`):

```
ec2-cloudlab:
  class: CloudLabEc2
  cloud-url: https://cloudlab.us/
  certificate: ~/.ssh/cloudlab.pem
  project-name: nsdf-testbed
  profile-name: nsdf-profile
  num: 1
  ssh-username: scorzell
  ssh-key-filename: ~/.ssh/id_nsdf
```

# Examples

Create new nodes`:

```
alias nsdf-cloud="python3 -m nsdf-cloud"

ACCOUNT=ec2-cloudlab
nsdf-cloud $ACCOUNT create nodes test1 --num 1 
```

List of nodes:

```
nsdf-cloud $ACCOUNT get nodes test1 
```

Extend lease of nodes:

```
nsdf-cloud $ACCOUNT extend nodes test1 
```

Delete nodes:

```
nsdf-cloud $ACCOUNT delete nodes test1 
```