# -*- coding: utf-8 -*-
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class ICollectiveVoltoFormsupportLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFormDataStore(Interface):
    def add(self, data):
        """
        Add data to the store

        @return: record id
        """

    def length(self):
        """
        @return: number of items stored into store
        """

    def search(self, query):
        """
        @return: items that match query
        """


class IPostEvent(Interface):
    """
    Event fired when a form is submitted (before actions)
    """


class ICaptchaSupport(Interface):
    def __init__(self, context, request):
        """Initialize adpater"""

    def verify(self, data):
        """Verify the captcha
        @return: True if verified, Raise exception otherwise
        """
