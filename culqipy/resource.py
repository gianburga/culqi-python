import culqipy
import requests
import json


class Util:
    def json_result(self, key, url, data, method):
        headers = {
            "Authorization": "Bearer " + key,
            "content-type": "application/json"
        }
        r = ""
        if method.upper() == "GET":
            if not data:
                r = requests.get(
                    culqipy.API_URL + url,
                    headers=headers,
                    timeout=60
                )
            else:
                r = requests.get(
                    culqipy.API_URL + url,
                    headers=headers,
                    params=data,
                    timeout=60
                )
        if method.upper() == "POST":
            r = requests.post(
                    culqipy.API_URL + url,
                    headers=headers,
                    data=data,
                    timeout=60
                )
        if method.upper() == "DELETE":
            r = requests.delete(
                    culqipy.API_URL + url,
                    headers=headers,
                    timeout=60
                )
        return r.json()


class ObjectHelper:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Balance:
    URL = "/balances/"

    def list(self, params):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL,
                params, "GET")

    def get(self, id):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL + id + "/",
                "", "GET")

Balance = Balance()


class Iins:
    URL = "/iins/"

    def get(self, id):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL + id + "/",
                "", "GET")

Iins = Iins()


class CulqiError(Exception):
    def __init__(self, message=None, error_code=None, detail=None):
        super(CulqiError, self).__init__(message)
        self.detail = detail
        self.error_code = error_code

class TokenError(CulqiError):
    pass

class TokenValidationError(TokenError):
    pass

class ChargeError(CulqiError):
    pass

class ChargeOperationDeniedError(CulqiError):
    pass


class Token:
    URL = "/tokens/"

    @classmethod
    def create(cls, card_number, currency_code, cvv, exp_month, exp_year,
               fingerprint, last_name, email, first_name):
        token = ObjectHelper()
        token.card_number = card_number
        token.currency_code = currency_code
        token.cvv = cvv
        token.expiration_month = exp_month
        token.expiration_year = exp_year
        token.fingerprint = fingerprint
        token.last_name = last_name
        token.email = email
        token.first_name = first_name
        response = Util().json_result(culqipy.COD_COMMERCE, cls.URL, token.to_json(), "POST")

        if response['object'] == 'error':
            raise TokenValidationError(error_code=response['code'], message=response['message'])
        return response

    @classmethod
    def get(cls, id):
        url = '{url}{id}/'.format(url=cls.URL, id=id)
        return Util().json_result(culqipy.API_KEY, url, "", "GET")


# Token = Token()


class Charge:
    URL = "/charges/"

    @classmethod
    def list(cls, params):
        return Util().json_result(culqipy.API_KEY, cls.URL, params, "GET")

    @classmethod
    def create(cls, address, address_city, amount, country_code,
               currency_code, email, first_name, installments,
               last_name, metadata, phone_number,
               product_description, token_id):
        charge = ObjectHelper()
        charge.address = address
        charge.address_city = address_city
        charge.amount = amount
        charge.country_code = country_code
        charge.currency_code = currency_code
        charge.email = email
        charge.first_name = first_name
        charge.installments = installments
        charge.last_name = last_name
        charge.metadata = metadata
        charge.phone_number = phone_number
        charge.product_description = product_description
        charge.token_id = token_id

        response = Util().json_result(culqipy.API_KEY, cls.URL, charge.to_json(), "POST")
        if response['object'] == 'error':
            if response['type'] == 'operacion_denegada':
                raise ChargeOperationDeniedError(
                    message=response['message'], error_code=response['code'], detail={
                        'error': response['user_message'],
                        'raw': response
                    })
            raise ChargeError(message=response['message'], error_code=response['code'], detail={
                'error': response['user_message'],
                'raw': response
            })
        return response

    @classmethod
    def get(cls, id):
        return Util().json_result(culqipy.API_KEY, cls.URL + id + "/", "", "GET")

# Charge = Charge()


class Plan:
    URL = "/plans/"

    def list(self, params):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL,
                params, "GET")

    def create(self, alias, amount, currency_code, interval,
               interval_count, limit, name, trial_days):
        plan = ObjectHelper()
        plan.alias = alias
        plan.amount = amount
        plan.currency_code = currency_code
        plan.interval = interval
        plan.interval_count = interval_count
        plan.limit = limit
        plan.name = name
        plan.trial_days = trial_days
        return Util().json_result(
                culqipy.API_KEY,
                self.URL,
                plan.to_json(), "POST")

    def get(self, id):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL + id + "/",
                "", "GET")

Plan = Plan()


class Subscription:
    URL = "/subscriptions/"

    def list(self, params):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL,
                params, "GET")

    def create(self, address, address_city, country_code, email,
               last_name, first_name, phone_number, plan_alias,
               token_id):
        subscription = ObjectHelper()
        subscription.address = address
        subscription.address_city = address_city
        subscription.country_code = country_code
        subscription.email = email
        subscription.last_name = last_name
        subscription.first_name = first_name
        subscription.phone_number = phone_number
        subscription.plan_alias = plan_alias
        subscription.token_id = token_id
        return Util().json_result(
                culqipy.API_KEY,
                self.URL,
                subscription.to_json(), "POST")

    def delete(self, id):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL + id + "/",
                "", "DELETE")

    def get(self, id):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL + id + "/",
                "", "GET")

Subscription = Subscription()


class Refund:
    URL = "/refunds/"

    def list(self, params):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL,
                params, "GET")

    def create(self, amount, charge_id, reason):
        refund = ObjectHelper()
        refund.amount = amount
        refund.charge_id = charge_id
        refund.reason = reason
        return Util().json_result(
                culqipy.API_KEY,
                self.URL,
                refund.to_json(), "POST")

    def get(self, id):
        return Util().json_result(
                culqipy.API_KEY,
                self.URL + id + "/",
                "", "GET")

Refund = Refund()
