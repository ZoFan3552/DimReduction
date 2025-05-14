<template>
    <div class="tree-container" ref="container" @contextmenu.prevent>
        <svg ref="svg"></svg>
        <!-- 右键菜单 -->
        <div v-if="showContextMenu" class="context-menu"
            :style="{ top: contextMenuY + 'px', left: contextMenuX + 'px' }">
            <ul>
                <!-- <li @click="onContextMenuOption('loop')">创建循环</li>
                <li @click="onContextMenuOption('mark')">标记节点</li> -->
                <li @click="onContextMenuOption('delete')">删除节点</li>
                <li @click="onContextMenuOption('collapse')">折叠/展开节点</li>
            </ul>
        </div>
    </div>
</template>

<script>
import * as d3 from "d3";
import { MessageBox } from 'element-ui';


export default {
    name: "TreeDiagram",
    props: {
        // 父组件传入的树状图数据
        treeData: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            svg: null,
            g: null, // D3 用于放置绘图元素的组
            width: 800,
            height: 600,
            zoom: null,
            selectedNode: null,
            showContextMenu: false,
            contextMenuX: 0,
            contextMenuY: 0
        };
    },
    mounted() {
        this.initSvg();
        this.drawTree();
        // 使用 ResizeObserver 来监听容器尺寸变化
        const resizeObserver = new ResizeObserver(this.onResize);
        resizeObserver.observe(this.$refs.container); // 监听容器的尺寸变化

        document.addEventListener("click", this.hideContextMenu);
    },
    beforeDestroy() {
        // 移除监听事件
        document.removeEventListener("click", this.hideContextMenu);
    },
    methods: {
        initSvg() {
            const container = this.$refs.container;
            this.width = container.clientWidth;
            this.height = container.clientHeight;
            this.svg = d3
                .select(this.$refs.svg)
                .attr("width", this.width)
                .attr("height", this.height)
                .attr("viewBox", `0 0 ${this.width} ${this.height}`)
                .style("cursor", "move");

            // 设置缩放行为
            this.zoom = d3.zoom().on("zoom", (event) => {
                this.g.attr("transform", event.transform);
            });
            this.svg.call(this.zoom);

            this.g = this.svg.append("g");
        },
        drawTree() {
            // 清空原有内容
            this.g.selectAll("*").remove();

            // 定义外边距，避免内容贴边
            const margin = { top: 50, right: 50, bottom: 50, left: 50 };

            // 新建一个分组用于绘制树
            const gTree = this.g.append("g").attr("class", "treeGroup");

            // 将树状数据转换为层级数据
            const root = d3.hierarchy(this.treeData);

            // 创建树布局，使用固定节点间距，便于调整显示效果
            const treeLayout = d3
                .tree()
                .nodeSize([100, 250]) // [垂直间距, 水平间距]
                .separation((a, b) => (a.parent === b.parent ? 1 : 1.5));

            treeLayout(root);

            // 调整整体位置：计算所有节点的最小坐标，加上外边距
            const nodes = root.descendants();
            const minX = d3.min(nodes, (d) => d.x);
            const minY = d3.min(nodes, (d) => d.y);
            const dx = -minX + margin.top;
            const dy = -minY + margin.left;
            gTree.attr("transform", `translate(${dy}, ${dx})`);






            // 绘制连线
            gTree
                .selectAll(".link")
                .data(root.links())
                .enter()
                .append("path")
                .attr("class", "link")
                .attr("fill", "none")
                .attr("stroke", "#777")
                .attr("stroke-width", 2)
                .attr("d", (d) => {
                    return (
                        "M" +
                        d.source.y +
                        "," +
                        d.source.x +
                        "C" +
                        (d.source.y + d.target.y) / 2 +
                        "," +
                        d.source.x +
                        " " +
                        (d.source.y + d.target.y) / 2 +
                        "," +
                        d.target.x +
                        " " +
                        d.target.y +
                        "," +
                        d.target.x
                    );
                });

            // 在连线上添加标签，显示步骤名称（取子节点的 operation）
            gTree
                .selectAll(".link-label")
                .data(root.links())
                .enter()
                .append("text")
                .attr("class", "link-label")
                .attr("text-anchor", "middle")
                .attr("dy", -5)
                .attr("x", (d) => (d.source.y + d.target.y) / 2)
                .attr("y", (d) => (d.source.x + d.target.x) / 2)
                .text((d) => d.target.data.operation);

            // 定义节点尺寸（正方形边长）
            const nodeSize = 80;
            // 定义颜色比例尺，用于根据 target 数组区分散点颜色
            const color = d3.scaleOrdinal(d3.schemeCategory10);

            // 绘制节点
            const node = gTree
                .selectAll(".node")
                .data(root.descendants())
                .enter()
                .append("g")
                .attr("class", "node")
                .attr("transform", (d) => `translate(${d.y},${d.x})`)
                .on("click", (event, d) => {
                    event.stopPropagation();
                    this.handleNodeClick(d.data);
                    // 首先取消所有节点的选中状态（注意 treeData 是你的根节点对象）
                    const clearSelected = (node) => {
                        node.selected = false;
                        if (node.children) {
                            node.children.forEach(clearSelected);
                        }
                    };
                    clearSelected(this.treeData); // 清除全部选中
                    d.data.selected = true;     // 选中当前节点

                    // 更新所有节点边框颜色
                    d3.selectAll(".node-rect")
                        .attr("stroke", d => d.data.selected ? "red" : "steelblue");
                })
                .on("contextmenu", (event, d) => {
                    event.preventDefault();
                    event.stopPropagation();
                    this.handleNodeRightClick(event, d.data);
                });


            // 绘制正方形作为节点背景
            node
                .append("rect")
                .attr('class', 'node-rect')
                .attr("x", -nodeSize / 2)
                .attr("y", -nodeSize / 2)
                .attr("width", nodeSize)
                .attr("height", nodeSize)
                .attr("fill", "#fff")
                .attr("stroke", d => d.data.selected ? 'red' : 'steelblue')
                .attr("stroke-width", 2);

            // 在正方形内部绘制散点图（仅当 dataset 为1D或2D时显示）
            node.each(function (d) {
                const data = d.data.dataset;
                if (!data || !Array.isArray(data) || data.length === 0) return;
                const pointDim = Array.isArray(data[0]) ? data[0].length : 0;
                // if (pointDim !== 1 && pointDim !== 2) return; // 若维数大于2，则不显示

                // target 数组用于给每个数据点赋予类别标签
                const target = d.data.target;
                const innerMargin = 5;
                const innerSize = nodeSize - innerMargin * 2;
                const gNode = d3.select(this);
                const scatterGroup = gNode
                    .append("g")
                    .attr("class", "scatter-group")
                    .attr(
                        "transform",
                        `translate(${-nodeSize / 2 + innerMargin}, ${-nodeSize / 2 + innerMargin})`
                    );


                if (pointDim === 1) {
                    // 1D 数据绘制散点图：将 x 值映射，y 固定在中间
                    const xs = data.map((pt) => pt[0]);
                    const xScale = d3
                        .scaleLinear()
                        .domain(d3.extent(xs))
                        .range([0, innerSize]);
                    scatterGroup
                        .selectAll("circle")
                        .data(data)
                        .enter()
                        .append("circle")
                        .attr("cx", (pt) => xScale(pt[0]))
                        .attr("cy", innerSize / 2)
                        .attr("r", 3)
                        .attr("fill", (pt, i) =>
                            target && target[i] !== undefined ? color(target[i]) : "#000"
                        );

                } else {

                    // 2D 数据绘制散点图
                    const xs = data.map((pt) => pt[0]);
                    const ys = data.map((pt) => pt[1]);
                    const xScale = d3
                        .scaleLinear()
                        .domain(d3.extent(xs))
                        .range([0, innerSize]);
                    const yScale = d3
                        .scaleLinear()
                        .domain(d3.extent(ys))
                        .range([innerSize, 0]);
                    scatterGroup
                        .selectAll("circle")
                        .data(data)
                        .enter()
                        .append("circle")
                        .attr("cx", (pt) => xScale(pt[0]))
                        .attr("cy", (pt) => yScale(pt[1]))
                        .attr("r", 3)
                        .attr("fill", (pt, i) =>
                            target && target[i] !== undefined ? color(target[i]) : "#000"
                        );
                }
            });
        },



        handleNodeClick(nodeData) {
            this.selectedNode = nodeData;
            // 向父组件发送选中的节点数据
            this.$emit("node-selected", nodeData);
        },
        handleNodeRightClick(event, nodeData) {
            this.selectedNode = nodeData;
            // 获取容器相对于视口的位置，确保菜单在容器内正确显示
            const containerRect = this.$refs.container.getBoundingClientRect();
            this.contextMenuX = event.clientX - containerRect.left;
            this.contextMenuY = event.clientY - containerRect.top;
            this.showContextMenu = true;
        },

        hideContextMenu() {
            this.showContextMenu = false;
        },

        // onContextMenuOption(option) {
        //     this.showContextMenu = false;

        //     if (option === "loop") {
        //         // 弹出一个简单的 prompt 让用户输入循环次数
        //         const loopCountStr = prompt("请输入循环次数：", "3");
        //         const loopCount = parseInt(loopCountStr);

        //         if (!isNaN(loopCount) && loopCount > 0) {
        //             this.$emit("node-contextmenu", {
        //                 option,
        //                 node: this.selectedNode,
        //                 loopCount: loopCount // 把循环次数也传出去
        //             });
        //         } else {
        //             alert("请输入有效的正整数！");
        //         }
        //     } else {
        //         // 非 loop 情况，直接发出事件
        //         this.$emit("node-contextmenu", {
        //             option,
        //             node: this.selectedNode
        //         });
        //     }
        // },

        onContextMenuOption(option) {
            this.showContextMenu = false;

            if (option === "loop") {
                MessageBox.prompt('请输入循环次数（正整数）', '设置循环次数', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    inputPattern: /^[1-9]\d*$/,  // 正整数验证
                    inputErrorMessage: '请输入有效的正整数'
                }).then(({ value }) => {
                    const loopCount = parseInt(value);
                    this.$emit("node-contextmenu", {
                        option,
                        node: this.selectedNode,
                        loopCount: loopCount
                    });
                }).catch(() => {
                    // 用户取消输入
                    console.log("用户取消设置循环次数");
                });
            } else {
                console.log(this.selectedNode.id);
                // 非 loop 选项直接触发
                this.$emit("node-contextmenu", {
                    option,
                    node: this.selectedNode
                });
            }
        },

        onResize() {
            requestAnimationFrame(() => {
                const container = this.$refs.container;
                if (container) {
                    this.width = container.clientWidth;
                    this.height = container.clientHeight;
                    this.svg.attr("width", this.width).attr("height", this.height);
                    this.svg.attr("viewBox", `0 0 ${this.width} ${this.height}`);
                    this.drawTree();
                }
            })

        }

    },
    watch: {
        treeData: {
            deep: true,
            handler() {
                this.drawTree();
            }
        }
    }
};
</script>


<style scoped>
.tree-container {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.link {
    fill: none;
}

.link-label {
    font-size: 12px;
    fill: #555;
}

.node rect {
    cursor: pointer;
}

.context-menu {
    position: absolute;
    background-color: #fff;
    border: 1px solid #ccc;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    z-index: 10;
}

.context-menu ul {
    list-style: none;
    margin: 0;
    padding: 5px 0;
}

.context-menu li {
    padding: 5px 15px;
    cursor: pointer;
}

.context-menu li:hover {
    background-color: #eee;
}
</style>