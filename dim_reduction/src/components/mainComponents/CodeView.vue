<template>
    <div class="dim-reduction-editor">
        <div class="editor-header">
            <h3>{{ title }}</h3>
            <p>{{ description }}</p>
        </div>

        <div class="examples-bar">
            <button v-for="algorithm in algorithms" :key="algorithm.value" @click="loadAlgorithm(algorithm.value)"
                class="algorithm-btn" :class="{ active: currentAlgorithm === algorithm.value }">
                <i :class="getAlgorithmIcon(algorithm.value)"></i>
                {{ algorithm.label }}
            </button>
        </div>

        <div class="editors-container">
            <!-- 左侧用户代码编辑区 -->
            <div class="editor-panel">
                <div class="panel-header">
                    <h4>我的代码</h4>
                    <div class="panel-actions">
                        <button @click="saveUserCode" class="btn btn-save">
                            <span>💾</span>
                            保存代码
                        </button>
                    </div>
                </div>
                <div class="code-editor user-editor" ref="userEditorContainer"></div>
                <div class="controls">
                    <button @click="runUserCode" class="btn btn-primary" :disabled="isUserRunning">
                        <span v-if="!isUserRunning">▶</span>
                        <span v-else class="spinner"></span>
                        {{ isUserRunning ? '运行中...' : '运行代码' }}
                    </button>
                    <button @click="clearUserOutput" class="btn btn-secondary">
                        <span>×</span>
                        清除输出
                    </button>
                </div>
                <div class="output-container">
                    <div class="output-header">
                        <span v-if="isUserRunning" class="spinner-small"></span>
                        <span v-else>📋</span>
                        输出结果：
                    </div>
                    <div class="output" :class="{ error: hasUserError, loading: isUserRunning }"
                        v-html="userOutput || '等待运行...'"></div>
                </div>
            </div>

            <!-- 右侧标准算法代码展示区 -->
            <div class="editor-panel">
                <div class="panel-header">
                    <h4>标准算法</h4>
                    <div class="panel-actions">
                        <span class="label-read-only">只读模式</span>
                    </div>
                </div>
                <div class="code-editor standard-editor" ref="standardEditorContainer"></div>
                <div class="controls">
                    <button @click="runStandardCode" class="btn btn-primary" :disabled="isStandardRunning">
                        <span v-if="!isStandardRunning">▶</span>
                        <span v-else class="spinner"></span>
                        {{ isStandardRunning ? '运行中...' : '运行代码' }}
                    </button>
                    <button @click="clearStandardOutput" class="btn btn-secondary">
                        <span>×</span>
                        清除输出
                    </button>
                </div>
                <div class="output-container">
                    <div class="output-header">
                        <span v-if="isStandardRunning" class="spinner-small"></span>
                        <span v-else>📋</span>
                        输出结果：
                    </div>
                    <div class="output" :class="{ error: hasStandardError, loading: isStandardRunning }"
                        v-html="standardOutput || '等待运行...'"></div>
                </div>
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
import axios from '@/utils/myAxios'

