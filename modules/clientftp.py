# ftp_client.py
import argparse
import logging
from ftplib import FTP, error_perm
from io import BytesIO

def connect_to_ftp(host, port, username, password, action, filename, filedata=None):
    ftp = FTP()
    try:
        ftp.connect(host, port)
        ftp.login(user=username, passwd=password)
        logging.info(ftp.getwelcome())

        ftp.retrlines('LIST')

        if action == 'upload' and filedata is not None:
            upload_data = BytesIO(filedata.encode())
            ftp.storbinary(f'STOR {filename}', upload_data)
            logging.info(f"Uploaded {filename}")
        elif action == 'download':
            download_data = BytesIO()
            ftp.retrbinary(f'RETR {filename}', download_data.write)
            logging.info(f"Downloaded data: {download_data.getvalue().decode()}")
        elif action == 'delete':
            ftp.delete(filename)
            logging.info(f"Deleted {filename}")
        elif action == 'rename':
            new_name = input("Enter new filename: ")
            ftp.rename(filename, new_name)
            logging.info(f"Renamed {filename} to {new_name}")

        ftp.quit()
    except error_perm as e:
        logging.error(f"FTP error: {e}")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FTP client script.")
    parser.add_argument('--host', default='localhost', help='FTP server hostname')
    parser.add_argument('--port', type=int, default=2121, help='FTP server port')
    parser.add_argument('--username', default='user', help='FTP username')
    parser.add_argument('--password', default='12345', help='FTP password')
    parser.add_argument('--action', choices=['upload', 'download', 'delete', 'rename'], required=True, help='FTP action')
    parser.add_argument('--filename', required=True, help='Filename for the action')
    parser.add_argument('--filedata', help='File data for upload (if action is upload)')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    connect_to_ftp(args.host, args.port, args.username, args.password, args.action, args.filename, args.filedata)
