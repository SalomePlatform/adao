#-*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
#
# This file is part of SALOME ADAO module
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

__author__="AndrÃ© Ribes - EDF R&D"

class DevelException(Exception):
    def __init__(self, message):
        """Canonical constructor"""
        Exception.__init__(self,message)

#
# ==============================================================================
# Interface of an eficas observer (for implementing the subject/observer pattern)
# ==============================================================================
#
from .enumerate import Enumerate

class EficasObserver:
    """
    This class specifies the interface of an eficas observer. See example at the
    bottom of this file.
    """
    def processEficasEvent(self, eficasWrapper, eficasEvent):
        """
        This function should be implemented in the concrete Observer.
        @param eficasWrapper the instance of the source EficasWrapper
        @param eficasEvent the emitted event (instance of EficasEvent)
        """
        raise DevelException("processEficasEvent not implemented yet")

class EficasEvent:
    EVENT_TYPES=Enumerate([
        'CLOSE',
        'SAVE',
        'CLOSE',
        'OPEN',
        'REOPEN',
        'NEW',
        'TABCHANGED'
    ])

    def __init__(self,eventType,callbackId=None):
        """
        Creates an eficas event to be used by an EficasWrapper to notify an
        EficasObserver.

        The eventType depends of the context of creation. It specify the nature
        of the event inside EficasWrapper that triggers the creation of this instance.

        The callbackId is an object used by the EficasObserver to map the
        notification (this received event) with the initial event (callback)
        This object can be anything and has to be defined through a convention
        that both the EficasWrapper and the EficasObserver can understand.
        Typically, the eficas observer set the callback id to the eficas wrapper
        before running the asynchronous show. Then, when an event is raised by
        the eficas wrapper toward its observer, it embeds the callback id so that
        the observer can match the received event to the initial trigger context.

        @param the eventType to be choosen in the EVENT_TYPES
        @param callbackId an arbitrary data object
        """
        if not self.EVENT_TYPES.isValid(eventType):
            raise DevelException("The event type "+str(eventType)+" is not defined")

        self.eventType = eventType
        self.callbackId = callbackId
