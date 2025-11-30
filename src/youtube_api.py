from googleapiclient.discovery import build
import time

#API_KEY = ""
#need to point API key to config file and make mine hidden from github

CHANNEL_ID = "UCrNnk0wFBnCS1awGjq_ijGQ"

def get_channel_id(channel_name:str, api_key:str) -> str:
  '''This function searches the youtube api build for the first channel
  id that matches the given channel name. You can double-check this is 
  correct by navigating to the channels youtube page. The url will be in 
  the format: www.youtube.com/channel/CHANNEL_ID '''
  
  youtube = build("youtube","v3",developerKey=API_KEY)

  response = youtube.search().list(
        q=channel_name,
        part="snippet",
        type="channel",
        maxResults=1
    ).execute()

  items = response.get("items",[])

  if not items:
    raise ValueError(f"No channel found with name: {channel_name}")
  
  return items[0]["id"]["channelId"]

#Test code to pull channel_id for "PBS_KIDS"
#CHANNEL_ID = get_channel_id("PBS KIDS",API_KEY)
#print(CHANNEL_ID)

def get_uploads_playlist_id(channel_id, api_key):
    '''This function pulls the playlist_id for a given channel_id. 
    This is necessary because the only reliable place where the API
    lists all of a channels videos is in this playlist of uploads.'''
    youtube = build("youtube", "v3", developerKey=api_key)
    response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    
    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return uploads_playlist_id

#Test code for pulling playlist_id given the channel_id above
#uploads_playlist_id = get_uploads_playlist_id(CHANNEL_ID, API_KEY)
#print(uploads_playlist_id)

def get_all_video_ids_from_playlist(playlist_id, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    video_ids = []
    next_page_token = None
    
    while True:
        response = youtube.playlistItems().list(
            playlistId=playlist_id,
            part="contentDetails",
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        
        for item in response.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])
        
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
        time.sleep(0.1)
    return video_ids

video_ids = get_all_video_ids_from_playlist(uploads_playlist_id,API_KEY)
#video_ids = get_all_video_ids(CHANNEL_ID,API_KEY)
print(video_ids)
