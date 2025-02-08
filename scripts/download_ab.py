import argparse
import json
import os
import time
import requests

# NETWORK_CONFIG=$(curl -s https://ak-conf.hypergryph.com/config/prod/b/network_config | jq -r .content)
# NETWORK_URLS=$(echo $NETWORK_CONFIG | jq -r .configs.$(echo $NETWORK_CONFIG | jq -r .funcVer).network)
# RES_VERSION=$(curl -s $(echo $NETWORK_URLS | jq -r .hv | sed 's/{0}/Android/') | jq -r .resVersion)
# ASSETS_URL='$(echo $NETWORK_URLS | jq -r .hu)/Android/assets/$RES_VERSION'

# mkdir assets && cd assets
# wget $ASSETS_URL/hot_update_list.json
# jq -c .abInfos[] hot_update_list.json | while read -r item; do
#     FILENAME=$(echo $item | jq -r .name)
#     wget $ASSETS_URL/$(echo '$FILENAME' | sed -e 's|/|_|g' -e 's|#|__|' -e 's|\..*|.dat|g')
# done

parser = argparse.ArgumentParser(description='Download Arknights assets.')
parser.add_argument('-s', '--server', choices=['cn', 'en'], default='cn', required=False)
parser.add_argument('-dd', '--download-dir', default='download')
parser.add_argument('-hu', '--hot-update-list', default='hot_update_list_{0}.json')
parser.add_argument('-io', '--ignore-old', action='store_true')
parser.add_argument('-fd', '--filter-downloads', default='')
parser.add_argument('-sd', '--specify-downloads', default='')
args = parser.parse_args()

server_urls = {
    'cn': 'https://ak-conf.hypergryph.com/config/prod/b/network_config',
    'en': 'https://ak-conf.arknights.global/config/prod/official/network_config'
}
server_url = server_urls[args.server]
download_dir = args.download_dir
hot_update_list_file = args.hot_update_list.format(args.server)
ignore_old = args.ignore_old
filter_downloads = args.filter_downloads.split(',') if len(args.filter_downloads) > 0 else []
specific_downloads = args.specify_downloads.split(',') if len(args.specify_downloads) > 0 else []

network_config = requests.get(server_url).json()
network_contents = json.loads(network_config['content'])
network_urls = network_contents['configs'][network_contents['funcVer']]['network']
res_version = requests.get(network_urls['hv'].replace('{0}', 'Android')).json()['resVersion']
assets_url = f'{network_urls["hu"]}/Android/assets/{res_version}'

if not os.path.exists(hot_update_list_file) or os.stat(hot_update_list_file).st_size == 0:
    old_hot_update_list = {'versionId': '', 'abInfos': []}
else:
    with open(hot_update_list_file, 'r') as f:
        old_hot_update_list = json.load(f)

if not specific_downloads and not ignore_old and old_hot_update_list['versionId'] == res_version:
    print('Up to date.')
    exit(0)

os.makedirs(download_dir, exist_ok=True)
hot_update_list = requests.get(f'{assets_url}/hot_update_list.json').json()
for item in hot_update_list['abInfos']:
    filename = item['name']
    hash = item['hash']

    if specific_downloads:
        if filename in specific_downloads:
            pass
        else:
            continue
    elif not ignore_old and any(x for x in old_hot_update_list['abInfos'] if x['name'] == filename and x['hash'] == hash):
        continue
    elif filter_downloads:
        if not any(x in filename for x in filter_downloads):
            continue

    print(filename)
    filename = filename.replace('/', '_').replace('#', '__').split('.')[0] + '.dat'
    retries = 5
    for attempt in range(retries):
        try:
            response = requests.get(f'{assets_url}/{filename}')
            response.raise_for_status()
            with open(f'{download_dir}/{filename}', 'wb') as f:
                f.write(response.content)
            os.system(f'unzip -q {download_dir}/{filename} -d {download_dir}/')
            os.remove(f'{download_dir}/{filename}')
            break
        except requests.exceptions.RequestException as e:
            print(f'Attempt {attempt + 1} failed: {e}')
            if attempt == retries - 1:
                print(f'Failed to download {filename} after {retries} attempts.')
            else:
                time.sleep(attempt + 1)

with open(hot_update_list_file, 'w') as f:
    f.write(json.dumps(hot_update_list))
    print(f'Updated {hot_update_list_file}: {old_hot_update_list["versionId"]} -> {res_version}')
