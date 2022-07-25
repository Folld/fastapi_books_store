from sqlalchemy.orm import Session
from authors.models import Author
from authors.schemas import AuthorOut, AuthorCreate, AuthorUpdate


class AuthorService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_authors(self, offset: int | None = None, limit: int | None = None):
        return self.session.query(Author).offset(offset).limit(limit).all()

    def create_author(self, author: AuthorCreate) -> AuthorOut:
        author_orm = Author(**author.dict())
        self.session.add(author_orm)
        self.session.commit()
        return AuthorOut.from_orm(author_orm)

    def update_author(self, author: AuthorUpdate) -> AuthorOut:
        author_orm = self.session.query(Author).filter_by(id=author.id)
        author_orm.update(author.dict(exclude_none=True))
        self.session.commit()
        return AuthorOut.from_orm(author_orm.first())
