# Import Module
import ftplib

# Fill Required Information
# HOSTNAME = 'ftp.xtesting.com.br'
# USERNAME = 'xtesting2'
# PASSWORD = 'Xtesting2@1234!1020'
# PATH = 'public_html/poc-detran/_lib/file/doc/'

HOSTNAME = 'ftp.innovatex.com.br'
USERNAME = 'u444691204'
PASSWORD = 'Innova@2010'
# PATH = 'smartworkti.com.br/web/smartaudit/_lib/file/doc/'

def send_file_to_remote_server(filepath: str, filename: str, path: str):
    # Connect FTP Server
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

    # force UTF-8 encoding
    ftp_server.encoding = 'utf-8'

    # Read file in binary mode
    with open(filepath, 'rb') as file:
        # Command for Uploading the file "STOR filename"
        ftp_server.storbinary(f'STOR {path + filename}', file)

    # Close the Connection
    ftp_server.quit()
