<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>4. UMAP算法步骤概述</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - 算法流程图和步骤动画 -->
            <div class="interaction-container">
                <h3>互动演示：UMAP算法流程</h3>
                <p>点击下面的步骤按钮，观察UMAP算法的执行过程。</p>

                <div class="algorithm-steps">
                    <el-steps :active="currentStep" finish-status="success" align-center>
                        <el-step v-for="(step, index) in algorithmSteps" :key="index" :title="step.shortTitle"
                            :description="step.shortDescription">
                        </el-step>
                    </el-steps>

                    <div class="step-navigation">
                        <el-button type="primary" icon="el-icon-arrow-left" :disabled="currentStep <= 0"
                            @click="prevStep">
                            上一步
                        </el-button>
                        <el-button type="primary" @click="nextStep"
                            :disabled="currentStep >= algorithmSteps.length - 1">
                            下一步 <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>
                </div>

                <div class="step-detail-container">
                    <h4>{{ algorithmSteps[currentStep].title }}</h4>
                    <div class="step-visualization" ref="stepVisualization"></div>
                    <div class="step-explanation" v-html="algorithmSteps[currentStep].explanation"></div>
                    <div class="step-code" v-if="algorithmSteps[currentStep].code">
                        <h5>伪代码:</h5>
                        <pre><code>{{ algorithmSteps[currentStep].code }}</code></pre>
                    </div>
                </div>

                <!-- 步骤完成测验 -->
                <div class="quiz-container" v-if="currentStep === algorithmSteps.length - 1 && !quizCompleted">
                    <h3>算法步骤测验</h3>
                    <p>将下面的算法步骤拖动到正确的顺序:</p>

                    <div class="sort-quiz">
                        <draggable v-model="userSortedSteps" animation="300" class="step-list">
                            <div v-for="item in userSortedSteps" :key="item.id" class="sort-item">
                                {{ item.text }}
                            </div>
                        </draggable>
                    </div>

                    <el-button type="primary" @click="checkSortQuiz" class="submit-btn">
                        检查顺序
                    </el-button>
                </div>

                <!-- 回应部分 -->
                <div v-if="quizCompleted" class="response-container">
                    <el-alert :title="quizFeedbackTitle" :type="quizCorrect ? 'success' : 'warning'"
                        :description="quizFeedbackDescription" show-icon>
                    </el-alert>

                    <div v-if="!quizCorrect" class="retry-section">
                        <p>正确的顺序是:</p>
                        <ol>
                            <li v-for="(step, index) in correctSortedSteps" :key="index">
                                {{ step.text }}
                            </li>
                        </ol>

                        <el-button type="info" @click="resetQuiz" class="retry-btn">
                            重新排序
                        </el-button>
                    </div>

                    <div v-if="quizCorrect || quizAttempts >= 2" class="next-section">
                        <p>🎉 恭喜完成算法步骤部分！您可以继续学习下一部分。</p>
                        <el-button type="success" @click="goToNextSection">
                            继续学习 <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import { marked } from 'marked';
import * as d3 from 'd3';
import draggable from 'vuedraggable';

// 设置渲染器以支持数学公式
import 'katex/dist/katex.min.css';
// import katex from 'katex';
import katex from 'katex';
// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}


