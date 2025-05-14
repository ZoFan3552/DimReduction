package com.zlz.pojo;

import java.util.List;
import java.util.Map;

public class TreeNode {
    private String name;
    private String algorithm;
    private Map<String, Object> params;
    private List<Map<String, Object>> dataset; // 数据集
    private double xVariance;
    private double yVariance;
    private boolean marked;
    private List<TreeNode> children;

    // Getter 和 Setter
    // ...

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAlgorithm() {
        return algorithm;
    }

    public void setAlgorithm(String algorithm) {
        this.algorithm = algorithm;
    }

    public Map<String, Object> getParams() {
        return params;
    }

    public void setParams(Map<String, Object> params) {
        this.params = params;
    }

    public List<Map<String, Object>> getDataset() {
        return dataset;
    }

    public void setDataset(List<Map<String, Object>> dataset) {
        this.dataset = dataset;
    }

    public double getXVariance() {
        return xVariance;
    }

    public void setXVariance(double xVariance) {
        this.xVariance = xVariance;
    }

    public double getYVariance() {
        return yVariance;
    }

    public void setYVariance(double yVariance) {
        this.yVariance = yVariance;
    }

    public boolean isMarked() {
        return marked;
    }

    public void setMarked(boolean marked) {
        this.marked = marked;
    }

    public List<TreeNode> getChildren() {
        return children;
    }

    public void setChildren(List<TreeNode> children) {
        this.children = children;
    }
}