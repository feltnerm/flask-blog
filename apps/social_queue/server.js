// Generated by CoffeeScript 1.3.3
(function() {
  var LastFm, Twitter, io, lastfm_options, twitter_options, util, _;

  _ = require('underscore');

  util = require('util');

  io = require('socket.io').listen(8080);

  LastFm = require('lastfm').LastFmNode;

  Twitter = require('twitter');

  lastfm_options = {
    api_key: 'f17f793660b92eabf5662385f6067490',
    secret: 'a28090a21e77cd6d74693d992f14f03a'
  };

  twitter_options = {
    consumer_key: 'YHDhqYrCdp0oHVDVKcWg',
    consumer_secret: '35fqOW9rpRBkUNt1sOALSXnFpaEOxJPMcLFugJWRj4',
    access_token_key: '273756715-KSWryWautYrY4aHyqgsI3KpRxPHAC8tP4TGJcrPP',
    access_token_secret: 'GHYiqm5IX65QkdsDcnekPDOdccsoTVCCZpexDslfI'
  };

  io.sockets.on('connection', function(socket) {
    var getNewTrack, getRecentTracks, lastfm, lastfmstream, twitter;
    lastfm = new LastFm(lastfm_options);
    lastfmstream = lastfm.stream('plugitin');
    lastfmstream.setMaxListeners(0);
    lastfmstream.start();
    twitter = new Twitter(twitter_options);
    twitter.verifyCredentials(function(data) {});
    twitter.getUserTimeline({
      trim_user: true,
      count: 10
    }, function(data) {
      var result, tweet, _i, _len, _results;
      console.log(data);
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
    getNewTrack = setInterval(function() {
      return lastfmstream.on('nowPlaying', function(data) {
        return lastfm.request('track.getInfo', {
          mbid: data.mbid,
          handlers: {
            success: function(data) {
              return socket.emit('new_track', data.track);
            },
            error: function(error) {
              return console.log(error.message);
            }
          }
        });
      });
    }, 300000);
    getRecentTracks = setTimeout(function() {
      return lastfm.request('user.getRecentTracks', {
        user: 'plugitin',
        limit: 5,
        handlers: {
          success: function(data) {
            var recent_tracks, track, _i, _len, _results;
            recent_tracks = _.sortBy(data.recenttracks.track, function(track) {
              return track.uts;
            });
            console.log(recent_tracks);
            _results = [];
            for (_i = 0, _len = recent_tracks.length; _i < _len; _i++) {
              track = recent_tracks[_i];
              _results.push(lastfm.request('track.getInfo', {
                mbid: track.mbid,
                handlers: {
                  success: function(data) {
                    return socket.emit('recent_tracks', data.track);
                  },
                  error: function(error) {
                    return console.log(error.message);
                  }
                }
              }));
            }
            return _results;
          },
          error: function(error) {
            return console.log(error.message);
          }
        }
      });
    }, 3000);
    lastfmstream.on('error', function(error) {
      return console.log(error);
    });
    socket.on('error', function(error) {
      return console.log(error);
    });
    return socket.on('disconnect', function() {
      return clearInterval(getNewTrack);
    });
  });

}).call(this);