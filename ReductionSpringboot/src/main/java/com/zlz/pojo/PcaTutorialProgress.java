package com.zlz.pojo;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "PCA_tutorial")
public class PcaTutorialProgress {

    @Id
    @Column(name = "userId")
    private String userId;

    @Column(name = "completeCount")
    private Integer completeCount;

    @Column(name = "`intro-to-pca`", columnDefinition = "TEXT")
    private String introToPca;

    @Column(name = "`data-variance`", columnDefinition = "TEXT")
    private String dataVariance;

    @Column(name = "`covariance-matrix`", columnDefinition = "TEXT")
    private String covarianceMatrix;

    @Column(name = "eigenvectors", columnDefinition = "TEXT")
    private String eigenvectors;

    @Column(name = "`selecting-pcs`", columnDefinition = "TEXT")
    private String selectingPcs;

    @Column(name = "`dimensionality-reduction`", columnDefinition = "TEXT")
    private String dimensionalityReduction;

    @Column(name = "`pca-applications`", columnDefinition = "TEXT")
    private String pcaApplications;

    @Column(name = "`pca-limitations`", columnDefinition = "TEXT")
    private String pcaLimitations;

    @Column(name = "`practical-example`", columnDefinition = "TEXT")
    private String practicalExample;

    // 将包含连字符的列名映射到Java属性
    public String getValueBySegmentId(String segmentId) {
        switch (segmentId) {
            case "intro-to-pca":
                return introToPca;
            case "data-variance":
                return dataVariance;
            case "covariance-matrix":
                return covarianceMatrix;
            case "eigenvectors":
                return eigenvectors;
            case "selecting-pcs":
                return selectingPcs;
            case "dimensionality-reduction":
                return dimensionalityReduction;
            case "pca-applications":
                return pcaApplications;
            case "pca-limitations":
                return pcaLimitations;
            case "practical-example":
                return practicalExample;
            default:
                return null;
        }
    }

    // 根据章节ID设置对应的值
    public void setValueBySegmentId(String segmentId, String value) {
        switch (segmentId) {
            case "intro-to-pca":
                this.introToPca = value;
                break;
            case "data-variance":
                this.dataVariance = value;
                break;
            case "covariance-matrix":
                this.covarianceMatrix = value;
                break;
            case "eigenvectors":
                this.eigenvectors = value;
                break;
            case "selecting-pcs":
                this.selectingPcs = value;
                break;
            case "dimensionality-reduction":
                this.dimensionalityReduction = value;
                break;
            case "pca-applications":
                this.pcaApplications = value;
                break;
            case "pca-limitations":
                this.pcaLimitations = value;
                break;
            case "practical-example":
                this.practicalExample = value;
                break;
        }
    }
}