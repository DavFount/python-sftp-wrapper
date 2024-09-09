# SFTP Wrapper Class

## Overview

The SFTP Wrapper Class is a Python class designed to simplify interactions with SFTP servers using the `pysftp` library. This wrapper provides an easy-to-use interface for common SFTP operations such as connecting to the server, uploading and downloading files, and listing directories.

## Features

- Connect to SFTP servers with ease
- Upload and download files
- List directories and manage files
- Handle exceptions and errors gracefully
- Optionally manage server host keys

## Installation

To use the SFTP Wrapper Class, you'll need to have Python 3.6 or higher and install the `pysftp` library. You can install it using `pip`:

```bash
pip install pysftp
```

Drop the sftp.py file into your project and enjoy!

## Example
I added an example of how I'm using this to move files on a cron job to move files between two SFTP vendors.