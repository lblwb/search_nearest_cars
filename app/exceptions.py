from fastapi import (
    HTTPException,
    status
)


class SearchCarsException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class CargoCannotBeCreated(SearchCarsException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to create a cargo"


class IncorrectIDException(SearchCarsException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect ID"


class IncorrectCodeException(SearchCarsException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect zipcode"


class IncorrectPickupCodeException(SearchCarsException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect pickup zipcode"


class IncorrectDeliveryCodeException(SearchCarsException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect delivery zipcode"
