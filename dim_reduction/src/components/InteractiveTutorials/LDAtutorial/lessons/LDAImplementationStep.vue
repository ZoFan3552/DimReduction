<!-- LDAImplementationStepByStep.vue - LDA实现步骤教学组件 -->
<template>
    <div class="tutorial-section" :id="sectionId">
        <div class="section-header">
            <h2 class="section-title">{{ title }}</h2>
            <div class="section-progress">
                <el-tag v-if="isCompleted" type="success" effect="dark">已完成</el-tag>
                <el-tag v-else type="info" effect="plain">进行中</el-tag>
                <div class="section-number">{{ sectionIndex }}/{{ totalSections }}</div>
            </div>
        </div>

        <!-- 教学内容展示区 -->
        <div class="content-area">
            <div class="markdown-content" v-html="compiledMarkdown"></div>
        </div>

        <!-- 互动区域 - 步骤排序和代码填空 -->
        <div v-if="!isCompleted" class="interaction-area">
            <h3 class="interaction-title">
                <i class="el-icon-setting"></i> 互动练习：LDA算法实现流程
            </h3>

            <p class="interaction-description">
                请按照正确的实现顺序排列以下LDA算法步骤，并完成关键代码片段。
            </p>

            <div class="implementation-exercise">
                <h4>1. 按照正确顺序排列LDA实现步骤</h4>

                <div class="step-sorting">
                    <draggable v-model="sortedSteps" :disabled="stepsSorted" class="steps-container"
                        handle=".step-drag-handle">
                        <div v-for="(step, index) in sortedSteps" :key="step.id" class="step-item" :class="{
                            'sorted': stepsSorted,
                            'correct-position': stepsSorted && step.correctPosition === index,
                            'wrong-position': stepsSorted && step.correctPosition !== index
                        }">
                            <div class="step-content">
                                <div class="step-drag-handle" v-if="!stepsSorted">
                                    <i class="el-icon-rank"></i>
                                </div>
                                <div class="step-number">
                                    {{ stepsSorted ? (step.correctPosition + 1) : (index + 1) }}
                                </div>
                                <div class="step-text">{{ step.text }}</div>
                                <div v-if="stepsSorted" class="step-status">
                                    <i :class="[
                                        step.correctPosition === index ? 'el-icon-check' : 'el-icon-close',
                                        step.correctPosition === index ? 'correct' : 'wrong'
                                    ]"></i>
                                </div>
                            </div>
                        </div>
                    </draggable>

                    <div class="step-actions" v-if="!stepsSorted">
                        <el-button type="primary" @click="checkStepOrder">
                            检查步骤顺序
                        </el-button>
                    </div>
                </div>

                <div v-if="stepsSorted" class="code-implementation">
                    <h4>2. 完成LDA算法的Python实现</h4>
                    <p class="code-description">
                        请阅读以下LDA算法的Python实现，并填充缺失的代码片段。
                    </p>

                    <div class="code-editor">
                        <el-tabs v-model="activeCodeTab">
                            <el-tab-pane label="LDA类定义" name="class">
                                <div class="code-block">
                                    <pre><code>class LDA:
      def __init__(self, n_components=None):
          """
          Linear Discriminant Analysis
  
          Parameters
          ----------
          n_components : int, optional
              Number of components for dimensionality reduction.
          """
          self.n_components = n_components
          self.eigenvectors = None
          self.mean_vectors = None
          self.overall_mean = None
  
      def fit(self, X, y):
          """
          Fit LDA model according to data.
  
          Parameters
          ----------
          X : array-like, shape (n_samples, n_features)
              Training data.
          y : array-like, shape (n_samples,)
              Target values.
  
          Returns
          -------
          self : object
              Returns self.
          """
          # 获取唯一类别和每个类的样本
          classes = np.unique(y)
          n_classes = len(classes)
          
          # 检查n_components设置
          if self.n_components is None:
              self.n_components = min(n_classes - 1, X.shape[1])
          
          # 计算每个类的均值向量和整体均值
          self.mean_vectors = []
          X_by_class = {}
          for c in classes:
              X_c = X[y == c]
              mean_vector = np.mean(X_c, axis=0)
              self.mean_vectors.append(mean_vector)
              X_by_class[c] = X_c
              
          # 计算整体均值
          self.overall_mean = np.mean(X, axis=0)
          
          # 计算类内散布矩阵 S_W
          S_W = self._compute_within_scatter_matrix(X_by_class)
          
          # 计算类间散布矩阵 S_B
          S_B = self._compute_between_scatter_matrix()
          
          # 计算S_W^(-1) * S_B的特征值和特征向量
          eigvals, eigvecs = self._solve_eigenvalue_problem(S_W, S_B)
          
          # 选择前n_components个特征向量
          indices = np.argsort(eigvals)[::-1]
          self.eigenvectors = eigvecs[:, indices[:self.n_components]]
          
          return self
  
      def transform(self, X):
          """
          Apply dimensionality reduction to X.
  
          Parameters
          ----------
          X : array-like, shape (n_samples, n_features)
              Data to be transformed.
              
          Returns
          -------
          X_new : array-like, shape (n_samples, n_components)
              Transformed data.
          """
          return np.dot(X - self.overall_mean, self.eigenvectors)</code></pre>
                                </div>
                            </el-tab-pane>

                            <el-tab-pane label="类内散布矩阵计算" name="within">
                                <div class="code-block">
                                    <pre><code>def _compute_within_scatter_matrix(self, X_by_class):
      """
      计算类内散布矩阵 S_W
      
      Parameters
      ----------
      X_by_class : dict
          每个类的数据点.
      
      Returns
      -------
      S_W : array-like, shape (n_features, n_features)
          类内散布矩阵.
      """
      n_features = len(self.overall_mean)
      S_W = np.zeros((n_features, n_features))
      
      for i, c in enumerate(X_by_class.keys()):
          X_c = X_by_class[c]
          mean_c = self.mean_vectors[i]
          
          # 选择正确的代码计算当前类的散布矩阵
          for j in range(len(X_by_class[c])):
              <el-select v-model="codeAnswers[0]" placeholder="选择代码" size="small" :disabled="codeChecked">
                <el-option 
                  v-for="(option, index) in codeOptions[0]" 
                  :key="index"
                  :label="option.label"
                  :value="option.value"
                ></el-option>
              </el-select>
      
      return S_W</code></pre>
                                </div>
                            </el-tab-pane>

                            <el-tab-pane label="类间散布矩阵计算" name="between">
                                <div class="code-block">
                                    <pre><code>def _compute_between_scatter_matrix(self):
      """
      计算类间散布矩阵 S_B
      
      Returns
      -------
      S_B : array-like, shape (n_features, n_features)
          类间散布矩阵.
      """
      n_features = len(self.overall_mean)
      n_classes = len(self.mean_vectors)
      S_B = np.zeros((n_features, n_features))
      
      for i in range(n_classes):
          mean_diff = <el-select v-model="codeAnswers[1]" placeholder="选择代码" size="small" :disabled="codeChecked">
            <el-option 
              v-for="(option, index) in codeOptions[1]" 
              :key="index"
              :label="option.label"
              :value="option.value"
            ></el-option>
          </el-select>
          
          # 类均值与整体均值的外积
          S_B += <el-select v-model="codeAnswers[2]" placeholder="选择代码" size="small" :disabled="codeChecked">
            <el-option 
              v-for="(option, index) in codeOptions[2]" 
              :key="index"
              :label="option.label"
              :value="option.value"
            ></el-option>
          </el-select>
      
      return S_B</code></pre>
                                </div>
                            </el-tab-pane>

                            <el-tab-pane label="特征值问题求解" name="eigen">
                                <div class="code-block">
                                    <pre><code>def _solve_eigenvalue_problem(self, S_W, S_B):
      """
      求解广义特征值问题 S_B * w = lambda * S_W * w
      
      Parameters
      ----------
      S_W : array-like, shape (n_features, n_features)
          类内散布矩阵.
      S_B : array-like, shape (n_features, n_features)
          类间散布矩阵.
      
      Returns
      -------
      eigvals : array-like, shape (n_features,)
          特征值.
      eigvecs : array-like, shape (n_features, n_features)
          特征向量 (每列一个特征向量).
      """
      # 可能需要处理S_W接近奇异的情况
      try:
          # 求解 S_W^(-1) * S_B 的特征值问题
          <el-select v-model="codeAnswers[3]" placeholder="选择代码" size="small" :disabled="codeChecked">
            <el-option 
              v-for="(option, index) in codeOptions[3]" 
              :key="index"
              :label="option.label"
              :value="option.value"
            ></el-option>
          </el-select>
          
          return eigvals, eigvecs
      except np.linalg.LinAlgError:
          # S_W 接近奇异，使用伪逆或正则化
          print("Warning: 类内散布矩阵接近奇异，使用伪逆")
          inv_S_W = np.linalg.pinv(S_W)
          eigvals, eigvecs = np.linalg.eig(np.dot(inv_S_W, S_B))
          return eigvals.real, eigvecs.real</code></pre>
                                </div>
                            </el-tab-pane>
                        </el-tabs>

                        <div class="code-actions" v-if="!codeChecked">
                            <el-button type="primary" @click="checkCode" :disabled="!allCodeAnswered">
                                检查代码
                            </el-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 回应区域 -->
        <div v-if="showResponse" class="response-area">
            <div class="response-content">
                <i :class="['response-icon', responseIconClass]"></i>
                <div class="response-message" v-html="compiledResponse"></div>
            </div>

            <div class="action-buttons" v-if="codeChecked && allCodeCorrect">
                <el-button type="primary" @click="completeSection">
                    继续学习 <i class="el-icon-arrow-right"></i>
                </el-button>
            </div>
        </div>

        <div v-if="isCompleted" class="completed-message">
            <i class="el-icon-circle-check"></i>
            <span>此部分已完成！</span>
            <el-button v-if="hasNext" type="text" @click="navigateToNext">
                前往下一部分 <i class="el-icon-arrow-right"></i>
            </el-button>
        </div>

        <el-divider></el-divider>
    </div>
