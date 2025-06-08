package com.zlz.pojo;


import javax.persistence.*;

/**
 * LDA教程进度实体类
 * 对应数据库中的LDA_tutorial表
 */
@Entity
@Table(name = "LDA_tutorial")
public class LdaTutorialProgress {

    @Id
    @Column(name = "user_id")
    private String userId;

    @Column(name = "`introduction-to-lda`", columnDefinition = "TEXT")
    private String introductionToLda;

    @Column(name = "`dimensionality-reduction`", columnDefinition = "TEXT")
    private String dimensionalityReduction;

    @Column(name = "`lda-mathematical-foundation`", columnDefinition = "TEXT")
    private String ldaMathematicalFoundation;

    @Column(name = "`within-class-scatter`", columnDefinition = "TEXT")
    private String withinClassScatter;

    @Column(name = "`between-class-scatter`", columnDefinition = "TEXT")
    private String betweenClassScatter;

    @Column(name = "`eigenvalue-formulation`", columnDefinition = "TEXT")
    private String eigenvalueFormulation;

    @Column(name = "`lda-implementation`", columnDefinition = "TEXT")
    private String ldaImplementation;

    @Column(name = "`lda-visualization`", columnDefinition = "TEXT")
    private String ldaVisualization;

    @Column(name = "`lda-applications`", columnDefinition = "TEXT")
    private String ldaApplications;

    // Getters and setters

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getIntroductionToLda() {
        return introductionToLda;
    }

    public void setIntroductionToLda(String introductionToLda) {
        this.introductionToLda = introductionToLda;
    }

    public String getDimensionalityReduction() {
        return dimensionalityReduction;
    }

    public void setDimensionalityReduction(String dimensionalityReduction) {
        this.dimensionalityReduction = dimensionalityReduction;
    }

    public String getLdaMathematicalFoundation() {
        return ldaMathematicalFoundation;
    }

    public void setLdaMathematicalFoundation(String ldaMathematicalFoundation) {
        this.ldaMathematicalFoundation = ldaMathematicalFoundation;
    }

    public String getWithinClassScatter() {
        return withinClassScatter;
    }

    public void setWithinClassScatter(String withinClassScatter) {
        this.withinClassScatter = withinClassScatter;
    }

    public String getBetweenClassScatter() {
        return betweenClassScatter;
    }

    public void setBetweenClassScatter(String betweenClassScatter) {
        this.betweenClassScatter = betweenClassScatter;
    }

    public String getEigenvalueFormulation() {
        return eigenvalueFormulation;
    }

    public void setEigenvalueFormulation(String eigenvalueFormulation) {
        this.eigenvalueFormulation = eigenvalueFormulation;
    }

    public String getLdaImplementation() {
        return ldaImplementation;
    }

    public void setLdaImplementation(String ldaImplementation) {
        this.ldaImplementation = ldaImplementation;
    }

    public String getLdaVisualization() {
        return ldaVisualization;
    }

    public void setLdaVisualization(String ldaVisualization) {
        this.ldaVisualization = ldaVisualization;
    }

    public String getLdaApplications() {
        return ldaApplications;
    }

    public void setLdaApplications(String ldaApplications) {
        this.ldaApplications = ldaApplications;
    }

    @Override
    public String toString() {
        return "LdaTutorialProgress{" +
                "userId='" + userId + '\'' +
                ", introductionToLda='" + (introductionToLda != null ? "[已完成]" : "[未完成]") + '\'' +
                ", dimensionalityReduction='" + (dimensionalityReduction != null ? "[已完成]" : "[未完成]") + '\'' +
                ", ldaMathematicalFoundation='" + (ldaMathematicalFoundation != null ? "[已完成]" : "[未完成]") + '\'' +
                ", withinClassScatter='" + (withinClassScatter != null ? "[已完成]" : "[未完成]") + '\'' +
                ", betweenClassScatter='" + (betweenClassScatter != null ? "[已完成]" : "[未完成]") + '\'' +
                ", eigenvalueFormulation='" + (eigenvalueFormulation != null ? "[已完成]" : "[未完成]") + '\'' +
                ", ldaImplementation='" + (ldaImplementation != null ? "[已完成]" : "[未完成]") + '\'' +
                ", ldaVisualization='" + (ldaVisualization != null ? "[已完成]" : "[未完成]") + '\'' +
                ", ldaApplications='" + (ldaApplications != null ? "[已完成]" : "[未完成]") + '\'' +
                '}';
    }
}