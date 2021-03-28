import typing as typ
from functools import wraps

from werkzeug.exceptions import HTTPException
from flask import request, Response, Blueprint, Flask, g as flask_g
from flask.testing import FlaskClient


class HdrAuthTokenError(RuntimeError):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class APIClass:
    """base class for all API classes"""
    endpoint: 'APIEndpoint' = None


class APIEndpoint:
    """
    - The APIEndpoint is instantiated ONCE for an entire API.
    - The instance is initialized with the API blueprint, And, the authorization info
    - The rule() decorator is called for each API endpoint during module startup, IOW, BEFORE the endpoint is called.
    It sets up the endpoint.  See the rule() decorator, below.  Each endpoints "rules" are persisted in the
    "rules_dict" - the key is the endpoint name.
    - The on_call() decorator is called whenever the endpoint is called.  It retrieves the "rules" for the endpoint
    and applies those rules, some before the endpoint is called, and some after it is called.  See on_call()
    """

    def __init__(self, blueprint: Blueprint, valid_auth_token=None, header_key='Authorization'):
        """
        :param Blueprint blueprint: used in the rule decorator
        :param valid_auth_token: for simple UUID-type authorizations, It declares the expected, "valid" auth_token
        :param header_key: if the auth_token is being passed in the header, declares the expected header key
        """
        self.blueprint = blueprint
        self.header_key = header_key
        self.valid_auth_token = valid_auth_token
        self.rules_dict: typ.Dict[str, dict] = {}

    def rule(self, routes, params: typ.List[str] = None, validators: typ.Dict[str, dict] = None, **options):
        """
        rule decorator: this decorator runs when the module is being setup (before the endpoint is called).
         - it declares any needed validators (see the validators param, below)
         - it calls the Blueprint's add_url_rule which eliminates the need for its route() decorator.
         - it remembers the Blueprint method; which is used in the test_endpoint(),
        :param routes: relative path from the Blueprint's url_prefix to the endpoint
        :param list params: describes expected, possible parameters
        :param dict validators: defines validators for the endpoint's params, request data or response data
        :param options: standard Blueprint kwargs
        """
        def decorator(func):
            func_name = func.__name__

            if params:
                param_dict = {}
                for param in params:
                    if isinstance(param, dict):
                        param_dict.update(param)
                    else:
                        param_dict[param] = None

                self.rules_dict[func_name] = {
                    'methods': options.get('methods'),
                    'params': param_dict,
                    'validators': validators}

            endpoint = options.pop("endpoint", func_name)
            route_list = routes if isinstance(routes, list) else [routes]
            for route in route_list:
                self.blueprint.add_url_rule(route, endpoint, func, **options)
            return func
        return decorator

    def on_call(self):
        """
        on_call decorator: this decorator is called whenever the endpoint is called.  It executes decorator rules -
        some before and some after the endpoint is called
        """
        def endpoint_wrapper(decorated_func):
            @wraps(decorated_func)
            def func_wrapper(*args, **kwargs):
                try:

                    func_name = decorated_func.__name__
                    flask_g.my_func_name = func_name
                    self.validate_hdr_auth_token()  # security first...
                    # request jdata validator
                    # request param, arg validator

                    response = decorated_func(*args, **kwargs)

                    if isinstance(response, Response):
                        return response  # it's an error or other non-200 response

                    # response jdata validator

                    return Response(response, status=200, headers={'content-type': 'application/json'})
                except HTTPException as http_err:
                    return Response(
                        F'Exception in {decorated_func.__name__}. XCP: {str(http_err)}', status=http_err.code)
                except HdrAuthTokenError as hdr_err:
                    return Response(
                        F'Exception in {decorated_func.__name__}. XCP: {str(hdr_err)}', status=401)
                except Exception as e:
                    return Response(
                        F'Exception in {decorated_func.__name__}. XCP: {str(e)}', status=400)
            return func_wrapper
        return endpoint_wrapper

    def get_params(self, *names):
        args = self.cast_args(request.args)
        targs = (args[name] if name in args else None for name in names)
        return targs

    def cast_args(self, req_args: dict):
        """
        Query parameters are declared in the rules decorator for ALL API endpoints and stored in a dictionary
        where the key is the function name. This method searches the caller's query parameters
        for any that match the ones declared in rules.  If found, it will attempt to cast it
        to the types defined in the rules
        :param req_args: this is k, v dict of the query parameters (aka args) supplied by the caller.
        :return:
        """
        func_name = flask_g.my_func_name
        # retrieve from the rules dict the functions parameter rules (if any)
        if 'params' in self.rules_dict[func_name]:
            param_defs = self.rules_dict[func_name].get('params')
            # get the caller-supplied query params & values
            cargs = dict(req_args.copy())  # copy as dict because args are immutable
            for k, v in cargs.items():
                # if there is a rule, and the rule defines an expected type
                if param_defs.get(k) and v:
                    # cast the query value to the rule's type
                    # python bool() function casting always return True for non empty string.
                    # https://stackoverflow.com/questions/21732123/convert-true-false-value-read-from-file-to-boolean?lq=1
                    if param_defs[k] == bool:
                        cargs[k] = v.lower() == 'true'
                    else:
                        cargs[k] = param_defs[k](v)
            return cargs  # ones that had a matching rule now are of the expected type
        else:  # No rules
            return req_args

    def validate_hdr_auth_token(self):
        """
        If the APIEndpoint instance is initialized with a "valid_auth_token", the endpoint requires
        an auth_token that must be validated
        """
        if self.valid_auth_token:
            auth_token = request.headers.get(self.header_key)
            if not auth_token:
                raise HdrAuthTokenError('Authorization Token is required', status_code=403)
            if auth_token != self.valid_auth_token:
                raise HdrAuthTokenError('Authorization token is invalid', status_code=401)

    def test_endpoint(self, view_func, flapp: Flask, variables=None, auth_token=None, **kwargs):
        assert variables is None or isinstance(variables, list)
        """
        generic test method that takes advantage of the rules and attributes already defined in
        this APIEndpoint instance:
         - from the API's blueprint - the url_prefix
         - from the endpoint's rules_dict, the method
         - the header_key from the instance attributes
        :param view_func: the endpoint which the caller wishes to call
        :param variables: the endpoint variable as a list (if any)
        :param auth_token:
        :param kwargs:
        :return:
        """
        # using Flask's app test_client() method...
        fclient: FlaskClient = flapp.test_client()

        methods = self.rules_dict[view_func]['methods']
        if 'GET' in methods:
            fclient_func = fclient.get
        elif 'POST' in methods:
            fclient_func = fclient.post
        elif 'PUT' in methods:
            fclient_func = fclient.put
        elif 'PATCH' in methods:
            fclient_func = fclient.patch
        elif 'DELETE' in methods:
            fclient_func = fclient.delete
        else:
            raise ValueError(F'Unknown methods: {methods}')

        headers = {'content-type': 'application/json'}
        if auth_token:
            headers[self.header_key] = auth_token

        rule = F"{self.blueprint.url_prefix}/{view_func}"

        var_path = '/'.join(str(var) for var in variables) if variables else variables
        rule = F'{rule}/{var_path}' if var_path else rule

        response = fclient_func(rule, query_string=kwargs, headers=headers)
        return response
