#!/usr/bin/env python3
"""The utils module containing important functions for the API"""


import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.utils import mediainfo
from tqdm import tqdm
from hashlib import sha1
import time
import requests
import uuid

load_dotenv()

def get_podcast_index_api_key():
    api_key = os.getenv("PODCAST_INDEX_API_KEY")
    api_secret = os.getenv("PODCAST_INDEX_API_SECRET")
    return api_key, api_secret

def get_podcast_info(podcast_name, episode_number):
    """Get the podcast url and episode title"""
    api_key, api_secret = get_podcast_index_api_key()

    # Generate a SHA-1 hash using the API key, API secret, and the current time
    api_header_time = str(int(time.time()))
    data_to_hash = api_key + api_secret + api_header_time
    api_header_hash = sha1(data_to_hash.encode()).hexdigest()

    headers = {
        'X-Auth-Key': api_key,
        'User-Agent': 'Podcast Clipper',
        'Authorization': api_header_hash,
        'X-Auth-Date': api_header_time
    }

    response = requests.get('https://api.podcastindex.org/api/1.0/search/byterm', headers=headers, params={
        'q': podcast_name
    })

    data = response.json()
    podcast_id = data['feeds'][0]['id']

    response = requests.get(f'https://api.podcastindex.org/api/1.0/episodes/byfeedid?id={podcast_id}&max=500&pretty', headers=headers)

    data = response.json()
    data_length = data['count']
    episode_title = data['items'][data_length - episode_number]['title']
    podcast_url = data['items'][data_length - episode_number]['enclosureUrl']
    return podcast_url, episode_title

def clean_episode_title(episode_title):
    """Cleans the episode title to remove special characters"""
    return "".join([c if c.isalnum() or c.isspace() else "_" for c in episode_title])

def download_episode(podcast_url, episode_path):
    """Downloads the podcast episode and includes a progress bar"""
    response = requests.get(podcast_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 # 1 Kibibyte
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc='Downloading Episode')

    with open(episode_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

def create_clip(audio, start_time_in_ms, end_time_in_ms, clip_path, audio_format):
    """Creates the podcast clip, and includes a status bar"""
    clip_duration = end_time_in_ms - start_time_in_ms
    progress_bar = tqdm(total=clip_duration, unit='ms', unit_scale=True, desc='Creating Clip')

    clip = audio[start_time_in_ms:end_time_in_ms]
    clip.export(clip_path, format=audio_format)
    
    progress_bar.update(clip_duration)
    progress_bar.close()

def download_podcast_clip(podcast_url, episode_title, start_time, end_time):
    """The central function for processing the podcast episode and podcast clip"""
    if not os.path.exists('episodes'):
        os.makedirs('episodes')

    episode_title_clean = clean_episode_title(episode_title)
    episode_path = os.path.join('episodes', episode_title_clean)
    
    if not os.path.exists(episode_path):
        download_episode(podcast_url, episode_path)

    audio_info = mediainfo(episode_path)
    audio_format = audio_info.get("format_name", "").split(",")[0].strip()

    if not os.path.exists('clips'):
        os.makedirs('clips')

    clip_filename = str(uuid.uuid4()) + get_file_extension(audio_format)
    clip_path = os.path.join('clips', clip_filename)
    audio = AudioSegment.from_file(episode_path, format=audio_format)

    start_time_in_ms = sum(x * int(t) for x, t in zip([3600000, 60000, 1000], start_time.split(':')))
    end_time_in_ms = sum(x * int(t) for x, t in zip([3600000, 60000, 1000], end_time.split(':')))

    create_clip(audio, start_time_in_ms, end_time_in_ms, clip_path, audio_format)

    return clip_path

def get_file_extension(audio_format):
    """Gets the right file extension to use for the filename"""
    format_to_extension = {
        'mp3': '.mp3',
        'mp4': '.m4a',
        'wav': '.wav',
        'flac': '.flac',
        'ogg': '.ogg',
        'webm': '.webm'
    }
    return format_to_extension.get(audio_format, '')
