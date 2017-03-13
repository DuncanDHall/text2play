# adapted from google's python api quickstart guide
# https://developers.google.com/sheets/api/quickstart/python

import httplib2
import httplib
import urlparse
import os
import csv
import re

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'WCS Spotify Playlist Updater'
SPREADSHEET_ID = '1tVBrly6vFsvObc13DdtvIBx-ORgTG2qb5QjyZ5y0zqM'



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_service(credentials):
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    return discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)


def get_spreadsheet_contents(ssID, service):
    rangeName = 'A2:C'
    result = service.spreadsheets().values().get(
            spreadsheetId=ssID, range=rangeName
            ).execute()
    return result.get('values', [])


def log_sheet(ssID, service, filename, header=''):
    contents = get_spreadsheet_contents(ssID, service)
    with open(filename + '.csv', 'w') as csvf:
        writer = csv.writer(csvf, delimiter=',')
        for row in contents:
            encoded_row = [cell.encode('utf-8') for cell in row]
            writer.writerow(encoded_row)


def read_csv(filename):
    with open(filename + '.csv', 'r') as csvf:
        reader = csv.reader(csvf, delimiter=',')
        return [row for row in reader]


def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    elif response.status/100 == 2:
        return url
    else:
        raise Exception('{} status recieved while following url: {}'.format(response.status, url))


def sheet_id_from_url(url):
    # example:
    # https://docs.google.com/spreadsheets/d/1tVBrly6vFsvObc13DdtvIBx-ORgTG2qb5QjyZ5y0zqM/edit#gid=0
    p = re.compile('spreadsheets/[a-z]/([^/]*)/edit')
    result = p.search(url)
    return result.group(1)


def log_linked_sheets(entries, service):
    for date, loc, short_link in entries:
        
        filename = date + '_' + loc
        path = 'playlists/' + filename

        if os.path.exists(path + '.csv'):
            print('playlist already logged: ' + path)
            break
        else:
            print('logging to: ' + path)

            ssID = sheet_id_from_url(unshorten_url(short_link))
            log_sheet(ssID, service, path)







def main():

    print('obtaining google credentials...')
    credentials = get_credentials()
    service = get_service(credentials)

    # refresh the dj set
    print('refreshing dj-set-collection.csv...')
    log_sheet(SPREADSHEET_ID, service, 'dj-set-collection')

    # check most recent entries in dj-set-collection and log
    log_linked_sheets(read_csv('dj-set-collection'), service)
    print('\nLogs refreshed!')

if __name__ == "__main__":
    main()

