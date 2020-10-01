import requests
import json
import configparser

class AtHock:
    def __init__(self, client_id, client_secret,username, password, org, base_url):
        self.org = org
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = 'password'
        self.username = username
        self.password = password
        self.acr_values = 'tenant:' + org
        self.scope = 'openid profile athoc.iws.web.api'
        self.base_url = base_url
        self.token_url = '/AuthServices/Auth/connect/token'
        self.oauth_url = self.base_url + self.token_url
        self.publish_url  = "{}/api/v2/orgs/{}/alerts".format(self.base_url, self.org)

    def get_bearer_token(self):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type" : self.grant_type,
            "username" : self.username,
            "password" : self.password,
            "acr_values" : self.acr_values,
            "scope" : self.scope
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(self.oauth_url, data=payload, headers=headers)
        return response

    def publish_alert(self, token, template_common_name, title, body, link):
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "TemplateCommonName": template_common_name,
            "Content": {
                "Title": title,
                "Body": body,
                "InfoLink": link,
            }
        }
        response = requests.post(self.publish_url, json=payload, headers=headers)
        return response