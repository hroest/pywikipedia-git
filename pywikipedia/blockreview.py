#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
This is not a complete bot; rather, it is a template from which simple
bots can be made. You can rename it to mybot.py, then edit it in
whatever way you want.

The following parameters are supported:

-dry              If given, doesn't do any real changes, but only shows
                  what would have been changed.

All other parameters will be regarded as part of the title of a single page,
and the bot will only work on that single page.
"""
#
# (C) xqt, 2010
#
__version__ = '$Id: basic.py 7845 2009-12-30 17:02:05Z xqt $'
#
import wikipedia as pywikibot
import userlib

# This is required for the text that is shown when you run this script
# with the parameter -help.

class BlockreviewBot:
    # notes
    note_admin = {
        'de': u"\n\n== Sperrprüfungswunsch ==\nHallo %(admin)s, \n\n[[%(user)s]] wünscht diePrüfung seiner/ihrer Sperre vom %(time)s über die Dauer von %(duration)s. Kommentar war ''%(comment)s''. Bitte äußere Dich dazu auf der [[%(usertalk)s#%(section)s|Diskussionsseite]]. -~~~~"
    }
    
    note_project = {
        'de': u"\n\n== [[%(user)s]] ==\n* gesperrt am %(time)s durch {{Benutzer|%(admin)s}} für eine Dauer von %(duration)s.\n* Kommentar war ''%(comment)s''.\n* [[Benutzer:%(admin)s]] wurde [[Benutzer Diskussion:%(admin)s#Sperrprüfungswunsch|benachrichtigt]].\n* [[%(usertalk)s#%(section)s|Link zur Diskussion]]\n:<small>-~~~~</small>\n;Antrag entgegengenommen"
    }

    # edit summary
    msg_admin = {
        'de': u'Bot-Benachrichtigung: Sperrprüfungswunsch von [[%(user)s]]',
    }

    unblock_tpl = {
        'de' : u'Benutzer:TAXman/Sperrprüfungsverfahren',
    }

    project_name = {
        'de' : u'Benutzer:TAXman/Sperrprüfung Neu'
        'pt' : u'Wikipedia:Pedidos a administradores/Discussão de bloqueio'
    }

    def __init__(self, dry):
        """
        Constructor. Parameters:
            * generator - The page generator that determines on which pages
                          to work on.
            * dry       - If True, doesn't do any real changes, but only shows
                          what would have been changed.
        """
        self.site = pywikibot.getSite()
        self.dry = dry
        self.info = None
        self.parts = None

    def run(self):
        try:
            genPage = pywikibot.Page(self.site,
                                     self.unblock_tpl[self.site.lang],
                                     defaultNamespace=10)
        except KeyError:
            pywikibot.output(u'ERROR: Language "%s" not supported by this bot.'
                             % self.site.lang)
        else:
            for page in genPage.getReferences(follow_redirects=False,
                                              withTemplateInclusion=True,
                                              onlyTemplateInclusion=True):
                if page.namespace() == 3:
                    self.treat(page)
                else:
                    pywikibot.output(u'Ignoring %s, user namespace required'
                                     % page.aslink())

    def treat(self, userPage):
        """
        Loads the given page, does some changes, and saves it.
        """
        talkText = self.load(userPage)
        if not talkText:
            return
        unblock_tpl = self.unblock_tpl[self.site.lang]
        project_name = self.project_name[self.site.lang]
        user = userlib.User(self.site, userPage.titleWithoutNamespace())
        saveAdmin = saveProject = False
        talkComment = None
        for templates in userPage.templatesWithParams():
            if templates[0] == unblock_tpl:
                self.getInfo(user)
                # Sperrprüfung ist neu eingetragen.
                # Sperrenden Admin benachrichtigen.
                if templates[1]==[] or templates[1][0]==u'1':
                    if self.info['action'] == 'block' or user.isBlocked():
                        admin = userlib.User(self.site, self.info['user'])
                        adminPage = admin.getUserTalkPage()
                        adminText = adminPage.get()
                        note = pywikibot.translate(self.site.lang,
                                                   self.note_admin) % self.parts
                        comment = pywikibot.translate(self.site.lang,
                                                      self.msg_admin) % self.parts
                        adminText += note
                        self.save(adminText, adminPage, comment, False)
                        talkText = talkText.replace(u'{{%s}}'   % unblock_tpl,
                                                    u'{{%s|2}}' % unblock_tpl)
                        talkText = talkText.replace(u'{{%s|1}}' % unblock_tpl,
                                                    u'{{%s|2}}' % unblock_tpl)
                        talkComment = u'Bot: Administrator [[Benutzer:%(admin)s|%(admin)s]] für Sperrprüfung benachrichtigt' \
                                      % self.parts
    
                        #testPage = pywikibot.Page(self.site, 'Benutzer:Xqt/Test')
                        #test = testPage.get()
                        #test += note
                        #self.save(test, testPage, '[[WP:BA#SPP-Bot|SPPB-Test]]')
                    else:
                        # nicht blockiert. Fall auf DS abschließen
                        talkText = talkText.replace(u'{{%s}}'   % unblock_tpl,
                                                    u'{{%s|4}}' % unblock_tpl)
                        talkText = talkText.replace(u'{{%s|1}}' % unblock_tpl,
                                                    u'{{%s|4}}' % unblock_tpl)
                        talkComment = u'Bot: Sperrprüfung abgeschlossen. Benutzer ist entsperrt.'
                # Admin ist benachrichtigt.
                # 2 Stunden warten, dann eintrag auf Projektseite
                elif templates[1][0]==u'2':
                    if self.info['action'] == 'block' or user.isBlocked():
                        # todo: Wartezeit einplanen
                        #       prüfen, ob Eintrag schon vorhanden
                        project = pywikibot.Page(self.site, project_name)
                        projText = project.get()
                        note = pywikibot.translate(self.site.lang,
                                                   self.note_project) % self.parts
                        comment = pywikibot.translate(self.site.lang,
                                                      self.msg_admin) % self.parts
                        projText += note
                        self.save(projText, project, comment, botflag = False)
                        talkText = talkText.replace(u'{{%s|2}}' % unblock_tpl,
                                                    u'{{%s|3}}' % unblock_tpl)
                        talkComment = u'Bot: [[%s|Wikipedia:Sperrprüfung]] eingetragen' \
                                      % project_name
                    else:
                        # nicht blockiert. Fall auf DS abschließen
                        talkText = talkText.replace(u'{{%s|2}}' % unblock_tpl,
                                                    u'{{%s|4}}' % unblock_tpl)
                        talkComment = u'Bot: Sperrprüfung abgeschlossen. Benutzer ist entsperrt.'
                elif templates[1][0]==u'3':
                    if self.info['action'] == 'block' or user.isBlocked():
                        pass
                    else:
                        # nicht blockiert. Fall auf DS abschließen
                        talkText = talkText.replace(u'{{%s|3}}' % unblock_tpl,
                                                    u'{{%s|4}}' % unblock_tpl)
                        talkComment = u'Bot: Sperrprüfung abgeschlossen. Benutzer ist entsperrt.'
                elif templates[1][0]==u'4':
                    # nothing left to do
                    pass
            else:
                # wrong template found
                pass
            
        if talkComment:
            self.save(talkText, userPage, talkComment)

    def getInfo(self, user):
        if not self.info:
            self.info = self.site.logpages(1, mode='block',
                                           title=user.getUserPage().title(),
                                           dump=True).next()
            self.parts = {
                'admin'    : self.info['user'],
                'user'     : self.info['title'],
                'usertalk' : user.getUserTalkPage().title(),
                'section'  : u'Sperrprüfung',
                'time'     : self.info['timestamp'],
                'duration' : self.info['block']['duration'],
                'comment'  : self.info['comment'],
            }
        

    def load(self, page):
        """
        Loads the given page, does some changes, and saves it.
        """
        try:
            # Load the page
            text = page.get()
        except pywikibot.NoPage:
            pywikibot.output(u"Page %s does not exist; skipping."
                             % page.aslink())
        except pywikibot.IsRedirectPage:
            pywikibot.output(u"Page %s is a redirect; skipping."
                             % page.aslink())
        else:
            return text
        return None

    def save(self, text, page, comment, minorEdit=True, botflag=True):
        if text != page.get():
            # Show the title of the page we're working on.
            # Highlight the title in purple.
            pywikibot.output(u"\n\n>>> \03{lightpurple}%s\03{default} <<<"
                             % page.title())
            # show what was changed
            pywikibot.showDiff(page.get(), text)
            pywikibot.output(u'Comment: %s' %comment)
            if not self.dry:
                choice = pywikibot.inputChoice(u'Do you want to accept these changes?', ['Yes', 'No'], ['y', 'N'], 'N')
                if choice == 'y':
                    try:
                        # Save the page
                        page.put(text, comment=comment, minorEdit=minorEdit, botflag=botflag)
                    except pywikibot.LockedPage:
                        pywikibot.output(u"Page %s is locked; skipping."
                                         % page.aslink())
                    except pywikibot.EditConflict:
                        pywikibot.output(
                            u'Skipping %s because of edit conflict'
                            % (page.title()))
                    except pywikibot.SpamfilterError, error:
                        pywikibot.output(
u'Cannot change %s because of spam blacklist entry %s'
                            % (page.title(), error.url))
                    else:
                        return True
        return False

def main():
    # If dry is True, doesn't do any real changes, but only show
    # what would have been changed.
    dry = show = False

    # Parse command line arguments
    for arg in pywikibot.handleArgs():
        if arg == "-dry":
            dry = True
        else:
            show = True

    if not show:
        # The preloading generator is responsible for downloading multiple
        # pages from the wiki simultaneously.
        bot = BlockreviewBot(dry)
        bot.run()
    else:
        pywikibot.showHelp()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
