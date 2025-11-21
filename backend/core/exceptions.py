from fastapi import HTTPException, status

def not_found(detail="Not found"):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

def bad_request(detail="Bad request"):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

def unauthorized(detail="Unauthorized"):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
