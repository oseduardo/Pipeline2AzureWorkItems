import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import OAuth2Error
from requests.auth import HTTPBasicAuth

client_id = "77EFB79A-99CA-4485-BF0F-5E469FE24B5D"
client_secret = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im9PdmN6NU1fN3AtSGpJS2xGWHo5M3VfVjBabyJ9.eyJjaWQiOiI3" \
                "N2VmYjc5YS05OWNhLTQ0ODUtYmYwZi01ZTQ2OWZlMjRiNWQiLCJjc2kiOiI2M2ViNWY1OS01YzMxLTQzN2QtYWRmNi1hM2E5M" \
                "mVjNTAzMDEiLCJuYW1laWQiOiJhNGMzNmVjNi01ZmNkLTY0NjYtYmU1Mi1iZjBhMTI2M2JmZDYiLCJpc3MiOiJhcHAudnN0b2" \
                "tlbi52aXN1YWxzdHVkaW8uY29tIiwiYXVkIjoiYXBwLnZzdG9rZW4udmlzdWFsc3R1ZGlvLmNvbSIsIm5iZiI6MTYwODU2ODk" \
                "yMywiZXhwIjoxNzY2MzM1MzIzfQ.JKN8opuv-xNb1xUxfWl6dwhR8gh77yFg0V7RmGzO9QFq5F14AOIWpsVDHRM4Gi3_Wue07" \
                "qV1r30CukQpWYd20OLIvZYzr4O4UVB5-5q54Ou1hxaVBczVorAuuG_zJUa0PDfY_yuu2LmeUlDVmmSLr7Ibx5B9gbq7i7mpT3" \
                "HzRAnlbxY0eDc0UaMrBvuwKFJeGmHdzxsAlAp9oUVNVZ1mcgZP7Pr02txjKIDwJ9ssRSQu4NbvxjM8OHZcv4ozos6LtB9kK1d" \
                "LZOoo23zaqQirgkR-DsCglwSuANNcg8RsQPp5e1_KsKcPGrl-nHwYEVqbdfcPUpLqqJzdcZ7SiuWegQ"
scope = ["vso.work_full"]
redirect_uri = "https%3A%2F%2Fwww.veracode.com"
authorize_url = "https://app.vssps.visualstudio.com/oauth2/authorize?response_type=Assertion" \
                "&client_id=" + client_id + "&scope=" + "vso.work_full" + "&redirect_uri=" + redirect_uri
token_url = "https://app.vssps.visualstudio.com/oauth2/token"
auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im9PdmN6NU1fN3AtSGpJS2xGWHo5M3VfVjBabyJ9.eyJhdWkiOiJjNWY0Y" \
            "zdhNC03NDQ5LTRmYWMtYTkzNi04ZTM2YWM1YjVkZGMiLCJuYW1laWQiOiJhNGMzNmVjNi01ZmNkLTY0NjYtYmU1Mi1iZjBhMTI2M2J" \
            "mZDYiLCJzY3AiOiJ2c28ud29ya19mdWxsIHZzby5hdXRob3JpemF0aW9uX2dyYW50IiwiaXNzIjoiYXBwLnZzdG9rZW4udmlzdWFsc" \
            "3R1ZGlvLmNvbSIsImF1ZCI6ImFwcC52c3Rva2VuLnZpc3VhbHN0dWRpby5jb20iLCJuYmYiOjE2MTIyOTk3MzMsImV4cCI6MTYxMjM" \
            "wMDYzM30.wzL6RAJ4Scj2_rzPWvGL35bTz58cZHd9qNa9zBGwJ-1IjLcRUaZ0WnDBjYJVC9Q3ROTEcUL_T4OnagDJAAeMZHFWbQ_eS" \
            "5VQ-7tAeN7oK9SVPBv2SHDr7ZNVLZyg2VNw7mbj4om32YHbC7OAGrFOEBnq952E6Rq2joAcYWLKUOYhLMuaaEtMUMXJ_q69I_jBg-Z" \
            "pei64R7JCg7fuwSYMRxO3ramJR3ZBbLbfr_GIUh3L2O5eQN6_wXheydUvM4yRccWYwectglBApHptpwU2m597GGsOxu6RAfT6DrspS" \
            "PzuZOGLAoNBVVfuYi3jS-xHIZIo1QTe6LSelteyKqbFdQ"
auth_response = "https://www.veracode.com/?code=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im9PdmN6NU1fN3AtSGpJS2x" \
                "GWHo5M3VfVjBabyJ9.eyJhdWkiOiJjNWY0YzdhNC03NDQ5LTRmYWMtYTkzNi04ZTM2YWM1YjVkZGMiLCJuYW1laWQiOiJhNGMz" \
                "NmVjNi01ZmNkLTY0NjYtYmU1Mi1iZjBhMTI2M2JmZDYiLCJzY3AiOiJ2c28ud29ya19mdWxsIHZzby5hdXRob3JpemF0aW9uX2" \
                "dyYW50IiwiaXNzIjoiYXBwLnZzdG9rZW4udmlzdWFsc3R1ZGlvLmNvbSIsImF1ZCI6ImFwcC52c3Rva2VuLnZpc3VhbHN0dWRp" \
                "by5jb20iLCJuYmYiOjE2MTIyOTk3MzMsImV4cCI6MTYxMjMwMDYzM30.wzL6RAJ4Scj2_rzPWvGL35bTz58cZHd9qNa9zBGwJ-" \
                "1IjLcRUaZ0WnDBjYJVC9Q3ROTEcUL_T4OnagDJAAeMZHFWbQ_eS5VQ-7tAeN7oK9SVPBv2SHDr7ZNVLZyg2VNw7mbj4om32YHb" \
                "C7OAGrFOEBnq952E6Rq2joAcYWLKUOYhLMuaaEtMUMXJ_q69I_jBg-Zpei64R7JCg7fuwSYMRxO3ramJR3ZBbLbfr_GIUh3L2O" \
                "5eQN6_wXheydUvM4yRccWYwectglBApHptpwU2m597GGsOxu6RAfT6DrspSPzuZOGLAoNBVVfuYi3jS-xHIZIo1QTe6LSeltey" \
                "KqbFdQ"
token_request_body = "client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer" \
                     "&grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&client_assertion=" + client_secret + \
                     "&assertion=" + auth_code + "&redirect_uri=" + redirect_uri

client = BackendApplicationClient(client_id=client_id, scope=scope)
oauth = OAuth2Session(client=client)
#authorization_response = oauth.get(authorize_url)
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "1500"
}

try:
    token = oauth.fetch_token(token_url, body=token_request_body, headers=headers, include_client_id=True, client_secret=client_secret)
except(OAuth2Error, requests.exceptions.RequestException) as e:
    print token

#auth_params = {'client_id': client_id, 'scope': scope, 'redirect_uri': 'https%3A%2F%2Fwww.veracode.com'}
print token

#token = oauth.fetch_token(token_url=token_url, include_client_id=client_id, client_secret=client_secret)
#print auth_url
#print state

#    token = oauth.fetch_token(token_url, body=token_request_body, headers=headers, include_client_id=True, client_secret=client_secret)
