# NSDF-cloud

This repository contains examples of how to create Virtual Machines on the cloud.

Another approach would be to use *Ansible Playbooks* that already have some support to popular clouds, but we found that, in certain cases, this process was missing the necessary advanced customization (like for example allocate an extra public IP for the load balancer) or was not fully supporting full and reliable resource deletion.

## Supported clouds

List:

* Amazon Web Services [Setup](./docs/aws.md)
* Chameleon Cloud [Setup](./docs/chameleon.md)
* CloudLab[ Setup](./docs/cloudlab.md)
* Vultr [Setup](./docs/vultr.md)
* *more to come soon*

# What to do next

Items:

* [ ] Enable XSede
  - [ ] JetStream TACC
  - [ ] JetStream Indiana
* [ ] Enable IBM Cloud
- [ ] Enable Google Cloud
- [ ] Enable Azure Cloud
* [ ] Automatic creation of experiment on CloudLab
* [ ] Create a "story" about big and distributed "cluster" with VMs coming from different cloud solutions (both commercial and educational)
  - [ ] For example we could create 50 VMs on several cluster, install kubernetes on it, then JupyterHub and, via a geographical-aware DNS, redirect people to the nearest NSDF cluster

# Python requirements

Install the following Python packages:

```
# update PIP
python3 -m pip install --upgrade pip

# install some python packages
python3 -m pip install \
   setuptools \
    textwrap3 \
    bs4 \
    lxml \
    boto3 \
    vultr \
    python-chi \
    bs4
```

# Security checks



```
python3 -m pip install install truffleHog
trufflehog ./
```