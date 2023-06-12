import boto3
import json
import os

def list_enabled_services():
    org_client = boto3.client('organizations')

    # Call the ListAWSServiceAccessForOrganization API to retrieve the enabled services
    list_services_output = org_client.list_aws_service_access_for_organization()

    # Extract the enabled services and their details from the response
    enabled_services = list_services_output['EnabledServicePrincipals']

    # Create a list to store the enabled service names
    service_names = []

    # Populate the list with the service names
    for service in enabled_services:
        service_names.append(service['ServicePrincipal'])

    # Create a dictionary to store the enabled services with their details
    data = {
        'EnabledServices': service_names
    }

    # Convert the dictionary to JSON format
    data_serialized = json.dumps(data, indent=4)

    # Find the output folder path
    current_directory = os.getcwd()
    output_folder = None
    for root, dirs, files in os.walk(current_directory):
        if 'output' in dirs:
            output_folder = os.path.join(root, 'output')
            break

    # Create the output folder if it doesn't exist
    if output_folder is None:
        raise Exception("Output folder not found.")

    # Specify the output file path
    service_enabled_folder = os.path.join(output_folder, 'Service_enabled')
    output_file = os.path.join(service_enabled_folder, 'enabled_services.json')

    # Create the Service_enabled folder if it doesn't exist
    if not os.path.exists(service_enabled_folder):
        os.makedirs(service_enabled_folder)

    # Write the enabled services to a JSON file in the specified folder
    with open(output_file, 'w') as file:
        file.write(data_serialized)

    print("JSON file generated successfully with enabled services.")
