# morpheus-vcenter-tags

## about

This is a python wrapper script for the VCenter API that allows the association of tags to a Virtual Machine in VSphere.

## usage

Example:

```text
slimshady@localhost:~# python tags.py -u admin -p password -t mytag -vc https://vsphere.local -vm sas.prod.local
```

```text
slimshady@localhost:~# python tags.py -h
usage: tags.py [-h] [-u USERNAME] [-p PASSWORD] [-t TAGNAME] [-vc VCENTER]
               [-vm VMNAME]

Script that takes in VCenter credentials, a VM name, a tag name (must exist)
and associates the tag with the VM.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        provide a VCenter username
  -p PASSWORD, --password PASSWORD
                        provide a VCenter password
  -t TAGNAME, --tagname TAGNAME
                        provide a VCenter username
  -vc VCENTER, --vcenter VCENTER
                        provide a VCenter URL
  -vm VMNAME, --vmname VMNAME
                        provide a Virtual Machine Name
```
