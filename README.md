# VibeSync

🎉 Welcome to VibeSync! 🎵 Dive into a world where your videos and music are in perfect harmony! With VibeSync, simply submit your video and let app sync it with the most fitting music based on the video’s context. Get ready to see your moments transformed as we generate a new video where the music pulses to the rhythm of your content. Experience your memories in a whole new way with VibeSync! 🚀 Let’s create magic together!


## Table of Contents


- [VibeSync](#vibesync)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Running the app](#running-the-app)



## Getting Started

To get this app locally up and running, follow the steps below.

### Prerequisites

- Clone the repository
- Create .env file in the root directory and add the following environment variables:
  - `YOUTUBE_API_KEY` - API token for the YouTube Music API
    - Follow the instructions [here](https://developers.google.com/youtube/v3/getting-started) to get the API key
  - `GEMINI_API_KEY` - API token for the Gemini API
    - Follow the instructions [here](https://ai.google.dev/tutorials/setup) to get the API key


### Running the app

- Ensure you have docker installed on your machine and docker daemon is running.
- Run the following command to run the app:
  ```bash
  docker-compose up
  ```
- The app will be running on `http://localhost:8000`
