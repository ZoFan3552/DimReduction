# app.py
import uuid

from flask import Flask, request, jsonify, Blueprint
import numpy as np
import pandas as pd
from uuid import uuid4
from flask_cors import CORS

covariance_api = Blueprint('covariance_api', __name__)

def generate_id():
    """生成唯一ID"""
    return str(uuid.uuid4())[:8]

@covariance_api.route('/api/calculate-covariance', methods=['POST'])
def calculate_covariance():
    """
    计算协方差矩阵的API端点

    接收的数据格式:
    {
        "nodeData": {
            "id": "4",
            "operation": "",
            "parameters": {},
            "target": [],
            "dataset": [ ... ],
            "computed": { },
            "children": []
        }
    }

    返回新节点，其中包含计算的协方差矩阵
    """
    try:
        # 获取请求数据
        request_data = request.json
        if not request_data or 'nodeData' not in request_data:
            return jsonify({'error': '请求数据无效'}), 400

        node_data = request_data['nodeData']

        # 验证数据集
        if not node_data.get('dataset') or not isinstance(node_data['dataset'], list) or len(node_data['dataset']) == 0:
            return jsonify({'error': '数据集为空或无效'}), 400

        # 将数据集转换为pandas DataFrame
        df = pd.DataFrame(node_data['dataset'])

        # 提取数值列用于计算协方差矩阵
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_columns) < 2:
            return jsonify({'error': '需要至少两个数值特征才能计算协方差矩阵'}), 400

        # 提取数值数据
        numeric_data = df[numeric_columns]

        # 计算协方差矩阵
        covariance_matrix = numeric_data.cov().values.tolist()

        # 创建新节点
        new_node = node_data.copy()
        new_node["id"] = generate_id()
        new_node["selected"] = False
        new_node["operation"] = "协方差矩阵"
        new_node["parameters"] = {}
        new_node["computed"]["covariance_matrix"] = covariance_matrix
        new_node["computed"]["featureNames"] = numeric_columns
        new_node["children"] = []
        # new_node["operation"] = "协方差矩阵"
        # new_node = {
        #     "id": generate_id(),
        #     "operation": "协方差矩阵",
        #     "parameters": {},
        #     "target": node_data['target'],  # 目标是源节点
        #     "dataset": node_data['dataset'],  # 保留原始数据集
        #     "computed": {
        #         "covariance_matrix": covariance_matrix,
        #         "featureNames": numeric_columns
        #     },
        #     "children": []
        # }

        return jsonify({
            'success': True,
            'node': new_node
        })

    except Exception as e:
        # 捕获并返回任何错误
        return jsonify({
            'error': f'计算协方差矩阵时发生错误: {str(e)}'
        }), 500


# 处理缺失数据的函数
def handle_missing_data(df):
    """处理数据集中的缺失值"""
    # 删除全部为NaN的行
    df = df.dropna(how='all')

    # 对于其他的缺失值，用列的均值填充
    for column in df.columns:
        if df[column].isnull().any():
            if np.issubdtype(df[column].dtype, np.number):
                df[column] = df[column].fillna(df[column].mean())
            else:
                # 对于非数值列，用最常见的值填充
                df[column] = df[column].fillna(df[column].mode()[0])

    return df


# 数据预处理函数
def preprocess_data(df, numeric_columns=None):
    """
    预处理数据，包括：
    1. 处理缺失值
    2. 标准化数值特征（可选）
    """
    # 处理缺失值
    df = handle_missing_data(df)

    # 如果指定了数值列，则只处理这些列
    if numeric_columns:
        df_numeric = df[numeric_columns]
    else:
        # 否则，自动检测数值列
        df_numeric = df.select_dtypes(include=[np.number])

    return df_numeric

