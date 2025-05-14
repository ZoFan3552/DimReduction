from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.backend import switch
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

app.register_blueprint(dataset_api)
app.register_blueprint(gradient_api)
app.register_blueprint(eigen_api)
app.register_blueprint(covariance_api)
app.register_blueprint(code_api)
app.register_blueprint(calculate_similarity_api)
app.register_blueprint(preprocess_api)
app.register_blueprint(LDAdiv_api)
app.register_blueprint(projection_api)


app.debug = True

CORS(app, origins=["http://localhost:7005"])


def load_dataset(dataset_name):
    """加载数据集"""
    if dataset_name == "iris":
        iris = datasets.load_iris()
        return iris.data.tolist()  # 转换为 Python 列表格式
    return []

def load_target(dataset_name):
    if dataset_name == "iris":
        iris = datasets.load_iris()
        return iris.target.tolist()  # 转换为 Python 列表格式
    return []


def apply_algorithm(algorithm, params, dataset):
    """根据算法和参数对数据集进行处理"""
    dataset_np = np.array(dataset)
    if algorithm == "t-SNE":
        tsne = TSNE(perplexity=params.get("perplexity", 30), n_iter=params.get("n_iter", 1000))
        result = tsne.fit_transform(dataset_np)
    elif algorithm == "PCA":
        pca = PCA(n_components=params.get("n_components", 2))
        result = pca.fit_transform(dataset_np)
    elif algorithm == "MDS":
        mds = MDS(n_components=params.get("n_components", 2))
        result = mds.fit_transform(dataset_np)
    else:
        result = dataset_np
    return result.tolist()

def calculate_variance(dataset, axis):
    """计算数据集的方差"""
    dataset_np = np.array(dataset)
    if axis == "x":
        return float(np.var(dataset_np[:, 0]))
    elif axis == "y":
        return float(np.var(dataset_np[:, 1]))
    return 0.0

def process_tree(node, dataset, target):
    """递归处理树节点"""
    if "algorithm" in node and node["algorithm"]:  # 非初始节点
        dataset = apply_algorithm(node["algorithm"], node.get("params", {}), dataset)
        node["dataset"] = dataset
        node["xVariance"] = calculate_variance(dataset, "x")
        # if dataset[0].length > 1:
        node["yVariance"] = calculate_variance(dataset, "y")
        # else:
        #     node["yVariance"] = 0
    elif "name" in node and node["name"] == "初始数据集":  # 初始节点
        node["dataset"] = dataset
        node["xVariance"] = calculate_variance(dataset, "x")
        node["yVariance"] = calculate_variance(dataset, "y")

    # 递归处理子节点
    if "children" in node and node["children"]:
        for child in node["children"]:
            process_tree(child, dataset, target)

@app.route('/api/process_tree', methods=['POST'])
def process_tree_endpoint():
    """处理整个树结构"""
    data = request.json
    dataset_name = data.get("datasetName", "")
    target = data.get("target", [])
    tree_data = data.get("treeData", {})

    # 加载数据集（仅适用于初始节点）
    dataset = load_dataset(dataset_name) if dataset_name else tree_data.get("dataset", [])
    target = load_target(dataset_name) if dataset_name else target.get("target", [])

    # 递归处理树
    process_tree(tree_data, dataset, target)
    print(tree_data)
    print(target)
    return jsonify({
        "treeData": tree_data,
        "target": target
    })













@app.route('/api/process_node', methods=['POST'])
def process_node():
    data = request.json
    # node_data = data['nodeData']
    operation = data['operation']['description']

    # switch(operation['description'])


    # elif operation == '相似度计算':
    #     return calculate_similarity(request)

    return '未能处理'


if __name__ == "__main__":
    app.run(port=5000)
