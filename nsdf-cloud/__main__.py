
import os,sys,logging,json,types
from distutils.command.check import check
from pprint import pprint,pformat

from .utils import *

# all the automation classes here
from .aws       import AmazonEC2
from .chameleon import ChameleonEC2
from .cloudlab  import CloudLabEc2
from .vultr      import VultrEc2
from .jetstream  import JetStreamEc2

# //////////////////////////////////////////////////////////////
def CreateAnsibleInventory(filename,nodes):

	logging.info(f"Creating ansible inventory {filename}")

	
	username=nodes[0]["ssh-username"]
	key_filename=nodes[0]["ssh-key-filename"]	
	hosts=[it['public_ip'] for it in nodes if it.get('type','node')=='node']

	with open(filename,'w') as f:
		f.write('\n'.join(
			hosts+
			[
			"",
			"[all:vars]",
			"ansible_connection=ssh",
			f"ansible_user={username}",
			f"ansible_ssh_private_key_file={key_filename}",
			"ansible_ssh_extra_args='-o StrictHostKeyChecking=no",
		]))
		f.write('\n')

# //////////////////////////////////////////////////////////////
def main(args):

	if not args:
		return

	# setup the logging
	logging.basicConfig(
		format='%(asctime)s %(levelname)-6s [%(filename)-12s:%(lineno)-3d] %(message)s',
		datefmt='%Y-%m-%d:%H:%M:%S',level=logging.INFO)

	target=args[0]
	args=args[1:]

	# in the ~/.nsdf/vault/vault.yml file there should be an item with the $TARGET name
	config=GetConfig(target)

	# override by command line
	# example --region us-east-1
	I=0
	while I< len(args)-1:
		if args[I].startswith("--"):
			key,value=args[I][2:].strip(),args[I+1].strip()
			logging.info(f"Adding to config {key}={value}")
			config[key]=value
			I+=2
		else:
			I+=1

	# dangerous
	# logging.info(f"Current config:\n{pformat(config)}")

	# create the class to automatically create VMs
	Class=config.pop("class")
	logging.info(f"Class is {Class}")
	instance=eval(f"{Class}(config)")

	# createNodes
	if len(args)>1 and args[0]=="create" and args[1]=="nodes":
		ret=instance.createNodes(args[2:])
		CreateAnsibleInventory(f"ansible-inventory.{args[2]}.ini",ret)

	# getNodes
	elif len(args)>1 and args[0]=="get" and args[1]=="nodes":
		ret=instance.getNodes(args[2:])
		CreateAnsibleInventory(f"ansible-inventory.{args[2]}.ini",ret)

	# deleteNodes
	elif len(args)>1 and args[0]=="delete" and args[1]=="nodes":
		ret=instance.deleteNodes(args[2:])

	# two arguments. Example: "get nodes" will call Class.getNodes(...)
	if len(args)>1 and hasattr(instance,f"{args[0]}{args[1].title()}"):
		ret=eval(f"instance.{args[0]}{args[1].title()}(args[2:])")
	
	# one argument. Example "list" will call Class.list(...)
	else:
		ret=eval(f"instance.{args[0]}(args[1:])")

	# if the return type is a generator, transform it into a python list
	ret=list(ret) if isinstance(ret, types.GeneratorType) else ret
	return ret

# //////////////////////////////////////////////////////////////
if __name__=="__main__":
	pprint(main(sys.argv[1:]))
