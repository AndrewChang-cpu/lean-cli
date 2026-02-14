# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from click import argument

from lean.click import LeanCommand
from lean.commands import lean
from lean.container import container
from lean.constants import PROJECT_CONFIG_FILE_NAME


def _resolve_project_path(project: str) -> Path:
    """Resolve project name or path to a local project directory.

    :param project: project name (directory name under CLI root) or path to project directory
    :return: path to the project directory
    :raises RuntimeError: if the project cannot be found locally
    """
    project_path = Path(project)
    if project_path.is_absolute() or project_path.exists():
        # Treat as path
        if project_path.is_file():
            project_path = project_path.parent
        if (project_path / PROJECT_CONFIG_FILE_NAME).is_file():
            return project_path
        raise RuntimeError(f"'{project}' is not a valid project directory (no {PROJECT_CONFIG_FILE_NAME} found).")

    # Treat as project name: look under CLI root
    cli_root = container.lean_config_manager.get_cli_root_directory()
    candidate = cli_root / project
    if candidate.is_dir() and (candidate / PROJECT_CONFIG_FILE_NAME).is_file():
        return candidate
    raise RuntimeError(f"Project '{project}' was not found. Looked for directory '{candidate}' with {PROJECT_CONFIG_FILE_NAME}.")


@lean.command(cls=LeanCommand, requires_lean_config=True, name="project-delete", aliases=["delete-project"])
@argument("project", type=str)
def delete_project(project: str) -> None:
    """Delete a project locally.

    The project is selected by name or path to the project directory.
    """
    project_manager = container.project_manager
    logger = container.logger

    project_path = _resolve_project_path(project)
    project_manager.delete_project(project_path)
    logger.info(f"Successfully deleted project '{project_path}'")
