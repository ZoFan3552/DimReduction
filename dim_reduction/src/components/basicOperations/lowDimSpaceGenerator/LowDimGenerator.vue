<template>
    <div class="low-dim-initializer">
        <el-card class="initializer-card">
            <div slot="header" class="card-header">
                <span>低维空间初始化</span>
                <el-button type="primary" size="small" :loading="isProcessing" :disabled="!selectedMethod || !hasData"
                    @click="initializeSpace">
                    初始化坐标
                </el-button>
            </div>

            <el-form label-position="top" size="small">
                <!-- 维度选择 -->
                <el-form-item label="目标维度">
                    <el-radio-group v-model="dimensions">
                        <el-radio :label="2">2维</el-radio>
                        <el-radio :label="3">3维</el-radio>
                    </el-radio-group>
                </el-form-item>

                <!-- 初始化方法选择 -->
                <el-form-item label="初始化方法">
                    <el-select v-model="selectedMethod" placeholder="请选择初始化方法" style="width: 100%">
                        <el-option v-for="method in initMethods" :key="method.value" :label="method.label"
                            :value="method.value"></el-option>
                    </el-select>
                </el-form-item>

                <!-- 方法参数设置 -->
                <div v-if="selectedMethod === 'normal'">
                    <el-form-item label="正态分布标准差">
                        <el-slider v-model="normalStdDev" :min="0.01" :max="5" :step="0.01" show-input></el-slider>
                    </el-form-item>
                </div>

                <div v-if="selectedMethod === 'uniform'">
                    <el-form-item label="均匀分布范围">
                        <el-slider v-model="uniformRange" :min="0.1" :max="10" :step="0.1" show-input></el-slider>
                    </el-form-item>
                </div>

                <div v-if="selectedMethod === 'circle'">
                    <el-form-item label="圆形半径">
                        <el-slider v-model="circleRadius" :min="0.5" :max="10" :step="0.1" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label="随机扰动">
                        <el-slider v-model="circleNoise" :min="0" :max="1" :step="0.01" show-input></el-slider>
                    </el-form-item>
                </div>

                <div v-if="selectedMethod === 'grid'">
                    <el-form-item label="网格扰动">
                        <el-slider v-model="gridNoise" :min="0" :max="1" :step="0.01" show-input></el-slider>
                    </el-form-item>
                </div>

                <div v-if="selectedMethod === 'pca'">
                    <el-alert title="提示" type="info" description="此方法将使用随机投影模拟PCA效果，速度快但不保证数据结构保留。" :closable="false"
                        show-icon></el-alert>
                </div>
            </el-form>
        </el-card>

        <!-- 可视化预览 -->
        <el-card v-if="previewData" class="preview-card">
            <div slot="header" class="card-header">
                <span>低维空间预览</span>
                <div class="preview-actions">
                    <el-button size="small" type="success" @click="applyToNode">应用到节点</el-button>
                    <el-button size="small" type="default" @click="resetPreview">重置</el-button>
                </div>
            </div>

            <div class="preview-container" ref="previewContainer"></div>

            <div class="preview-info">
                <el-alert title="数据点分布预览" type="success" description="此图展示了初始化后的低维数据分布。每个点的颜色代表其原始类别。" :closable="false"
                    show-icon></el-alert>
            </div>
        </el-card>

        <!-- 处理中对话框 -->
        <el-dialog title="正在处理" :visible.sync="processingVisible" :close-on-click-modal="false"
            :close-on-press-escape="false" :show-close="false" width="30%">
            <div class="processing-content">
                <el-progress type="circle" :percentage="processingProgress"></el-progress>
                <p>{{ processingMessage }}</p>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'LowDimensionInitializer',
    props: {

        nodeData: {
            type: Object,
            default: () => ({})
        },

        // 当前节点ID
        // nodeId: {
        //     type: String,
        //     required: true
        // },
        // 当前节点数据集
        // dataset: {
        //     type: Array,
        //     default: () => []
        // },
        // 数据标签
        // labels: {
        //     type: Array,
        //     default: () => []
        // }
    },
    data() {
        return {
            // labels: this.nodeData.target,
            // dataset: this.nodeData.dataset,
            // 初始化参数
            dimensions: 2,
            selectedMethod: '',
            normalStdDev: 1.0,
            uniformRange: 5.0,
            circleRadius: 3.0,
            circleNoise: 0.2,
            gridNoise: 0.2,

            // 处理状态
            isProcessing: false,
            processingVisible: false,
            processingProgress: 0,
            processingMessage: '',

            // 预览数据
            previewData: null,

            // 可用的初始化方法
            initMethods: [
                { value: 'origin', label: '原点集中 (全部数据点在坐标原点)' },
                { value: 'normal', label: '正态分布 (高斯分布随机初始化)' },
                { value: 'uniform', label: '均匀分布 (随机分布在一个区域内)' },
                { value: 'circle', label: '圆形分布 (数据点分布在圆周上)' },
                { value: 'grid', label: '网格分布 (有序网格状排列)' },
                { value: 'pca', label: '随机投影 (近似PCA效果)' }
            ]
        };
    },
    computed: {
        // 是否有数据可处理
        hasData() {
            return this.nodeData.dataset && this.nodeData.dataset.length > 0;
        }
    },
    methods: {
        // 初始化低维空间
        initializeSpace() {
            if (!this.selectedMethod || !this.hasData) return;

            this.isProcessing = true;
            this.processingVisible = true;
            this.processingProgress = 0;
            this.processingMessage = `正在使用${this.getMethodName()}初始化坐标...`;

            // 模拟进度
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += 5;
                if (progress >= 90) {
                    clearInterval(progressInterval);
                }
                this.processingProgress = progress;
            }, 50);

            // 使用setTimeout模拟异步处理
            setTimeout(() => {
                // 生成低维坐标
                const lowDimCoordinates = this.generateLowDimCoordinates();

                // 清除计时器
                clearInterval(progressInterval);
                this.processingProgress = 100;
                this.processingMessage = '初始化完成!';

                // 设置预览数据
                this.previewData = {
                    coordinates: lowDimCoordinates,
                    labels: this.nodeData.target
                };

                // 关闭处理对话框
                setTimeout(() => {
                    this.processingVisible = false;
                    this.isProcessing = false;

                    // 渲染预览
                    this.$nextTick(() => {
                        this.renderPreview();
                    });
                }, 500);
            }, 1000);
        },

        // 获取方法名称
        getMethodName() {
            const method = this.initMethods.find(m => m.value === this.selectedMethod);
            return method ? method.label : this.selectedMethod;
        },

        // 生成低维坐标
        generateLowDimCoordinates() {
            const n = this.nodeData.dataset.length;
            const d = this.dimensions;
            const coordinates = [];

            switch (this.selectedMethod) {
                case 'origin':
                    {// 所有点都在原点附近的小范围内
                        const range = 0.1; // 定义小范围的大小，可以根据需要调整
                        for (let i = 0; i < n; i++) {
                            const point = new Array(d).fill(0).map(() => (Math.random() * 2 - 1) * range); // 在[-range, range]范围内生成随机数
                            coordinates.push(point);
                        }
                    }
                    break;

                case 'normal':
                    // 正态分布
                    for (let i = 0; i < n; i++) {
                        const point = [];
                        for (let j = 0; j < d; j++) {
                            // Box-Muller变换生成正态分布随机数
                            const u1 = Math.random();
                            const u2 = Math.random();
                            const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
                            point.push(z * this.normalStdDev);
                        }
                        coordinates.push(point);
                    }
                    break;

                case 'uniform':
                    {// 均匀分布
                        const range = this.uniformRange;
                        for (let i = 0; i < n; i++) {
                            const point = [];
                            for (let j = 0; j < d; j++) {
                                point.push((Math.random() * 2 - 1) * range);
                            }
                            coordinates.push(point);
                        }
                    }
                    break;

                case 'circle':
                    // 圆形分布
                    if (d === 2) {
                        // 2D圆形
                        for (let i = 0; i < n; i++) {
                            const angle = (i / n) * 2 * Math.PI;
                            const radius = this.circleRadius * (1 + (Math.random() * 2 - 1) * this.circleNoise);
                            coordinates.push([
                                Math.cos(angle) * radius,
                                Math.sin(angle) * radius
                            ]);
                        }
                    } else {
                        // 3D球面
                        for (let i = 0; i < n; i++) {
                            const phi = Math.acos(2 * Math.random() - 1) - Math.PI / 2;
                            const theta = Math.random() * 2 * Math.PI;
                            const radius = this.circleRadius * (1 + (Math.random() * 2 - 1) * this.circleNoise);

                            coordinates.push([
                                radius * Math.cos(phi) * Math.cos(theta),
                                radius * Math.cos(phi) * Math.sin(theta),
                                radius * Math.sin(phi)
                            ]);
                        }
                    }
                    break;

                case 'grid':
                    {// 网格分布
                        const side = Math.ceil(Math.sqrt(n));
                        const step = 10 / side;

                        for (let i = 0; i < n; i++) {
                            const row = Math.floor(i / side);
                            const col = i % side;

                            if (d === 2) {
                                coordinates.push([
                                    -5 + col * step + (Math.random() * 2 - 1) * step * this.gridNoise,
                                    -5 + row * step + (Math.random() * 2 - 1) * step * this.gridNoise
                                ]);
                            } else {
                                const layer = Math.floor(i / (side * side));
                                const layerIdx = i % (side * side);
                                const layerRow = Math.floor(layerIdx / side);
                                const layerCol = layerIdx % side;

                                coordinates.push([
                                    -5 + layerCol * step + (Math.random() * 2 - 1) * step * this.gridNoise,
                                    -5 + layerRow * step + (Math.random() * 2 - 1) * step * this.gridNoise,
                                    -5 + layer * step + (Math.random() * 2 - 1) * step * this.gridNoise
                                ]);
                            }
                        }
                    }
                    break;

                case 'pca':
                    {// 随机投影（模拟PCA效果）
                        // 生成随机投影矩阵
                        const projectionMatrix = [];
                        for (let i = 0; i < this.nodeData.dataset[0].length; i++) {
                            const row = [];
                            for (let j = 0; j < d; j++) {
                                row.push(Math.random() * 2 - 1);
                            }
                            projectionMatrix.push(row);
                        }

                        // 对每个数据点进行投影
                        for (let i = 0; i < n; i++) {
                            const point = new Array(d).fill(0);
                            for (let j = 0; j < this.nodeData.dataset[i].length; j++) {
                                for (let k = 0; k < d; k++) {
                                    point[k] += this.nodeData.dataset[i][j] * projectionMatrix[j][k];
                                }
                            }
                            coordinates.push(point);
                        }

                        // 归一化
                        const scale = this.getScaleFactor(coordinates);
                        for (let i = 0; i < coordinates.length; i++) {
                            for (let j = 0; j < coordinates[i].length; j++) {
                                coordinates[i][j] /= scale;
                            }
                        }
                    }
                    break;

                default:
                    // 默认均匀分布
                    for (let i = 0; i < n; i++) {
                        const point = [];
                        for (let j = 0; j < d; j++) {
                            point.push((Math.random() * 2 - 1) * 5);
                        }
                        coordinates.push(point);
                    }
            }

            return coordinates;
        },

        // 获取缩放因子
        getScaleFactor(coordinates) {
            // 找出坐标的最大绝对值
            let maxAbs = 0;
            for (const point of coordinates) {
                for (const coord of point) {
                    maxAbs = Math.max(maxAbs, Math.abs(coord));
                }
            }

            // 设置缩放因子，使最大值约为5
            return maxAbs / 5 || 1;
        },

        // 渲染预览
        renderPreview() {
            if (!this.previewData) return;

            const container = this.$refs.previewContainer;
            if (!container) return;

            // 清空容器
            container.innerHTML = '';

            // 设置预览区域尺寸
            const width = container.clientWidth;
            const height = 400;

            // 创建SVG元素
            const svg = d3.select(container)
                .append('svg')
                .attr('width', width)
                .attr('height', height)
                .attr('viewBox', [-width / 2, -height / 2, width, height])
                .style('background', '#f9f9f9')
                .style('border-radius', '4px');

            // 添加坐标轴
            svg.append('line')
                .attr('x1', -width / 2)
                .attr('y1', 0)
                .attr('x2', width / 2)
                .attr('y2', 0)
                .attr('stroke', '#ddd')
                .attr('stroke-width', 1);

            svg.append('line')
                .attr('x1', 0)
                .attr('y1', -height / 2)
                .attr('x2', 0)
                .attr('y2', height / 2)
                .attr('stroke', '#ddd')
                .attr('stroke-width', 1);

            // 创建颜色比例尺
            const uniqueLabels = [...new Set(this.previewData.labels)];
            const colors = d3.schemeCategory10;
            const colorScale = d3.scaleOrdinal()
                .domain(uniqueLabels)
                .range(colors);

            // 创建比例尺
            const coordinates = this.previewData.coordinates;

            // 计算X和Y的范围
            const xExtent = d3.extent(coordinates, d => d[0]);
            const yExtent = d3.extent(coordinates, d => d[1]);
            const xRange = Math.max(1, xExtent[1] - xExtent[0]);
            const yRange = Math.max(1, yExtent[1] - yExtent[0]);

            // 设置比例尺的定义域和值域
            const xScale = d3.scaleLinear()
                .domain([xExtent[0] - xRange * 0.1, xExtent[1] + xRange * 0.1])
                .range([-width / 2 + 40, width / 2 - 40]);

            const yScale = d3.scaleLinear()
                .domain([yExtent[0] - yRange * 0.1, yExtent[1] + yRange * 0.1])
                .range([height / 2 - 40, -height / 2 + 40]);

            // 绘制点
            svg.selectAll('circle')
                .data(coordinates)
                .enter()
                .append('circle')
                .attr('cx', d => xScale(d[0]))
                .attr('cy', d => yScale(d[1]))
                .attr('r', 5)
                .attr('fill', (d, i) => colorScale(this.previewData.labels[i]))
                .attr('stroke', '#fff')
                .attr('stroke-width', 1)
                .attr('opacity', 0.7);

            // 添加图例
            const legend = svg.append('g')
                .attr('font-family', 'sans-serif')
                .attr('font-size', 10)
                .attr('text-anchor', 'end')
                .selectAll('g')
                .data(uniqueLabels)
                .enter().append('g')
                .attr('transform', (d, i) => `translate(${width / 2 - 20}, ${-height / 2 + 20 + i * 20})`);

            legend.append('rect')
                .attr('width', 15)
                .attr('height', 15)
                .attr('fill', d => colorScale(d));

            legend.append('text')
                .attr('x', -5)
                .attr('y', 9.5)
                .attr('dy', '0.32em')
                .text(d => `类别 ${d}`);
        },

        // 应用到节点
        applyToNode() {
            if (!this.previewData) return;

            this.isProcessing = true;
            this.processingVisible = true;
            this.processingProgress = 0;
            this.processingMessage = '正在应用坐标到节点...';

            // 模拟进度
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += 10;
                if (progress >= 90) {
                    clearInterval(progressInterval);
                }
                this.processingProgress = progress;
            }, 50);

            // 发送事件通知父组件
            setTimeout(() => {
                clearInterval(progressInterval);
                this.processingProgress = 100;
                this.processingMessage = '应用成功!';

                // 发送事件
                this.$emit('coordinates-initialized', {
                    // nodeId: this.nodeId,
                    coordinates: this.previewData.coordinates,
                    method: {
                        method: this.selectedMethod,
                        dimensions: this.dimensions
                    }


                });

                // 关闭处理对话框
                setTimeout(() => {
                    this.processingVisible = false;
                    this.isProcessing = false;
                }, 500);
            }, 1000);
        },

        // 重置预览
        resetPreview() {
            this.previewData = null;
        }
    }
};
</script>

<style scoped>
.low-dim-initializer {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.initializer-card,
.preview-card {
    width: 100%;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.preview-container {
    height: 400px;
    margin-bottom: 20px;
}

.preview-info {
    margin-top: 20px;
}

.processing-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.processing-content p {
    margin-top: 20px;
    color: #606266;
}
</style>