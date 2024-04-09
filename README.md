# AWS Worker Template Project

This is a template repository for creating AWS workers. It includes a standardized file structure and setup for managing AWS workers, along with a pre-configured GitHub Actions workflow.

## Project Structure

The project is structured as follows:

```plaintext
.
├── .env
├── .github
│   └── workflows
│       ├── image-ecr-lambda-deployment.yml
│       └── unit-test.yml
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── src
│   ├── __init__.py
│   └── app.py
└── test
    └── __init__.py
```

## Configuration

Before running the application, ensure that you configure the following placeholder values:

- `.env`: Update the required environment variables to match your AWS configuration.
- `image-ecr-lambda-deployment.yml`: Provide values for the `ecr_name` and `lambda_names` after creating the necessary resources in AWS.

NOTE: please reference the AWS.md for information on creating these resources.

```yml
with:
  ecr_name: your-ecr # update value
  lambda_names: 'your-lambda-one,your-lambda-two' # update value(s)
```

## Usage

1. Create a new repository from the template on GitHub:

   - Navigate to the GitHub repository page (e.g., <https://github.com/lgcypower/lgcy-worker-template>).
   - Click on the "Use this template" button.
   - Follow the on-screen instructions to create a new repository from the template.

   <br />

2. Clone the newly created repository onto your local machine:

```bash
git clone https://github.com/lgcypower/new-worker-directory.git
```

3. Navigate to the project directory:

```bash
cd new-worker-directory
```

4. Create a Virtual Environment (Optional, but highly recomended):

- Conda

```bash
CONDA_ENV_NAME="your_env_name"
PYTHON_VERSION=3.11
conda create -n ${CONDA_ENV_NAME} python=${PYTHON_VERSION} anaconda
conda activate ${CONDA_ENV_NAME}
```

- Venv

```bash
python -m venv .venv
source .venv/bin/activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
GITHUB_USERNAME="replace with your username"
GITHUB_TOKEN="replace with your token"
pip install git+https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/lgcypower/lgcy-utils.git
```

6. Configure the environment variables in the `.env` file.

7. Run the application:

```bash
python src/app.py
```

## How to Run Tests

To run the tests, execute the following command:

```bash
python -m pytest test/
```

with verbose output

```bash
python -m pytest test/ -vv
```

## Updating the README

Update the README.md file with documentation specific to your new worker to provide clear instructions and information about its functionalities.

Consider including the following sections in your documentation:

- `Overview`: Provide a brief overview of the worker's purpose and key functionalities.
- `Configuration`: Explain the required environment variables and configurations for the worker to function correctly.
- `Usage`: Describe how to use the worker, including any specific input requirements and expected output.
- `Examples`: Provide usage examples or use cases to illustrate the worker's capabilities.
- `Troubleshooting`: Include a troubleshooting section to address common issues and solutions.

## Imports

Getting all imports to work across local testing, lambda environment executions, and tests has raised some challenges. The following is what we have found to work across all environments.

### app.py imports

This needs to be conditionally set to work when trying to run locally and in the lambda environment. This is already configured in the template and we recommend to use the following format.

```py
# app.py

if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    from src.helpers import function_1, YourClass
else:
    from helpers import function_1, YourClass

# helpers.__init__.py
from .function_1 import function_1
from .your_class import YourClass
# notice the relative import format used here. You will get import errors if this is not used.
```

The following would also work

```py
if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    from src.helpers.function_1 import function_1
    from src.helpers.your_class import YourClass
else:
    from helpers.function_1 import function_1
    from helpers.your_class import YourClass

# File Structure
# helpers/
# - __init__.py
# - function_1.py
# - your_class.py
```

## helper directory imports

Items shared between files inside your helper directory should use relative imports.

```py
# File Structure
# helpers/
# - __init__.py
# - function_1.py
# - your_class.py


# __init__.py
from .function_1 import function_1

# function_1.py
from .your_class import YourClass
```

### test imports

Test files should use absolute imports from the root of the project. The same applies to any

```py
# test/my_test.py
from src.helpers.function_1 import function_1

with open("./test/fixtures/incoming_message.json", "r") as fixture_json:
  fixture = json.load(fixture_json)

@patch("src.helpers.function_file.function_1", return_value=None)
def test_function():
  pass
```
