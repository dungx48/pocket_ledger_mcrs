from service.authentication_service import AuthenticationService

class AuthenticationController:
    def __init__(self):
        self.auth_service = AuthenticationService(secret_key="your_secret_key")

    def login(self, username, password):
        return self.auth_service.authenticate(username, password)

    def logout(self):
        return self.auth_service.logout()