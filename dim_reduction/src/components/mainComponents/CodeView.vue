<template>
    <div class="python-editor">
        <div class="editor-header">
            <h3>{{ title }}</h3>
            <p>{{ description }}</p>
        </div>

        <div class="examples-bar">
            <button v-for="(example, key) in examples" :key="key" @click="loadExample(key)" class="example-btn">
                <i :class="getExampleIcon(key)"></i>
                {{ example.name }}
            </button>
        </div>

        <div class="code-editor" ref="editorContainer"></div>

        <div class="controls">
            <button @click="runCode" class="btn btn-primary" :disabled="isRunning">
                <span v-if="!isRunning">▶</span>
                <span v-else class="spinner"></span>
                {{ isRunning ? '运行中...' : '运行代码' }}
            </button>
            <button @click="clearOutput" class="btn btn-secondary">
                <span>×</span>
                清除输出
            </button>
        </div>

        <div class="output-container">
            <div class="output-header">
                <span v-if="isRunning" class="spinner-small"></span>
                <span v-else>📋</span>
                输出结果：
            </div>
            <div class="output" :class="{ error: hasError, loading: isRunning }" v-html="output || '等待运行...'">
            </div>
        </div>
    </div>
</template>

<script>
import CodeMirror from 'codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/python/python'
import 'codemirror/addon/edit/closebrackets'
import 'codemirror/addon/edit/matchbrackets'
import 'codemirror/addon/selection/active-line'
import axios from 'axios'

