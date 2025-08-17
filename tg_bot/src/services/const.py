from src.services.projects import get_project_page
from src.services.tasks import get_task_page


HANDEL_PAGE_CALLBACKS = {
    "get_task_page": get_task_page,
    "get_project_page": get_project_page,
}