export default {
    name: 'DimReductionEditor',

    props: {
        title: {
            type: String,
            default: 'Python 数据降维算法对比学习'
        },
        description: {
            type: String,
            default: '在左侧编写你的数据降维算法代码，右侧可查看并运行标准算法，进行对比学习'
        },
        apiUrl: {
            type: String,
            default: 'http://localhost:5000/run'
        },

        tutorialType: {
            type: String,
            default: 'PCA', // 默认教程类型
            validator: function (value) {
                return ['PCA', 'LDA', 'tSNE', 'UMAP', 'common'].indexOf(value) !== -1
            }
        }
    },

    data() {
        return {
            userId: null,
            // 用户代码相关
            userCode: '',
            userOutput: '',
            isUserRunning: false,
            hasUserError: false,
            userEditor: null,

            // 标准算法代码相关
            standardCode: '',
            standardOutput: '',
            isStandardRunning: false,
            hasStandardError: false,
            standardEditor: null,

            // 算法类型
            currentAlgorithm: this.tutorialType,

            // 可用算法列表
            algorithms: [
                { value: 'PCA', label: 'PCA算法' },
                { value: 'tSNE', label: 't-SNE算法' },
                { value: 'UMAP', label: 'UMAP算法' }
            ],

            // 初始代码模板
            defaultCode: `# 导入必要的库
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
        }
    },

    created() {
        // 组件创建时加载当前选定的算法
        this.currentAlgorithm = this.tutorialType;
        this.userId = localStorage.getItem('userId');
    },

    mounted() {
        this.initEditors();
        this.loadAlgorithm(this.currentAlgorithm);
    },

    beforeDestroy() {
        // 销毁编辑器实例
        if (this.userEditor) {
            if (typeof this.userEditor.toTextArea === "function") {
                this.userEditor.toTextArea();
            } else if (typeof this.userEditor.destroy === "function") {
                this.userEditor.destroy();
            }
            this.userEditor = null;
        }

        if (this.standardEditor) {
            if (typeof this.standardEditor.toTextArea === "function") {
                this.standardEditor.toTextArea();
            } else if (typeof this.standardEditor.destroy === "function") {
                this.standardEditor.destroy();
            }
            this.standardEditor = null;
        }
    },

    methods: {
        getAlgorithmIcon(algorithm) {
            const icons = {
                'PCA': '📊',
                'tSNE': '🔬',
                'UMAP': '🌐'
            };
            return icons[algorithm] || '📄';
        },

        initEditors() {
            // 初始化用户代码编辑器
            this.userEditor = CodeMirror(this.$refs.userEditorContainer, {
                value: this.userCode || this.defaultCode,
                mode: 'python',
                theme: 'default',
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
            });

            this.userEditor.on('change', (editor) => {
                this.userCode = editor.getValue();
            });

            // 初始化标准算法代码编辑器（只读模式）
            this.standardEditor = CodeMirror(this.$refs.standardEditorContainer, {
                value: this.standardCode,
                mode: 'python',
                theme: 'default',
                lineNumbers: true,
                autoCloseBrackets: true,
                matchBrackets: true,
                indentUnit: 4,
                tabSize: 4,
                indentWithTabs: false,
                lineWrapping: true,
                styleActiveLine: true,
                readOnly: true // 设置为只读
            });

            // 设置编辑器高度
            this.userEditor.setSize('100%', '400px');
            this.standardEditor.setSize('100%', '400px');
        },

        async loadAlgorithm(algorithmType) {
            this.currentAlgorithm = algorithmType;

            try {
                // 加载用户已保存的代码
                const userCodeResponse = await axios.get(`/tutorial/user-code`, {
                    params: {
                        userId: this.userId,
                        algorithmType: algorithmType
                    }
                });

                // 如果有用户保存的代码，则使用，否则使用默认代码
                if (userCodeResponse && userCodeResponse.code) {
                    this.userCode = userCodeResponse.code;
                } else {
                    this.userCode = this.defaultCode;
                }

                // 更新用户编辑器内容
                if (this.userEditor) {
                    this.userEditor.setValue(this.userCode);
                }

                // 加载标准算法代码
                const standardCodeResponse = await axios.get(`/tutorial/standard-code`, {
                    params: {
                        algorithmType: algorithmType
                    }
                });

                // 更新标准算法代码
                if (standardCodeResponse && standardCodeResponse.code) {
                    this.standardCode = standardCodeResponse.code;
                } else {
                    this.standardCode = '# 标准算法代码未找到';
                }

                // 更新标准代码编辑器内容
                if (this.standardEditor) {
                    this.standardEditor.setValue(this.standardCode);
                }

                // 清空两侧的输出
                this.clearUserOutput();
                this.clearStandardOutput();

                // 通知父组件算法已更改
                this.$emit('algorithm-changed', this.currentAlgorithm);

            } catch (error) {
                console.error('加载算法代码失败:', error);
                this.$emit('loading-error', error);
            }
        },

        async saveUserCode() {
            try {
                const response = await axios.post('/tutorial/save-code', {
                    userId: this.userId,
                    algorithmType: this.currentAlgorithm,
                    code: this.userCode
                });

                if (response && response.success) {
                    // 可以在这里添加保存成功的提示
                    this.$emit('code-saved', {
                        userId: this.userId,
                        algorithmType: this.currentAlgorithm
                    });

                    // 显示保存成功的消息（需要一个消息提示组件）
                    // this.$message.success('代码保存成功！');
                    alert('代码保存成功！');
                    console.log("代码保存成功！");
                }
            } catch (error) {
                console.error('保存代码失败:', error);
                this.$emit('save-error', error);

                // 显示保存失败的消息
                // this.$message.error('保存失败: ' + error.message);
                alert('保存失败: ' + (error.response?.data?.message || error.message));
            }
        },

        async runUserCode() {
            this.isUserRunning = true;
            this.hasUserError = false;
            this.userOutput = '正在运行代码...';

            try {
                const response = await axios.post(this.apiUrl, {
                    code: this.userCode
                });

                this.userOutput = response.output;
                this.hasUserError = response.error;

                this.$emit('user-code-executed', {
                    code: this.userCode,
                    output: this.userOutput,
                    error: this.hasUserError
                });
            } catch (error) {
                this.userOutput = '错误: ' + (error.response?.error || error.message);
                this.hasUserError = true;

                this.$emit('user-execution-error', error);
            } finally {
                this.isUserRunning = false;
            }
        },

        async runStandardCode() {
            this.isStandardRunning = true;
            this.hasStandardError = false;
            this.standardOutput = '正在运行代码...';

            try {
                const response = await axios.post(this.apiUrl, {
                    code: this.standardCode
                });

                this.standardOutput = response.output;
                this.hasStandardError = response.error;

                this.$emit('standard-code-executed', {
                    code: this.standardCode,
                    output: this.standardOutput,
                    error: this.hasStandardError
                });
            } catch (error) {
                this.standardOutput = '错误: ' + (error.response?.error || error.message);
                this.hasStandardError = true;

                this.$emit('standard-execution-error', error);
            } finally {
                this.isStandardRunning = false;
            }
        },

        clearUserOutput() {
            this.userOutput = '';
            this.hasUserError = false;
            this.$emit('user-output-cleared');
        },

        clearStandardOutput() {
            this.standardOutput = '';
            this.hasStandardError = false;
            this.$emit('standard-output-cleared');
        }
    }
}
</script>

<style scoped>
.dim-reduction-editor {
    height: 100%;
    overflow-y: auto;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.editor-header {
    margin-bottom: 20px;
    border-bottom: 1px solid #e8e8e8;
    padding-bottom: 16px;
}

.editor-header h3 {
    margin: 0;
    color: #1a1a1a;
    font-size: 24px;
    font-weight: 600;
}

.editor-header p {
    margin: 8px 0 0 0;
    color: #666;
    font-size: 14px;
}

.examples-bar {
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.algorithm-btn {
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

.algorithm-btn:hover {
    background-color: #e3f2fd;
    border-color: #90caf9;
    transform: translateY(-1px);
}

.algorithm-btn.active {
    background-color: #2196F3;
    color: white;
    border-color: #1976D2;
}

.editors-container {
    display: flex;
    gap: 20px;
}

.editor-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    /* 防止flex子项目溢出 */
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.panel-header h4 {
    margin: 0;
    color: #333;
    font-size: 16px;
    font-weight: 500;
}

.panel-actions {
    display: flex;
    align-items: center;
}

.label-read-only {
    font-size: 12px;
    color: #666;
    padding: 4px 8px;
    background-color: #f5f5f5;
    border-radius: 4px;
}

.code-editor {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

.code-editor:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.standard-editor .CodeMirror {
    background-color: #fafafa;
}

.controls {
    margin-bottom: 12px;
    display: flex;
    gap: 8px;
}

.btn {
    padding: 8px 16px;
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

.btn-primary {
    background-color: #2196F3;
    color: white;
}

.btn-primary:hover {
    background-color: #1976D2;
}

.btn-primary:disabled {
    background-color: #bbdefb;
    cursor: not-allowed;
}

.btn-secondary {
    background-color: #f5f5f5;
    color: #666;
}

.btn-secondary:hover {
    background-color: #e0e0e0;
}

.btn-save {
    background-color: #4CAF50;
    color: white;
}

.btn-save:hover {
    background-color: #388E3C;
}

.output-container {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px;
    background-color: #fafafa;
    margin-bottom: 20px;
    flex-grow: 1;
    min-height: 120px;
    max-height: 600px;
    overflow-y: auto;
}

.output-header {
    font-size: 14px;
    font-weight: 500;
    color: #666;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.output {
    font-family: 'Courier New', monospace;
    font-size: 13px;
    white-space: pre-wrap;
    line-height: 1.5;
}

.output.error {
    color: #d32f2f;
}

.output.loading {
    color: #666;
    font-style: italic;
}

.spinner {
    display: inline-block;
    width: 12px;
    height: 12px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s ease-in-out infinite;
}

.spinner-small {
    display: inline-block;
    width: 10px;
    height: 10px;
    border: 2px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top-color: #2196F3;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* 响应式设计 */
@media (max-width: 992px) {
    .editors-container {
        flex-direction: column;
    }

    .editor-panel {
        margin-bottom: 20px;
    }
}
</style>