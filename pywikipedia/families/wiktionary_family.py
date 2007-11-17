# -*- coding: utf-8  -*-

import urllib
import family, config

__version__ = '$Id$'

# The Wikimedia family that is known as Wiktionary

# Known wiktionary languages, given as a dictionary mapping the language code
# to the hostname of the site hosting that wiktionary. For human consumption,
# the full name of the language is given behind each line as a comment

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'wiktionary'
        self.langs = {
            'minnan':'zh-min-nan.wiktionary.org',
            'nb':'no.wiktionary.org',
            'zh-cn':'zh.wiktionary.org',
            'zh-tw':'zh.wiktionary.org'
            }
        
        for lang in self.knownlanguages:
            if not lang in ['ee','ht','ny', 'se', 'tum']:
                self.langs[lang] = lang+'.wiktionary.org'
        
        # Most namespaces are inherited from family.Family.

        # Override defaults
        self.namespaces[3]['pl'] = u'Dyskusja Wikipedysty'

        self.namespaces[4] = {
            '_default': [u'Wiktionary', self.namespaces[4]['_default']],
            'ar': u'ويكاموس',
            'bg': u'Уикиречник',
            'bs': u'Vikirječnik',
            'ca': u'Viccionari',
            'cs': u'Wikislovník',
            'cy': u'Wiciadur',
            'eo': u'Vikivortaro',
            'es': u'Wikcionario',
            'et': u'Vikisõnaraamat',
            'fa': u'ویکی‌واژه',
            'fi': u'Wikisanakirja',
            'fo': u'Wiktionary',
            'fr': u'Wiktionnaire',
            'ga': u'Vicífhoclóir',
            'gu': u'વિક્ષનરી',
            'he': u'ויקימילון',
            'hi': u'विक्षनरी',
            'hr': u'Wječnik',
            'hu': u'Wikiszótár',
            'is': u'Wikiorðabók',
            'it': u'Wikizionario',
            'ka': u'ვიქსიკონი',
            'kk': u'Уикисөздік',
            'ko': u'위키낱말사전',
            'la': u'Victionarium',
            'ml': u'വിക്കി‌‌ നിഘണ്ടു',
            'ms': u'Wiktionary',
            'nl': u'WikiWoordenboek',
            'oc': u'Wikiccionari',
            'pl': u'Wikisłownik',
            'pt': u'Wikcionário',
            'ro': u'Wikţionar',
            'ru': u'Викисловарь',
            'sk': u'Wikislovník',
            'sl': u'Wikislovar',
            'sr': u'Викиречник',
            'tr': u'Vikisözlük',
            'tt': u'Wiktionary',
            'ur': u'وکی لغت',
            'uz': u'Vikilug‘at',
            'vo': u'Vükivödabuk',
            'yi': u'װיקיװערטערבוך',
        }
        
        self.namespaces[5] = {
            '_default': [u'Wiktionary talk', self.namespaces[5]['_default']],
            'ab': u'Обсуждение Wiktionary',
            'af': u'Wiktionarybespreking',
            'als': u'Wiktionary Diskussion',
            'an': u'Descusión Wiktionary',
            'ar': u'نقاش ويكاموس',
            'ast': u'Wiktionary discusión',
            'av': u'Обсуждение Wiktionary',
            'ay': u'Wiktionary Discusión',
            'az': u'Wiktionary müzakirəsi',
            'ba': u'Wiktionary б-са фекер алышыу',
            'be': u'Wiktionary размовы',
            'bg': u'Уикиречник беседа',
            'bm': u'Discussion Wiktionary',
            'bn': u'Wiktionary আলাপ',
            'br': u'Kaozeadenn Wiktionary',
            'bs': u'Razgovor s Vikirječnikom',
            'ca': u'Viccionari Discussió',
            'cs': u'Wikislovník diskuse',
            'csb': u'Diskùsëjô Wiktionary',
            'cy': u'Sgwrs Wiciadur',
            'da': u'Wiktionary-diskussion',
            'de': u'Wiktionary Diskussion',
            'el': u'Wiktionary συζήτηση',
            'eo': u'Vikivortaro diskuto',
            'es': u'Wikcionario Discusión',
            'et': u'Vikisõnaraamat arutelu',
            'eu': u'Wiktionary eztabaida',
            'fa': u'بحث ویکی‌واژه',
            'fi': u'Keskustelu Wikisanakirjasta',
            'fo': u'Wiktionary kjak',
            'fr': u'Discussion Wiktionnaire',
            'fy': u'Wiktionary oerlis',
            'ga': u'Plé Vicífhoclóra',
            'gn': u'Wiktionary Discusión',
            'gu': u'વિક્ષનરી talk',
            'he': u'שיחת ויקימילון',
            'hi': u'विक्षनरी वार्ता',
            'hr': u'Razgovor Wječnik',
            'hsb': u'Wiktionary diskusija',
            'hu': u'Wikiszótár vita',
            'hy': u'Wiktionary քննարկում',
            'ia': u'Discussion Wiktionary',
            'id': u'Pembicaraan Wiktionary',
            'is': u'Wikiorðabókarspjall',
            'it': u'Discussioni Wikizionario',
            'ja': u'Wiktionary‐ノート',
            'jv': u'Dhiskusi Wiktionary',
            'ka': u'ვიქსიკონი განხილვა',
            'kk': u'Уикисөздік талқылауы',
            'kn': u'Wiktionary ಚರ್ಚೆ',
            'ko': u'위키낱말사전토론',
            'ku': u'Wiktionary nîqaş',
            'la': u'Disputatio Victionarii',
            'lb': u'Wiktionary Diskussion',
            'li': u'Euverlèk Wiktionary',
            'ln': u'Discussion Wiktionary',
            'lt': u'Wiktionary aptarimas',
            'lv': u'Wiktionary diskusija',
            'mk': u'Разговор за Wiktionary',
            'ml': u'വിക്കി‌‌ നിഘണ്ടു സംവാദം',
            'mr': u'Wiktionary चर्चा',
            'ms': u'Perbincangan Wiktionary',
            'nah': u'Wiktionary Discusión',
            'nds': u'Wiktionary Diskuschoon',
            'nl': u'Overleg WikiWoordenboek',
            'nn': u'Wiktionary-diskusjon',
            'no': u'Wiktionary-diskusjon',
            'oc': u'Discussion Wikiccionari',
            'pa': u'Wiktionary ਚਰਚਾ',
            'pl': u'Wikidyskusja',
            'pt': u'Wikcionário Discussão',
            'qu': u'Wiktionary rimanakuy',
            'ro': u'Discuţie Wikţionar',
            'ru': u'Обсуждение Викисловаря',
            'sa': u'Wiktionaryसंभाषणं',
            'sc': u'Wiktionary discussioni',
            'scn': u'Discussioni Wiktionary',
            'sk': u'Diskusia k Wikislovníku',
            'sl': u'Pogovor o Wikislovarju',
            'sq': u'Wiktionary diskutim',
            'sr': u'Разговор о викиречнику',
            'su': u'Obrolan Wiktionary',
            'sv': u'Wiktionarydiskussion',
            'ta': u'Wiktionary பேச்சு',
            'te': u'Wiktionary చర్చ',
            'tg': u'Баҳси Wiktionary',
            'th': u'คุยเรื่องWiktionary',
            'tr': u'Vikisözlük tartışma',
            'tt': u'Wiktionary bäxäse',
            'uk': u'Обговорення Wiktionary',
            'ur': u'تبادلۂ خیال وکی لغت',
            'uz': u'Vikilug‘at munozarasi',
            'vi': u'Thảo luận Wiktionary',
            'vo': u'Bespik dö Vükivödabuk',
            'wa': u'Wiktionary copene',
            'wo': u'Discussion Wiktionary',
            'yi': u'װיקיװערטערבוך רעדן',
        }

        self.namespaces[100] = {
            '_default': u'Appendix',
            'bg': u'Словоформи',
            'bs': u'Portal',
            'cy': u'Atodiad',
            'fi': u'Liite',
            'fr': u'Annexe',
            'he': u'נספח',
            'it': u'Appendice',
            'ko': u'부록',
            'pl': u'Aneks',
            'pt': u'Apêndice',
            'ro': u'Portal',
            'ru': u'Приложение',
            'sr': u'Портал',
            'sv': u'WT',
        }
        self.namespaces[101] = {
            '_default': u'Appendix talk',
            'bg': u'Словоформи беседа',
            'bs': u'Razgovor o Portalu',
            'cy': u'Sgwrs Atodiad',
            'fi': u'Keskustelu liitteestä',
            'fr': u'Discussion Annexe',
            'he': u'שיחת נספח',
            'it': u'Discussioni appendice',
            'ko': u'부록 토론',
            'pl': u'Dyskusja aneksu',
            'pt': u'Apêndice Discussão',
            'ro': u'Discuţie Portal',
            'ru': u'Обсуждение приложения',
            'sr': u'Разговор о порталу',
            'sv': u'WT-diskussion',
        }

        self.namespaces[102] = {
            '_default': u'Concordance',
            'bs': u'Indeks',
            'cy': u'Odliadur',
            'de': u'Verzeichnis',
            'fr': u'Transwiki',
            'pl': u'Indeks',
            'pt': u'Vocabulário',
            'ro': u'Apendice',
            'ru': u'Конкорданс',
            'sv': u'Appendix',
        }

        self.namespaces[103] = {
            '_default': u'Concordance talk',
            'bs': u'Razgovor o Indeksu',
            'cy': u'Sgwrs Odliadur',
            'de': u'Verzeichnis Diskussion',
            'fr': u'Discussion Transwiki',
            'pl': u'Dyskusja indeksu',
            'pt': u'Vocabulário Discussão',
            'ro': u'Discuţie Apendice',
            'ru': u'Обсуждение конкорданса',
            'sv': u'Appendixdiskussion',
        }

        self.namespaces[104] = {
            '_default': u'Index',
            'bs': u'Dodatak',
            'cy': u'WiciSawrws',
            'fr': u'Portail',
            'pl': u'Portal',
            'pt': u'Rimas',
            'ru': u'Индекс',
        }

        self.namespaces[105] = {
            '_default': u'Index talk',
            'bs': u'Razgovor o Dodatku',
            'cy': u'Sgwrs WiciSawrws',
            'fr': u'Discussion Portail',
            'pl': u'Dyskusja portalu',
            'pt': u'Rimas Discussão',
            'ru': u'Обсуждение индекса',
        }

        self.namespaces[106] = {
            'en': u'Rhymes',
            'is': u'Viðauki',
            'pt': u'Portal',
            'ru': u'Рифмы',
        }

        self.namespaces[107] = {
            'en': u'Rhymes talk',
            'is': u'Viðaukaspjall',
            'pt': u'Portal Discussão',
            'ru': u'Обсуждение рифм',
        }

        self.namespaces[108] = {
            'en': u'Transwiki',
        }

        self.namespaces[109] = {
            'en': u'Transwiki talk',
        }

        self.namespaces[110] = {
            'en': u'Wikisaurus',
        }

        self.namespaces[111] = {
            'en': u'Wikisaurus talk',
        }

        self.namespaces[112] = {
            'en': u'WT',
        }

        self.namespaces[113] = {
            'en': u'WT talk',
        }

        # Other than most Wikipedias, page names must not start with a capital
        # letter on ALL Wiktionaries.

        self.nocapitalize = self.langs.keys()
    
        self.obsolete = {'nb':'no',
                    'minnan':'zh-min-nan',
                    'zh-tw':'zh',
                    'zh-cn':'zh'}
    
        # Which languages have a special order for putting interlanguage links,
        # and what order is it? If a language is not in interwiki_putfirst,
        # alphabetical order on language code is used. For languages that are in
        # interwiki_putfirst, interwiki_putfirst is checked first, and
        # languages are put in the order given there. All other languages are put
        # after those, in code-alphabetical order.
    
        self.interwiki_putfirst = {
            'en': self.alphabetic,
            'et': self.alphabetic,
            'fi': self.alphabetic,
            'fr': self.alphabetic,
            'he': ['en'],
            'hu': ['en'],
            'pl': self.alphabetic,
            'simple': self.alphabetic
            }
            
        self.languages_by_size = [
            'en', 'fr', 'vi', 'zh', 'io', 'el', 'pl', 'it', 'de', 'hu',
            'fi', 'nl', 'bg', 'pt', 'ku', 'es', 'gl', 'sr', 'id', 'sv',
            'et', 'ru', 'ko', 'tr', 'ja', 'sl', 'scn', 'fa', 'ar', 'no',
            'la', 'ta', 'zh-min-nan', 'he', 'hy', 'af', 'ro', 'da', 'ang', 'hi',
            'cs', 'sk', 'is', 'uk', 'co', 'ca', 'simple', 'st', 'fy', 'hr',
            'nds', 'csb', 'ky', 'kk', 'ia', 'gu', 'sq', 'sd', 'eo', 'lt',
            'cy', 'vo', 'ml', 'ie', 'th', 'yi', 'mk', 'bs', 'qu', 'am',
            'mr', 'be', 'rw', 'tl', 'eu', 'ms', 'ast', 'an', 'ga', 'pa',
            'nah', 'ha', 'oc'
            ]
        
        self.interwiki_on_one_line = ['pl']

        self.interwiki_attop = ['pl']

    def version(self, code):
        return "1.11"
    
    def shared_image_repository(self, code):
        return ('commons', 'commons')

