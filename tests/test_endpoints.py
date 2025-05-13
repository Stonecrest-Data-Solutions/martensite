import pytest
from martensite.server import app
from martensite_utils import proto_to_numpy, numpy_to_proto, message_pb2
import numpy as np


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def runner():
    return app.test_cli_runner()


def test_request_home(client):
    response = client.get("/")
    assert b"<p>Hello, World! This is a Martensite server</p>" in response.data


def test_request_inputs(client):
    response = client.get("/inputs")
    json_out = response.json[0]

    assert json_out["name"] == "input"
    assert json_out["shape"] == [1, 1, 32, 32]
    assert json_out["type"] == "tensor(float)"


def test_request_outputs(client):
    response = client.get("/outputs")
    json_out = response.json[0]

    assert json_out["name"] == "output"
    assert json_out["shape"] == [1, 10]
    assert json_out["type"] == "tensor(float)"


def test_request_inference(client):
    test_data = np.random.random((1, 1, 32, 32)).astype(np.float32)
    proto = numpy_to_proto(test_data)
    response = client.post(
        "/inference",
        data=proto.SerializeToString()
    )

    assert response.status_code == 200

    proto = message_pb2.NDArrayProto()
    proto.ParseFromString(response.data)
    returned_array = proto_to_numpy(proto)

    assert returned_array.shape == (1, 10)
    assert str(returned_array.dtype) == "float32"
