<template>
    <el-collapse v-model="activeNames" @change="handleChange">
        <el-collapse-item title="节点详情" name="1">
            <div class="node-detail-container">
                <!-- 左侧散点图区域 -->
                <div class="scatter-plot" ref="scatterContainer"></div>
                <!-- 右侧节点其他信息 -->
                <div class="node-info">
                    <!-- <pre>{{ nodeDataInfo }}</pre> -->
                    <NodeDetailDisplay :nodeData="nodeData"></NodeDetailDisplay>
                </div>
            </div>
        </el-collapse-item>
        <el-collapse-item title="操作" name="2">

            <operation-board :nodeData="nodeData" @applyOperation="applyOperation" @datasetImported="datasetImported"
                @coordinatesInitialized="coordinatesInitialized" @gradientUpdated="gradientUpdated"
                @handleCalculationComplete="handleCalculationComplete" @analysisComplete="analysisComplete"
                @projectionComplete="projectionComplete"></operation-board>

        </el-collapse-item>
        <el-collapse-item title="变化图" name="3">

            <div>指标的变化图</div>

        </el-collapse-item>
    </el-collapse>

</template>

<script>
import * as d3 from "d3";
import OperationBoard from "./multipleDisplay/OperationBoard.vue";
import NodeDetailDisplay from "./multipleDisplay/NodeDetailDisplay.vue";

