import pandas as pd
from googleapiclient.discovery import build


class YouTubeAnalytics:
    def __init__(self, channel_id, credentials=None):
        self.channel_id = channel_id
        if credentials:
            self.youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
            self.youtube = build('youtube', 'v3', credentials=credentials)
        else:
            raise ValueError("Credentials are required")

    def get_playlist_data(self, playlist_groups, start_date, end_date):
        """Get data for multiple playlist groups"""
        all_data = {}
        
        for group_name, playlist_ids in playlist_groups.items():
            print(f"Processing playlist group: {group_name}")
            group_data = []
            
            for playlist_id in playlist_ids:
                video_info = self._get_video_info(playlist_id)
                views_data = self._get_daily_views(video_info, start_date, end_date)
                group_data.extend(views_data)
            
            if group_data:
                all_data[group_name] = pd.DataFrame(group_data)
        
        return all_data

    def _get_video_info(self, playlist_id):
        video_info = []
        request = self.youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50
        )
        
        while request:
            response = request.execute()
            for item in response['items']:
                video_info.append({
                    'video_id': item['snippet']['resourceId']['videoId'],
                    'title': item['snippet']['title'],
                    'playlist_id': playlist_id,
                    'published_at': pd.to_datetime(item['snippet']['publishedAt'].split('T')[0]).strftime('%Y-%m-%d')
                })
            request = self.youtube.playlistItems().list_next(request, response)
        
        return video_info

    def _get_daily_views(self, video_info, start_date, end_date):
        daily_views = []
        for video in video_info:
            try:
                request = self.youtube_analytics.reports().query(
                    ids=f'channel=={self.channel_id}',
                    startDate=start_date,
                    endDate=end_date,
                    metrics='views',
                    filters=f'video=={video["video_id"]}'
                )
                response = request.execute()
                
                for row in response.get('rows', []):
                    daily_views.append({
                        'video_id': video['video_id'],
                        'title': video['title'],
                        'published_at': pd.to_datetime(video['published_at']),
                        'views': row[0]
                    })
            except Exception as e:
                print(f"Error getting analytics for video {video['title']}: {str(e)}")

        return daily_views
