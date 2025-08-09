from aiogram.fsm.state import StatesGroup, State


# TaskFilters(offset=0, limit=config.page_limit, project_id=project_id)
# class BrowseState(State):
#     def __init__(self, state = None, group_name = None):
#         super().__init__(state, group_name)
#         self.filters: BaseFilters | None
#         self.fetch: Callable


class UserBrowse(StatesGroup):
    menu = State()
    my_projects = State()
    my_tasks_menu = State()
    my_tasks_author = State()
    my_tasks_assign = State()
