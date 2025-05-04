import numpy as np
from flask import Flask, request, Response
import onnxruntime as ort

from martensite_utils import proto_to_numpy, numpy_to_proto, NDArrayProto
from sympy.codegen.ast import float64

app = Flask(__name__)

session = ort.InferenceSession("src/model.onnx")

@app.route("/")
def hello_world():
    return "<p>Hello, World! This is a Martensite server</p>"

@app.route("/inference", methods=["POST"])
def inference():
    proto = NDArrayProto()
    proto.ParseFromString(request.data)

    nd_array = proto_to_numpy(proto)

    output = session.run(None, {'input': nd_array})

    new_proto = numpy_to_proto(output[0])

    resp = Response(
        new_proto.SerializeToString(),
        status=200,
        mimetype="application/octet-stream"
    )
    return resp

@app.route("/inputs", methods=["GET"])
def get_inputs():
    inputs = session.get_inputs()
    output_data = [
        {'name': inp.name, 'shape': inp.shape, 'type': inp.type} for inp in inputs
    ]
    return output_data

@app.route("/outputs", methods=["GET"])
def get_outputs():
    outputs = session.get_outputs()
    output_data = [
        {'name': out.name, 'shape': out.shape, 'type': out.type} for out in outputs
    ]

    return output_data
