import numpy as np
import requests

from martensite_utils import post_numpy_array, proto_to_numpy, NDArrayProto


if __name__ == '__main__':

    resp = requests.get("http://127.0.0.1:8000/inputs")
    inputs_meta = resp.json()
    print(inputs_meta)

    resp = requests.get("http://127.0.0.1:8000/outputs")
    outputs_meta = resp.json()
    print(outputs_meta)

    test_array = np.random.random(inputs_meta[0]["shape"])

    infer_resp = post_numpy_array(test_array.astype(np.float32), "http://127.0.0.1:8000/inference")

    out_proto = NDArrayProto()
    out_proto.ParseFromString(infer_resp.content)
    out_array = proto_to_numpy(out_proto)

    print(f"Inference Results:\n\t{out_array}\n")
