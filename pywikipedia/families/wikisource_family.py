# -*- coding: utf-8  -*-
import family

__version__ = '$Id$'

# The Wikimedia family that is known as Wikisource

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'wikisource'

        self.languages_by_size = [
            'en', 'ru', 'zh', 'pt', 'fr', 'de', 'es', 'it', 'he', 'fa', 'ar',
            'hu', 'pl', 'cs', 'th', 'ro', 'ko', 'hr', 'te', 'fi', 'sv', 'sl',
            'vi', 'bn', 'nl', 'tr', 'el', 'sr', 'uk', 'ja', 'ml', 'la', 'br',
            'li', 'hy', 'yi', 'az', 'ca', 'mk', 'sa', 'vec', 'is', 'ta', 'bs',
            'da', 'no', 'id', 'eo', 'et', 'bg', 'sah', 'lt', 'gl', 'kn', 'cy',
            'sk', 'fo', 'zh-min-nan',
        ]

        if family.config.SSL_connection:
            for lang in self.languages_by_size:
                self.langs[lang] = None
            self.langs['-'] = None
        else:
            for lang in self.languages_by_size:
                self.langs[lang] = '%s.wikisource.org' % lang
            self.langs['-'] = 'wikisource.org'

        # Override defaults
        self.namespaces[2]['pl'] = 'Wikiskryba'
        self.namespaces[3]['pl'] = 'Dyskusja wikiskryby'

        # Most namespaces are inherited from family.Family.
        # Translation used on all wikis for the different namespaces.
        # (Please sort languages alphabetically)
        # You only need to enter translations that differ from _default.
        self.namespaces[4] = {
            '_default': [u'Wikisource', self.namespaces[4]['_default']],
            'ang': u'Wicifruma',
            'ar': [u'ويكي مصدر', u'وم'],
            'az': u'VikiMənbə',
            'bg': u'Уикиизточник',
            'bn': u'উইকিসংকলন',
            'br': u'Wikimammenn',
            'bs': u'Wikizvor',
            'ca': u'Viquitexts',
            'cs': [u'Wikizdroje', u'WS', u'WZ'],
            'cy': u'Wicitestun',
            'de': [u'Wikisource', u'WS'],
            'el': u'Βικιθήκη',
            'eo': u'Vikifontaro',
            'et': u'Vikitekstid',
            'fa': u'ویکی‌نبشته',
            'fi': u'Wikiaineisto',
            'fo': u'Wikiheimild',
            'he': u'ויקיטקסט',
            'hr': u'Wikizvor',
            'ht': u'Wikisòrs',
            'hu': u'Wikiforrás',
            'hy': u'Վիքիդարան',
            'is': u'Wikiheimild',
            'ko': u'위키문헌',
            'la': u'Vicifons',
            'li': u'Wikibrónne',
            'lt': u'Vikišaltiniai',
            'ml': u'വിക്കിഗ്രന്ഥശാല',
            'nb': u'Wikikilden',
            'no': u'Wikikilden',
            'pl': [u'Wikiźródła', u'WS'],
            'ru': u'Викитека',
            'sah': u'Бикитиэкэ',
            'sl': u'Wikivir',
            'sr': u'Викизворник',
            'ta': [u'Wikisource', u'விக்கிபீடியா'],
            'th': u'วิกิซอร์ซ',
            'tr': u'VikiKaynak',
            'uk': [u'Wikisource', u'ВД'],
            'yi': [u'װיקיביבליאָטעק', u'וויקיביבליאטעק'],
            'zh': u'Wikisource',
        }
        self.namespaces[5] = {
            '_default': [u'Wikisource talk', self.namespaces[5]['_default']],
            'ang': u'Wicifruma talk',
            'ar': [u'نقاش ويكي مصدر', u'نو'],
            'az': u'VikiMənbə müzakirəsi',
            'bg': u'Уикиизточник беседа',
            'bn': [u'উইকিসংকলন আলোচনা', u'উইকিসংকলন আলাপ'],
            'br': u'Kaozeadenn Wikimammenn',
            'bs': u'Razgovor s Wikizvor',
            'ca': u'Viquitexts Discussió',
            'cs': [u'Diskuse k Wikizdrojům', u'Wikisource diskuse', u'Wikizdroje diskuse'],
            'cy': u'Sgwrs Wicitestun',
            'da': [u'Wikisource diskussion', u'Wikisource-diskussion'],
            'de': u'Wikisource Diskussion',
            'el': u'Βικιθήκη συζήτηση',
            'eo': u'Vikifontaro diskuto',
            'es': u'Wikisource discusión',
            'et': [u'Vikitekstide arutelu', u'Vikitekstid arutelu'],
            'fa': u'بحث ویکی‌نبشته',
            'fi': u'Keskustelu Wikiaineistosta',
            'fo': [u'Wikiheimild-kjak', u'Wikiheimild kjak'],
            'fr': u'Discussion Wikisource',
            'gl': u'Conversa Wikisource',
            'he': u'שיחת ויקיטקסט',
            'hr': u'Razgovor o Wikizvoru',
            'ht': u'Diskisyon Wikisòrs',
            'hu': [u'Wikiforrás-vita', u'Wikiforrás vita'],
            'hy': u'Վիքիդարանի քննարկում',
            'id': u'Pembicaraan Wikisource',
            'is': u'Wikiheimildspjall',
            'it': u'Discussioni Wikisource',
            'ja': [u'Wikisource・トーク', u'Wikisource‐ノート'],
            'kn': u'Wikisource ಚರ್ಚೆ',
            'ko': u'위키문헌토론',
            'la': u'Disputatio Vicifontis',
            'li': u'Euverlèk Wikibrónne',
            'lt': u'Vikišaltiniai aptarimas',
            'mk': u'Разговор за Wikisource',
            'ml': u'വിക്കിഗ്രന്ഥശാല സംവാദം',
            'nb': u'Wikikilden-diskusjon',
            'nl': u'Overleg Wikisource',
            'no': u'Wikikilden-diskusjon',
            'pl': u'Dyskusja Wikiźródeł',
            'pt': u'Wikisource Discussão',
            'ro': [u'Discuție Wikisource', u'Discuţie Wikisource'],
            'ru': u'Обсуждение Викитеки',
            'sa': [u'Wikisourceसम्भाषणम्', u'Wikisourceसंभाषणं'],
            'sah': u'Бикитиэкэ Ырытыы',
            'sk': [u'Diskusia k Wikisource', u'Komentár k Wikipédii'],
            'sl': u'Pogovor o Wikiviru',
            'sr': [u'Разговор о Викизворнику', u'Razgovor o Викизворник'],
            'sv': u'Wikisourcediskussion',
            'ta': [u'Wikisource பேச்சு', u'விக்கிபீடியா பேச்சு'],
            'te': u'Wikisource చర్చ',
            'th': u'คุยเรื่องวิกิซอร์ซ',
            'tr': u'VikiKaynak tartışma',
            'uk': u'Обговорення Wikisource',
            'vec': u'Discussion Wikisource',
            'vi': u'Thảo luận Wikisource',
            'yi': [u'װיקיביבליאָטעק רעדן', u'וויקיביבליאטעק רעדן'],
            'zh': u'Wikisource talk',
        }

        self.namespaces[90] = {
            'sv': u'Tråd',
        }

        self.namespaces[91] = {
            'sv': u'Tråddiskussion',
        }

        self.namespaces[92] = {
            'sv': u'Summering',
        }

        self.namespaces[93] = {
            'sv': u'Summeringsdiskussion',
        }

        self.namespaces[100] = {
            'ar': u'بوابة',
            'az': u'Portal',
            'bg': u'Автор',
            'bn': u'লেখক',
            'br': u'Meneger',
            'cs': u'Autor',
            'el': u'Σελίδα',
            'en': u'Portal',
            'fa': u'درگاه',
            'fr': u'Transwiki',
            'he': u'קטע',
            'hr': u'Autor',
            'hu': u'Szerző',
            'hy': u'Հեղինակ',
            'id': u'Pengarang',
            'ko': u'저자',
            'ml': u'രചയിതാവ്',
            'nl': u'Hoofdportaal',
            'pl': u'Strona',
            'pt': u'Portal',
            'sl': u'Stran',
            'sr': u'Аутор',
            'te': u'ద్వారము',
            'tr': u'Kişi',
            'vec': u'Autor',
            'vi': u'Chủ đề',
        }

        self.namespaces[101] = {
            'ar': u'نقاش البوابة',
            'az': u'Portal müzakirəsi',
            'bg': u'Автор беседа',
            'bn': u'লেখক আলাপ',
            'br': u'Kaozeadenn meneger',
            'cs': u'Diskuse k autorovi',
            'el': u'Συζήτηση σελίδας',
            'en': u'Portal talk',
            'fa': u'بحث درگاه',
            'fr': u'Discussion Transwiki',
            'he': u'שיחת קטע',
            'hr': u'Razgovor o autoru',
            'hu': u'Szerző vita',
            'hy': u'Հեղինակի քննարկում',
            'id': u'Pembicaraan Pengarang',
            'ko': u'저자토론',
            'ml': u'രചയിതാവിന്റെ സംവാദം',
            'nl': u'Overleg hoofdportaal',
            'pl': u'Dyskusja strony',
            'pt': u'Portal Discussão',
            'sl': u'Pogovor o strani',
            'sr': u'Разговор о аутору',
            'te': u'ద్వారము చర్చ',
            'tr': u'Kişi tartışma',
            'vec': u'Discussion autor',
            'vi': u'Thảo luận Chủ đề',
        }

        self.namespaces[102] = {
            'ar': u'مؤلف',
            'az': u'Müəllif',
            'br': u'Pajenn',
            'ca': u'Pàgina',
            'da': u'Forfatter',
            'de': u'Seite',
            'el': u'Βιβλίο',
            'en': u'Author',
            'es': u'Página',
            'et': u'Lehekülg',
            'fa': u'مؤلف',
            'fr': u'Auteur',
            'hr': u'Stranica',
            'hy': u'Պորտալ',
            'id': u'Indeks',
            'it': u'Autore',
            'la': u'Scriptor',
            'mk': u'Автор',
            'ml': u'കവാടം',
            'nb': u'Forfatter',
            'nl': u'Auteur',
            'no': u'Forfatter',
            'pl': u'Indeks',
            'pt': u'Autor',
            'ro': u'Autor',
            'te': u'రచయిత',
            'vec': u'Pagina',
            'vi': u'Tác gia',
            'zh': u'Author',
        }

        self.namespaces[103] = {
            'ar': u'نقاش المؤلف',
            'az': u'Müəllif müzakirəsi',
            'br': u'Kaozeadenn pajenn',
            'ca': u'Pàgina Discussió',
            'da': u'Forfatterdiskussion',
            'de': u'Seite Diskussion',
            'el': u'Συζήτηση βιβλίου',
            'en': u'Author talk',
            'es': u'Página Discusión',
            'et': u'Lehekülje arutelu',
            'fa': u'بحث مؤلف',
            'fr': u'Discussion Auteur',
            'hr': u'Razgovor o stranici',
            'hy': u'Պորտալի քննարկում',
            'id': u'Pembicaraan Indeks',
            'it': u'Discussioni autore',
            'la': u'Disputatio Scriptoris',
            'mk': u'Разговор за автор',
            'ml': u'കവാടത്തിന്റെ സംവാദം',
            'nb': u'Forfatterdiskusjon',
            'nl': u'Overleg auteur',
            'no': u'Forfatterdiskusjon',
            'pl': u'Dyskusja indeksu',
            'pt': u'Autor Discussão',
            'ro': u'Discuție Autor',
            'te': u'రచయిత చర్చ',
            'vec': u'Discussion pagina',
            'vi': u'Thảo luận Tác gia',
            'zh': u'Author talk',
        }

        self.namespaces[104] = {
            '_default': u'Page',
            'ar': u'صفحة',
            'br': [u'Oberour', u'Author'],
            'ca': [u'Llibre', u'Index'],
            'da': u'Side',
            'de': u'Index',
            'eo': u'Paĝo',
            'es': [u'Índice', u'Index'],
            'et': [u'Register', u'Index'],
            'fa': [u'برگه', u'Page'],
            'he': u'עמוד',
            'hr': [u'Sadržaj', u'Index'],
            'hu': u'Oldal',
            'hy': u'Էջ',
            'id': u'Halaman',
            'it': u'Progetto',
            'la': u'Pagina',
            'ml': [u'സൂചിക', u'Index'],
            'no': u'Side',
            'pl': [u'Autor', u'Author'],
            'pt': [u'Galeria', u'Index'],
            'ro': u'Pagină',
            'ru': u'Страница',
            'sl': [u'Kazalo', u'Index'],
            'sv': u'Sida',
            'te': [u'పుట', u'పేజీ'],
            'vec': [u'Indice', u'Index'],
            'vi': u'Trang',
        }

        self.namespaces[105] = {
            '_default': u'Page talk',
            'ar': u'نقاش الصفحة',
            'br': [u'Kaozeadenn oberour', u'Author talk'],
            'ca': [u'Llibre Discussió', u'Index talk'],
            'da': u'Sidediskussion',
            'de': [u'Index Diskussion', u'Index talk'],
            'eo': u'Paĝo-Diskuto',
            'es': [u'Índice Discusión', u'Index talk'],
            'et': [u'Registri arutelu', u'Index talk'],
            'fa': u'گفتگوی برگه',
            'fr': u'Discussion Page',
            'he': u'שיחת עמוד',
            'hr': [u'Razgovor o sadržaju', u'Index talk'],
            'hu': u'Oldal vita',
            'hy': u'Էջի քննարկում',
            'id': u'Pembicaraan Halaman',
            'it': u'Discussioni progetto',
            'la': u'Disputatio Paginae',
            'ml': [u'സൂചികയുടെ സംവാദം', u'Index talk'],
            'no': u'Sidediskusjon',
            'pl': [u'Dyskusja autora', u'Author talk'],
            'pt': [u'Galeria Discussão', u'Index talk'],
            'ro': u'Discuție Pagină',
            'ru': u'Обсуждение страницы',
            'sl': [u'Pogovor o kazalu', u'Index talk'],
            'sv': u'Siddiskussion',
            'te': [u'పుట చర్చ', u'పేజీ చర్చ'],
            'vec': [u'Discussion indice', u'Index talk'],
            'vi': u'Thảo luận Trang',
            'zh': u'Page talk',
        }

        self.namespaces[106] = {
            '-': u'Index',
            'ar': u'فهرس',
            'ca': u'Autor',
            'da': u'Indeks',
            'en': u'Index',
            'eo': u'Indekso',
            'et': u'Autor',
            'fa': u'فهرست',
            'fr': u'Portail',
            'he': u'ביאור',
            'hu': u'Index',
            'hy': u'Ինդեքս',
            'id': u'Portal',
            'it': u'Portale',
            'la': u'Liber',
            'ml': u'താൾ',
            'no': u'Indeks',
            'pt': u'Página',
            'ro': u'Index',
            'ru': u'Индекс',
            'sv': u'Författare',
            'te': u'సూచిక',
            'vi': u'Mục lục',
            'zh': u'Index',
        }

        self.namespaces[107] = {
            '-': u'Index talk',
            'ar': u'نقاش الفهرس',
            'ca': u'Autor Discussió',
            'da': u'Indeksdiskussion',
            'en': u'Index talk',
            'eo': u'Indekso-Diskuto',
            'et': u'Autori arutelu',
            'fa': u'گفتگوی فهرست',
            'fr': u'Discussion Portail',
            'he': u'שיחת ביאור',
            'hu': u'Index vita',
            'hy': u'Ինդեքսի քննարկում',
            'id': u'Pembicaraan Portal',
            'it': u'Discussioni portale',
            'la': u'Disputatio Libri',
            'ml': u'താളിന്റെ സംവാദം',
            'no': u'Indeksdiskusjon',
            'pt': u'Página Discussão',
            'ro': u'Discuție Index',
            'ru': u'Обсуждение индекса',
            'sv': u'Författardiskussion',
            'te': u'సూచిక చర్చ',
            'vi': u'Thảo luận Mục lục',
            'zh': u'Index talk',
        }

        self.namespaces[108] = {
            '-': u'Author',
            'he': u'מחבר',
            'it': u'Pagina',
            'pt': u'Em Tradução',
            'sv': u'Index',
        }

        self.namespaces[109] = {
            '-': u'Author talk',
            'he': u'שיחת מחבר',
            'it': u'Discussioni pagina',
            'pt': u'Discussão Em Tradução',
            'sv': u'Indexdiskussion',
        }

        self.namespaces[110] = {
            'he': u'תרגום',
            'it': u'Indice',
            'pt': u'Anexo',
        }

        self.namespaces[111] = {
            'he': u'שיחת תרגום',
            'it': u'Discussioni indice',
            'pt': u'Anexo Discussão',
        }

        self.namespaces[112] = {
            'fr': u'Livre',
            'he': u'מפתח',
        }

        self.namespaces[113] = {
            'fr': u'Discussion Livre',
            'he': u'שיחת מפתח',
        }

        self.alphabetic = ['ang','ar','az','bg','bs','ca','cs','cy',
                      'da','de','el','en','es','et','fa','fi',
                      'fo','fr','gl','he','hr','ht','hu','id',
                      'is','it','ja', 'ko','la','lt','ml','nl',
                      'no','pl','pt','ro','ru','sk','sl','sr',
                      'sv','te','th','tr','uk','vi','yi','zh']

        self.obsolete = {
            'ang': None, # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Old_English_Wikisource
            'dk': 'da',
            'ht': None, # http://meta.wikimedia.org/wiki/Proposals_for_closing_projects/Closure_of_Haitian_Creole_Wikisource
            'jp': 'ja',
            'minnan':'zh-min-nan',
            'nb': 'no',
            'tokipona': None,
            'zh-tw': 'zh',
            'zh-cn': 'zh'
        }

        self.interwiki_putfirst = {
            'en': self.alphabetic,
            'fi': self.alphabetic,
            'fr': self.alphabetic,
            'he': ['en'],
            'hu': ['en'],
            'pl': self.alphabetic,
            'simple': self.alphabetic
        }
        # Global bot allowed languages on http://meta.wikimedia.org/wiki/Bot_policy/Implementation#Current_implementation
        self.cross_allowed = [
            'el','fa','it','ko','no','vi','zh'
        ]
        # CentralAuth cross avaliable projects.
        self.cross_projects = [
            'wikipedia', 'wiktionary', 'wikibooks', 'wikiquote', 'wikinews', 'wikiversity',
            'meta', 'mediawiki', 'test', 'incubator', 'commons', 'species'
        ]

        self.authornamespaces = {
            '_default': [0],
            'ar': [102],
            'bg': [100],
            'cs': [100],
            'da': [102],
            'en': [102],
            'fa': [102],
            'fr': [102],
            'hr': [100],
            'hu': [100],
            'hy': [100],
            'it': [102],
            'ko': [100],
            'la': [102],
            'nl': [102],
            'no': [102],
            'pl': [104],
            'pt': [102],
            'sv': [106],
            'tr': [100],
            'vi': [102],
            'zh': [102],
            }

        self.crossnamespace[0] = {
            '_default': self.authornamespaces,
        }
        self.crossnamespace[100] = {
            'bg': self.authornamespaces,
            'cs': self.authornamespaces,
            'hr': self.authornamespaces,
            'hu': self.authornamespaces,
            'hy': self.authornamespaces,
            'ko': self.authornamespaces,
            'tr': self.authornamespaces,
        }

        self.crossnamespace[102] = {
            'ar': self.authornamespaces,
            'da': self.authornamespaces,
            'en': self.authornamespaces,
            'fa': self.authornamespaces,
            'fr': self.authornamespaces,
            'it': self.authornamespaces,
            'la': self.authornamespaces,
            'nl': self.authornamespaces,
            'no': self.authornamespaces,
            'pt': self.authornamespaces,
            'vi': self.authornamespaces,
            'zh': self.authornamespaces,
        }

        self.crossnamespace[104] = {
            'pl': self.authornamespaces,
        }

        self.crossnamespace[106] = {
            'sv': self.authornamespaces,
        }

    def shared_image_repository(self, code):
        return ('commons', 'commons')

    if family.config.SSL_connection:
        def hostname(self, code):
            return 'secure.wikimedia.org'

        def protocol(self, code):
            return 'https'

        def scriptpath(self, code):
            if code == '-':
                return '/wikipedia/sources/w'

            return '/%s/%s/w' % (self.name, code)

        def nicepath(self, code):
            if code == '-':
                return '/wikipedia/sources/wiki/'
            return '/%s/%s/wiki/' % (self.name, code)
