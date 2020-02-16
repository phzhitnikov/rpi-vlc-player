import logging

import vlc


class Player():
    def __init__(self, media_list, instance_args=[]):
        self.instance = vlc.Instance(instance_args)
        self.player = self.instance.media_player_new()
        self.playlist = self.instance.media_list_player_new()
        self.playlist.set_media_player(self.player)

        # Populate media list
        self.medialist = self.instance.media_list_new(media_list)
        self.playlist.set_media_list(self.medialist)

        self.event_manager = self.player.event_manager()

    def play(self):
        self.playlist.play()

    def play_item(self, num):
        self.playlist.play_item_at_index(num - 1)

    def stop(self):
        self.player.stop()

    def set_repeat(self):
        self.playlist.set_playback_mode(vlc.PlaybackMode.repeat)

    def set_loop(self):
        self.playlist.set_playback_mode(vlc.PlaybackMode.loop)

    def set_position(self, num):
        pos = float(num) / 100
        self.player.set_position(pos)

    def is_fragment_pos_set(self, start_pos, end_pos):
        start_pos = float(start_pos) / 100
        end_pos = float(end_pos) / 100

        current_pos = self.player.get_position()
        return (current_pos >= start_pos and current_pos <= end_pos)

    def register_on_position_callback(self, position, callback, *callback_args):
        pos = float(position) / 100

        def on_pos_callback(event):
            new_position = event.u.new_position
            logging.debug("Video position: {0}".format(new_position))

            if new_position >= pos or new_position < 0:
                logging.debug("on_pos_callback fired on pos: {}".format(pos))
                callback(event, *callback_args)

        self._detach_events()
        self.add_event_callback(vlc.EventType.MediaPlayerPositionChanged, on_pos_callback)

        # Workaround: MediaPlayerPositionChanged doesn't fire if playlist ended
        if position == 100:
            self.add_event_callback(vlc.EventType.MediaPlayerEndReached, callback, *callback_args)

    def play_fragment(self, start_pos, end_pos, end_callback=None, *end_callback_args):
        logging.info("play_fragment <{} - {}>".format(start_pos, end_pos))

        # BUG: if playback_mode is not "loop", on MediaPlayerEndReached vlc can't restart playback (deadlock on restart)
        player_state = self.player.get_state()
        logging.debug("play_fragment: player state: {}".format(player_state))

        if player_state == vlc.State.Ended:
            logging.warning("player.state = Ended: Warning! Don't use fragment position = 100!")

        if not player_state == vlc.State.Playing:
            self.play()

        self.set_position(start_pos)

        def callback(event):
            if end_callback:
                logging.debug("play_fragment: Firing end_callback")
                end_callback(event, *end_callback_args)
            else:
                logging.debug("play_fragment: stopping playback")
                self.player.stop()

        self.register_on_position_callback(end_pos, callback)

    def loop_fragment(self, start_pos, end_pos):
        logging.info("loop_fragment <{} - {}>".format(start_pos, end_pos))

        def on_fragment_end(event, start_pos, *args):
            logging.info("Fragment ended. Restarting at pos <{0}>".format(start_pos))
            self.set_position(start_pos)

        self.play_fragment(start_pos, end_pos, on_fragment_end, start_pos)

    def add_event_callback(self, event, callback, *args):
        self.event_manager.event_attach(event, callback, *args)

    def _detach_events(self):
        self.event_manager.event_detach(vlc.EventType.MediaPlayerPositionChanged)
        self.event_manager.event_detach(vlc.EventType.MediaPlayerEndReached)
