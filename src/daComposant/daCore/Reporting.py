# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2021 EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

"""
    Gestion simple de rapports structurés créés par l'utilisateur.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import os.path

# ==============================================================================
# Classes de services non utilisateur

class _ReportPartM__(object):
    """
    Store and retrieve the data for C: internal class
    """
    def __init__(self, part="default"):
        self.__part    = str(part)
        self.__styles  = []
        self.__content = []

    def append(self, content, style="p", position=-1):
        if position == -1:
            self.__styles.append(style)
            self.__content.append(content)
        else:
            self.__styles.insert(position, style)
            self.__content.insert(position, content)
        return 0

    def get_styles(self):
        return self.__styles

    def get_content(self):
        return self.__content

class _ReportM__(object):
    """
    Store and retrieve the data for C: internal class
    """
    def __init__(self, part='default'):
        self.__document = {}
        self.__document[part] = _ReportPartM__(part)

    def append(self,  content, style="p", position=-1, part='default'):
        if part not in self.__document:
            self.__document[part] = _ReportPartM__(part)
        self.__document[part].append(content, style, position)
        return 0

    def get_styles(self):
        op = list(self.__document.keys()) ; op.sort()
        return [self.__document[k].get_styles() for k in op]

    def get_content(self):
        op = list(self.__document.keys()) ; op.sort()
        return [self.__document[k].get_content() for k in op]

    def clear(self):
        self.__init__()

class __ReportC__(object):
    """
    Get user commands, update M and V: user intertace to create the report
    """
    m = _ReportM__()

    def append(self, content="", style="p", position=-1, part="default"):
        return self.m.append(content, style, position, part)

    def retrieve(self):
        st = self.m.get_styles()
        ct = self.m.get_content()
        return st, ct

    def clear(self):
        self.m.clear()

class __ReportV__(object):
    """
    Interact with user and C: template for reports
    """

    default_filename="report.txt"

    def __init__(self, c):
        self.c = c

    def save(self, filename=None):
        if filename is None:
            filename = self.default_filename
        _filename = os.path.abspath(filename)
        #
        h = self.get()
        fid = open(_filename, 'w')
        fid.write(h)
        fid.close()
        return filename, _filename

    def retrieve(self):
        return self.c.retrieve()

    def __str__(self):
        return self.get()

    def close(self):
        del self.c
        return 0

# ==============================================================================
# Classes d'interface utilisateur : ReportStorage, ReportViewIn*
# Tags de structure : (title, h1, h2, h3, p, uli, oli, <b></b>, <i></i>)

ReportStorage = __ReportC__

class ReportViewInHtml(__ReportV__):
    """
    Report in HTML
    """

    default_filename="report.html"
    tags = {
        "oli":"li",
        "uli":"li",
        }

    def get(self):
        st, ct = self.retrieve()
        inuLi, inoLi = False, False
        pg = "<html>\n<head>"
        pg += "\n<title>Report in HTML</title>"
        pg += "\n</head>\n<body>"
        for k,ps in enumerate(st):
            pc = ct[k]
            try:
                ii = ps.index("title")
                title = pc[ii]
                pg += "%s\n%s\n%s"%('<hr noshade><h1 align="center">',title,'</h1><hr noshade>')
            except Exception:
                pass
            for i,s in enumerate(ps):
                c = pc[i]
                if s == "uli" and not inuLi:
                    pg += "\n<ul>"
                    inuLi = True
                elif s == "oli" and not inoLi:
                    pg += "\n<ol>"
                    inoLi = True
                elif s != "uli" and inuLi:
                    pg += "\n</ul>"
                    inuLi = False
                elif s != "oli" and inoLi:
                    pg += "\n</ol>"
                    inoLi = False
                elif s == "title":
                    continue
                for t in self.tags:
                    if s == t: s = self.tags[t]
                pg += "\n<%s>%s</%s>"%(s,c,s)
        pg += "\n</body>\n</html>"
        return pg

class ReportViewInRst(__ReportV__):
    """
    Report in RST
    """

    default_filename="report.rst"
    tags = {
        "p":["\n\n",""],
        "uli":["\n  - ",""],
        "oli":["\n  #. ",""],
        }
    titles = {
        # "title":["=","="],
        "h1":["","-"],
        "h2":["","+"],
        "h3":["","*"],
        }
    translation = {
        "<b>":"**",
        "<i>":"*",
        "</b>":"**",
        "</i>":"*",
        }

    def get(self):
        st, ct = self.retrieve()
        inuLi, inoLi = False, False
        pg = ""
        for k,ps in enumerate(st):
            pc = ct[k]
            try:
                ii = ps.index("title")
                title = pc[ii]
                pg += "%s\n%s\n%s"%("="*80,title,"="*80)
            except Exception:
                pass
            for i,s in enumerate(ps):
                c = pc[i]
                if s == "uli" and not inuLi:
                    pg += "\n"
                    inuLi = True
                elif s == "oli" and not inoLi:
                    pg += "\n"
                    inoLi = True
                elif s != "uli" and inuLi:
                    pg += "\n"
                    inuLi = False
                elif s != "oli" and inoLi:
                    pg += "\n"
                    inoLi = False
                for t in self.translation:
                    c = c.replace(t,self.translation[t])
                if s in self.titles.keys():
                    pg += "\n%s\n%s\n%s"%(self.titles[s][0]*len(c),c,self.titles[s][1]*len(c))
                elif s in self.tags.keys():
                    pg += "%s%s%s"%(self.tags[s][0],c,self.tags[s][1])
            pg += "\n"
        return pg

class ReportViewInPlainTxt(__ReportV__):
    """
    Report in plain TXT
    """

    default_filename="report.txt"
    tags = {
        "p":["\n",""],
        "uli":["\n  - ",""],
        "oli":["\n  - ",""],
        }
    titles = {
        # "title":["=","="],
        "h1":["",""],
        "h2":["",""],
        "h3":["",""],
        }
    translation = {
        "<b>":"",
        "<i>":"",
        "</b>":"",
        "</i>":"",
        }

    def get(self):
        st, ct = self.retrieve()
        inuLi, inoLi = False, False
        pg = ""
        for k,ps in enumerate(st):
            pc = ct[k]
            try:
                ii = ps.index("title")
                title = pc[ii]
                pg += "%s\n%s\n%s"%("="*80,title,"="*80)
            except Exception:
                pass
            for i,s in enumerate(ps):
                c = pc[i]
                if s == "uli" and not inuLi:
                    inuLi = True
                elif s == "oli" and not inoLi:
                    inoLi = True
                elif s != "uli" and inuLi:
                    inuLi = False
                elif s != "oli" and inoLi:
                    inoLi = False
                for t in self.translation:
                    c = c.replace(t,self.translation[t])
                if s in self.titles.keys():
                    pg += "\n%s\n%s\n%s"%(self.titles[s][0]*len(c),c,self.titles[s][1]*len(c))
                elif s in self.tags.keys():
                    pg += "\n%s%s%s"%(self.tags[s][0],c,self.tags[s][1])
            pg += "\n"
        return pg

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')