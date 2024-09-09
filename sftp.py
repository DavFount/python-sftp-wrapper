import pysftp
from urllib.parse import urlparse
import os

class Sftp:
    def __init__(self, hostname, username, password=None, private_key=None, private_key_pass=None, port=22):
        """Constructor Method"""
        if not password and not private_key:
            raise Exception("Either password or private_key must be provided")
        self.connection = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.private_key = private_key
        self.private_key_pass = private_key_pass
        self.port = port

    def connect(self):
        """Connect to SFTP Server"""
        try:
            self.connection = pysftp.Connection(host=self.hostname, username=self.username, password=self.password, private_key=self.private_key, private_key_pass=self.private_key_pass, port=self.port)
        except Exception as e:
            raise Exception(e)
        finally:
            print(f"Connected to {self.hostname} as {self.username}")


    def disconnect(self):
        """Closes the SFTP Connection"""
        self.connection.close()
        print(f"Disconnected from {self.hostname}")

    def listdir(self, remote_path):
        """List files in the remote directory"""
        for obj in self.connection.listdir(remote_path):
            yield obj

    def listdir_attr(self, remote_path):
        """List files in the remote directory with attributes"""
        for attr in self.connection.listdir_attr(remote_path):
            yield attr
    
    def upload(self, source_path, remote_path):
        """Uploads the source files to the remote sftp server"""
        try:
            self.connection.put(source_path, remote_path)
        except Exception as e:
            raise Exception(e)
        
    def download(self, remote_path, target_path):
        """Downloads the file from the remote server to the target path"""

        try:
            print(f"Downloading from {self.hostname} as {self.username} [(remote path : {remote_path}); (target path : {target_path})]")

            path, _ = os.path.split(target_path)
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except Exception as e:
                    raise Exception(e)
            self.connection.get(remote_path, target_path)
            print("Download Complete")
        except Exception as e:
            raise Exception(e)
