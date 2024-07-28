import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace these with your Sonarr details
SONARR_API_KEY = 'YOUR_API_KEY'
SONARR_URL = 'http://localhost:8989/api/v3'  # Change to '/api' if using Sonarr v2

# Helper function to get all series
def get_all_series():
    url = f'{SONARR_URL}/series'
    headers = {
        'X-Api-Key': SONARR_API_KEY
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Helper function to get all episodes for a series
def get_episodes_for_series(series_id):
    url = f'{SONARR_URL}/episode?seriesId={series_id}'
    headers = {
        'X-Api-Key': SONARR_API_KEY
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Helper function to unmonitor a season
def unmonitor_season(series_id, season_number, series_name):
    url = f'{SONARR_URL}/series/{series_id}'
    headers = {
        'X-Api-Key': SONARR_API_KEY
    }
    series = requests.get(url, headers=headers).json()
    for season in series['seasons']:
        if season['seasonNumber'] == season_number:
            season['monitored'] = False
            break
    response = requests.put(url, json=series, headers=headers)
    response.raise_for_status()
    logger.info(f"Unmonitored Season {season_number} for Series '{series_name}'")

# Helper function to unmonitor a series
def unmonitor_series(series_id, series_name):
    url = f'{SONARR_URL}/series/{series_id}'
    headers = {
        'X-Api-Key': SONARR_API_KEY
    }
    series = requests.get(url, headers=headers).json()
    series['monitored'] = False
    response = requests.put(url, json=series, headers=headers)
    response.raise_for_status()
    logger.info(f"Unmonitored Series '{series_name}'")

def main():
    try:
        series_list = get_all_series()
        logger.info(f"Found {len(series_list)} series in the library.")

        for series in series_list:
            series_id = series['id']
            series_name = series['title']
            episodes = get_episodes_for_series(series_id)
            
            # Group episodes by season
            seasons = {}
            for episode in episodes:
                season_number = episode['seasonNumber']
                if season_number not in seasons:
                    seasons[season_number] = []
                seasons[season_number].append(episode)
            
            # Check each season if all episodes are unmonitored
            all_seasons_unmonitored = True
            for season_number, episodes in seasons.items():
                season_info = next((s for s in series['seasons'] if s['seasonNumber'] == season_number), None)
                if season_info and season_info['monitored']:
                    if all(not episode['monitored'] for episode in episodes):
                        unmonitor_season(series_id, season_number, series_name)
                    else:
                        all_seasons_unmonitored = False
            
            # Check if all seasons are unmonitored
            if all_seasons_unmonitored:
                unmonitor_series(series_id, series_name)

        logger.info("Completed processing all series.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
