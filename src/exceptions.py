from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class Error(Exception):
    def __init__(self, *, msg=None, error_trace=None):
        ''' Custom base class for app exceptions '''

        super(Error, self).__init__(msg)

        self.message = msg
        self.error_trace = error_trace


class CredentialsException(Error):
    def __init__(self, *, msg=None, error_trace=None):
        '''Custom exception for invalid JWT Credentials'''

        super(CredentialsException, self).__init__(
            msg=msg or "Invalid credentials",
            error_trace=error_trace,
        )


class ItemNotFound(Error):
    def __init__(self, *, msg=None, error_trace=None):
        ''' Custom common class for an item not found exception'''

        super(ItemNotFound, self).__init__(
            msg=msg or "Item not found",
            error_trace=error_trace
        )


def register_error_handlers(app: FastAPI):
    @app.exception_handler(CredentialsException)
    def _(_: Request, exception: CredentialsException):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"}, content={"message": exception.message})

    @app.exception_handler(ItemNotFound)
    def _(_: Request, exception: ItemNotFound):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": exception.message})
