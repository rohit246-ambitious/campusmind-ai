from sqlalchemy.orm import Query


def paginate(query: Query, page: int, limit: int):
    """
    Generic pagination helper for SQLAlchemy queries
    """

    # 1. Ensure page number is valid
    if page < 1:
        page = 1

    # 2. Ensure limit is valid
    if limit < 1:
        limit = 10

    # 3. Calculate how many records to skip
    offset = (page - 1) * limit

    # 4. Apply pagination to the query
    return query.offset(offset).limit(limit).all()
