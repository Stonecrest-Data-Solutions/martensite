import requests
import numpy as np
from martensite_utils import numpy_to_proto, proto_to_numpy, message_pb2

URL = "http://localhost:8000"


def test_home_page():
    response = requests.get(URL + "/")
    assert response.status_code == 200


def test_inputs():
    response = requests.get(URL + "/inputs")
    json_out = response.json()[0]

    assert json_out["name"] == "input"
    assert json_out["shape"] == [1, 1, 32, 32]
    assert json_out["type"] == "tensor(float)"


def test_outputs():
    response = requests.get(URL + "/outputs")
    json_out = response.json()[0]

    assert json_out["name"] == "output"
    assert json_out["shape"] == [1, 10]
    assert json_out["type"] == "tensor(float)"


def test_inference():
    test_data = np.random.random((1, 1, 32, 32)).astype(np.float32)
    proto = numpy_to_proto(test_data)
    response = requests.post(
        URL + "/inference",
        data=proto.SerializeToString()
    )

    assert response.status_code == 200

    proto = message_pb2.NDArrayProto()
    proto.ParseFromString(response.content)
    returned_array = proto_to_numpy(proto)

    assert returned_array.shape == (1, 10)
    assert str(returned_array.dtype) == "float32"
