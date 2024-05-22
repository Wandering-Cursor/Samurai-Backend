from sqlmodel import Session, func
from sqlmodel.sql.expression import SelectOfScalar


def get_count(
    session: Session,
    q: SelectOfScalar,
) -> int:
    count_q = q.with_only_columns(func.count()).order_by(None)
    iterator = session.exec(count_q)
    for count in iterator:
        return count
    return 0