export default {
    name: 'Section4Algorithm',
    components: {
        draggable
    },
    data() {
        return {
            markdownContent: `
  ## UMAP算法步骤概述
  
  前面我们理解了UMAP的数学基础，现在让我们详细地看看UMAP算法的执行步骤。UMAP算法可以分为以下几个主要阶段:
  
  ### 算法总览
  
  UMAP算法的整体流程如下:
  
  1. **构建高维空间中的模糊拓扑表示**
     - 计算每个点的局部度量
     - 为每个点找到k近邻
     - 构建模糊简单复形
  
  2. **构建低维空间中的初始嵌入**
     - 使用随机投影或其他方法初始化低维表示
     - 优化低维嵌入以匹配高维拓扑
  
  3. **优化低维嵌入**
     - 设置优化目标函数
     - 使用随机梯度下降进行优化
     - 生成最终的低维表示
  
  接下来，我们将更详细地探讨每个步骤，并通过交互式演示来理解它们的工作原理。在这个过程中，我们将看到各个参数如何影响算法的执行和结果。
  
  ### 算法特点
  
  在深入了解算法步骤之前，让我们总结一下UMAP的几个关键特点:
  
  1. **灵活的距离度量** - UMAP可以使用各种距离度量，包括欧几里得距离、余弦距离、汉明距离等。
  
  2. **可扩展性** - UMAP的计算复杂度为O(n log n)，比t-SNE更高效，可以处理更大的数据集。
  
  3. **保留全局结构** - UMAP通过复杂的拓扑表示，能够更好地保留数据的全局结构。
  
  4. **理论基础扎实** - UMAP建立在严格的数学理论上，而不仅仅是启发式算法。
  
  通过接下来的互动演示，我们将直观地理解UMAP算法的每一个步骤是如何协同工作的。
        `,
            currentStep: 0,
            algorithmSteps: [
                {
                    shortTitle: "计算局部度量",
                    shortDescription: "为每个点定义局部度量",
                    title: "步骤1: 计算局部度量",
                    explanation: `
              <p>UMAP首先为数据中的每个点构建一个局部度量。这个步骤基于流形假设，即在每个点的局部邻域内，数据近似欧几里得空间。</p>
              <p>对于每个点 <strong>x</strong>，UMAP:
                <ul>
                  <li>计算到其k个最近邻的距离</li>
                  <li>找到参数 <strong>σ<sub>x</sub></strong>，使得在这个局部度量下，x与其邻居的连接满足某些条件</li>
                  <li>这个 <strong>σ<sub>x</sub></strong> 参数控制了局部距离的缩放</li>
                </ul>
              </p>
              <p>这一步的关键是使得每个点都有一个适合其局部密度的度量，这样算法可以在不同密度的区域都表现良好。</p>
            `,
                    code: `
  # 为每个点计算局部度量参数
  for x in data:
      # 找到x的k个最近邻
      knn = compute_knn(x, k=n_neighbors)
      
      # 计算到第k个近邻的距离
      rho = knn_dists[k-1]
      
      # 使用二分搜索找到使得以下条件成立的sigma_x值:
      # sum(exp(-(d(x,y_i) - rho) / sigma_x)) = log2(k)
      sigma_x = binary_search_sigma(x, knn, rho)
      
      # 存储这个局部度量参数
      local_metrics[x] = sigma_x
            `
                },
                {
                    shortTitle: "构建模糊图",
                    shortDescription: "计算点之间的连接强度",
                    title: "步骤2: 构建高维空间的模糊图表示",
                    explanation: `
              <p>使用第一步计算的局部度量，UMAP构建一个加权图，其中权重表示点之间的相似度或连接强度。这个图捕捉了数据的拓扑结构。</p>
              <p>对于每对点x和y，UMAP计算:
                <ul>
                  <li>点x在其局部度量下"认为"与点y的相似度: <strong>v<sub>x,y</sub></strong> = exp(-(d(x,y) - ρ<sub>x</sub>)/σ<sub>x</sub>)</li>
                  <li>点y在其局部度量下"认为"与点x的相似度: <strong>v<sub>y,x</sub></strong> = exp(-(d(y,x) - ρ<sub>y</sub>)/σ<sub>y</sub>)</li>
                  <li>合并这两个值得到最终权重: <strong>w(x,y)</strong> = v<sub>x,y</sub> + v<sub>y,x</sub> - v<sub>x,y</sub>·v<sub>y,x</sub></li>
                </ul>
              </p>
              <p>这个模糊图是对高维数据拓扑的表示，它考虑了全局和局部关系。</p>
            `,
                    code: `
  # 构建模糊图
  graph = empty_weighted_graph()
  
  for x in data:
      for y in knn[x]:
          # 计算x认为与y的连接强度
          d_x = distance(x, y)
          v_xy = exp(-(d_x - rho_x) / sigma_x)
          
          # 计算y认为与x的连接强度
          d_y = distance(y, x)
          v_yx = exp(-(d_y - rho_y) / sigma_y)
          
          # 合并得到最终权重
          weight = v_xy + v_yx - v_xy * v_yx
          
          # 添加边到图中
          graph.add_edge(x, y, weight)
            `
                },
                {
                    shortTitle: "初始化低维嵌入",
                    shortDescription: "创建初始低维投影",
                    title: "步骤3: 初始化低维空间的嵌入",
                    explanation: `
              <p>在构建了高维空间的拓扑表示后，UMAP需要在低维空间中创建初始点分布。这个初始分布将在后续步骤中被优化。</p>
              <p>初始化方法包括:
                <ul>
                  <li>随机初始化: 在低维空间中随机分配点位置</li>
                  <li>使用PCA或其他线性投影方法进行初始化</li>
                  <li>使用其他算法(如Laplacian Eigenmaps)的结果作为初始化</li>
                </ul>
              </p>
              <p>初始化的质量会影响算法的收敛速度，但最终结果对初始化并不是特别敏感。</p>
            `,
                    code: `
  # 初始化低维嵌入
  if init == 'random':
      # 随机初始化
      embedding = random_uniform(-10, 10, (n_samples, n_components))
  elif init == 'spectral':
      # 使用谱嵌入(如Laplacian Eigenmaps)
      embedding = spectral_embedding(graph, n_components)
  elif init == 'pca':
      # 使用PCA进行初始化
      embedding = pca(data, n_components)
  else:
      # 使用提供的初始化
      embedding = init
            `
                },
                {
                    shortTitle: "优化嵌入",
                    shortDescription: "使用梯度下降优化投影",
                    title: "步骤4: 优化低维嵌入",
                    explanation: `
              <p>最后，UMAP通过优化一个目标函数来调整低维空间中点的位置，使其尽可能地匹配高维空间的拓扑结构。</p>
              <p>优化过程:
                <ul>
                  <li>定义吸引力和排斥力，基于高维空间中点的连接强度</li>
                  <li>使用随机梯度下降(SGD)最小化交叉熵损失函数</li>
                  <li>随着迭代进行，学习率逐渐减小</li>
                  <li>当达到最大迭代次数或收敛时停止</li>
                </ul>
              </p>
              <p>这个过程可以类比为一个物理系统，其中连接强的点之间有吸引力，连接弱或没有连接的点之间有排斥力。</p>
            `,
                    code: `
  # 优化低维嵌入
  for epoch in range(n_epochs):
      # 更新学习率
      alpha = initial_alpha * (1.0 - (epoch / n_epochs))
      
      # 随机选择边进行优化
      for edge in random_sample(graph.edges, n_samples_per_epoch):
          source, target, weight = edge
          
          # 计算低维空间中的距离
          dist = distance(embedding[source], embedding[target])
          
          # 计算吸引力和排斥力
          if dist > min_dist:
              # 计算梯度
              grad_coeff = -2.0 * weight * (1.0 / (1.0 + dist**2))
              grad = grad_coeff * (embedding[source] - embedding[target])
              
              # 更新嵌入
              embedding[source] += alpha * grad
              embedding[target] -= alpha * grad
      
      # 计算负采样(排斥力)
      for i in range(n_negative_samples):
          source = random_int(0, n_samples)
          target = random_int(0, n_samples)
          
          # 如果两点没有连接，添加排斥力
          if not graph.has_edge(source, target):
              dist = distance(embedding[source], embedding[target])
              grad_coeff = 2.0 / ((1.0 + dist**2) * n_samples)
              grad = grad_coeff * (embedding[source] - embedding[target])
              
              # 更新嵌入
              embedding[source] += alpha * grad
              embedding[target] -= alpha * grad
            `
                },
                {
                    shortTitle: "完成降维",
                    shortDescription: "生成最终的低维表示",
                    title: "步骤5: 完成降维并输出结果",
                    explanation: `
              <p>经过上述步骤，UMAP算法完成了降维过程，生成最终的低维表示。</p>
              <p>最终结果:
                <ul>
                  <li>每个原始高维数据点对应一个低维空间中的点</li>
                  <li>低维表示保留了高维数据的关键拓扑结构</li>
                  <li>相似的数据点在低维空间中保持接近</li>
                  <li>数据簇的结构和相对位置得到保持</li>
                </ul>
              </p>
              <p>这个最终的低维表示可以用于可视化、聚类或作为后续机器学习任务的输入特征。</p>
            `,
                    code: `
  # 最终处理和返回结果
  if output_metric == 'euclidean':
      # 对结果进行归一化
      embedding = normalize(embedding)
  
  # 返回降维后的表示
  return embedding
            `
                }
            ],
            correctSortedSteps: [
                { id: 1, text: "计算每个数据点的局部度量参数" },
                { id: 2, text: "基于局部度量构建高维空间的模糊图表示" },
                { id: 3, text: "在低维空间中初始化数据点的位置" },
                { id: 4, text: "通过优化目标函数调整低维空间中点的位置" },
                { id: 5, text: "完成降维并输出保留拓扑结构的结果" }
            ],
            userSortedSteps: [],
            quizCompleted: false,
            quizCorrect: false,
            quizAttempts: 0,
            isCompleted: false,
            stepVisualizations: null
        }
    },
    computed: {
        renderedContent() {
            const withMath = renderMath(this.markdownContent)
            return marked(withMath)
        },
        quizFeedbackTitle() {
            return this.quizCorrect ? '排序正确！' : '排序不正确';
        },
        quizFeedbackDescription() {
            return this.quizCorrect
                ? '您已经正确理解了UMAP算法的执行步骤顺序！'
                : '排序不正确。请查看下方的正确顺序，理解各步骤之间的依赖关系。';
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(4);
        }

        // 初始化排序问题的顺序（随机打乱）
        this.userSortedSteps = [...this.correctSortedSteps]
            .sort(() => Math.random() - 0.5);

        // 初始化每个步骤的可视化
        this.initStepVisualizations();
    },
    methods: {
        initStepVisualizations() {
            // 创建一个数组来存储每个步骤的可视化函数
            this.stepVisualizations = [
                this.visualizeStep1,
                this.visualizeStep2,
                this.visualizeStep3,
                this.visualizeStep4,
                this.visualizeStep5
            ];

            // 渲染当前步骤的可视化
            this.$nextTick(() => {
                if (this.$refs.stepVisualization) {
                    this.renderCurrentStepVisualization();
                }
            });
        },

        renderCurrentStepVisualization() {
            // 清除现有可视化
            d3.select(this.$refs.stepVisualization).selectAll("*").remove();

            // 调用当前步骤的可视化函数
            if (this.stepVisualizations && this.stepVisualizations[this.currentStep]) {
                this.stepVisualizations[this.currentStep]();
            }
        },

        visualizeStep1() {
            // 第一步：局部度量可视化
            const width = this.$refs.stepVisualization.clientWidth;
            const height = 300;

            const svg = d3.select(this.$refs.stepVisualization)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 生成示例数据点
            const points = [];
            for (let i = 0; i < 50; i++) {
                points.push({
                    id: i,
                    x: Math.random() * width * 0.8 + width * 0.1,
                    y: Math.random() * height * 0.8 + height * 0.1,
                    radius: 5
                });
            }

            // 随机选择一个焦点
            const focusPoint = points[Math.floor(Math.random() * points.length)];
            focusPoint.radius = 8;

            // 计算所有点到焦点的距离
            points.forEach(point => {
                if (point !== focusPoint) {
                    const dx = point.x - focusPoint.x;
                    const dy = point.y - focusPoint.y;
                    point.distance = Math.sqrt(dx * dx + dy * dy);
                } else {
                    point.distance = 0;
                }
            });
            // 找到距离排序后的k个最近邻
            const k = 7;
            const neighbors = [...points]
                .filter(p => p !== focusPoint)
                .sort((a, b) => a.distance - b.distance)
                .slice(0, k);

            // 绘制所有点
            svg.selectAll("circle.point")
                .data(points)
                .enter()
                .append("circle")
                .attr("class", "point")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", d => d.radius)
                .attr("fill", d => d === focusPoint ? "#F56C6C" :
                    (neighbors.includes(d) ? "#67C23A" : "#909399"))
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5);

            // 绘制连接线
            svg.selectAll("line")
                .data(neighbors)
                .enter()
                .append("line")
                .attr("x1", focusPoint.x)
                .attr("y1", focusPoint.y)
                .attr("x2", d => d.x)
                .attr("y2", d => d.y)
                .attr("stroke", "#67C23A")
                .attr("stroke-width", 1.5)
                .attr("stroke-dasharray", "3,3");

            // 添加距离标签
            svg.selectAll("text.distance")
                .data(neighbors)
                .enter()
                .append("text")
                .attr("class", "distance")
                .attr("x", d => (focusPoint.x + d.x) / 2)
                .attr("y", d => (focusPoint.y + d.y) / 2 - 5)
                .attr("text-anchor", "middle")
                .attr("font-size", "10px")
                .attr("fill", "#303133")
                .text(d => d.distance.toFixed(1));

            // 添加局部度量圆
            const maxNeighborDist = neighbors[k - 1].distance;
            svg.append("circle")
                .attr("cx", focusPoint.x)
                .attr("cy", focusPoint.y)
                .attr("r", maxNeighborDist)
                .attr("fill", "none")
                .attr("stroke", "#F56C6C")
                .attr("stroke-width", 1)
                .attr("stroke-dasharray", "5,5");

            // 添加说明文本
            svg.append("text")
                .attr("x", 10)
                .attr("y", 20)
                .attr("font-size", "12px")
                .attr("fill", "#303133")
                .text(`红色点: 焦点 | 绿色点: ${k}个最近邻 | 虚线圆: 局部度量范围 (σ)`)
        },

        visualizeStep2() {
            // 第二步：构建模糊图可视化
            const width = this.$refs.stepVisualization.clientWidth;
            const height = 300;

            const svg = d3.select(this.$refs.stepVisualization)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 生成网格状的点
            const rows = 5;
            const cols = 7;
            const margin = 40;
            const gridWidth = width - margin * 2;
            const gridHeight = height - margin * 2;
            const cellWidth = gridWidth / (cols - 1);
            const cellHeight = gridHeight / (rows - 1);

            const points = [];
            for (let i = 0; i < rows; i++) {
                for (let j = 0; j < cols; j++) {
                    points.push({
                        id: i * cols + j,
                        x: margin + j * cellWidth,
                        y: margin + i * cellHeight,
                        row: i,
                        col: j
                    });
                }
            }

            // 计算点之间的连接
            const edges = [];
            for (let i = 0; i < points.length; i++) {
                for (let j = i + 1; j < points.length; j++) {
                    const source = points[i];
                    const target = points[j];

                    // 计算曼哈顿距离
                    const manhattanDist = Math.abs(source.row - target.row) + Math.abs(source.col - target.col);

                    // 只连接曼哈顿距离为1的点（上下左右相邻）
                    if (manhattanDist === 1) {
                        edges.push({
                            source,
                            target,
                            weight: 1.0
                        });
                    }
                    // 对角线连接，权重较低
                    else if (manhattanDist === 2 &&
                        Math.abs(source.row - target.row) === 1 &&
                        Math.abs(source.col - target.col) === 1) {
                        edges.push({
                            source,
                            target,
                            weight: 0.5
                        });
                    }
                }
            }

            // 绘制连接线，线宽表示权重
            svg.selectAll("line")
                .data(edges)
                .enter()
                .append("line")
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y)
                .attr("stroke", "#409EFF")
                .attr("stroke-width", d => d.weight * 3)
                .attr("opacity", d => 0.3 + d.weight * 0.7);

            // 绘制所有点
            svg.selectAll("circle")
                .data(points)
                .enter()
                .append("circle")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 6)
                .attr("fill", "#409EFF")
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5);

            // 添加说明文本
            svg.append("text")
                .attr("x", 10)
                .attr("y", 20)
                .attr("font-size", "12px")
                .attr("fill", "#303133")
                .text("模糊图: 线条粗细表示连接强度 (上下左右连接强度高，对角线连接强度低)");
        },

        visualizeStep3() {
            // 第三步：初始化低维嵌入可视化
            const width = this.$refs.stepVisualization.clientWidth;
            const height = 300;

            const svg = d3.select(this.$refs.stepVisualization)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 生成三个簇的数据
            const numClusters = 3;
            const pointsPerCluster = 15;
            const points = [];

            const colors = ["#F56C6C", "#E6A23C", "#67C23A"];

            for (let c = 0; c < numClusters; c++) {
                const centerX = Math.random() * width * 0.6 + width * 0.2;
                const centerY = Math.random() * height * 0.6 + height * 0.2;

                for (let i = 0; i < pointsPerCluster; i++) {
                    points.push({
                        id: c * pointsPerCluster + i,
                        x: centerX + (Math.random() - 0.5) * 40,
                        y: centerY + (Math.random() - 0.5) * 40,
                        cluster: c,
                        color: colors[c]
                    });
                }
            }

            // 绘制背景网格
            const gridSize = 20;
            for (let x = 0; x < width; x += gridSize) {
                svg.append("line")
                    .attr("x1", x)
                    .attr("y1", 0)
                    .attr("x2", x)
                    .attr("y2", height)
                    .attr("stroke", "#f0f0f0")
                    .attr("stroke-width", 1);
            }

            for (let y = 0; y < height; y += gridSize) {
                svg.append("line")
                    .attr("x1", 0)
                    .attr("y1", y)
                    .attr("x2", width)
                    .attr("y2", y)
                    .attr("stroke", "#f0f0f0")
                    .attr("stroke-width", 1);
            }

            // 绘制坐标轴
            svg.append("line")
                .attr("x1", 20)
                .attr("y1", height - 20)
                .attr("x2", width - 20)
                .attr("y2", height - 20)
                .attr("stroke", "#909399")
                .attr("stroke-width", 1.5)
                .attr("marker-end", "url(#arrowhead)");

            svg.append("line")
                .attr("x1", 20)
                .attr("y1", height - 20)
                .attr("x2", 20)
                .attr("y2", 20)
                .attr("stroke", "#909399")
                .attr("stroke-width", 1.5)
                .attr("marker-end", "url(#arrowhead)");

            // 添加箭头定义
            svg.append("defs").append("marker")
                .attr("id", "arrowhead")
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 8)
                .attr("refY", 0)
                .attr("markerWidth", 6)
                .attr("markerHeight", 6)
                .attr("orient", "auto")
                .append("path")
                .attr("d", "M0,-5L10,0L0,5")
                .attr("fill", "#909399");

            // 添加坐标轴标签
            svg.append("text")
                .attr("x", width - 15)
                .attr("y", height - 5)
                .attr("font-size", "12px")
                .attr("fill", "#909399")
                .text("维度1");

            svg.append("text")
                .attr("x", 5)
                .attr("y", 15)
                .attr("font-size", "12px")
                .attr("fill", "#909399")
                .text("维度2");

            // 绘制点
            svg.selectAll("circle")
                .data(points)
                .enter()
                .append("circle")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 5)
                .attr("fill", d => d.color)
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5);

            // 添加说明文本
            svg.append("text")
                .attr("x", 10)
                .attr("y", 40)
                .attr("font-size", "12px")
                .attr("fill", "#303133")
                .text("低维空间初始化: 不同颜色代表不同簇的点");
        },

        visualizeStep4() {
            // 第四步：优化低维嵌入可视化 - 使用力导向图模拟优化过程
            const width = this.$refs.stepVisualization.clientWidth;
            const height = 300;

            const svg = d3.select(this.$refs.stepVisualization)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 生成三个簇的数据
            const numClusters = 3;
            const pointsPerCluster = 12;
            const points = [];

            const colors = ["#F56C6C", "#E6A23C", "#67C23A"];

            // 初始状态 - 点分布较混乱
            for (let c = 0; c < numClusters; c++) {
                const centerX = width / 2 + (Math.random() - 0.5) * 60;
                const centerY = height / 2 + (Math.random() - 0.5) * 60;

                for (let i = 0; i < pointsPerCluster; i++) {
                    points.push({
                        id: c * pointsPerCluster + i,
                        x: centerX + (Math.random() - 0.5) * 100,
                        y: centerY + (Math.random() - 0.5) * 100,
                        cluster: c,
                        color: colors[c],
                        targetX: width * (0.25 + c * 0.25), // 目标位置 - 优化后应该达到的位置
                        targetY: height / 2
                    });
                }
            }

            // 创建连接 - 同一簇内的点相互连接
            const links = [];
            for (let i = 0; i < points.length; i++) {
                for (let j = i + 1; j < points.length; j++) {
                    if (points[i].cluster === points[j].cluster) {
                        links.push({
                            source: points[i],
                            target: points[j],
                            strength: 0.5
                        });
                    }
                }
            }

            // 绘制迭代状态标签
            const iterationLabel = svg.append("text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .attr("font-size", "14px")
                .attr("font-weight", "bold")
                .attr("fill", "#303133")
                .text("优化迭代: 0");

            // 绘制连接线
            const lineElements = svg.selectAll("line")
                .data(links)
                .enter()
                .append("line")
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y)
                .attr("stroke", "#ddd")
                .attr("stroke-width", 0.5)
                .attr("opacity", 0.3);

            // 绘制点
            const circleElements = svg.selectAll("circle")
                .data(points)
                .enter()
                .append("circle")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 5)
                .attr("fill", d => d.color)
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5);

            // 添加说明文本
            svg.append("text")
                .attr("x", 10)
                .attr("y", height - 10)
                .attr("font-size", "12px")
                .attr("fill", "#303133")
                .text("优化过程: 同一颜色的点相互吸引，不同颜色的点相互排斥");

            // 使用d3力导向模拟优化过程
            d3.forceSimulation(points)
                .force("link", d3.forceLink(links).strength(d => d.strength))
                .force("charge", d3.forceManyBody().strength(-20))
                .force("cluster", forceCluster())
                .force("collide", d3.forceCollide(6))
                .on("tick", ticked)
                .alpha(0.3)
                .alphaDecay(0.005);

            let iteration = 0;

            function ticked() {
                lineElements
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                circleElements
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);

                iteration++;
                iterationLabel.text(`优化迭代: ${iteration}`);

                // 限制在可视区域内
                points.forEach(d => {
                    d.x = Math.max(5, Math.min(width - 5, d.x));
                    d.y = Math.max(5, Math.min(height - 5, d.y));
                });
            }

            // 添加自定义力，将点吸引到目标位置
            function forceCluster() {
                // let alpha = 0.2;

                function force(alpha) {
                    for (let i = 0, n = points.length; i < n; i++) {
                        const d = points[i];
                        // 添加一个力将点拉向其目标位置
                        d.vx += (d.targetX - d.x) * alpha;
                        d.vy += (d.targetY - d.y) * alpha;
                    }
                }

                // force.initialize = function (_) {
                //     points = [_];
                // };

                return force;
            }
        },

        visualizeStep5() {
            // 第五步：完成降维可视化
            const width = this.$refs.stepVisualization.clientWidth;
            const height = 300;

            const svg = d3.select(this.$refs.stepVisualization)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 创建三个完全分离的簇
            const numClusters = 3;
            const pointsPerCluster = 20;
            const points = [];

            const colors = ["#F56C6C", "#E6A23C", "#67C23A"];

            // 最终状态 - 点形成清晰的簇
            for (let c = 0; c < numClusters; c++) {
                const centerX = width * (0.25 + c * 0.25);
                const centerY = height / 2;

                for (let i = 0; i < pointsPerCluster; i++) {
                    const angle = Math.random() * Math.PI * 2;
                    const radius = Math.random() * 30;
                    points.push({
                        id: c * pointsPerCluster + i,
                        x: centerX + Math.cos(angle) * radius,
                        y: centerY + Math.sin(angle) * radius,
                        cluster: c,
                        color: colors[c]
                    });
                }
            }

            // 绘制簇椭圆
            const clusterCenters = [];
            for (let c = 0; c < numClusters; c++) {
                const centerX = width * (0.25 + c * 0.25);
                const centerY = height / 2;
                clusterCenters.push({ x: centerX, y: centerY, cluster: c });

                svg.append("ellipse")
                    .attr("cx", centerX)
                    .attr("cy", centerY)
                    .attr("rx", 40)
                    .attr("ry", 40)
                    .attr("fill", colors[c])
                    .attr("opacity", 0.1)
                    .attr("stroke", colors[c])
                    .attr("stroke-width", 1)
                    .attr("stroke-dasharray", "3,3");
            }

            // 绘制点
            svg.selectAll("circle.point")
                .data(points)
                .enter()
                .append("circle")
                .attr("class", "point")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 5)
                .attr("fill", d => d.color)
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5);

            // 绘制簇中心
            svg.selectAll("circle.center")
                .data(clusterCenters)
                .enter()
                .append("circle")
                .attr("class", "center")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 8)
                .attr("fill", d => colors[d.cluster])
                .attr("stroke", "#fff")
                .attr("stroke-width", 2)
                .attr("opacity", 0.8);

            // 添加说明文本
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .attr("font-size", "14px")
                .attr("font-weight", "bold")
                .attr("fill", "#303133")
                .text("最终降维结果");

            svg.append("text")
                .attr("x", 10)
                .attr("y", height - 10)
                .attr("font-size", "12px")
                .attr("fill", "#303133")
                .text("相似点聚集在一起，形成清晰的簇。大圆表示簇中心。");
        },

        prevStep() {
            if (this.currentStep > 0) {
                this.currentStep--;
                this.renderCurrentStepVisualization();
            }
        },

        nextStep() {
            if (this.currentStep < this.algorithmSteps.length - 1) {
                this.currentStep++;
                this.renderCurrentStepVisualization();
            }
        },

        checkSortQuiz() {
            // 检查排序是否正确
            this.quizCompleted = true;
            this.quizCorrect = true;

            for (let i = 0; i < this.correctSortedSteps.length; i++) {
                if (this.userSortedSteps[i].id !== this.correctSortedSteps[i].id) {
                    this.quizCorrect = false;
                    break;
                }
            }

            this.quizAttempts++;

            if (this.quizCorrect || this.quizAttempts >= 2) {
                this.isCompleted = true;
                this.$emit('complete');
            }
        },

        resetQuiz() {
            this.quizCompleted = false;
            // 重新随机排序
            this.userSortedSteps = [...this.correctSortedSteps]
                .sort(() => Math.random() - 0.5);
        },

        goToNextSection() {
            this.$emit('complete');
            this.$emit('scrollToSection')
        }
    },
    watch: {
        currentStep() {
            this.renderCurrentStepVisualization();
        }
    }
}
</script>

