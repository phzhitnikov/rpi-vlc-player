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

    def add_event_callback(self, event, callback, *args):
        self.event_manager.event_attach(event, callback, *args)

    def set_position(self, num):
        pos = float(num) / 100
        self.player.set_position(pos)

    def is_fragment_pos_set(self, start_pos, end_pos):
        start_pos = float(start_pos) / 100
        end_pos = float(end_pos) / 100

        current_pos = self.player.get_position()
        if current_pos >= start_pos and current_pos <= end_pos:
            return True

        return False

    def play_fragment(self, start_pos, end_pos, end_callback=None, end_callback_args=[]):
        logging.debug("play_fragment <{} - {}>".format(start_pos, end_pos))

        # FIXME: if playback_mode is not "loop", on MediaPlayerEndReached vlc can't restart playback
        if not self.player.get_state() == vlc.State.Playing:
            self.play()

        self.set_position(start_pos)
        end_pos = float(end_pos) / 100

        def on_pos_change(event):
            logging.debug("Fragment pos: {0}".format(event.u.new_position))
            if event.u.new_position >= end_pos:
                if end_callback:
                    logging.debug("play_fragment: Firing end_callback")
                    end_callback(event, *end_callback_args)
                else:
                    logging.debug("play_fragment: stopping playback")
                    self.player.stop()

        self._detach_events()
        self.add_event_callback(vlc.EventType.MediaPlayerPositionChanged, on_pos_change)
        # self.add_event_callback(vlc.EventType.MediaPlayerEndReached, end_callback, *end_callback_args)

    def loop_fragment(self, start_pos, end_pos):
        def on_fragment_end(event, start_pos, *args):
            logging.debug("Fragment ended. Restarting at pos <{0}>".format(start_pos))
            self.set_position(start_pos)

        logging.debug("loop_fragment <{} - {}>".format(start_pos, end_pos))
        self.play_fragment(start_pos, end_pos, on_fragment_end, [start_pos, end_pos])

    def _detach_events(self):
        self.event_manager.event_detach(vlc.EventType.MediaPlayerPositionChanged)
        self.event_manager.event_detach(vlc.EventType.MediaPlayerEndReached)
