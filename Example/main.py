import os
import json
from sftp import Sftp
from os.path import isfile, join

with open('settings.json', 'r') as f:
    settings = json.load(f)

def main():
    for job in settings['jobs']:
        try:
            # Create SFTP Instances
            source_sftp = Sftp(hostname=job['source']['host'], username=job['source']['username'], private_key=job['source']['private_key'], private_key_pass=job['source']['private_key_pass'])
            destination_sftp = Sftp(hostname=job['destination']['host'], username=job['destination']['username'], private_key=job['destination']['private_key'], private_key_pass=job['destination']['private_key_pass'])
            
            # Connect to source SFTP
            source_sftp.connect()
            source_file_count = 0
            
            # Obtain list of source files excluding hidden files
            source_files = [file for file in source_sftp.listdir(job['source']['path']) if not file.startswith('.')]
            for file in source_files:

                # Download files from SFTP
                source_sftp.download(file, f'{job['temp_path']}/{file}')

                # Remove files from source SFTP
                source_sftp.remove(file)

                # Increase File Counter
                source_file_count += 1

            # Disconnect from Source SFTP Server
            source_sftp.disconnect()
            
            # Verify files are downloaded
            if source_file_count == 0:
                if(job['notifications']['enabled']):
                    send_message('No Source Files Downloaded', '[ERROR] Missng Source Files', job['notifications']['recipients'], job['email'])
                continue

            # Connect to destination SFTP
            destination_sftp.connect()

            # Upload files to SFTP
            files = [f for f in os.listdir(job['temp_path']) if isfile(join(job['temp_path'], f))]
            for file in files:
                destination_sftp.upload(f'{job['temp_path']}/{file}', f'{job['destination']['path']}/{file}')
                # Move files to local archive
                rename_file(f'{job['temp_path']}/{file}', f'{job['temp_path']}/archive/{file}')
            
            # Compare Source Files to Uploaded Files
            source_file_names = [f.split('/t')[-1] for f in source_files]
            uploaded_files = [f.split('/t')[-1] for f in destination_sftp.listdir(job['destination']['path']) if not f.startswith('.')]

            if set(source_file_names).difference(uploaded_files):
                if(job['notifications']['enabled']):
                    send_message(f'Missing Files: {set(source_file_names).difference(uploaded_files)} \n Source Files: {set(source_file_names)} \n Destination Files: {set(uploaded_files)}', '[ERROR] Missng Files', job['notifications']['recipients'], job['email'])
                continue

            # Send Success Message
            if(job['notifications']['enabled']):
                    send_message(f'Files Successfully Transferred (Total Files: {source_file_count})', '[Success] File Transfer Completed', job['notifications']['recipients'], job['email'])

            # Disconnect from Destination SFTP Server
            destination_sftp.disconnect()
                
        except Exception as e:
            send_message(str(e), '[Error] Unknown Issue with SFTP File Transfer', job['notifications']['recipients'], job['email'])

def send_message(message, subject, recipients, smtp_settings):
    print('Sending an email!')

def rename_file(old_path, new_path):
    path, _ = os.path.split(new_path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            raise Exception(e)
    os.rename(old_path, new_path)

if __name__ == '__main__':
    main()