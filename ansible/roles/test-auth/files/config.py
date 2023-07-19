SECRET_KEY = "ohsosecret"
OIDC_CLIENT_SECRETS = "/home/vagrant/client_secrets.json"
OIDC_SCOPES = [
    "openid",
    "email",
    "profile",
    "https://id.fedoraproject.org/scope/groups",
    "https://id.fedoraproject.org/scope/agreements",
]
OPENID_ENDPOINT = "https://tinystage.tinystage.test/idp/openid/"
FAS_OPENID_ENDPOINT = OPENID_ENDPOINT
