"""
Shared repositories for database access.

Lambda functions should ONLY import from this module.
They should NEVER import from shared.models or shared.database directly.

:Authors:
    - Pablo Contreras

:Created:
    - 2025/01/19
"""

from .user_repository import UserRepository
from .skill_repository import SkillRepository
from .project_repository import ProjectRepository
from .employer_repository import EmployerRepository
from .job_type_repository import JobTypeRepository
from .work_repository import WorkRepository

__all__ = [
    "UserRepository",
    "SkillRepository",
    "ProjectRepository",
    "EmployerRepository",
    "JobTypeRepository",
    "WorkRepository",
]
