import requests

host = 'https://www.amazon.com/ap/oa'
client_id = 'amzn1.application-oa2-client.eff87481021541f18fb1dab9620f8b68'
client_secret = 'b37150c8aa6f117e43975d07074444c2771194924f14ec10f3a39af3986b3cac'
scope = 'alexa%3Avoice_service%3Apre_auth+alexa%3Aall'
scope_data = '%7B%22alexa%3Aall%22%3A%7B%22productID%22%3A%22telexi%22%2C%22productInstanceAttributes%22%3A%7B%22deviceSerialNumber%22%3A%2212345%22%7D%7D%7D'
response_type = 'code'
state = '6042d10f-6bcd-49'
redirect_uri = 'https%3A%2F%2Flocalhost'

url = '{}?client_id={}&scope={}&scope_data={}&response_type={}&state={}'.format(host, client_id, scope, scope_data,
                                                                                response_type, state)
scope_data2 = {
  "alexa:all": {
    "productID": "telexi",
    "productInstanceAttributes": {
        "deviceSerialNumber": "abc123"
    }
  }
}


def make_post():
    response = requests.post(url)
    print(response.status_code)
    print(response)
    print(response.text)
    print(response.content)


make_post()