from flask import Flask, request, jsonify, Blueprint
import numpy as np
from sklearn.decomposition import PCA
from flask import Flask, request, jsonify
import numpy as np
import uuid
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy import linalg
import json

"""
LDA矩阵计算器 - Flask后端
提供计算类内散度矩阵和类间散度矩阵的API
"""

LDAdiv_api = Blueprint('LDAdiv_api', __name__)

def calculate_within_class_scatter(X, y, regularization=0.0):
    """
    计算类内散度矩阵

    参数:
    X: 特征矩阵，shape (n_samples, n_features)
    y: 标签数组，shape (n_samples,)
    regularization: 正则化参数，默认为0

    返回:
    S_w: 类内散度矩阵
    stats: 矩阵相关统计信息
    """
    classes = np.unique(y)
    n_features = X.shape[1]

    # 初始化类内散度矩阵
    S_w = np.zeros((n_features, n_features))

    # 对每个类别计算类内散度矩阵
    for c in classes:
        # 获取该类别的样本
        X_c = X[y == c]

        # 计算类别均值
        mean_c = np.mean(X_c, axis=0).reshape(-1, 1)  # 转换为列向量

        # 对该类别中的每个样本计算偏差
        for i in range(X_c.shape[0]):
            x_i = X_c[i].reshape(-1, 1)  # 转换为列向量
            deviation = x_i - mean_c
            S_w += np.dot(deviation, deviation.T)

    # 添加正则化项
    if regularization > 0:
        S_w += regularization * np.eye(n_features)

    # 计算矩阵统计信息
    stats = calculate_matrix_stats(S_w)

    return S_w.tolist(), stats


def calculate_between_class_scatter(X, y, weight_type='proportional'):
    """
    计算类间散度矩阵

    参数:
    X: 特征矩阵，shape (n_samples, n_features)
    y: 标签数组，shape (n_samples,)
    weight_type: 权重类型，'equal'表示等权重，'proportional'表示按比例权重

    返回:
    S_b: 类间散度矩阵
    stats: 矩阵相关统计信息
    """
    classes = np.unique(y)
    n_samples = X.shape[0]
    n_features = X.shape[1]

    # 计算总体均值
    mean_overall = np.mean(X, axis=0).reshape(-1, 1)  # 转换为列向量

    # 初始化类间散度矩阵
    S_b = np.zeros((n_features, n_features))

    # 对每个类别计算贡献
    for c in classes:
        # 获取该类别的样本
        X_c = X[y == c]
        n_c = X_c.shape[0]

        # 计算类别均值
        mean_c = np.mean(X_c, axis=0).reshape(-1, 1)  # 转换为列向量

        # 计算偏差
        deviation = mean_c - mean_overall

        # 根据权重类型确定权重
        if weight_type == 'equal':
            weight = 1.0
        else:  # 'proportional'
            weight = n_c

        # 累加到类间散度矩阵
        S_b += weight * np.dot(deviation, deviation.T)

    # 计算矩阵统计信息
    stats = calculate_matrix_stats(S_b)

    return S_b.tolist(), stats


def calculate_matrix_stats(matrix):
    """
    计算矩阵的统计信息，包括秩、行列式和特征值

    参数:
    matrix: numpy矩阵

    返回:
    包含统计信息的字典
    """
    # 计算矩阵的秩
    rank = np.linalg.matrix_rank(matrix)

    # 计算行列式（对于非奇异矩阵）
    try:
        det = np.linalg.det(matrix)
    except:
        det = 0.0

    # 计算特征值
    try:
        eigenvalues = np.linalg.eigvals(matrix)
        # 按绝对值从大到小排序
        eigenvalues = sorted(eigenvalues, key=abs, reverse=True)
    except:
        eigenvalues = []

    return {
        "rank": int(rank),
        "determinant": float(det),
        "eigenvalues": [float(val) for val in eigenvalues]
    }


@LDAdiv_api.route('/api/calculate-lda-matrix', methods=['POST'])
def calculate_lda_matrix():
    """
    计算LDA矩阵的API端点
    接收nodeData和参数，返回包含计算结果的新节点
    """
    try:
        # 解析请求数据
        request_data = request.get_json()

        node_data = request_data.get('nodeData')
        matrix_type = request_data.get('matrixType')
        parameters = request_data.get('parameters')

        # 验证数据
        if not node_data or not node_data.get('dataset') or not node_data.get('target'):
            return jsonify({"error": "数据不足"}), 400

        # 提取特征和标签
        dataset = np.array(node_data.get('dataset'))
        target = np.array(node_data.get('target'))

        # 根据矩阵类型进行计算
        if matrix_type == 'within':
            matrix, stats = calculate_within_class_scatter(
                dataset,
                target,
                regularization=parameters.get('regularization', 0.0)
            )
            result_key = 'within_class_scatter_matrix'
            stats_key = 'withinClassStats'
        else:  # 'between'
            matrix, stats = calculate_between_class_scatter(
                dataset,
                target,
                weight_type=parameters.get('weightType', 'proportional')
            )
            result_key = 'between_class_scatter_matrix'
            stats_key = 'betweenClassStats'

        # 创建新节点
        new_node = node_data.copy()
        new_node["id"] = str(uuid.uuid4())
        new_node["selected"] = False
        new_node["operation"] = "LDA矩阵计算"
        new_node["parameters"] = {
                "matrixType": matrix_type,
                "parameters": parameters
            }
        new_node["computed"][result_key] = matrix
        new_node["computed"][stats_key] = stats
        new_node["children"] = []

        return jsonify(new_node)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

