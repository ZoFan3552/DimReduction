from flask import Flask, request, jsonify, Blueprint
from sklearn import datasets
import numpy as np
import pandas as pd
import tempfile
import os
from sklearn.datasets import fetch_openml

from utils.jsonProcess import make_json_safe

dataset_api = Blueprint('dataset_api', __name__)

# 加载经典数据集的函数映射
DATASETS = {
    'iris': datasets.load_iris,
    'wine': datasets.load_wine,
    'breast_cancer': datasets.load_breast_cancer,
    'digits': datasets.load_digits,
    'boston': fetch_openml(name='boston', version=1, as_frame=True),
    'mnist_small': lambda: load_mnist_small()  # 自定义函数加载MNIST小样本
}


# boston = fetch_openml(name='boston', version=1, as_frame=True)

def load_mnist_small():
    """加载MNIST数据集的小样本版本"""
    from sklearn.datasets import fetch_openml
    from sklearn.utils import Bunch

    # 获取MNIST数据集的一小部分
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True, parser='auto')
    X = X[:2000]  # 只取前2000个样本
    y = y[:2000]

    return Bunch(
        data=X,
        target=y.astype(int),
        feature_names=[f'pixel_{i}' for i in range(X.shape[1])],
        target_names=np.unique(y),
        DESCR="MNIST手写数字数据集(小样本版)"
    )


def format_dataset_preview(dataset):
    """
    将数据集格式化为前端可用的预览格式

    Args:
        dataset: sklearn数据集对象或自定义数据集

    Returns:
        dict: 格式化的数据集预览
    """
    # print("开始格式化数据集",dataset.data)
    # 检查是否为sklearn数据集
    if hasattr(dataset, 'data') and hasattr(dataset, 'target'):
        X = dataset.data
        y = dataset.target

        # 获取特征名称
        if hasattr(dataset, 'feature_names') and dataset.feature_names is not None:
            feature_names = dataset.feature_names
        else:
            feature_names = [f'特征 {i + 1}' for i in range(X.shape[1])]

        # 获取目标类名称
        if hasattr(dataset, 'target_names') and dataset.target_names is not None:
            target_names = dataset.target_names
            # 将数字标签映射到名称
            if len(y.shape) == 1:  # 一维数组
                y_labels = np.array([target_names[int(i)] for i in y])
            else:
                y_labels = y  # 对于回归问题保持原样
        else:
            target_names = np.unique(y)
            y_labels = y
    else:
        # 假定为DataFrame或自定义格式
        if isinstance(dataset, pd.DataFrame):
            # 假设最后一列是目标
            X = dataset.iloc[:, :-1].values
            y = dataset.iloc[:, -1].values
            feature_names = dataset.columns[:-1].tolist()
            target_names = np.unique(y)
            y_labels = y
        else:
            # 自定义格式，假设有X和y字段
            X = dataset.get('X', [])
            y = dataset.get('y', [])
            feature_names = dataset.get('feature_names', [f'特征 {i + 1}' for i in range(len(X[0]) if X else 0)])
            target_names = dataset.get('target_names', np.unique(y).tolist() if len(y) > 0 else [])
            y_labels = y

    # 构建样本数据
    samples = []
    for i in range(min(len(X), 100)):  # 最多返回100个样本
        samples.append(X[i].tolist() if hasattr(X[i], 'tolist') else X[i])

    # 构建目标数据
    targets = []
    for i in range(min(len(y_labels), 100)):  # 与样本数保持一致
        if hasattr(y_labels[i], 'tolist'):
            targets.append(y_labels[i].tolist())
        else:
            # 对于字符串或数字，直接添加
            targets.append(y_labels[i])

    result = {
        'samples': samples,
        'targets': targets,
        # 'feature_names': feature_names,
        'feature_names': feature_names.tolist() if hasattr(feature_names, 'tolist') else feature_names,
        'target_names': target_names.tolist() if hasattr(target_names, 'tolist') else target_names,
        'n_samples': len(X),
        'n_features': X.shape[1] if hasattr(X, 'shape') and len(X) > 0 else 0,
        'n_classes': len(target_names)
    }

    print(result)
    return result



@dataset_api.route('/api/dataset/<dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    """根据数据集ID返回对应的数据集"""
    try:
        if dataset_id in DATASETS:
            # 加载经典数据集
            dataset = DATASETS[dataset_id]()

            # 构建符合前端需要的树节点结构
            response = {
                "id": "1",
                "selected": False,
                "operation": f"原始数据集 ({dataset_id})",
                "parameters": {},
                # "target": dataset.target.tolist(),
                "target": [dataset.target_names[i] for i in dataset.target],
                "dataset": dataset.data.tolist(),
                "computed": {},
                "feature_names": dataset.feature_names.tolist() if hasattr(dataset.feature_names, 'tolist') else dataset.feature_names,
                "target_names": dataset.target_names.tolist() if hasattr(dataset.target_names, 'tolist') else dataset.target_names
            }

            return jsonify(response)
        else:
            return jsonify({"error": f"找不到数据集: {dataset_id}"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dataset_api.route('/api/dataset/<dataset_id>/preview', methods=['GET'])
def get_dataset_preview(dataset_id):
    """根据数据集ID返回对应的数据集"""
    print("dataset_id",dataset_id)
    try:
        if dataset_id in DATASETS:
            # 加载经典数据集
            dataset = DATASETS[dataset_id]()

            return jsonify(format_dataset_preview(dataset))
        else:
            return jsonify({"error": f"找不到数据集: {dataset_id}"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dataset_api.route('/api/dataset', methods=['GET'])
def test():
    return jsonify({"succeed": "成功"})

@dataset_api.route('/api/dataset/upload', methods=['POST'])
def upload_dataset():
    """处理上传的数据集文件"""
    if 'file' not in request.files:
        return jsonify({"error": "没有上传文件"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "没有选择文件"}), 400

    try:
        # 保存上传的文件到临时目录
        fd, temp_path = tempfile.mkstemp(suffix='.csv')
        file.save(temp_path)

        # 根据文件类型读取数据
        if file.filename.endswith('.csv'):
            df = pd.read_csv(temp_path)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(temp_path)
        else:
            os.close(fd)
            os.remove(temp_path)
            return jsonify({"error": "不支持的文件格式"}), 400

        # 假设最后一列是目标变量
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values

        # 构建符合前端需要的树节点结构
        response = {
            "id": "1",
            "selected": False,
            "operation": "原始数据集 (上传)",
            "parameters": {},
            "target": y.tolist(),
            "dataset": X.tolist(),
            "computed": {}
        }

        # 清理临时文件
        os.close(fd)
        os.remove(temp_path)

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
