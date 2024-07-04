import http.client
import json
import sys
import urllib.parse
import time

# qBittorrent Web UI credentials
QB_HOST = 'localhost'
QB_PORT = 8080
QB_USERNAME = 'username'
QB_PASSWORD = 'password'

def get_qbittorrent_cookie():
    conn = http.client.HTTPConnection(QB_HOST, QB_PORT)
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    login_data = urllib.parse.urlencode({'username': QB_USERNAME, 'password': QB_PASSWORD})

    conn.request('POST', '/api/v2/auth/login', login_data, headers)
    response = conn.getresponse()

    if response.status == 200:
        # Extract cookies from the response headers
        cookies = response.getheader('Set-Cookie')
        conn.close()
        return cookies
    else:
        conn.close()
        raise Exception('Failed to log in to qBittorrent')

def get_torrent_info(cookies, hash):
    conn = http.client.HTTPConnection(QB_HOST, QB_PORT)
    headers = {'Cookie': cookies}

    conn.request('GET', f'/api/v2/torrents/info?hashes={hash}', headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    if response.status == 200:
        torrents = json.loads(data)
        if torrents:
            return torrents[0]
    return None

def resume_torrent(cookies, hash, retries=1):
    torrent = get_torrent_info(cookies, hash)
    if not torrent:
        print(f"Torrent with hash {hash} not found.")
        return

    # Check specific attributes
    if 'SubsPlease' in torrent['name'] and torrent['size'] <= 2 * 1024 * 1024 * 1024 and torrent['save_path'] == '/data/torrents/links':
        attempts = 0
        time.sleep(10) # wait for torrent to be checked
        while attempts <= retries:
            conn = http.client.HTTPConnection(QB_HOST, QB_PORT)
            headers = {'Content-type': 'application/x-www-form-urlencoded', 'Cookie': cookies}

            resume_data = urllib.parse.urlencode({'hashes': hash})
            conn.request('POST', '/api/v2/torrents/resume', resume_data, headers)
            response = conn.getresponse()
            response_body = response.read().decode('utf-8')  # Decode response body for logging
            conn.close()

            if response.status == 200:
                print(f"Resumed torrent: {torrent['name']}")
                return
            else:
                print(f"Attempt {attempts + 1}: Failed to resume torrent: {torrent['name']} with response: {response_body}")
                attempts += 1
                if attempts <= retries:
                    print("Waiting 10 seconds before retrying...")
                    time.sleep(10)

            if attempts > retries:
                print(f"Final attempt failed. Unable to resume torrent: {torrent['name']}.")
    else:
        print(f"Torrent {torrent['name']} does not meet the criteria.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        torrent_hash = sys.argv[1]
        try:
            cookies = get_qbittorrent_cookie()
            resume_torrent(cookies, torrent_hash)
        except Exception as e:
            print(str(e))
    else:
        print("No torrent hash provided.")