_ = require('underscore')
util = require('util')
io = require('socket.io').listen(8080)
LastFm = require('lastfm').LastFmNode
Twitter = require('twitter')

lastfm_options =
    api_key: 'f17f793660b92eabf5662385f6067490'
    secret: 'a28090a21e77cd6d74693d992f14f03a'

twitter_options = 
    consumer_key: 'YHDhqYrCdp0oHVDVKcWg'
    consumer_secret: '35fqOW9rpRBkUNt1sOALSXnFpaEOxJPMcLFugJWRj4'
    access_token_key: '273756715-KSWryWautYrY4aHyqgsI3KpRxPHAC8tP4TGJcrPP'
    access_token_secret: 'GHYiqm5IX65QkdsDcnekPDOdccsoTVCCZpexDslfI'

io.sockets.on('connection', (socket) ->

    lastfm = new LastFm(lastfm_options)
    lastfmstream = lastfm.stream('plugitin')
    lastfmstream.setMaxListeners(0)
    lastfmstream.start()


    twitter = new Twitter(twitter_options)
    twitter.verifyCredentials( (data) ->
    )

    twitter.getUserTimeline({trim_user: true, count: 10}, (data) ->
        console.log(data)
        for tweet in data
            result = {text: tweet.text, date: tweet.created_at}
            socket.emit('tweet', result)
    )

    getNewTrack = setInterval(() ->
        lastfmstream.on('nowPlaying', (data) ->
            lastfm.request('track.getInfo',
                mbid: data.mbid
                handlers:
                    success: (data) ->
                        socket.emit('new_track', data.track)
                    error: (error) ->
                        console.log(error.message)
            )
        )
    , 300000)

    getRecentTracks = setTimeout(() ->
        lastfm.request('user.getRecentTracks',
            user: 'plugitin'
            limit: 5
            handlers:
                success: (data) ->
                    recent_tracks = _.sortBy(data.recenttracks.track, (track) ->
                        return track.uts
                    )
                    console.log(recent_tracks)
                    for track in recent_tracks
                        lastfm.request('track.getInfo',
                            mbid: track.mbid
                            handlers:
                                success: (data) ->
                                    socket.emit('recent_tracks', data.track)
                                error: (error) ->
                                    console.log(error.message)
                        )
                error: (error) ->
                    console.log(error.message)
        )
    , 3000)

    lastfmstream.on('error', (error) ->
        console.log(error)
    )

    socket.on('error', (error) ->
        console.log(error)
        )

    socket.on('disconnect', ->
        clearInterval(getNewTrack);
    )
)
