# PodSnipsAPI

PodSnipsAPI is a Flask-based web API that allows users to create short clips from podcast episodes. By providing the name of a podcast, an episode number, and start/end timestamps, users can quickly generate a clip of their desired segment.

## Features

- **Search Podcasts**: Find podcasts by name.
- **Download Episodes**: Automatically download podcast episodes.
- **Clip Creation**: Create short audio clips from podcast episodes based on user-defined timestamps.
- **Format-Agnostic**: Handles audio in various formats, not just MP3.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Olyray/PodSnipsAPI.git

2. **Navigate to the project directory**:
    ```bash
    cd PodSnipsAPI

3. **Install the required python packages**:
    ```bash
    pip install -r requirements.txt

## Usage

1. **Set up the environment variables**:
The API makes use of the Podcast Index API. So, you need to have the podcast index API and secret key. You can register for this at the [Podcast Index website](https://api.podcastindex.org/).

Then use the provided .env.example as template. Rename it to .env and use fill in your API credentials.

2. **Run the Flask app**:
    ```bash
    ./app.py

The API would then be accessible at http://127.0.0.1:5000/  . Use the /api/v1/create_clip to send requests by sending a POST request with the required parameters.

```
curl -X POST http://127.0.0.1:5000/api/v1/create_clip -H "Content-Type: application/json" -d '{"podcast_name": "History of China", "episode_number": 1, "start_time": "00:00:10", "end_time": "00:00:50"}'
```


This would create an output like this:

```
{
  "clip_url": "http://127.0.0.1:5000/clips/ef84f97a-5412-4ef4-a787-1e588cf8ba0b.mp3",
  "message": "Clip created successfully"
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)