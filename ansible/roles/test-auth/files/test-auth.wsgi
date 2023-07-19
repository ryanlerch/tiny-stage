import os

os.environ["KRB5CCNAME"] = "/tmp/krb5cc-httpd"
os.environ["GSS_USE_PROXY"] = "yes"
os.environ["TESTAUTH_SETTINGS"] = "/home/vagrant/test-auth.conf.py"
os.environ["OIDC_CLIENT_SECRETS"] = "/home/vagrant/test-auth.client_secrets.json"

from test_auth import application
