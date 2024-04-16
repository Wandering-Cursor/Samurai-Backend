from sqlalchemy import func
from sqlmodel import Session
from sqlmodel.sql.expression import SelectOfScalar


def get_count(
    session: Session,
    q: SelectOfScalar,
    join: bool = True,
) -> int:
    count_q = q.with_only_columns(func.count()).order_by(None)
    if join:
        count_q = count_q.select_from(*q.froms)

    iterator = session.exec(count_q)
    for count in iterator:
        return count
    return 0
