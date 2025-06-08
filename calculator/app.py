from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn import datasets
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from code_handle.codeHandle import code_api
from node_operations.LDAdiv import LDAdiv_api
from node_operations.covariance_calcu import covariance_api
from node_operations.data_projection import projection_api
from node_operations.eigenvalue_calcu import eigen_api
from node_operations.node_preprocess import preprocess_api
from node_operations.similarity_calculation import calculate_similarity_api

from node_operations.data_import import dataset_api
from node_operations.gradient_descent import gradient_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(dataset_api)
app.register_blueprint(gradient_api)
app.register_blueprint(eigen_api)
app.register_blueprint(covariance_api)
app.register_blueprint(code_api)
app.register_blueprint(calculate_similarity_api)
app.register_blueprint(preprocess_api)
app.register_blueprint(LDAdiv_api)
app.register_blueprint(projection_api)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
