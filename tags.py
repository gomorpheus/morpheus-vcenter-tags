import requests
import sys


def get_session_id(username, password):
    session_headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json", 
        "vmware-use-header-authn": "test", 
        "vmware-api-session-id": "null"
        }
    session_response = requests.post(vcenter + '/rest/com/vmware/cis/session', headers=headers, auth=(username, password), verify=False)
    session_id = session_response.json()['value']
    return session_id


def get_tag_id(session_id, tagname):
    headers = {
        "Accept": "application/json", 
        "vmware-api-session-id": session_id
        }
    tag_response = requests.get(vcenter + '/rest/com/vmware/cis/tagging/tag', headers=headers, verify=False)

    for i in tag_response.json()['value']:
        tag_details = requests.get(vcenter + '/rest/com/vmware/cis/tagging/tag/id:' + i, headers=headers, verify=False)
        if tag_details.json()['value']['name'] == tagname:
            tag_id = tag_details.json()['value']['id']
        else:
            pass
    
    return tag_id

def get_vm_id(session_id, vmname):
    headers = {
        "Accept": "application/json", 
        "vmware-api-session-id": session_id
        }
    vm_response = requests.get(vcenter + '/rest/vcenter/vm', headers=headers, verify=False)
    for i in vm_response.json()['value']:
        if i['name'] == vmname:
            vm_id = i['vm']
        else:
            pass
    return vm_id


def create_tag_association(tag_id, vm_id, session_id):
    headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'vmware-api-session-id': session_id,
    }
    querystring = {"~action":"attach"}
    payload = {"object_id": {"id": "vm-40935", "type": "VirtualMachine"}}
    response = requests.post(vcenter + '/rest/com/vmware/cis/tagging/tag-association/id:' + tag_id, headers=headers, json=payload, params=querystring, verify=False)

    return response.text


if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    tagname = sys.argv[3]
    vcenter = sys.argv[4]
    vmname = sys.argv[5]
    session_id = get_session_id(username, password)
    tag_id = get_tag_id(session_id, tagname)
    vm_id = get_vm_id(session_id, vmname)
    create_tag_association(tag_id, vm_id, session_id)
