import secrets
config = {
    'secrets-app_secret_key': secrets.token_hex(15),
    'pin': secrets.token_hex(10)
}