from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .request_kb import RequestKb
from tg_bot.types.request import RequestStatus


class RequestTeamKb(RequestKb):
    __method_get_all: str = "get_all"
    __method_get_by: str = "get_by"
    __method_set_status: str = "set_status"
    __method_moderation: str = "moderation"
    __method_view: str = "view"

    # Get
    __ib_get_all: InlineKeyboardButton = InlineKeyboardButton(text="Получить всё", callback_data="get_all?type=team")

    __ib_get_by_status_wait: InlineKeyboardButton = InlineKeyboardButton(text="В ожидании",
                                                                         callback_data="get_by?type=team&by=status&value=wait")
    __ib_get_by_status_success: InlineKeyboardButton = InlineKeyboardButton(text="Успешно",
                                                                            callback_data="get_by?type=team&by=status&value=success")
    __ib_get_by_status_process: InlineKeyboardButton = InlineKeyboardButton(text="В процессе",
                                                                            callback_data="get_by?type=team&by=status&value=process")
    __ib_get_by_status_cancel: InlineKeyboardButton = InlineKeyboardButton(text="Отменено",
                                                                           callback_data="get_by?type=team&by=status&value=cancel")
    __ib_get_by_status_fail: InlineKeyboardButton = InlineKeyboardButton(text="Провал",
                                                                         callback_data="get_by?type=team&by=status&value=fail")

    # Moderation
    __ib_moderation_yes: InlineKeyboardButton = InlineKeyboardButton(text="Да",
                                                                     callback_data="moderation?type=team&value=yes")
    __ib_moderation_no: InlineKeyboardButton = InlineKeyboardButton(text="Нет",
                                                                    callback_data="moderation?type=team&value=no")
    __ib_moderation_postpone: InlineKeyboardButton = InlineKeyboardButton(text="Нет",
                                                                          callback_data="moderation?type=team&value=postpone")

    # Set status
    __ib_set_status: InlineKeyboardButton = InlineKeyboardButton(text="Изменить статус",
                                                                 callback_data="set_status?type=team")

    __ib_confirm_set_yes: InlineKeyboardButton = InlineKeyboardButton(text="Да",
                                                                      callback_data="confirm_set?type=team&value=yes")
    __ib_confirm_set_no: InlineKeyboardButton = InlineKeyboardButton(text="Нет",
                                                                     callback_data="confirm_set?type=team&value=no")

    @staticmethod
    async def get_ib(text: str, method: str, request_type: str, request_id: str, status: str) -> InlineKeyboardButton:
        ib_moderation: InlineKeyboardButton = InlineKeyboardButton(text=text,
                                                                   callback_data=f"{method}?type={request_type}&status={status}&id={request_id}")
        return ib_moderation

    async def view(self, request_type: str, request_status: str, request_id: str) -> InlineKeyboardMarkup:
        view_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3)

        if request_status == RequestStatus.PROCESS or request_status == RequestStatus.WAIT:
            ib_moderation_yes: InlineKeyboardButton = await self.get_ib(text="Да",
                                                                        method=self.__method_moderation,
                                                                        request_type=request_type,
                                                                        request_id=request_id,
                                                                        status=RequestStatus.SUCCESS)
            ib_moderation_no: InlineKeyboardButton = await self.get_ib(text="Нет",
                                                                       method=self.__method_moderation,
                                                                       request_type=request_type,
                                                                       request_id=request_id,
                                                                       status=RequestStatus.FAIL)
            ib_moderation_postpone: InlineKeyboardButton = await self.get_ib(text="Отложить",
                                                                             method=self.__method_moderation,
                                                                             request_type=request_type,
                                                                             request_id=request_id,
                                                                             status=RequestStatus.WAIT)
            view_kb.add(ib_moderation_yes).add(ib_moderation_no).add(ib_moderation_postpone)
        else:
            ib_set_status: InlineKeyboardButton = await self.get_ib(text="Изменить статус",
                                                                    method=self.__method_set_status,
                                                                    request_type=request_type,
                                                                    request_id=request_id,
                                                                    status=RequestStatus.WAIT)
            view_kb.add(ib_set_status)

        return view_kb

    async def get_all(self, requests: list) -> InlineKeyboardMarkup:
        ikb_all_requests: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)

        for request in requests:
            request_text: str = f"{request.get('date')} {request.get('item').get('team_name')} {request.get('status')}"
            ib_request: InlineKeyboardButton = await self.get_ib(text=request_text,
                                                                 method=self.__method_view,
                                                                 request_type=request.get('type'),
                                                                 request_id=request.get('id'),
                                                                 status=request.get('status'))
            ikb_all_requests.add(ib_request)

        return ikb_all_requests

    async def get_by(self) -> InlineKeyboardMarkup:
        get_by_status_bs: list = [
            self.__ib_get_by_status_wait,
            self.__ib_get_by_status_success,
            self.__ib_get_by_status_process,
            self.__ib_get_by_status_cancel,
            self.__ib_get_by_status_fail
        ]

        ikb_get_by_status: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1).add(*get_by_status_bs)

        return ikb_get_by_status

    async def moderation(self) -> InlineKeyboardMarkup:
        pass

    async def set(self) -> InlineKeyboardMarkup:
        pass
