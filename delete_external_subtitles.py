import os
import ffmpeg
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_embedded_subtitles_info(file_path):
    try:
        # Probe the file for information
        probe = ffmpeg.probe(file_path)
        # Get subtitle streams
        subtitle_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle']

        subtitles_info = []
        for stream in subtitle_streams:
            info = {
                'index': stream['index'],
                'codec': stream.get('codec_name', 'unknown'),
                'language': stream['tags'].get('language', 'unknown') if 'tags' in stream else 'unknown',
                'title': stream['tags'].get('title', 'unknown') if 'tags' in stream else 'unknown'
            }
            subtitles_info.append(info)

        return subtitles_info
    except ffmpeg.Error as e:
        logging.error(f"Error probing file {file_path}: {e}")
        return []

def has_english_embedded_subtitles(file_path):
    subtitles_info = get_embedded_subtitles_info(file_path)
    for info in subtitles_info:
        if info['language'] == 'eng':
            return True
    return False

def delete_external_subtitles(media_dir, dry_run=True):
    # Supported video extensions
    video_extensions = ('.mkv', '.mp4', '.avi', '.mov')

    logging.info(f"Starting scan in directory: {media_dir}")

    for root, dirs, files in os.walk(media_dir):
        logging.debug(f"Scanning directory: {root}")
        for file in files:
            if file.endswith(video_extensions):
                video_path = os.path.join(root, file)
                logging.debug(f"Checking file: {video_path}")
                if has_english_embedded_subtitles(video_path):
                    logging.info(f"English embedded subtitles found in: {video_path}")
                    # Construct the expected path for the external subtitle file
                    base_name = os.path.splitext(video_path)[0]
                    subtitle_name = base_name + '.en.srt'
                    logging.debug(f"Checking existence of external subtitle: {subtitle_name}")

                    if os.path.exists(subtitle_name):
                        if dry_run:
                            logging.info(f"[DRY RUN] Would delete external subtitle: {subtitle_name}")
                        else:
                            logging.info(f"Deleting external subtitle: {subtitle_name}")
                            os.remove(subtitle_name)
                    else:
                        logging.debug(f"No external subtitle found at: {subtitle_name}")
                else:
                    logging.info(f"No English embedded subtitles in: {video_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for embedded English subtitles and delete external ones if found.')
    parser.add_argument('directory', type=str, help='The directory of the media library to scan.')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without deleting any files.')
    args = parser.parse_args()

    media_directory = args.directory
    dry_run = args.dry_run

    delete_external_subtitles(media_directory, dry_run)
