util = require('util')
io = require('socket.io').listen(8080)
LastFm = require('lastfm').LastFmNode
Twitter = require('twitter')

lastfm_options =
    api_key: 'f17f793660b92eabf5662385f6067490'
    secret: 'a28090a21e77cd6d74693d992f14f03a'

lastfm = new LastFm(lastfm_options)
lastfmstream = lastfm.stream('plugitin')

lastfmstream.start()

twitter_options = 
    consumer_key: 'YHDhqYrCdp0oHVDVKcWg'
    consumer_secret: '35fqOW9rpRBkUNt1sOALSXnFpaEOxJPMcLFugJWRj4'
    access_token_key: '273756715-KSWryWautYrY4aHyqgsI3KpRxPHAC8tP4TGJcrPP'
    access_token_secret: 'GHYiqm5IX65QkdsDcnekPDOdccsoTVCCZpexDslfI'

twitter = new Twitter(twitter_options)
twitter.verifyCredentials( (data) ->
)

io.sockets.on('connection', (socket) ->

    tweets = setInterval( ->
        twitter.getUserTimeline({trim_user: true, count: 20}, (data) ->
            for tweet in data
                result = {text: tweet.text, date: tweet.created_at}
                socket.emit('tweet', result)
        )
    , 300000)

    tracks = setInterval( ->
        lastfmstream.on('nowPlaying', (track) ->
            socket.emit('track', {name: track.name})
        )
    , 300000)

    socket.on('disconnect', ->
        clearInterval(tweets)
        clearInterval(tracks)
    )
)
