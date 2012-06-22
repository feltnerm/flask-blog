(function() {
  var LastFm, Twitter, io, lastfm, lastfm_options, lastfmstream, twitter, twitter_options, util;

  util = require('util');

  io = require('socket.io').listen(8080);

  LastFm = require('lastfm').LastFmNode;

  Twitter = require('twitter');

  lastfm_options = {
    api_key: 'f17f793660b92eabf5662385f6067490',
    secret: 'a28090a21e77cd6d74693d992f14f03a'
  };

  lastfm = new LastFm(lastfm_options);

  lastfmstream = lastfm.stream('plugitin');

  lastfmstream.start();

  twitter_options = {
    consumer_key: 'YHDhqYrCdp0oHVDVKcWg',
    consumer_secret: '35fqOW9rpRBkUNt1sOALSXnFpaEOxJPMcLFugJWRj4',
    access_token_key: '273756715-KSWryWautYrY4aHyqgsI3KpRxPHAC8tP4TGJcrPP',
    access_token_secret: 'GHYiqm5IX65QkdsDcnekPDOdccsoTVCCZpexDslfI'
  };

  twitter = new Twitter(twitter_options);

  twitter.verifyCredentials(function(data) {});

  io.sockets.on('connection', function(socket) {
    var tracks, tweets;
    tweets = setInterval(function() {
      return twitter.getUserTimeline({
        trim_user: true,
        count: 20
      }, function(data) {
        var result, tweet, _i, _len, _results;
        _results = [];
        for (_i = 0, _len = data.length; _i < _len; _i++) {
          tweet = data[_i];
          result = {
            text: tweet.text,
            date: tweet.created_at
          };
          _results.push(socket.emit('tweet', result));
        }
        return _results;
      });
    }, 300000);
    tracks = setInterval(function() {
      return lastfmstream.on('nowPlaying', function(track) {
        return socket.emit('track', {
          name: track.name
        });
      });
    }, 300000);
    return socket.on('disconnect', function() {
      clearInterval(tweets);
      return clearInterval(tracks);
    });
  });

}).call(this);
