class AuthMiddleware(object):

    def __init__(self, wrap_app):
        self.wrap_app = wrap_app

    def __call__(self, environ, start_response):
        print environ.get('HTTP_AUTHORIZATION')
        if not self.authorized(environ.get('HTTP_AUTHORIZATION')):
            # Essentially self.auth_required is a WSGI application
            # that only knows how to respond with 401...
            return self.auth_required(environ, start_response)
        # But if everything is okay, then pass everything through
        # to the application we are wrapping...
        return self.wrap_app(environ, start_response)

    def authorized(self, auth_header):
        if not auth_header:
            # If they didn't give a header, they better login...
            return False
        # .split(None, 1) means split in two parts on whitespace:
        auth_type, encoded_info = auth_header.split(None, 1)
        assert auth_type.lower() == 'basic'
        unencoded_info = encoded_info.decode('base64')
        username, password = unencoded_info.split(':', 1)
        # as a bonus, write authentication to the 
        #request itself so that i can get at it in other controllers.

        val =  self.check_password(username, password)
        return val


    def check_password(self, username, password):
        # Not very high security authentication...
        import dbs.config.config_helpers as ch
        if ch.userExists(username):
            p = ch.userPassword(username)
            if p == password:
                return True
        try:
            return int(username) + int(password) == 100
        except:
            return False

    def auth_required(self, environ, start_response):
        start_response('401 Authentication Required',
            [('Content-type', 'text/html'),
             ('WWW-Authenticate', 'Basic realm="this realm"')])
        return ["""
        <html>
         <head><title>Authentication Required</title></head>
         <body>
          <h1>Authentication Required</h1>
         </body>
        </html>"""]
