from googleapiclient.discovery import build

api_key = 'ADD_YOUR_KEY'

playlist_ids = {
    'PLz1DmTkYpZW6pbDdQKLRmDNzJL78s-D2b': 4169,     # Robbie's 
    'PLPCWXaq8VyL2vi649E08OJAFzJtIA-Yaa': 421       # soul samples
}  

video_links = []
next_page_token = None


youtube = build('youtube', 'v3', developerKey=api_key)

for playlist_id, max_results in playlist_ids.items():
    while True:
        # Request playlist items
        playlist_items = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=5000,
            pageToken=next_page_token  
        ).execute()
        
        items = playlist_items.get('items', [])
        for item in items:
            video_links.append(f'https://www.youtube.com/watch?v={item["contentDetails"]["videoId"]}')

        next_page_token = playlist_items.get('nextPageToken')

        if not next_page_token:
            break  # No more pages
        
        # Extract video links
        # video_links = [f'https://www.youtube.com/watch?v={item["contentDetails"]["videoId"]}' for item in playlist_items['items']]



with open('links.txt', 'a') as file:
    for link in video_links:
        file.write(f'{link}\n')