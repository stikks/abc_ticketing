import json
from datetime import datetime
import six

from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden, HttpResponse
from django.core import serializers

from rest_framework import status, response, decorators
from rest_framework.authtoken.models import Token
from bson import json_util, ObjectId
from rest_framework.compat import SHORT_SEPARATORS, LONG_SEPARATORS, INDENT_SEPARATORS
from rest_framework.renderers import JSONRenderer

from . import models, forms, serializers


def is_request_authenticated(fxn):
    def wrap(request, *args, **kwargs):

        key = request.META.get('HTTP_X_AUTH_TOKEN')

        if not key:
            return HttpResponseForbidden()

        token = Token.objects.filter(key=key).first()

        if token:
            return fxn(request, token.user.id, **kwargs)

        return HttpResponseForbidden()

    wrap.__name__ = fxn.__name__
    wrap.__doc__ = fxn.__doc__

    return wrap


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONRenderer(JSONRenderer):
    """
    update json renderer
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        ret = json.dumps(
            data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            separators=separators, default=json_util.default
        )

        if isinstance(ret, six.text_type):
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))
        return ret


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = CustomJSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@decorators.api_view(['POST'])
def authenticate_user(request):
    """
        authenticates user and generate authorization token
    """
    form = forms.LoginForm(json.loads(request.body))

    if form.is_valid():
        user = authenticate(**form.cleaned_data)
        if not user:
            return response.Response({'error': 'Invalid username/password combination'},
                                     status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        account = models.Account.objects.get(user_ptr=user)

        return response.Response({'token': token.key, 'user': {
            'first_name': account.first_name, 'middle_name': account.middle_name, 'email': account.email,
            'last_name': account.last_name, 'mobile_number': account.mobile_number, 'username': account.username,
            'state_of_correspondence': account.state_of_correspondence
        }}, status=status.HTTP_200_OK)

    return response.Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['POST'])
def register_user(request):
    """
    register new user account
    :param request:
    :return:
    """
    form = forms.RegistrationForm(json.loads(request.body))

    if form.is_valid():
        user = models.Account.objects.create_user(**form.cleaned_data)

        return response.Response({'message': "User with id - {} has been created".format(user.id)},
                                 status=status.HTTP_201_CREATED)

    return response.Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['GET'])
@is_request_authenticated
def dashboard(request, user_id):
    """
    retrieve therapy sessions
    :param request:
    :param user_id:
    :return:
    """
    account = models.Account.objects.get(user_ptr_id=user_id)
    voucher_requests = account.voucher_requests.all()
    discount_vouchers = account.discount_vouchers.all()

    voucher_data = [dict(date_created=d.date_created, code=d.code) for d in discount_vouchers]
    request_data = [dict(date_created=c.date_created, status=c.status, rejection_reason=c.rejection_reason)
                    for c in voucher_requests]

    return response.Response({'voucher_requests': request_data, 'discount_vouchers': voucher_data})
