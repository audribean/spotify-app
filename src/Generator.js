import { map, pick } from 'lodash';
var spotifyApi = new SpotifyWebApi();
spotifyApi.setAccessToken('Spotify OAuth Token');

/*
Gathers longterm top tracks
Then parses through them for calmness
Then adds those to the calm playlist
Playlist will be 50 tracks max and 15 min
If less, then we'll use recommendations to fill
If more, then we'll delete any with index 50+
*/
function calmPlaylist() {
    var jsonTracks = spotifyApi.getMyTopTracks({time_range: long_term, limit: 50});
    // parse stuff to get array of URIs
    var uri;
    const calmTracks = uri.forEach(filterCalm);
}

function filterCalm(item) {
    var stats = spotifyApi.getAudioFeaturesForTrack({trackId: item});
    var energy;
    var liveness;
    var tempo;
    var instrumentalness;
    var danceability;
    var loudness;
    var valence;

    if (energy > 0.2) break;
    if (liveness > 0.2) break;
    if (tempo > 100) break;
    if (instrumentalness < 0.5) break;
    if (danceability > 0.4) break;
    if (loudness > -15) break;
    if (valence > 0.2) break;
    
    // function to add songs to playlist here
}


/*
CALM PLAYLIST
- Finds user's top artists who have ambient, instrumental, and calm music
- First fills the playlist with songs that are saved and are deemed calm
- Fills rest with other calm songs
*/
