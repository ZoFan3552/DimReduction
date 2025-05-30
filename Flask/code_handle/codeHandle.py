from flask import request, jsonify, Blueprint
import io
import traceback
import contextlib
import matplotlib

# 设置matplotlib后端，解决多线程问题
matplotlib.use('Agg')
# 设置matplotlib不在交互模式
import matplotlib.pyplot as plt

plt.switch_backend('Agg')
import base64
from io import BytesIO
import numpy as np
import pandas as pd
import scipy
import json

code_api = Blueprint('code_api', __name__)

class PlotCapture:
    """捕获matplotlib图形并转换为base64"""

    def __init__(self):
        self.figures = []

    def __enter__(self):
        self._original_show = plt.show
        plt.show = self._capture_show
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        plt.show = self._original_show
        # 关闭所有图形
        plt.close('all')

    def _capture_show(self):
        fig = plt.gcf()
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        self.figures.append(f'<img src="data:image/png;base64,{img_base64}" style="max-width: 100%;">')
        plt.close(fig)


@code_api.route('/run', methods=['POST'])
def run_code():
    try:
        code = request.json.get('code', '')

        # 创建一个字符串IO对象来捕获输出
        output_buffer = io.StringIO()

        # 创建一个受限的执行环境
        safe_globals = {
            '__builtins__': __builtins__,
            'print': lambda *args, **kwargs: print(*args, **kwargs, file=output_buffer)
        }

        # 允许导入的安全模块
        safe_modules = {
            'numpy': np,
            'np': np,
            'pandas': pd,
            'pd': pd,
            'matplotlib': matplotlib,
            'plt': plt,
            'sklearn': __import__('sklearn'),
            'scipy': scipy,
            'math': __import__('math'),
            'random': __import__('random'),
            'collections': __import__('collections'),
            'itertools': __import__('itertools'),
            'functools': __import__('functools'),
            'json': json
        }

        # 导入安全模块到执行环境
        safe_globals.update(safe_modules)

        # 创建临时的图形管理器
        plt.ioff()  # 关闭交互模式

        # 捕获标准输出和matplotlib图形
        with contextlib.redirect_stdout(output_buffer), PlotCapture() as plot_capture:
            try:
                # 执行代码
                exec(code, safe_globals)

                # 获取输出
                output = output_buffer.getvalue()

                # 添加图形到输出
                if plot_capture.figures:
                    output += '\n\n' + '\n'.join(plot_capture.figures)

                return jsonify({
                    'output': output or '代码执行成功，但没有输出。',
                    'error': False
                })

            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
                return jsonify({
                    'output': error_msg,
                    'error': True
                })

    except Exception as e:
        return jsonify({
            'output': f"服务器错误: {str(e)}",
            'error': True
        }), 500


