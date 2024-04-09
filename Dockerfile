ARG PYTHON_VERSION=3.11
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}
# Install the function's dependencies using file requirements.txt
# from your project folder.
ARG GITHUB_TOKEN
ARG GITHUB_USERNAME

COPY requirements.txt  .
RUN yum install -y git
RUN pip install --upgrade pip
RUN pip3 install "git+https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/lgcypower/lgcy-utils.git"
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
# Copy function code
COPY src/ ${LAMBDA_TASK_ROOT}/src

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "src/app.handler" ]