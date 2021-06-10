from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


#Google API Client Imports
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaIoBaseDownload, MediaFileUpload

# import tkinter 
from tkinter import filedialog
from mttkinter import *
SCOPES = ['https://www.googleapis.com/auth/drive']


def build_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    return service

def login(request):
    build_service()
    return HttpResponse('Authentication Done')


@api_view()
def list(request, token):
    if token == 'None':
        pageToken = None
    else:
        pageToken = token
    drive_service = build_service()
    results = drive_service.files().list(
                                        pageSize=10,
                                        pageToken=pageToken,
                                        fields="nextPageToken, files(id, name)").execute()
    search_list = results.get('files', [])
    if not search_list:
        return Response('No files found.')
    else:
        file_list = [{'nextPageToken' : results.get('nextPageToken')}]
        for file in search_list:
            file_data = {'title' : file['name'],
                        'id' :   file['id'] 
                        }
            file_list.append(file_data)

    return Response(file_list)

@api_view()
def filename_search(request, filename, token):
    if token == 'None':
        pageToken = None
    else:
        pageToken = token
    drive_service = build_service()
    results = drive_service.files().list(q=f"name contains '{filename}'",
                                        pageSize=10,
                                        pageToken=pageToken,
                                        fields="nextPageToken, files(id, name)").execute()
    search_list = results.get('files', [])
    if not search_list:
        return Response('No files found.')
    else:
        file_list = [{'nextPageToken' : results.get('nextPageToken')}]
        for file in search_list:
            file_data = {'title' : file['name'],
                        'id' :   file['id'] 
                        }
            file_list.append(file_data)

    return Response(file_list)
    
@api_view()
def download(request,filename,file_id):
    drive_service = build_service()

    file = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, file)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    with io.open('files/'+filename, 'wb') as f:
        fh.seek(0)
        f.write(fh.read()) 
    return Response("Download Successfull")


@api_view()
def upload(request):

    drive_service = build_service()

    root = mtTkinter.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames()
    for file in files:
        filename = str(file).split('/')
        file_metadata = {'name': f'{filename[-1]}'}
        media = MediaFileUpload(file)
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()

    return Response("The files have been uploaded")


def logout(request):
    os.remove("token.json")
    return HttpResponse("Logout Successful") 
