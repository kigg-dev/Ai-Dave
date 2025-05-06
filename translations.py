from PyQt5.QtCore import QTranslator


class Translations:
    def __init__(self):
        self.translations = {
            'en': {
                'Chat': 'Chat',
                'Settings': 'Settings',
                'Type your message here...': 'Type your message here...',
                'Send': 'Send',
                'Language': 'Language',
                'Theme': 'Theme',
                'Toggle Dark/Light Theme': 'Toggle Dark/Light Theme',
                'You': 'You',
                'Dave': 'Dave',
                'Error': 'Error',
                'Clear Chat': 'Clear Chat',
                'Save Chat': 'Save Chat',
                'Load Chat': 'Load Chat',
                'Chat History': 'Chat History',
                'Clear History': 'Clear History',
                'Confirmation': 'Confirmation',
                'Are you sure you want to clear chat history?': 'Are you sure you want to clear chat history?',
                'Yes': 'Yes',
                'No': 'No',
                'Dark': 'Dark',
                'Light': 'Light'
            },
            'ru': {
                'Chat': 'Чат',
                'Settings': 'Настройки',
                'Type your message here...': 'Введите ваше сообщение...',
                'Send': 'Отправить',
                'Language': 'Язык',
                'Theme': 'Тема',
                'Toggle Dark/Light Theme': 'Переключить темную/светлую тему',
                'You': 'Вы',
                'Dave': 'Дейв',
                'Error': 'Ошибка',
                'Clear Chat': 'Очистить чат',
                'Save Chat': 'Сохранить чат',
                'Load Chat': 'Загрузить чат',
                'Chat History': 'История чата',
                'Clear History': 'Очистить историю',
                'Confirmation': 'Подтверждение',
                'Are you sure you want to clear chat history?': 'Вы уверены, что хотите очистить историю чата?',
                'Yes': 'Да',
                'No': 'Нет',
                'Dark': 'Темный',
                'Light': 'Светлый'
            },
            'de': {
                'Chat': 'Chat',
                'Settings': 'Einstellungen',
                'Type your message here...': 'Geben Sie Ihre Nachricht ein...',
                'Send': 'Senden',
                'Language': 'Sprache',
                'Theme': 'Design',
                'Toggle Dark/Light Theme': 'Dunkles/Helles Design umschalten',
                'You': 'Sie',
                'Dave': 'Dave',
                'Error': 'Fehler',
                'Clear Chat': 'Chat löschen',
                'Save Chat': 'Chat speichern',
                'Load Chat': 'Chat laden',
                'Chat History': 'Chat-Verlauf',
                'Clear History': 'Geschichte löschen',
                'Confirmation': 'Bestätigung',
                'Are you sure you want to clear chat history?': 'Sind Sie sicher, dass Sie den Chat-Verlauf löschen möchten?',
                'Yes': 'Ja',
                'No': 'Nein',
                'Dark': 'Dunkel',
                'Light': 'Hell'
            }
        }
        self.current_language = 'en'
    
    def get_translation(self, language, key):
        return self.translations.get(language, self.translations['en']).get(key, key)
    
    def set_language(self, language):
        self.current_language = language 