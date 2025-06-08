# app.py
from flask import  request, jsonify, Blueprint
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler
import uuid
import traceback
from scipy import stats


from utils.jsonProcess import make_json_safe

preprocess_api = Blueprint('preprocess_api', __name__)

@preprocess_api.route('/api/preprocess', methods=['POST'])
def preprocess_data():
    """
    处理数据集预处理请求，直接接收完整的节点数据和操作选项
    """
    try:
        # 获取请求数据
        request_data = request.json

        if not request_data or 'nodeData' not in request_data or 'options' not in request_data:
            return jsonify(make_json_safe({
                'success': False,
                'error': '请求格式不正确，缺少必要参数'
            })), 400

        # 获取节点数据和预处理选项
        node_data = request_data['nodeData']
        options = request_data['options']

        # 验证节点数据格式
        if 'dataset' not in node_data:
            return jsonify(make_json_safe({
                'success': False,
                'error': '节点数据格式不正确，缺少dataset字段'
            })), 400

        # 将原始数据转换为Pandas DataFrame以便处理
        try:
            df = pd.DataFrame(node_data['dataset'])
            target = np.array(node_data['target']) if 'target' in node_data else None
        except Exception as e:
            return jsonify(make_json_safe({
                'success': False,
                'error': f'数据格式转换错误: {str(e)}'
            })), 400

        # 创建新节点（复制原始节点的基本结构）
        new_node = node_data.copy()
        new_node['id'] = str(uuid.uuid4())  # 生成新的唯一ID
        new_node['selected'] = False
        new_node['operation'] = '数据预处理'
        new_node['parameters'] = options
        new_node['parent_id'] = node_data.get('id')
        new_node['children'] = []

        # 执行预处理操作
        df_processed, target_processed, processing_info = apply_preprocessing(df, target, options)

        # 如果处理失败
        if not processing_info['success']:
            return jsonify(make_json_safe({
                'success': False,
                'error': processing_info['error']
            })), 400

        # 更新节点数据
        new_node['dataset'] = df_processed.values.tolist()
        if target_processed is not None:
            new_node['target'] = target_processed.tolist()

        # 返回成功响应
        return jsonify(make_json_safe({
            'success': True,
            'node': new_node,
            'processing_info': processing_info
        }))

    except Exception as e:
        # 记录异常堆栈
        error_traceback = traceback.format_exc()
        print(error_traceback)

        # 返回错误响应
        return jsonify(make_json_safe({
            'success': False,
            'error': f'处理请求时发生错误: {str(e)}'
        })), 500


