var LastFm, SocialQueue, Twitter, io, util, _;

_ = require('underscore');

util = require('util');

io = require('socket.io').listen(8080);

LastFm = require('lastfm').LastFmNode;

Twitter = require('twitter');

SocialQueue = (function() {

  function SocialQueue() {
    this.lastfm = this.connectLastFm();
    this.twitter = this.connectTwitter();
    this.current_recent_tracks = [];
    this.latest_recent_tracks = [];
  }

  SocialQueue.prototype.connectLastFm = function() {
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

  SocialQueue.prototype.connectTwitter = function() {
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

  return SocialQueue;

})();

io.sockets.on('connection', function(socket) {
  var sq;
  sq = new SocialQueue();
  socket.on('error', function(error) {
    return console.error(error);
  });
  return socket.on('disconnect', function() {});
});
