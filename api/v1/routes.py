#!/usr/bin/env python3
"""The routes for the blueprint"""


from flask import Blueprint, request, jsonify, url_for
from .utils import get_podcast_info, download_podcast_clip
import os

bp = Blueprint('api_v1', __name__)

@bp.route('/create_clip', methods=['POST'])
def create_clip():
    data = request.json
    podcast_name = data['podcast_name']
    episode_number = data['episode_number']
    start_time = data['start_time']
    end_time = data['end_time']
    podcast_url, episode_title = get_podcast_info(podcast_name, episode_number)
    clip_path = download_podcast_clip(podcast_url, episode_title, start_time, end_time)
    clip_filename = os.path.basename(clip_path)
    clip_url = url_for('serve_clip', filename=clip_filename, _external=True)

    return jsonify({"message": "Clip created successfully", "clip_url": clip_url})