def apply_preprocessing(df, target, options):
    """
    应用预处理选项到数据集

    Args:
        df: 输入DataFrame
        target: 目标变量数组
        options: 预处理选项字典

    Returns:
        tuple: (处理后的DataFrame, 处理后的目标变量, 处理信息)
    """
    # 初始化处理信息
    processing_info = {
        'success': True,
        'message': '预处理成功',
        'steps': [],
        'rows_before': len(df),
        'columns_before': len(df.columns),
        'missing_values_before': df.isna().sum().sum()
    }

    # 创建副本，避免修改原始数据
    df_processed = df.copy()
    target_processed = target.copy() if target is not None else None

    try:
        # 1. 处理特征过程选项
        if 'featureProcess' in options:
            # 移除常数特征
            if 'remove_constant' in options['featureProcess']:
                constant_cols = [col for col in df_processed.columns if df_processed[col].nunique() <= 1]
                if constant_cols:
                    df_processed = df_processed.drop(constant_cols, axis=1)
                    processing_info['steps'].append(f'移除了{len(constant_cols)}个常数特征')

            # 移除重复行
            if 'remove_duplicates' in options['featureProcess']:
                duplicates_count = df_processed.duplicated().sum()
                if duplicates_count > 0:
                    df_processed = df_processed.drop_duplicates().reset_index(drop=True)
                    # 如果有目标变量，也需要相应地调整
                    if target_processed is not None:
                        # 创建临时DataFrame包含索引和目标
                        temp_df = pd.DataFrame({'target': target_processed})
                        # 标记重复行
                        dup_mask = df.duplicated()
                        # 只保留非重复行的目标值
                        target_processed = temp_df[~dup_mask]['target'].values

                    processing_info['steps'].append(f'移除了{duplicates_count}行重复数据')

        # 2. 空缺值处理
        if 'missingValues' in options and options['missingValues'] != 'none':
            missing_count = df_processed.isna().sum().sum()

            if missing_count > 0:
                if options['missingValues'] == 'drop_rows':
                    # 记录删除前的行数
                    rows_before = len(df_processed)

                    # 标记含缺失值的行
                    missing_mask = df_processed.isna().any(axis=1)

                    # 删除含缺失值的行
                    df_processed = df_processed.dropna().reset_index(drop=True)

                    # 如果有目标变量，也需要相应地调整
                    if target_processed is not None:
                        target_processed = target_processed[~missing_mask]

                    processing_info['steps'].append(f'删除了{rows_before - len(df_processed)}行含缺失值的数据')

                elif options['missingValues'] == 'fill_mean':
                    df_processed = df_processed.fillna(df_processed.mean())
                    processing_info['steps'].append('使用均值填充了缺失值')

                elif options['missingValues'] == 'fill_median':
                    df_processed = df_processed.fillna(df_processed.median())
                    processing_info['steps'].append('使用中位数填充了缺失值')

                elif options['missingValues'] == 'fill_mode':
                    # 对每列使用众数填充
                    for col in df_processed.columns:
                        df_processed[col] = df_processed[col].fillna(
                            df_processed[col].mode()[0] if not df_processed[col].mode().empty else 0)
                    processing_info['steps'].append('使用众数填充了缺失值')

                elif options['missingValues'] == 'fill_zero':
                    df_processed = df_processed.fillna(0)
                    processing_info['steps'].append('使用0填充了缺失值')

        # 3. 异常值处理
        if 'outliers' in options and options['outliers'] != 'none':
            # 只处理数值型列
            numeric_cols = df_processed.select_dtypes(include=['number']).columns.tolist()

            if numeric_cols:
                if options['outliers'] == 'remove_iqr':
                    # 使用IQR方法检测异常值
                    outlier_rows = np.zeros(len(df_processed), dtype=bool)

                    for col in numeric_cols:
                        Q1 = df_processed[col].quantile(0.25)
                        Q3 = df_processed[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR

                        # 标记该列中的异常值行
                        outlier_mask = (df_processed[col] < lower_bound) | (df_processed[col] > upper_bound)
                        outlier_rows = outlier_rows | outlier_mask

                    # 移除包含异常值的行
                    outlier_count = outlier_rows.sum()
                    if outlier_count > 0:
                        df_processed = df_processed[~outlier_rows].reset_index(drop=True)

                        # 如果有目标变量，也需要相应地调整
                        if target_processed is not None:
                            target_processed = target_processed[~outlier_rows]

                        processing_info['steps'].append(f'使用IQR方法移除了{outlier_count}行异常值')

                elif options['outliers'] == 'remove_zscore':
                    # 使用Z分数方法检测异常值
                    outlier_rows = np.zeros(len(df_processed), dtype=bool)

                    for col in numeric_cols:
                        z_scores = np.abs(stats.zscore(df_processed[col].fillna(df_processed[col].median())))
                        # 通常Z分数大于3的视为异常值
                        outlier_mask = z_scores > 3
                        outlier_rows = outlier_rows | outlier_mask

                    # 移除包含异常值的行
                    outlier_count = outlier_rows.sum()
                    if outlier_count > 0:
                        df_processed = df_processed[~outlier_rows].reset_index(drop=True)

                        # 如果有目标变量，也需要相应地调整
                        if target_processed is not None:
                            target_processed = target_processed[~outlier_rows]

                        processing_info['steps'].append(f'使用Z分数法移除了{outlier_count}行异常值')

                elif options['outliers'] == 'clip':
                    # 将异常值截断到合理范围内
                    for col in numeric_cols:
                        Q1 = df_processed[col].quantile(0.25)
                        Q3 = df_processed[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR

                        # 计算被截断的值的数量
                        outlier_count = ((df_processed[col] < lower_bound) | (df_processed[col] > upper_bound)).sum()

                        # 将值限制在上下限范围内
                        df_processed[col] = df_processed[col].clip(lower=lower_bound, upper=upper_bound)

                        if outlier_count > 0:
                            processing_info['steps'].append(f'将列"{col}"中的{outlier_count}个异常值截断到合理范围')

        # 4. 特征缩放
        if 'scaling' in options and options['scaling'] != 'none':
            # 只处理数值型列
            numeric_cols = df_processed.select_dtypes(include=['number']).columns.tolist()

            if numeric_cols:
                # 保存非数值列
                non_numeric_df = df_processed.select_dtypes(exclude=['number'])

                # 对数值列进行缩放
                numeric_df = df_processed[numeric_cols]

                if options['scaling'] == 'standardization':
                    scaler = StandardScaler()
                    scaled_data = scaler.fit_transform(numeric_df)
                    processing_info['steps'].append('应用了标准化(Z-Score)缩放')

                elif options['scaling'] == 'normalization':
                    scaler = MinMaxScaler()
                    scaled_data = scaler.fit_transform(numeric_df)
                    processing_info['steps'].append('应用了归一化(Min-Max)缩放')

                elif options['scaling'] == 'robust':
                    scaler = RobustScaler()
                    scaled_data = scaler.fit_transform(numeric_df)
                    processing_info['steps'].append('应用了稳健缩放')

                elif options['scaling'] == 'max_abs':
                    scaler = MaxAbsScaler()
                    scaled_data = scaler.fit_transform(numeric_df)
                    processing_info['steps'].append('应用了最大绝对值缩放')

                # 创建新的DataFrame，包含缩放后的数值列
                scaled_df = pd.DataFrame(scaled_data, columns=numeric_cols, index=numeric_df.index)

                # 合并回非数值列
                if len(non_numeric_df.columns) > 0:
                    df_processed = pd.concat([scaled_df, non_numeric_df], axis=1)
                else:
                    df_processed = scaled_df

        # 记录处理后的信息
        processing_info['rows_after'] = len(df_processed)
        processing_info['columns_after'] = len(df_processed.columns)
        processing_info['missing_values_after'] = df_processed.isna().sum().sum()

        return df_processed, target_processed, processing_info

    except Exception as e:
        # 处理过程中发生错误
        error_traceback = traceback.format_exc()
        print(error_traceback)

        return df, target, {
            'success': False,
            'error': str(e),
            'steps': processing_info['steps']
        }


