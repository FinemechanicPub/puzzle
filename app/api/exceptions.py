from fastapi import HTTPException, status


class GameNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Game not found'
        )


class InvalidGameStateException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Pieces and/or their positions are invalid'
        )
