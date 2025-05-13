# Testing Process

This document describes the testing process for Martensite. As Martensite is a web server that runs in a Docker
container it takes a few steps to test correctly and currently isn't fully automated. As such These are the steps that
must be taken in order to ensure the best possible product. It is advisable that each PR includes a copy of
**test_checklist.md** that is used in conjunction with a run of tests to ensure that the tests were passed correctly.

**NOTE:** All commands are assumed to be run from the project root.

## Setup

First, put a symlink to `./test_files/model.onnx` at `/model/model.onnx` as
this is where the server expects the model to be located (and where it will
be located in the Docker container).

```shell
sudo mkdir /model && sudo ln -s ./test_files/model.onnx /model/model.onnx
```

This will enable `test_endpoints.py` to run with Pytest.

## Automated Endpoint Testing

This step tests the Flask server endpoints but not within the Docker container. It ensures that the Flask server is
responding to requests correctly and with the correct information.

```shell
pytest tests/test_endpoints.py
```

Ensure that all tests pass and if not, investigate the failures.

## Docker Build Testing

Next, we want to ensure that the Docker container builds correctly.

```shell
docker build -t martensite:{TESTID} .
```

Ensure that the container builds correctly, as it will be used in the next step.

## Docker Container Testing

Now we will test a running container. First, start the container.

```shell
docker run --rm -p 127.0.0.1:8000:8000 -v tests/test_files/model.onnx:/model/model.onnx martensite:{TESTID}
```

Then from a different container, run the test script.

```shell
pytest tests/test_docker_integration.py
```

Ensure that all tests pass.

## Tear Down

Those conclude the tests for Martensite. You can clean up your environment by:

1. Remove the directory and link at `/model/model.onnx`
2. Stop and remove the Martensite Test container
3. Delete the Martensite test build from your Docker store