export default {
    name: 'PythonEditor',

    props: {
        title: {
            type: String,
            default: 'Python 数据降维算法练习'
        },
        description: {
            type: String,
            default: '在这里编写和运行你的数据降维算法代码（PCA、t-SNE、UMAP等）'
        },
        apiUrl: {
            type: String,
            default: 'http://localhost:5000/run'
        },
        initialCode: {
            type: String,
            default: ''
        }
    },

    data() {
        return {
            code: this.initialCode || this.getDefaultCode(),
            output: '',
            isRunning: false,
            hasError: false,
            editor: null,
            examples: {
                pca: {
                    name: 'PCA示例',
                    code: this.getPCAExample()
                },
                tsne: {
                    name: 't-SNE示例',
                    code: this.getTSNEExample()
                },
                simple: {
                    name: '简单数据处理',
                    code: this.getSimpleExample()
                }
            }
        }
    },

    mounted() {
        this.initEditor()
    },

    beforeDestroy() {
        if (!this.editor) return; // 检查是否存在

        // CodeMirror 5.x
        if (typeof this.editor.toTextArea === "function") {
            this.editor.toTextArea();
        }
        // CodeMirror 6.x
        else if (typeof this.editor.destroy === "function") {
            this.editor.destroy();
        }

        this.editor = null; // 清除引用
        // if (this.editor) {
        //     console.log(this.editor)
        //     this.editor.toTextArea()
        // }
    },

    methods: {
        getExampleIcon(key) {
            const icons = {
                pca: '📊',
                tsne: '🔬',
                simple: '📝'
            }
            return icons[key] || '📄'
        },

        initEditor() {
            this.editor = CodeMirror(this.$refs.editorContainer, {
                value: this.code,
                mode: 'python',
                theme: 'default', // 使用默认主题
                lineNumbers: true,
                autoCloseBrackets: true,
                matchBrackets: true,
                indentUnit: 4,
                tabSize: 4,
                indentWithTabs: false,
                lineWrapping: true,
                styleActiveLine: true,
                extraKeys: {
                    "Ctrl-Space": "autocomplete",
                    "F11": function (cm) {
                        cm.setOption("fullScreen", !cm.getOption("fullScreen"));
                    },
                    "Esc": function (cm) {
                        if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
                    }
                }
            })

            this.editor.on('change', (editor) => {
                this.code = editor.getValue()
            })

            this.editor.setSize('100%', '450px')
        },

        loadExample(exampleKey) {
            if (this.examples[exampleKey]) {
                this.code = this.examples[exampleKey].code
                this.editor.setValue(this.code)
            }
        },

        async runCode() {
            this.isRunning = true
            this.hasError = false
            this.output = '正在运行代码...'

            try {
                const response = await axios.post(this.apiUrl, {
                    code: this.code
                })

                this.output = response.data.output
                this.hasError = response.data.error

                this.$emit('code-executed', {
                    code: this.code,
                    output: this.output,
                    error: this.hasError
                })
            } catch (error) {
                this.output = '错误: ' + (error.response?.data?.error || error.message)
                this.hasError = true

                this.$emit('execution-error', error)
            } finally {
                this.isRunning = false
            }
        },

        clearOutput() {
            this.output = ''
            this.hasError = false
            this.$emit('output-cleared')
        },

        getDefaultCode() {
            return `# 导入必要的库
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

# 设置中文字体（使用系统支持的字体）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑，适用于Windows
  
# 生成示例数据
X, y = make_blobs(n_samples=100, n_features=2, centers=3, random_state=42)
  
# 在这里实现你的降维算法
print("数据形状:", X.shape)
  
# 可视化结果
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis')
plt.title('示例数据')
plt.show()`
        },

        getPCAExample() {
            return `# PCA（主成分分析）实现示例
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

# 设置中文字体（使用系统支持的字体）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑，适用于Windows
  
# 加载数据
iris = load_iris()
X = iris.data
y = iris.target
  
# 标准化数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
  
# PCA实现
class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.components = None
        self.mean = None
        self.explained_variance_ratio = None
      
    def fit(self, X):
        # 中心化
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
          
        # 计算协方差矩阵
        cov_matrix = np.cov(X_centered.T)
          
        # 特征值分解
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
          
        # 排序
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
          
        # 存储主成分
        self.components = eigenvectors[:, :self.n_components]
          
        # 计算解释方差比例
        self.explained_variance_ratio = eigenvalues[:self.n_components] / np.sum(eigenvalues)
          
        return self
      
    def transform(self, X):
        X_centered = X - self.mean
        return np.dot(X_centered, self.components)
  
# 应用PCA
pca = PCA(n_components=2)
pca.fit(X_scaled)
X_pca = pca.transform(X_scaled)
  
# 可视化
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis')
plt.xlabel(f'第一主成分 ({pca.explained_variance_ratio[0]:.2%})')
plt.ylabel(f'第二主成分 ({pca.explained_variance_ratio[1]:.2%})')
plt.title('PCA降维后的鸢尾花数据集')
plt.colorbar(scatter, label='类别')
plt.grid(True, alpha=0.3)
plt.show()
  
print(f"解释方差比例: {pca.explained_variance_ratio}")
print(f"累计解释方差: {np.cumsum(pca.explained_variance_ratio)}")`
        },

        getTSNEExample() {
            return `# t-SNE实现示例（简化版）
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler

# 设置中文字体（使用系统支持的字体）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑，适用于Windows
  
# 加载数据
digits = load_digits()
X = digits.data[:300]  # 使用部分数据以加快计算
y = digits.target[:300]
  
# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
  
# 简化的t-SNE实现
class SimpleTSNE:
    def __init__(self, n_components=2, perplexity=30.0, learning_rate=200.0, n_iter=1000):
        self.n_components = n_components
        self.perplexity = perplexity
        self.learning_rate = learning_rate
        self.n_iter = n_iter
      
    def _calculate_pairwise_distances(self, X):
        sum_X = np.sum(np.square(X), axis=1)
        distances = np.add(np.add(-2 * np.dot(X, X.T), sum_X).T, sum_X)
        return distances
      
    def fit_transform(self, X):
        n_samples = X.shape[0]
          
        # 计算成对距离
        distances = self._calculate_pairwise_distances(X)
          
        # 初始化低维表示
        Y = np.random.randn(n_samples, self.n_components) * 0.0001
          
        # 简化的优化过程
        for iteration in range(self.n_iter):
            if iteration % 100 == 0:
                print(f"迭代 {iteration}/{self.n_iter}")
              
            # 计算低维空间的距离
            distances_Y = self._calculate_pairwise_distances(Y)
              
            # 计算梯度（简化版）
            Q = 1 / (1 + distances_Y)
            np.fill_diagonal(Q, 0)
            Q = Q / np.sum(Q)
            Q = np.maximum(Q, 1e-12)
              
            # 简化的梯度更新
            Y += np.random.randn(*Y.shape) * 0.1 * self.learning_rate / (iteration + 1)
          
        return Y
  
# 应用t-SNE
tsne = SimpleTSNE(n_components=2, n_iter=500)
X_tsne = tsne.fit_transform(X_scaled)
  
# 可视化
plt.figure(figsize=(10, 8))
scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='Spectral', s=50)
plt.colorbar(scatter, label='数字类别')
plt.title('t-SNE降维后的手写数字数据集')
plt.xlabel('t-SNE维度1')plt.ylabel('t-SNE维度2')
plt.grid(True, alpha=0.3)
plt.show()

print("t-SNE降维完成！")`
        },

        getSimpleExample() {
            return `# 简单的数据处理示例
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（使用系统支持的字体）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑，适用于Windows
  
# 生成随机数据
np.random.seed(42)
data = np.random.randn(100, 2)
  
# 计算均值和标准差
mean = np.mean(data, axis=0)
std = np.std(data, axis=0)
  
# 标准化数据
data_normalized = (data - mean) / std
  
# 可视化
plt.figure(figsize=(12, 5))
  
plt.subplot(1, 2, 1)
plt.scatter(data[:, 0], data[:, 1], alpha=0.6)
plt.title('原始数据')
plt.xlabel('特征1')
plt.ylabel('特征2')
plt.grid(True, alpha=0.3)
  
plt.subplot(1, 2, 2)
plt.scatter(data_normalized[:, 0], data_normalized[:, 1], alpha=0.6)
plt.title('标准化后的数据')
plt.xlabel('特征1 (标准化)')plt.ylabel('特征2 (标准化)')
plt.grid(True, alpha=0.3)
  
plt.tight_layout()
plt.show()
  
print(f"原始数据均值: {mean}")
print(f"原始数据标准差: {std}")
print(f"标准化后数据均值: {np.mean(data_normalized, axis=0)}")
print(f"标准化后数据标准差: {np.std(data_normalized, axis=0)}")`
        }
    }
}
</script>

<style scoped>
.python-editor {
    height: 100%;
    overflow-y: auto;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    /* padding: 24px; */
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.editor-header {
    margin-bottom: 24px;
    border-bottom: 1px solid #e8e8e8;
    padding-bottom: 16px;
}

.editor-header h3 {
    margin: 0;
    color: #1a1a1a;
    font-size: 26px;
    font-weight: 600;
}

.editor-header p {
    margin: 8px 0 0 0;
    color: #666;
    font-size: 15px;
}

.examples-bar {
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.example-btn {
    padding: 8px 16px;
    background-color: #f0f7ff;
    color: #2196F3;
    border: 1px solid #d0e3ff;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
}

.example-btn:hover {
    background-color: #e3f2fd;
    border-color: #90caf9;
    transform: translateY(-1px);
}

.code-editor {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

.code-editor:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.controls {
    margin-bottom: 24px;
    display: flex;
    gap: 12px;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}
</style>