<style scoped>
.section-container {
    margin-bottom: 40px;
}

.section-card {
    margin-bottom: 20px;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.markdown-content {
    margin-bottom: 30px;
}

.interaction-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 4px;
    margin-top: 20px;
}

.algorithm-steps {
    margin-bottom: 30px;
}

.step-navigation {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}

.step-detail-container {
    margin-top: 30px;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.step-visualization {
    width: 100%;
    height: 300px;
    margin: 15px 0;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    overflow: hidden;
}

.step-explanation {
    margin: 15px 0;
    line-height: 1.6;
}

.step-code {
    margin: 15px 0;
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 4px;
    overflow-x: auto;
}


/* 最彻底的样式修复（添加到全局CSS或scoped样式） */
.step-code pre {
    all: initial;
    /* 重置所有继承样式 */
    display: block;
    white-space: pre;
    /* 必须用pre（不是pre-wrap） */
    font-family: monospace;
    /* 等宽字体 */
    margin: 0;
    padding: 1em;
    overflow: auto;
    background: #f5f5f5;
    border-radius: 4px;
}

.step-code code {
    display: block;
    line-height: 1.5;
    /* 行高 */
    tab-size: 4;
    /* 缩进宽度 */
}

.quiz-container {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px dashed #dcdfe6;
}

.sort-quiz {
    margin: 20px 0;
}

.step-list {
    list-style: none;
    padding: 0;
}

.sort-item {
    padding: 10px 15px;
    background-color: white;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    margin-bottom: 10px;
    cursor: move;
    transition: all 0.3s;
}

.sort-item:hover {
    background-color: #f5f7fa;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.submit-btn {
    margin-top: 20px;
}

.response-container {
    margin-top: 20px;
}

.retry-section {
    margin-top: 20px;
    padding: 15px;
    background-color: #f2f6fc;
    border-radius: 4px;
}

.retry-btn {
    margin-top: 15px;
}

.next-section {
    margin-top: 20px;
    text-align: center;
}

/* 全局样式适配 */
:deep(h2),
:deep(h3),
:deep(h4),
:deep(h5) {
    margin-top: 15px;
    margin-bottom: 15px;
}

:deep(ul),
:deep(ol) {
    padding-left: 20px;
    margin: 10px 0;
}

:deep(li) {
    margin: 5px 0;
}

:deep(strong) {
    color: #409EFF;
}
</style>