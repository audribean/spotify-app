import React from 'react';

// Code for logging in taken from
// https://levelup.gitconnected.com/how-to-create-a-spotify-music-search-app-in-react-1d71c8007e45

const Home = (props) => {
    const {
      REACT_APP_CLIENT_ID,
      REACT_APP_AUTHORIZE_URL,
      REACT_APP_REDIRECT_URL
    } = process.env;
    const handleLogin = () => {
      window.location = `${REACT_APP_AUTHORIZE_URL}?client_id=${REACT_APP_CLIENT_ID}&redirect_uri=${REACT_APP_REDIRECT_URL}&response_type=token&show_dialog=true`;
    };
    return (
      <div className="login">
        <Header />
        <Button variant="info" type="submit" onClick={handleLogin}>
          Login to Spotify
        </Button>
      </div>
    );
  };