from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.communication.schemas.message import (
    MessageRepresentation,
    MessagesSearchResponse,
)
from samurai_backend.models.communication.message import MessageModel
from samurai_backend.utils.get_count import get_count

if TYPE_CHECKING:
    from pydantic.types import UUID4
    from sqlmodel import Session

    from samurai_backend.communication.schemas.message import MessagesSearchSchema


async def get_message(session: Session, message_id: UUID4) -> MessageModel:
    query = select(MessageModel).where(
        MessageModel.message_id == message_id,
    )

    return session.exec(query).first()


async def get_messages(
    session: Session,
    search_schema: MessagesSearchSchema,
) -> MessagesSearchResponse:
    query = select(MessageModel).where(
        MessageModel.chat_id == search_schema.chat_id,
    )

    if search_schema.file_only:
        query = query.where(MessageModel.file_id is not None)

    if search_schema.text:
        query = query.where(MessageModel.text.icontains(search_schema.text))

    if search_schema.sent_after:
        query = query.where(MessageModel.created_at >= search_schema.sent_after)
    if search_schema.sent_before:
        query = query.where(MessageModel.created_at <= search_schema.sent_before)

    if search_schema.descending:
        query = query.order_by(MessageModel.created_at.desc())
    else:
        query = query.order_by(MessageModel.created_at)

    total = get_count(session, query)
    query = query.offset(search_schema.offset).limit(search_schema.page_size)

    messages = session.exec(query)

    return MessagesSearchResponse(
        content=[
            MessageRepresentation.model_validate(message, from_attributes=True)
            for message in messages
        ],
        meta=MessagesSearchResponse.construct_meta(
            total=total,
            page=search_schema.page,
            page_size=search_schema.page_size,
        ),
    )
