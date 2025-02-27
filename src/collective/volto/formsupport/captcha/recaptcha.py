from . import CaptchaSupport
from collective.volto.formsupport import _
from plone.formwidget.recaptcha.interfaces import IReCaptchaSettings
from plone.formwidget.recaptcha.norecaptcha import submit
from plone.registry.interfaces import IRegistry
from zExceptions import BadRequest
from zope.component import queryUtility
from zope.i18n import translate


class RecaptchaSupport(CaptchaSupport):
    def __init__(self, context, request):
        super().__init__(context, request)
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IReCaptchaSettings)

    def verify(self, data):
        if not self.settings.private_key:
            raise ValueError(
                "No recaptcha private key configured. Go to "
                "path/to/site/@@recaptcha-settings to configure."
            )
        if not data or not data.get("token"):
            raise BadRequest(
                translate(
                    _("No captcha token provided."),
                    context=self.request,
                )
            )
        token = data["token"]
        remote_addr = self.request.get("HTTP_X_FORWARDED_FOR", "").split(",")[0]
        if not remote_addr:
            remote_addr = self.request.get("REMOTE_ADDR")
        res = submit(token, self.settings.private_key, remote_addr)
        if not res.is_valid:
            raise BadRequest(
                translate(
                    _("The code you entered was wrong, please enter the new one."),
                    context=self.request,
                )
            )
