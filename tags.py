import requests
import argparse


def get_session_id(vcenter, username, password):
    session_headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json", 
        "vmware-use-header-authn": "test", 
        "vmware-api-session-id": "null"
        }
    session_response = requests.post(vcenter + '/rest/com/vmware/cis/session', headers=session_headers, auth=(username, password), verify=False)
    session_id = session_response.json()['value']
    print 'session response: ' + session_response.text
    return session_id


def get_tag_id(vcenter, session_id, tagname):
    headers = {
        "Accept": "application/json", 
        "vmware-api-session-id": session_id
        }
    tag_response = requests.get(vcenter + '/rest/com/vmware/cis/tagging/tag', headers=headers, verify=False)
    print 'tag_response: ' + tag_response.text

    for i in tag_response.json()['value']:
        tag_details = requests.get(vcenter + '/rest/com/vmware/cis/tagging/tag/id:' + i, headers=headers, verify=False)
        print 'tag_details: ' + tag_details.text
        if tag_details.json()['value']['name'] == tagname:
            tag_id = tag_details.json()['value']['id']
        else:
            pass
    
    return tag_id

def get_vm_id(vcenter, session_id, vmname):
    headers = {
        "Accept": "application/json", 
        "vmware-api-session-id": session_id
        }
    vm_response = requests.get(vcenter + '/rest/vcenter/vm', headers=headers, verify=False)
    print 'vm_response: ' + vm_response.text
    for i in vm_response.json()['value']:
        if i['name'] == vmname:
            vm_id = i['vm']
        else:
            pass
    return vm_id


def create_tag_association(vcenter, tag_id, vm_id, session_id):
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'vmware-api-session-id': session_id,
        }
    querystring = {"~action":"attach"}
    payload = {"object_id": {"id": vm_id, "type": "VirtualMachine"}}
    response = requests.post(vcenter + '/rest/com/vmware/cis/tagging/tag-association/id:' + tag_id, headers=headers, json=payload, params=querystring, verify=False)
    print 'create tag response: ' + response.text
    return response.text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script that takes in VCenter credentials, a VM name, a tag name (must exist) and associates the tag with the VM.')
    parser.add_argument(
        '-u',
        '--username',
        default='administrator',
        help='provide a VCenter username'
    )

    parser.add_argument(
        '-p',
        '--password',
        default='password',
        help='provide a VCenter password'
    )

    parser.add_argument(
        '-t',
        '--tagname',
        default='administrator',
        help='provide a VCenter username'
    )

    parser.add_argument(
        '-vc',
        '--vcenter',
        default='https://vcenter.local',
        help='provide a VCenter URL'
    )

    parser.add_argument(
        '-vm',
        '--vmname',
        default='example',
        help='provide a Virtual Machine Name'
    )
    parsed = parser.parse_args()
    username = parsed.username
    
    session_id = get_session_id(parsed.vcenter, parsed.username, parsed.password)
    tag_id = get_tag_id(parsed.vcenter, session_id, parsed.tagname)
    vm_id = get_vm_id(parsed.vcenter, session_id, parsed.vmname)
    create_tag_association(parsed.vcenter, tag_id, vm_id, session_id)