</template>

<script>
import { marked } from 'marked';
import 'katex/dist/katex.min.css';
import katex from 'katex';
import draggable from 'vuedraggable';

// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}

export default {
    name: 'LDAImplementationStepByStep',
    components: {
        draggable
    },
    props: {
        sectionId: {
            type: String,
            default: 'lda-implementation'
        },
        sectionIndex: {
            type: Number,
            required: true
        },
        totalSections: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            title: "LDA实现步骤",
            markdownContent: `
  # LDA实现步骤
  
  在理解了LDA的数学原理后，我们来看看如何具体实现LDA算法。本节将按照清晰的步骤，详细讲解LDA的Python实现过程。
  
  ## LDA算法的基本流程
  
  LDA算法实现可以分为以下几个关键步骤：
  
  1. **数据准备和预处理**：加载数据，并进行必要的预处理（如标准化）
  2. **计算每个类的均值向量和全局均值向量**：分别计算每个类别的样本均值，以及所有样本的整体均值
  3. **计算类内散布矩阵** $S_W$：基于每个类内部样本与其类均值的离差平方和
  4. **计算类间散布矩阵** $S_B$：基于各类均值与全局均值的离差平方和
  5. **求解广义特征值问题**：解 $S_B w = \\lambda S_W w$ 或等价的 $S_W^{-1}S_B w = \\lambda w$
  6. **选取前k-1个特征向量**：构建投影矩阵
  7. **数据投影**：利用得到的投影矩阵将原始数据降维
  
  ## 实现中的关键点和技巧
  
  在实现LDA时，需要注意以下几点：
  
  ### 1. 类内散布矩阵可能接近奇异
  
  在高维小样本问题中，类内散布矩阵 $S_W$ 可能接近奇异（不可逆），使得无法直接计算 $S_W^{-1}S_B$。为处理这一问题，常用的方法包括：
  
  - 使用伪逆（Moore-Penrose逆）代替矩阵逆
  - 对 $S_W$ 进行正则化，如添加小的对角项：$S_W + \\alpha I$
  - 先使用PCA降维，再应用LDA
  
  ### 2. 降维空间的维度限制
  
  对于 $k$ 类问题，LDA最多可以得到 $k-1$ 个有效的特征向量（因为类间散布矩阵 $S_B$ 的秩最大为 $k-1$）。这意味着不论原始特征空间维度多高，LDA降维后的维度最大只能是类别数减1。
  
  ### 3. 处理不平衡数据集
  
  当不同类别的样本数量差异很大时，可能会导致过度偏向样本数量多的类别。可以通过对类内散布矩阵中各类的贡献进行归一化来处理。
  
  ## 算法实现示例
  
  下面我们将展示LDA算法的Python实现。在Interactive Exercise部分，你可以尝试排列正确的实现顺序并填充关键代码片段，以加深对算法实现的理解。
        `,
            isCompleted: false,

            // 步骤排序数据
            originalSteps: [
                {
                    id: 1,
                    text: "数据预处理，如标准化、归一化",
                    correctPosition: 0
                },
                {
                    id: 2,
                    text: "计算每个类的均值向量和全局均值向量",
                    correctPosition: 1
                },
                {
                    id: 3,
                    text: "计算类内散布矩阵S_W",
                    correctPosition: 2
                },
                {
                    id: 4,
                    text: "计算类间散布矩阵S_B",
                    correctPosition: 3
                },
                {
                    id: 5,
                    text: "求解广义特征值问题S_B w = λS_W w",
                    correctPosition: 4
                },
                {
                    id: 6,
                    text: "选择对应于最大特征值的特征向量",
                    correctPosition: 5
                },
                {
                    id: 7,
                    text: "使用选出的特征向量构建投影矩阵",
                    correctPosition: 6
                },
                {
                    id: 8,
                    text: "应用投影矩阵将数据降维",
                    correctPosition: 7
                }
            ],
            sortedSteps: [],
            stepsSorted: false,
            allStepsCorrect: false,

            // 代码填空数据
            activeCodeTab: 'class',
            codeOptions: [
                [
                    { value: 0, label: "x_diff = X_c[j] - self.overall_mean" },
                    { value: 1, label: "x_diff = X_c[j] - mean_c" },
                    { value: 2, label: "S_W += np.outer(X_c[j], mean_c)" },
                    { value: 3, label: "S_W += np.outer(x_diff, x_diff)" }
                ],
                [
                    { value: 0, label: "self.mean_vectors[i] - self.mean_vectors[0]" },
                    { value: 1, label: "self.mean_vectors[i]" },
                    { value: 2, label: "self.mean_vectors[i] - self.overall_mean" },
                    { value: 3, label: "self.overall_mean - self.mean_vectors[i]" }
                ],
                [
                    { value: 0, label: "np.dot(mean_diff, mean_diff)" },
                    { value: 1, label: "np.outer(mean_diff, mean_diff)" },
                    { value: 2, label: "mean_diff * mean_diff.T" },
                    { value: 3, label: "mean_diff.T @ mean_diff" }
                ],
                [
                    { value: 0, label: "eigvals, eigvecs = np.linalg.eigh(S_B)" },
                    { value: 1, label: "eigvals, eigvecs = np.linalg.eig(np.dot(np.linalg.inv(S_W), S_B))" },
                    { value: 2, label: "eigvals, eigvecs = np.linalg.eig(np.dot(S_W, S_B))" },
                    { value: 3, label: "eigvals, eigvecs = np.linalg.svd(S_B)" }
                ]
            ],
            codeAnswers: [null, null, null, null],
            correctCodeAnswers: [1, 2, 1, 1],
            codeChecked: false,
            codeResults: [],
            allCodeCorrect: false,

            // 回应部分数据
            showResponse: false,
            response: ''
        }
    },
    computed: {
        compiledMarkdown() {
            const withMath = renderMath(this.markdownContent);
            return marked(withMath);
        },
        compiledResponse() {
            const withMath = renderMath(this.response);
            return marked(withMath);
        },
        responseIconClass() {
            if (this.stepsSorted && !this.codeChecked) {
                return this.allStepsCorrect ? 'el-icon-check correct' : 'el-icon-warning-outline warning';
            } else if (this.codeChecked) {
                return this.allCodeCorrect ? 'el-icon-check correct' : 'el-icon-close incorrect';
            }
            return '';
        },
        hasNext() {
            return this.sectionIndex < this.totalSections;
        },
        allCodeAnswered() {
            return this.codeAnswers.every(answer => answer !== null);
        }
    },
    created() {
        // 检查该部分是否已完成
        const completedSections = this.getCompletedSections();
        this.isCompleted = completedSections.includes(this.sectionId);

        // 初始化步骤排序
        this.sortedSteps = [...this.originalSteps].sort(() => Math.random() - 0.5);
    },
    methods: {
        checkStepOrder() {
            this.stepsSorted = true;

            // 检查步骤是否全部正确
            this.allStepsCorrect = this.sortedSteps.every((step, index) => step.correctPosition === index);

            // 生成回应
            if (this.allStepsCorrect) {
                this.response = `
  ### 🎉 步骤顺序完全正确！
  
  你已经正确地排列了LDA算法的实现步骤。这种清晰的算法流程对于理解和实现LDA至关重要。
  
  现在请继续完成代码填空部分，实现LDA算法的核心功能。
          `;
            } else {
                // 计算正确的步骤数量
                const correctCount = this.sortedSteps.filter((step, index) => step.correctPosition === index).length;

                this.response = `
  ### 部分步骤顺序不正确
  
  你正确排列了${correctCount}/${this.sortedSteps.length}个步骤。请注意算法的逻辑流程，特别是散布矩阵计算和特征值求解的顺序。
  
  不过不用担心，我已经为你显示了正确的步骤顺序。请继续完成代码填空部分，实现LDA算法的核心功能。
          `;
            }

            this.showResponse = true;
        },

        checkCode() {
            this.codeChecked = true;

            // 检查代码是否全部正确
            this.codeResults = this.codeAnswers.map((answer, index) => answer === this.correctCodeAnswers[index]);
            this.allCodeCorrect = this.codeResults.every(result => result);

            // 生成回应
            if (this.allCodeCorrect) {
                this.response = `
  ### 🎉 太棒了！所有代码片段都填写正确！
  
  你已经成功实现了LDA算法的核心功能：
  
  1. 在类内散布矩阵计算中，正确地使用了每个样本与其类均值的差向量外积
  2. 在类间散布矩阵计算中，正确地计算了类均值与全局均值的差向量及其外积
  3. 正确地求解了S_W^(-1) * S_B的特征值问题
  
  这些是LDA算法实现中的关键步骤。通过本练习，你应该已经掌握了LDA的完整实现流程。在实际应用中，你还可以考虑更多优化，如处理奇异矩阵、正则化等高级技巧。
          `;
            } else {
                // 找出错误的代码
                let errorMessages = "";

                if (!this.codeResults[0]) {
                    errorMessages += "- 在类内散布矩阵计算中，我们需要计算每个样本与其**类均值**（而不是全局均值）的差向量\n";
                }

                if (!this.codeResults[1]) {
                    errorMessages += "- 在类间散布矩阵计算中，mean_diff应该是类均值与全局均值的差向量\n";
                }

                if (!this.codeResults[2]) {
                    errorMessages += "- 计算类间散布矩阵时，我们需要使用外积（outer product）而不是点积\n";
                }

                if (!this.codeResults[3]) {
                    errorMessages += "- 求解特征值问题时，我们需要计算S_W^(-1) * S_B的特征值和特征向量\n";
                }

                this.response = `
  ### ❌ 有些代码片段不正确
  
  ${errorMessages}
  
  请仔细回顾LDA的数学原理，并检查你的代码实现。
          `;
            }

            this.showResponse = true;
        },

        completeSection() {
            this.isCompleted = true;
            this.$emit('complete', this.sectionId);

            // 滚动到下一部分
            if (this.hasNext) {
                this.navigateToNext();
            }
        },

        getCompletedSections() {
            const saved = localStorage.getItem('lda-tutorial-progress');
            if (saved) {
                try {
                    return JSON.parse(saved);
                } catch (e) {
                    console.error('Failed to parse completed sections:', e);
                    return [];
                }
            }
            return [];
        },

        navigateToNext() {
            // 计算下一个部分的ID
            const allSections = this.$parent.sections;
            const currentIndex = allSections.findIndex(s => s.id === this.sectionId);

            if (currentIndex >= 0 && currentIndex < allSections.length - 1) {
                const nextSectionId = allSections[currentIndex + 1].id;
                this.$parent.scrollToSection(nextSectionId);
            }
        }
    }
}
</script>

<style scoped>
.tutorial-section {
    margin-bottom: 30px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.section-title {
    margin: 0;
    color: #303133;
}

.section-progress {
    display: flex;
    align-items: center;
}

.section-number {
    margin-left: 10px;
    font-size: 14px;
    color: #909399;
}

.content-area {
    margin-bottom: 20px;
}

.markdown-content {
    line-height: 1.6;
}

/* 互动区域样式 */
.interaction-area {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
}

.interaction-title {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    color: #606266;
}
</style>