export default {
    // name: "NodeDetailDisplay",
    components: {
        OperationBoard,
        NodeDetailDisplay,
    },
    props: {
        nodeData: {
            type: Object,
            default: () => ({})
        }
    },
    data() {
        return {
            activeNames: [],
            svg: null,         // 散点图SVG
            gPoints: null,     // 存放数据点的组（将应用缩放平移）
            gXAxis: null,      // x轴所在组（固定位置）
            gYAxis: null,      // y轴所在组（固定位置）
            chartWidth: 300,
            chartHeight: 300,
            margin: { top: 20, right: 20, bottom: 20, left: 30 },
            zoom: null,
            // 原始的比例尺，用于计算缩放后的新比例尺
            xScale: null,
            yScale: null,
            // 当前高亮的类别，默认为 null（无高亮）
            highlightCategory: null
        };
    },
    computed: {
        nodeDataInfo() {
            return JSON.stringify(this.nodeData, null, 2);
        }
    },
    mounted() {
        this.drawScatterPlot();
    },
    watch: {
        nodeData: {
            handler() {
                this.drawScatterPlot();
            },
            deep: true
        }
    },
    methods: {

        gradientUpdated(data) {
            this.$emit("gradientUpdated", data);
        },

        coordinatesInitialized(data) {
            this.$emit("coordinatesInitialized", data);
        },

        datasetImported(data) {
            this.$emit("datasetImported", data);
        },

        handleChange(val) {
            console.log(val);
        },

        applyOperation(data) {
            // console.log("接受到数据集进行导入2", data)
            this.$emit("applyOperation", data);
        },

        handleCalculationComplete(data) {
            this.$emit("handleCalculationComplete", data);
        },

        analysisComplete(data) {
            this.$emit("analysisComplete", data);
        },

        projectionComplete(data) {
            this.$emit("projectionComplete", data);
        },

        drawScatterPlot() {
            if (!this.nodeData || !this.nodeData.dataset) {
                return;
            }
            const container = this.$refs.scatterContainer;
            // 清空容器内容
            container.innerHTML = "";
            // 创建 SVG（固定尺寸，可根据需求调整）
            this.svg = d3.select(container)
                .append("svg")
                .attr("width", this.chartWidth)
                .attr("height", this.chartHeight)
                .attr("viewBox", `0 0 ${this.chartWidth} ${this.chartHeight}`)
                .style("border", "1px solid #ccc");

            // 定义内部绘图区域尺寸
            const innerWidth = this.chartWidth - this.margin.left - this.margin.right;
            const innerHeight = this.chartHeight - this.margin.top - this.margin.bottom;

            // 新建一个组用于存放数据点，初始平移到内边距位置
            this.gPoints = this.svg.append("g")
                .attr("class", "points-group")
                .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);

            // 分别建立坐标轴组，不随缩放平移
            this.gXAxis = this.svg.append("g")
                .attr("class", "x-axis-group")
                .attr("transform", `translate(${this.margin.left}, ${this.chartHeight - this.margin.bottom})`);
            this.gYAxis = this.svg.append("g")
                .attr("class", "y-axis-group")
                .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);

            // 获取数据，并处理数据维度
            let data = this.nodeData.dataset;
            if (!data || !Array.isArray(data) || data.length === 0) {
                // 没有数据则不绘制
                return;
            }
            const dim = Array.isArray(data[0]) ? data[0].length : 0;
            if (dim < 2) {
                data = data.map(d => [d[0], 0]);
            } else if (dim > 2) {
                data = data.map(d => [d[0], d[1]]);
            }

            // 建立原始比例尺（不变）用于绘制轴和数据点基础位置
            this.xScale = d3.scaleLinear()
                .domain(d3.extent(data, d => d[0]))
                .range([0, innerWidth])
                .nice();
            this.yScale = d3.scaleLinear()
                .domain(d3.extent(data, d => d[1]))
                .range([innerHeight, 0])
                .nice();

            // 绘制坐标轴
            this.gXAxis.call(d3.axisBottom(this.xScale));
            this.gYAxis.call(d3.axisLeft(this.yScale));

            // 定义颜色比例尺，根据 nodeData.target 数组（要求长度与数据点一致）
            const target = this.nodeData.target;
            const color = d3.scaleOrdinal(d3.schemeCategory10);

            // 绘制数据点（并添加点击事件实现高亮）
            const circles = this.gPoints.selectAll(".point")
                .data(data)
                .enter()
                .append("circle")
                .attr("class", "point")
                .attr("cx", d => this.xScale(d[0]))
                .attr("cy", d => this.yScale(d[1]))
                .attr("r", 4)
                .attr("fill", (d, i) => {
                    return target && target[i] !== undefined ? color(target[i]) : "#000";
                })
                .style("opacity", 1)
                .on("click", (event, d) => {
                    event.stopPropagation();
                    // 获取点击数据点的类别（target对应索引）
                    const index = data.indexOf(d);
                    const clickedCategory = target ? target[index] : null;
                    // 如果已经高亮则取消，否则设置为高亮
                    this.highlightCategory = (this.highlightCategory === clickedCategory) ? null : clickedCategory;
                    // 更新所有数据点透明度
                    circles.style("opacity", (d, i) => {
                        const cat = target && target[i] !== undefined ? target[i] : null;
                        return this.highlightCategory === null || cat === this.highlightCategory ? 1 : 0.25;
                    });
                });

            // 定义缩放行为，只对数据点组起作用，坐标轴单独更新
            this.zoom = d3.zoom()
                .scaleExtent([0.5, 10])
                .on("zoom", (event) => {
                    // 获取当前变换
                    const transform = event.transform;
                    // 更新数据点组
                    this.gPoints.attr("transform", `translate(${this.margin.left + transform.x}, ${this.margin.top + transform.y}) scale(${transform.k})`);
                    // 根据缩放更新坐标轴：使用变换后的比例尺
                    const newXScale = transform.rescaleX(this.xScale);
                    const newYScale = transform.rescaleY(this.yScale);
                    this.gXAxis.call(d3.axisBottom(newXScale));
                    this.gYAxis.call(d3.axisLeft(newYScale));
                });

            this.svg.call(this.zoom);
        }
    }
};
</script>

<style scoped>
/* 穿透作用域修改 */
::v-deep .el-collapse-item__header {
    background: linear-gradient(145deg, #68b1f9, #d8efe0);
    border-radius: 4px;
    margin: 5px 0;
}

/* 修改展开时图标颜色 */
::v-deep .el-collapse-item__arrow {
    color: #409eff;
}



.node-detail-container {
    display: flex;
    flex-direction: row;
    height: 300px;
}

.scatter-plot {
    flex: 0 0 auto;
    /* width: 50%; */
    height: 100%;
    position: relative;
}

.node-info {
    flex: 1;
    overflow: auto;
    padding: 10px;
    border: 1px solid #ccc;
    font-family: monospace;
    white-space: pre-wrap;
}
</style>