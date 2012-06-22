// Generated by CoffeeScript 1.3.3
(function() {
  var LastFm, Twitter, connectLastFm, connectTwitter, io, util, _;

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

  io.sockets.on('connection', function(socket) {
    var lastfm, twitter;
    lastfm = connectLastFm();
    twitter = connectTwitter();
    lastfm.node.request('user.getRecentTracks', {
      user: 'plugitin',
      limit: 6,
      handlers: {
        success: function(data) {
          var recent_tracks, t, _i, _len, _ref, _results;
          recent_tracks = _.sortBy(data.recenttracks.track, function(t) {
            return t.uts;
          });
          lastfm.stream.on('nowPlaying', function(t) {
            return recent_tracks.push(t);
          });
          _ref = recent_tracks.reverse();
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            t = _ref[_i];
            _results.push(lastfm.node.request('track.getInfo', {
              mbid: t.mbid,
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
    socket.on('error', function(error) {
      return console.log(error);
    });
    return socket.on('disconnect', function() {
      return console.log('disconnected');
    });
  });

}).call(this);
