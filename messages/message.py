class Message:
    @staticmethod
    def start_play() -> str:
        return 'Сначала включите музыку'

    @staticmethod
    def already_pause() -> str:
        return 'Музыка уже на паузе'

    @staticmethod
    def successful_pause() -> str:
        return 'Пауза поставлена!'

    @staticmethod
    def successful_resume() -> str:
        return 'Воспроизведение продолжается!'

    @staticmethod
    def already_play() -> str:
        return 'Муызка уже играет'

    @staticmethod
    def now_playing(track:str) -> str:
        return f'Сейчас играет: {track}'

    @staticmethod
    def nothing_is_playing() -> str:
        return 'Сейчас ничего не играет'

    @staticmethod
    def empty_queue() -> str:
        return 'В очереди пока нет треков'

    @staticmethod
    def queue_cleared() -> str:
        return 'Очередь очищена'

    @staticmethod
    def not_connected():
        return 'Бот не подключен к голосовму каналу'

    @staticmethod
    def connect_to_channel():
        return 'Сначала подключитесь к голосовму каналу'

    @staticmethod
    def added_to_queue(track:str) -> str:
        return f'Трек "{track}" добавлен в очередь!'

    @staticmethod
    def added_playlist_to_queue(playlist) -> str:
        return f'Плейлист "{playlist}" добавлен в очередь!'

    @staticmethod
    def loading_playlist() -> str:
        return f'Плейлист загружается...'

    @staticmethod
    def full_queue() -> str:
        return 'Очередь переполнена! Максимальный размер - 50 треков!'

    @staticmethod
    def full_queue_for_playlist():
        return 'Неудалось добавить все треки плейлиста в очередь! Максимальный размер очереди - 50 треков!'

    @staticmethod
    def disconnect_message():
        return 'Все пользватели покинули голосовой канал. Воспроизведение остановлено!'

    @staticmethod
    def successful_skip():
        return 'Трек скипнут!'

    @staticmethod
    def leave_channel():
        return 'Проигрывание треков прекращено!'


