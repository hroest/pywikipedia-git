# -*- coding: utf-8  -*-
import family

__version__ = '$Id$'

# The Wikimedia family that is known as Wikinews

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'wikinews'

        self.languages_by_size = [
            'sr', 'en', 'pl', 'de', 'fr', 'it', 'pt', 'es', 'zh', 'ja', 'sv',
            'ru', 'fi', 'he', 'cs', 'bg', 'ro', 'ta', 'ar', 'sd', 'hu', 'no',
            'uk', 'ca', 'tr', 'bs', 'th',
        ]

        if family.config.SSL_connection:
            self.langs = dict([(lang, None) for lang in self.languages_by_size])
        else:
            self.langs = dict([(lang, '%s.wikinews.org' % lang) for lang in self.languages_by_size])

        # Override defaults
        self.namespaces[2]['cs'] = u'Redaktor'
        self.namespaces[2]['pl'] = u'Wikireporter'
        self.namespaces[3]['cs'] = u'Diskuse s redaktorem'
        self.namespaces[3]['pl'] = u'Dyskusja Wikireportera'


        # Most namespaces are inherited from family.Family.
        # Translation used on all wikis for the different namespaces.
        # (Please sort languages alphabetically)
        # You only need to enter translations that differ from _default.
        self.namespaces[4] = {
            '_default': [u'Wikinews', self.namespaces[4]['_default']],
            'ar': u'ويكي الأخبار',
            'bg': u'Уикиновини',
            'bs': u'Wikivijesti',
            'ca': u'Viquinotícies',
            'cs': u'Wikizprávy',
            'es': u'Wikinoticias',
            'fi': u'Wikiuutiset',
            'he': u'ויקיחדשות',
            'hu': u'Wikihírek',
            'it': u'Wikinotizie',
            'ja': u'ウィキニュース',
            'no': u'Wikinytt',
            'pt': u'Wikinotícias',
            'ro': u'Wikiştiri',
            'ru': u'Викиновости',
            'sr': u'Викивести',
            'th': u'วิกิข่าว',
            'tr': u'Vikihaber',
            'uk': u'ВікіНовини',
            'zh': [u'Wikinews', u'维基新闻'],
        }
        self.namespaces[5] = {
            '_default': [u'Wikinews talk', self.namespaces[5]['_default']],
            'ar': u'نقاش ويكي الأخبار',
            'bg': u'Уикиновини беседа',
            'bs': u'Razgovor s Wikivijestima',
            'ca': u'Viquinotícies Discussió',
            'cs': u'Diskuse k Wikizprávám',
            'de': u'Wikinews Diskussion',
            'es': u'Wikinoticias Discusión',
            'fi': u'Keskustelu Wikiuutisista',
            'fr': u'Discussion Wikinews',
            'he': u'שיחת ויקיחדשות',
            'hu': u'Wikihírek-vita',
            'it': u'Discussioni Wikinotizie',
            'ja': u'ウィキニュース・トーク',
            'nl': u'Overleg Wikinews',
            'no': u'Wikinytt-diskusjon',
            'pl': u'Dyskusja Wikinews',
            'pt': u'Wikinotícias Discussão',
            'ro': u'Discuție Wikiştiri',
            'ru': u'Обсуждение Викиновостей',
            'sd': u'Wikinews بحث',
            'sr': u'Разговор о Викивестима',
            'sv': u'Wikinewsdiskussion',
            'ta': u'Wikinews பேச்சு',
            'th': u'คุยเรื่องวิกิข่าว',
            'tr': u'Vikihaber tartışma',
            'uk': u'Обговорення ВікіНовини',
            'zh': [u'Wikinews talk', u'维基新闻讨论'],
        }

        self.namespaces[90] = {
            'ar': u'Thread',
            'bg': u'Thread',
            'bs': u'Thread',
            'ca': u'Thread',
            'cs': u'Thread',
            'de': u'Thread',
            'en': u'Thread',
            'es': u'Thread',
            'fi': u'Viestiketju',
            'fr': u'Thread',
            'he': u'Thread',
            'hu': u'Thread',
            'it': u'Thread',
            'ja': u'Thread',
            'no': u'Thread',
            'pl': u'Thread',
            'pt': u'Tópico',
            'ro': u'Thread',
            'ru': u'Thread',
            'sd': u'Thread',
            'sr': u'Thread',
            'sv': u'Thread',
            'ta': u'Thread',
            'th': u'Thread',
            'tr': u'Thread',
            'uk': u'Thread',
            'zh': u'Thread',
        }
        
        self.namespaces[91] = {
            'ar': u'Thread talk',
            'bg': u'Thread talk',
            'bs': u'Thread talk',
            'ca': u'Thread talk',
            'cs': u'Thread talk',
            'de': u'Thread talk',
            'en': u'Thread talk',
            'es': u'Thread talk',
            'fi': u'Keskustelu viestiketjusta',
            'fr': u'Thread talk',
            'he': u'Thread talk',
            'hu': u'Thread talk',
            'it': u'Thread talk',
            'ja': u'Thread talk',
            'no': u'Thread talk',
            'pl': u'Thread talk',
            'pt': u'Tópico discussão',
            'ro': u'Thread talk',
            'ru': u'Thread talk',
            'sd': u'Thread talk',
            'sr': u'Thread talk',
            'sv': u'Thread talk',
            'ta': u'Thread talk',
            'th': u'Thread talk',
            'tr': u'Thread talk',
            'uk': u'Thread talk',
            'zh': u'Thread talk',
        }
        
        self.namespaces[92] = {
            'ar': u'Summary',
            'bg': u'Summary',
            'bs': u'Summary',
            'ca': u'Summary',
            'cs': u'Summary',
            'de': u'Summary',
            'en': u'Summary',
            'es': u'Summary',
            'fi': u'Yhteenveto',
            'fr': u'Summary',
            'he': u'Summary',
            'hu': u'Summary',
            'it': u'Summary',
            'ja': u'Summary',
            'no': u'Summary',
            'pl': u'Summary',
            'pt': u'Resumo',
            'ro': u'Summary',
            'ru': u'Summary',
            'sd': u'Summary',
            'sr': u'Summary',
            'sv': u'Summary',
            'ta': u'Summary',
            'th': u'Summary',
            'tr': u'Summary',
            'uk': u'Summary',
            'zh': u'Summary',
        }
        
        self.namespaces[93] = {
            'ar': u'Summary talk',
            'bg': u'Summary talk',
            'bs': u'Summary talk',
            'ca': u'Summary talk',
            'cs': u'Summary talk',
            'de': u'Summary talk',
            'en': u'Summary talk',
            'es': u'Summary talk',
            'fi': u'Keskustelu yhteenvedosta',
            'fr': u'Summary talk',
            'he': u'Summary talk',
            'hu': u'Summary talk',
            'it': u'Summary talk',
            'ja': u'Summary talk',
            'no': u'Summary talk',
            'pl': u'Summary talk',
            'pt': u'Resumo discussão',
            'ro': u'Summary talk',
            'ru': u'Summary talk',
            'sd': u'Summary talk',
            'sr': u'Summary talk',
            'sv': u'Summary talk',
            'ta': u'Summary talk',
            'th': u'Summary talk',
            'tr': u'Summary talk',
            'uk': u'Summary talk',
            'zh': u'Summary talk',
        }
        
        self.namespaces[100] = {
            'ar': u'بوابة',
            'cs': u'Portál',
            'de': u'Portal',
            'en': u'Portal',
            'es': u'Comentarios',
            'he': u'פורטל',
            'it': u'Portale',
            'ja': u'ポータル',
            'no': u'Kommentarer',
            'pl': u'Portal',
            'pt': u'Portal',
            'ru': u'Портал',
            'sv': u'Portal',
            'tr': u'Portal',
            'zh': u'频道',
        }

        self.namespaces[101] = {
            'ar': u'نقاش البوابة',
            'cs': u'Diskuse k portálu',
            'de': u'Portal Diskussion',
            'en': u'Portal talk',
            'es': u'Comentarios Discusión',
            'he': u'שיחת פורטל',
            'it': u'Discussioni portale',
            'ja': [u'ポータル・トーク', u'ポータル‐ノート'],
            'no': u'Kommentarer-diskusjon',
            'pl': u'Dyskusja portalu',
            'pt': u'Portal Discussão',
            'ru': u'Обсуждение портала',
            'sv': u'Portaldiskussion',
            'tr': u'Portal tartışma',
            'zh': u'频道 talk',
        }

        self.namespaces[102] = {
            'ar': u'تعليقات',
            'bg': u'Мнения',
            'de': u'Meinungen',
            'en': u'Comments',
            'fr': u'Transwiki',
            'hu': u'Portál',
            'pt': u'Efeméride',
            'ru': u'Комментарии',
            'sr': u'Коментар',
        }

        self.namespaces[103] = {
            'ar': u'نقاش التعليقات',
            'bg': u'Мнения беседа',
            'de': u'Meinungen Diskussion',
            'en': u'Comments talk',
            'fr': u'Discussion Transwiki',
            'hu': u'Portálvita',
            'pt': u'Efeméride Discussão',
            'ru': u'Обсуждение комментариев',
            'sr': u'Разговор о коментару',
        }

        self.namespaces[104] = {
            'fr': u'Page',
        }

        self.namespaces[105] = {
            'fr': u'Discussion Page',
        }

        self.namespaces[106] = {
            'fr': u'Dossier',
            'no': u'Portal',
        }

        self.namespaces[107] = {
            'fr': u'Discussion Dossier',
            'no': u'Portal-diskusjon',
        }

        self.namespaces[108] = {
            'ja': u'短信',
        }

        self.namespaces[109] = {
            'ja': u'短信‐ノート',
        }


        self.obsolete = {
            'jp': 'ja',
            'nb': 'no',
            'nl': None, # https://bugzilla.wikimedia.org/show_bug.cgi?id=20325
            'zh-tw': 'zh',
            'zh-cn': 'zh'
        }

        # Which languages have a special order for putting interlanguage links,
        # and what order is it? If a language is not in interwiki_putfirst,
        # alphabetical order on language code is used. For languages that are in
        # interwiki_putfirst, interwiki_putfirst is checked first, and
        # languages are put in the order given there. All other languages are put
        # after those, in code-alphabetical order.
        self.interwiki_putfirst = {
            'en': self.alphabetic,
            'fi': self.alphabetic,
            'fr': self.alphabetic,
            'he': ['en'],
            'pl': self.alphabetic,
        }

        # Global bot allowed languages on http://meta.wikimedia.org/wiki/Bot_policy/Implementation#Current_implementation
        self.cross_allowed = ['cs', 'hu',]
        # CentralAuth cross avaliable projects.
        self.cross_projects = [
            'wikipedia', 'wiktionary', 'wikibooks', 'wikiquote', 'wikisource', 'wikiversity', 
            'meta', 'mediawiki', 'test', 'incubator', 'commons', 'species'
        ]

    def code2encoding(self, code):
        return 'utf-8'

    def version(self, code):
        return '1.16wmf4'

    def shared_image_repository(self, code):
        return ('commons', 'commons')

    if family.config.SSL_connection:
        def hostname(self, code):
            return 'secure.wikimedia.org'

        def protocol(self, code):
            return 'https'

        def scriptpath(self, code):
            return '/%s/%s/w' % (self.name, code)

        def nicepath(self, code):
            return '/%s/%s/wiki/' % (self.name, code)
