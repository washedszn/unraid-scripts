# Media Library Scripts

This repository contains a collection of scripts I use on my Unraid server.

## Scripts

### `calculate_media_size_on_disk.sh`
Calculates the total size of media files on disk, grouped by media type profiles.

### `delete_external_subtitles.py`
Checks for embedded English subtitles in media files and deletes corresponding external `.en.srt` subtitle files if embedded subtitles are found.

### `non_hardlink_size.sh`
Calculates the total size of non-hardlinked files in a specified directory.

### `non_season_pack_counter.sh`
Counts the number of leaf directories and identifies directories containing multiple release versions of files.

### `tv_file_sizes.sh`
Calculates and outputs file size statistics (total, minimum, maximum, average, percentiles) for `.mkv` and `.mp4` files in a specified directory.

### `resume_xseed_torrent.py`
Resumes torrents in qBittorrent that meet specific criteria (name contains 'SubsPlease', size <= 2GB, and save path is '/data/torrents/links').

## License

This repository is licensed under the MIT License. See the `LICENSE` file for more information.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.
