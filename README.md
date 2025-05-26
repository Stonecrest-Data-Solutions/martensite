# Summary

Martensite is a simple ONNX inference server that runs in a Docker container and allows you to
serve your AI models with a simple API powered by Flask and Gunicorn.

# Usage


## Docker Container

Martensite is run just like any other Docker container, but you have to add your ONNX model.
To add your model to the container, mount it as a Docker volume to `/model/model.onnx`. You
will also most likely want to forward the ports and to do that forward your desired IP/Port
to the container's port `8000`. Below is an example for running the Martensite container.

```commandline
docker run -p 127.0.0.1:8000:8000 -v ./mymodel.onnx:/model/model.onnx martensite
```

## API Endpoints

There are three main endpoints that Martensite has:

- `/inputs`: Returns information on the inputs of the model
- `/outputs`: Returns information on the outputs of the model
- `/inference`: Runs model inference when sent an array of data

### /inputs

This endpoint can be accessed with a simple `get` request. It will return JSON data that
contains the inputs name, shape, and type.

Returned JSON example:
```json
{
  "name": "input",
  "shape": [1, 32, 32, 1],
  "type": "float"
}
```

### /outputs

This endpoint can be accessed with a simple `get` request. It will return JSON data that
contains the outputs name, shape, and type

Returned JSON example:
```json
{
  "name": "output",
  "shape": [1, 10],
  "type": "float"
}
```

### /inference

This endpoint is used by sending a `POST` request that contains array data
using the protobuf format from `martensite_utils`. It then responds with the
results of the inference in the same protobuf format. An example of running
inference on a server is given below. The ONNX model loaded in the server
has an input shape of [10, 10] and a type of `float32`.

```python
import numpy as np
import requests
from martensite_utils.from_numpy import numpy_to_raw_proto
from martensite_utils.to_numpy import raw_proto_to_numpy

input_array = np.random.random((10, 10))
input_data = numpy_to_raw_proto(input_array)

response = requests.post(
    url="http://127.0.0.1:8000/inference",
    data=input_data
)

received_data = raw_proto_to_numpy(response.content)
print(f"Result: {received_data}")
```

## Limitations

Currently, Martensite can only handle single-input, single-output ONNX models.