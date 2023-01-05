import json
import datetime
import logging
import hashlib
import uuid
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler

from validators import ValidateRequiredField
from fields import (
    CharField,
    EmailField,
    PhoneField,
    DateField,
    BirthDayField,
    GenderField,
    ClientIDsField,
    ArgumentsField,
)
from scoring import get_score, get_interests

SALT = "Otus"
ADMIN_LOGIN = "admin"
ADMIN_SALT = "42"
OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
INVALID_REQUEST = 422
INTERNAL_ERROR = 500
ERRORS = {
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    INVALID_REQUEST: "Invalid Request",
    INTERNAL_ERROR: "Internal Server Error",
}
UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}

ADMIN_SCORE = 42


class ClientsInterestsRequest:
    client_ids = ClientIDsField(required=True, nullable=False)
    date = DateField(required=False, nullable=True)

    def __init__(self, *args, **kwargs):
        if len(args):
            self.client_ids = self.get_value_from_args(args, 0)
            self.date = self.get_value_from_args(args, 1)

        else:
            self.client_ids = self.get_value_from_kwargs(kwargs, 'client_ids')
            self.date = self.get_value_from_kwargs(kwargs, 'date')

    def __str__(self):
        return f'client_ids={self.client_ids}' \
               f'\ndate={self.date}'

    @staticmethod
    def get_value_from_kwargs(kwargs, key):
        """ Получить значение из kwargs"""
        if key in kwargs:
            return kwargs.get(key)

        # если значения нет, то вернуть RequiredField RequiredFieldNoneValue
        return ValidateRequiredField.RequiredFieldNoneValue()

    @staticmethod
    def get_value_from_args(args, index):
        """ Получить значение из args"""
        if len(args) > index:
            return args[index]

        # если значения нет, то вернуть RequiredFieldNoneValue
        return ValidateRequiredField.RequiredFieldNoneValue()


class OnlineScoreRequest:
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)

    def __init__(self, *args, **kwargs):
        if len(args):
            self.first_name = self.get_value_from_args(args, 0)
            self.last_name = self.get_value_from_args(args, 1)
            self.email = self.get_value_from_args(args, 2)
            self.phone = self.get_value_from_args(args, 3)
            self.birthday = self.get_value_from_args(args, 4)
            self.gender = self.get_value_from_args(args, 5)

        else:
            self.first_name = self.get_value_from_kwargs(kwargs, 'first_name')
            self.last_name = self.get_value_from_kwargs(kwargs, 'last_name')
            self.email = self.get_value_from_kwargs(kwargs, 'email')
            self.phone = self.get_value_from_kwargs(kwargs, 'phone')
            self.birthday = self.get_value_from_kwargs(kwargs, 'birthday')
            self.gender = self.get_value_from_kwargs(kwargs, 'gender')

    def __str__(self):
        return f'first_name={self.first_name}, last_name={self.last_name}' \
               f'\ngender={self.gender}' \
               f'\nemail={self.email}' \
               f'\nphone={self.phone}' \
               f'\nbirthday={self.birthday}'

    @staticmethod
    def get_value_from_kwargs(kwargs, key):
        """ Получить значение из kwargs"""
        if key in kwargs:
            return kwargs.get(key)

        # если значения нет, то вернуть RequiredField RequiredFieldNoneValue
        return ValidateRequiredField.RequiredFieldNoneValue()

    @staticmethod
    def get_value_from_args(args, index):
        """ Получить значение из args"""
        if len(args) > index:
            return args[index]

        # если значения нет, то вернуть RequiredFieldNoneValue
        return ValidateRequiredField.RequiredFieldNoneValue()


class MethodRequest:
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN

    def __init__(self, *args, **kwargs):
        if len(args):
            self.account = self.get_value_from_args(args, 0)
            self.login = self.get_value_from_args(args, 1)
            self.token = self.get_value_from_args(args, 2)
            self.arguments = self.get_value_from_args(args, 3)
            self.method = self.get_value_from_args(args, 4)

        else:
            self.account = self.get_value_from_kwargs(kwargs, 'account')
            self.login = self.get_value_from_kwargs(kwargs, 'login')
            self.token = self.get_value_from_kwargs(kwargs, 'token')
            self.arguments = self.get_value_from_kwargs(kwargs, 'arguments')
            self.method = self.get_value_from_kwargs(kwargs, 'method')

    def __str__(self):
        return f'account={self.account}, login={self.login}' \
               f'\ntoken={self.token}' \
               f'\narguments={self.arguments}' \
               f'\nmethod={self.method}'

    def get_fill_arguments(self):
        return [arg for arg in self.arguments]

    @staticmethod
    def get_value_from_kwargs(kwargs, key):
        """ Получить значение из kwargs"""
        if key in kwargs:
            return kwargs.get(key)

        # если значения нет, то вернуть RequiredField RequiredFieldNoneValue
        return ValidateRequiredField.RequiredFieldNoneValue()

    @staticmethod
    def get_value_from_args(args, index):
        """ Получить значение из args"""
        if len(args) > index:
            return args[index]

        # если значения нет, то вернуть RequiredFieldNoneValue
        return ValidateRequiredField.RequiredFieldNoneValue()


def check_auth(request):
    if request.is_admin:
        digest = hashlib.sha512(
            (datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode()
        ).hexdigest()
    else:
        digest = hashlib.sha512(
            (request.account + request.login + SALT).encode()
        ).hexdigest()
    if digest == request.token:
        return True
    return False


def service_online_score(model, store, ctx):
    score_data = OnlineScoreRequest(**model.arguments)

    if (score_data.phone and score_data.email) or \
        (score_data.last_name and score_data.first_name) or \
        (score_data.birthday and (score_data.gender or score_data.gender == 0)):

        ctx.update({'has': model.get_fill_arguments()})

        if model.is_admin:
            return {"score": ADMIN_SCORE}, OK

        score = get_score(
            store,
            score_data.phone,
            score_data.email,
            score_data.birthday,
            score_data.gender,
            score_data.first_name,
            score_data.last_name,
        )
        return {"score": score}, OK

    return {
        "code": INVALID_REQUEST,
        "error": "Essential arguments are empty"
    }, INVALID_REQUEST


def service_clients_interests(model, store, ctx):
    interests_data = ClientsInterestsRequest(**model.arguments)

    ctx.update({'nclients': len(interests_data.client_ids) if interests_data.client_ids else 0})

    response_data = {id: get_interests(store, None) for id in interests_data.client_ids}

    return response_data, OK


def method_handler(request, ctx, store):
    data = request.get('body', {})
    try:
        model = MethodRequest(**data)

        if not check_auth(model):
            return {
                "code": FORBIDDEN,
                "error": "Forbidden"
            }, FORBIDDEN

        if model.method == 'online_score':
            return service_online_score(model, store, ctx)

        elif model.method == 'clients_interests':
            return service_clients_interests(model, store, ctx)

        return {
            "code": INVALID_REQUEST,
            "error": "Method isn't defined"
        }, BAD_REQUEST

    except Exception as e:
        return {
            "code": INVALID_REQUEST,
            "error": str(e)
        }, INVALID_REQUEST


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = None

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except Exception:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path]({"body": request, "headers": self.headers}, context, self.store)
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
        context.update(r)
        logging.info(context)
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-l", "--log", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
