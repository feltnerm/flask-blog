_       = require('underscore')
util    = require('util')
io      = require('socket.io').listen(8080)
LastFm  = require('lastfm').LastFmNode
Twitter = require('twitter')

connectLastFm = () ->
    options =
        api_key: 'f17f793660b92eabf5662385f6067490'
        secret: 'a28090a21e77cd6d74693d992f14f03a'
    lastfm = new LastFm(options)
    lastfm_stream = lastfm.stream('plugitin')
    lastfm_stream.setMaxListeners(0)
    lastfm_stream.start()
    console.log('Connected to Last.FM')
    return {'node': lastfm, 'stream': lastfm_stream}

connectTwitter = () ->
    options = 
        consumer_key: 'YHDhqYrCdp0oHVDVKcWg'
        consumer_secret: '35fqOW9rpRBkUNt1sOALSXnFpaEOxJPMcLFugJWRj4'
        access_token_key: '273756715-KSWryWautYrY4aHyqgsI3KpRxPHAC8tP4TGJcrPP'
        access_token_secret: 'GHYiqm5IX65QkdsDcnekPDOdccsoTVCCZpexDslfI'
    twitter = new Twitter(options)
    twitter.verifyCredentials( (data) ->
        console.log('Connected to Twitter')
    )
    return {'node': twitter}

io.sockets.on('connection', (socket) ->
    
    lastfm = connectLastFm()
    twitter = connectTwitter()

    lastfm.node.request('user.getRecentTracks',
        user: 'plugitin'
        limit: 6 
        handlers:
            success: (data) ->
                recent_tracks = _.sortBy(data.recenttracks.track, (t) ->
                    return t.uts
                )

                lastfm.stream.on('nowPlaying', (t) ->
                    recent_tracks.push(t)
                )
                for t in recent_tracks.reverse()
                    lastfm.node.request('track.getInfo',
                        mbid: t.mbid
                        handlers:
                            success: (data) ->
                                socket.emit('recent_tracks', data.track)
                            error: (error) ->
                                console.log(error.message)
                    )
            error: (error) ->
                console.log(error.message)
        )

    socket.on('error', (error) ->
        console.log(error)
    )
    socket.on('disconnect', () ->
        console.log('disconnected') 
    )

)
