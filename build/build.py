import json
import configparser
import os
import csv

from atlassian import Confluence

cli_config = configparser.ConfigParser()
browser_config = configparser.ConfigParser()
csv_config = []
html_config = [
    '<table>',
    '<tr><td>Client Name</td><td>Account Name</td><td>Account ID</td><td>Role Name</td></tr>'
]

errors = []

def generate_client(client_name):
    global has_errors

    if client_name != client_name.lower():
        errors.append(f'{client_name} should be lower')
    
    print('')
    print(f'CLIENT: {client_name}')

    with open(f'clients/{client_name}.json') as f:
        data = json.load(f)
        accounts = data["accounts"]
        data['roles']['ItocBilling'] = {"color": "0000cc"}
        data['roles']['ItocReadOnly'] = {"color": "008a70"}
        data['roles']['ItocReadOnlyAccess'] = {"color": "008a70"}
        data['roles']['ItocAdmin'] = {"color": "ff2600"}
        data['roles']['ITOCAccountAccess'] = {"color": "ff2600"}
        data['roles']['ItocAccountAccess'] = {"color": "ff2600"}
        data['roles']['ItocAdminAccess'] = {"color": "ff2600"}
        for account_name in accounts.keys():
            if account_name != account_name.lower():
                errors.append(f'{client_name}\'s account named {account_name} should be lower')
            if " " in account_name:
                errors.append(f'{client_name}\'s account named {account_name} should not include a space')
            
            print(f'ACCOUNT NAME: {account_name}')
            account = accounts[account_name]
            account_id = account['account_id']
            if " " in account_id or account_id.isnumeric() == False:
                errors.append(f'{client_name}\'s account named {account_name}\'s account should not include a space and be a number')

            for role in account['roles']:
                print(f'ROLE: {role}')
                region = account['region'] if 'region' in account else 'ap-southeast-2'
                
                if not isinstance(region, str):
                    errors.append(f'{client_name} - {account_name} - {role} has an incorrect region that isn\'t a string')
                    return

                if not role in data['roles'] or not "color" in data['roles'][role]:
                    errors.append(f'{client_name} - {account_name} - {role} missing color line')
                    return

                role_lower = role.lower()
                role_label = f'{role}!' if 'admin' in role_lower else role

                cli_config[f'profile {client_name}-{account_name}-{role_lower}'] = {
                    "role_arn": f'arn:aws:iam::{account_id}:role/{role}',
                    "source_profile": "itoc-identity",
                    "mfa_serial": "arn:aws:iam::394966198205:mfa/${USER}",
                    "region": account['region'] if 'region' in account else 'ap-southeast-2',
                }
                browser_config[f'profile {client_name}-{account_name}-{role_lower}'] = {
                    "role_arn": f'arn:aws:iam::{account_id}:role/{role_label}',
                    "source_profile": "itoc-identity",
                    "color": data['roles'][role]['color'],
                    "region": account['region'] if 'region' in account else 'ap-southeast-2',
                }
                csv_config.append([client_name, account_name, account_id, role_lower])
                html_config.append(f'<tr><td>{client_name}</td><td>{account_name}</td><td>{account_id}</td><td>{role_lower}</td></tr>')

client_files_path = os.path.join(os.getcwd(),"clients")
client_files = [f for f in os.listdir(client_files_path) if os.path.isfile(os.path.join(client_files_path, f))]
for file in sorted(client_files):
    generate_client(file.replace('.json', ''))

if len(errors):
    print('\nERRORS:')
    for error in errors:
        print(error)
    exit(1)

path = os.path.join(os.getcwd(),"configs")
if not os.path.exists(path):
    os.mkdir(path)

print('')
print('Writing cli-config.ini')
with open('cli-starter.ini') as starter:
    with open('configs/cli-config.ini', 'w') as configfile:
        configfile.write(starter.read())
        cli_config.write(configfile)

print('Writing browser-config.ini')
with open('browser-starter.ini') as starter:
    with open('configs/browser-config.ini', 'w') as configfile:
        configfile.write(starter.read())
        browser_config.write(configfile)

print('Writing accounts.csv')
with open('configs/accounts.csv', 'w', encoding='UTF8', newline='') as f:
    header = ['Client', 'Account Name', 'Account ID', 'Role Name']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(csv_config)

if os.environ.get('UPDATE_CONFLUENCE'):
    confluence = Confluence(
        url='https://itocau.atlassian.net/wiki',
        username=os.environ.get('CONFLUENCE_USERNAME'),
        password=os.environ.get('CONFLUENCE_PASSWORD'))
    print('Retrieved Username and password')

    html_config.append(f'</table>')
    html_config = '\r\n'.join(html_config)

    print(html_config)

    confluence.update_page(2690368865974, "Itoc Client AWS Account IDs", html_config)