from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from authors.models import Author


class AuthorService:
    def __init__(self, session: Session):
        self.session = session

    def check_author_exists(self, author_id: int, raise_exception: False) -> bool | None:
        exist = bool(self.session.query(Author).filter_by(id=author_id).first())
        if raise_exception and not exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No author id {author_id}')
        return exist
