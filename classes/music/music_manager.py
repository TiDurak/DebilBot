class Queue:
    def __init__(self):
        self.__queue = []
        self.__playing_now = None

    def add_track(self, title):
        self.__queue.append(title)

    def play_next(self):
        if self.length() > 0:
            next_track = self.__queue.pop(0)
            self.__playing_now = next_track
            return next_track
        else:
            return 0

    def get_playing_now(self):
        track = self.__playing_now
        return track

    def set_playing_now(self, track):
        self.__playing_now = track

    def clear(self):
        self.__queue = []
        self.__playing_now = None

    def is_empty(self):
        if self.length() == 0:
            return True
        else:
            return False

    def length(self) -> int:
        return len(self.__queue)

    def get_by_id(self, id):
        return self.__queue[id]

class GuildQueue:
    def __init__(self):
        self.queue = Queue()

class MusicManager:
    def __init__(self):
        self.__guild_queues = {}

    def get_guild_queue(self, guild_id):
        if self.__guild_queues.get(guild_id) is None:
            self.__guild_queues[guild_id] = GuildQueue()
        return self.__guild_queues[guild_id]