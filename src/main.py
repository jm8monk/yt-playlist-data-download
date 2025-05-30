import yaml
import os
from youtube_analytics import YouTubeAnalytics
from auth import authenticate

def load_settings(settings_file='settings/settings.yaml'):
    with open(settings_file, 'r') as f:
        return yaml.safe_load(f)

def main():
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('tokens', exist_ok=True)

    settings = load_settings()
    # Process each channel
    for channel_name, config in settings['channels'].items():
        try:
            print(f"\nProcessing {channel_name}...")
            credentials = authenticate(channel_name)
            analytics = YouTubeAnalytics(
                channel_id=config['channel_id'],
                credentials=credentials
            )
            playlist_data = analytics.get_playlist_data(
                config['playlists'],
                settings['date_range']['start_date'],
                settings['date_range']['end_date']
            )
            # Save data
            for group_name, df in playlist_data.items():
                if not df.empty:
                    output_file = f'data/{group_name}_daily_stats.xlsx'
                    df.to_excel(output_file, index=False, encoding='utf-8-sig')
                    print(f"Data saved to {output_file}")
        except Exception as e:
            print(f"Error processing {channel_name}: {str(e)}")

if __name__ == '__main__':
    main()
