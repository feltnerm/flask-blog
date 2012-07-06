var LastFm, Twitter, compare_recent_tracks, connectLastFm, connectTwitter, current_recent_tracks, current_recent_tweets, get_recent_tracks, get_recent_tweets, io, lastfm, latest_recent_tracks, latest_recent_tweets, twitter, util, _;

_ = require('underscore');

util = require('util');

io = require('socket.io').listen(8080);

LastFm = require('lastfm').LastFmNode;

Twitter = require('twitter');

connectLastFm = function() {
  var lastfm, lastfm_stream, options;
  options = {
    api_key: 'f17f793660b92eabf5662385f6067490',
    secret: 'a28090a21e77cd6d74693d992f14f03a'
  };
  lastfm = new LastFm(options);
  lastfm_stream = lastfm.stream('plugitin');
  lastfm_stream.setMaxListeners(0);
  lastfm_stream.start();
  console.log('Connected to Last.FM');
  return {
    'node': lastfm,
    'stream': lastfm_stream
  };
};

connectTwitter = function() {
  var options, twitter;
  options = {
    consumer_key: 'YHDhqYrCdp0oHVDVKcWg',
    consumer_secret: '35fqOW9rpRBkUNt1sOALSXnFpaEOxJPMcLFugJWRj4',
    access_token_key: '273756715-KSWryWautYrY4aHyqgsI3KpRxPHAC8tP4TGJcrPP',
    access_token_secret: 'GHYiqm5IX65QkdsDcnekPDOdccsoTVCCZpexDslfI'
  };
  twitter = new Twitter(options);
  twitter.verifyCredentials(function(data) {
    return console.log('Connected to Twitter');
  });
  return {
    'node': twitter
  };
};

lastfm = connectLastFm();

twitter = connectTwitter();

current_recent_tracks = [];

latest_recent_tracks = [];

current_recent_tweets = [];

latest_recent_tweets = [];

compare_recent_tracks = function(updated_recent_tracks) {
  var update_recent_tracks;
  update_recent_tracks = JSON.parse(JSON.stringify(updated_recent_tracks));
  if (_.isEmpty(current_recent_tracks)) {
    console.log('current tracks empty: updating');
    current_recent_tracks = updated_recent_tracks;
  }
  latest_recent_tracks = updated_recent_tracks;
  return current_recent_tracks = _.z;
};

get_recent_tracks = function() {
  console.log('Querying Last.FM');
  return lastfm.node.request('user.getRecentTracks', {
    user: 'plugitin',
    limit: 5,
    handlers: {
      success: function(data) {
        if (data) return compare_recent_tracks(data.recenttracks.track);
      },
      error: function(error) {
        return console.log(error);
      }
    }
  });
};

get_recent_tweets = function() {
  return console.log('Polling twitter');
};

io.sockets.on('connection', function(socket) {
  var lastfm_poller;
  get_recent_tracks();
  lastfm_poller = setInterval(function() {
    var new_tracks;
    get_recent_tracks();
    console.log('latest len: ' + latest_recent_tracks.length);
    console.log('current len: ' + current_recent_tracks.length);
    if (JSON.stringify(latest_recent_tracks) !== JSON.stringify(current_recent_tracks)) {
      console.log('difference!');
      new_tracks = _.difference(latest_recent_tracks, current_recent_tracks);
      return socket.emit('new_tracks', new_tracks);
    } else {
      return console.log('same');
    }
  }, 3000);
  socket.emit('recent_tracks', current_recent_tracks);
  socket.on('error', function(error) {
    return console.log(error);
  });
  return socket.on('disconnect', function() {
    return clearInterval(lastfm_poller);
  });
});
