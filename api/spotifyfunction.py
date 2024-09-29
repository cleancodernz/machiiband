import logging
import azure.functions as func
import requests
import os
import spotifyintegration

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure Function: Song search request received.')
    
    # Get the song name from the request
    song_name = req.params.get('song_name')
    if not song_name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            song_name = req_body.get('song_name')
    
    if not song_name:
        return func.HttpResponse(
            "Please pass a song name on the query string or in the request body",
            status_code=400
        )
    
    # Get Spotify token
    token = spotifyintegration.get_spotify_token()
    
    # Search for the song
    track = spotifyintegration.search_spotify_song(song_name, token)
    
    if track:
        preview_url = track.get('preview_url', None)
        if preview_url:
            return func.HttpResponse(f'Preview URL: {preview_url}', status_code=200)
        else:
            return func.HttpResponse(f'No preview available for "{song_name}".', status_code=404)
    else:
        return func.HttpResponse(f'Song "{song_name}" not found.', status_code=404)
