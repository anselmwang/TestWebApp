# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:27:55 2016

@author: yuwan
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import Imp

import cherrypy


class App:
    @cherrypy.expose
    def Add(self, a, b):
        return Imp.json.dumps((int(a)+int(b),))
        
cherrypy.quickstart(App())
    
    