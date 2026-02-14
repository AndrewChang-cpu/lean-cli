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

from json import load
from pathlib import Path

json_modules = {}
file_name = "modules-1.14.json"
directory = Path(__file__).parent
file_path = directory.parent / file_name

# Prefer local bundled file; do not fetch from QuantConnect CDN when file exists (local-only friendly).
if file_path.is_file():
    with open(file_path, encoding="utf-8") as f:
        data = load(f)
        json_modules = data["modules"]
else:
    # Optional: try to fetch from CDN once when file is missing (e.g. first run before bundling).
    error = None
    try:
        import requests
        res = requests.get(f"https://cdn.quantconnect.com/cli/{file_name}", timeout=5)
        if res.ok:
            data = res.json()
            file_path.parent.mkdir(parents=True, exist_ok=True)
            from json import dump
            with open(file_path, "w", encoding="utf-8") as f:
                dump(data, f, ensure_ascii=False, indent=4)
            json_modules = data["modules"]
        else:
            res.raise_for_status()
    except Exception as e:
        error = str(e)
    if not json_modules:
        error_message = f": {error}" if error else ""
        raise FileNotFoundError(
            f"Modules file not found at {file_path}. "
            f"Bundle {file_name} in the lean package directory or ensure the CDN is reachable.{error_message}"
        )
