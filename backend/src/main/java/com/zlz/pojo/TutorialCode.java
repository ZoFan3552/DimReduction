package com.zlz.pojo;


import javax.persistence.*;

@Entity
@Table(name = "tutorial_code")
public class TutorialCode {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "user_id", nullable = false)
    private String userId;

    @Column(name = "pca_code", columnDefinition = "TEXT")
    private String pcaCode;

    @Column(name = "lda_code", columnDefinition = "TEXT")
    private String ldaCode;



    @Column(name = "tsne_code", columnDefinition = "TEXT")
    private String tsneCode;

    @Column(name = "umap_code", columnDefinition = "TEXT")
    private String umapCode;

    // Getters and Setters
    public String getLdaCode() {
        return ldaCode;
    }

    public void setLdaCode(String ldaCode) {
        this.ldaCode = ldaCode;
    }
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getPcaCode() {
        return pcaCode;
    }

    public void setPcaCode(String pcaCode) {
        this.pcaCode = pcaCode;
    }

    public String getTsneCode() {
        return tsneCode;
    }

    public void setTsneCode(String tsneCode) {
        this.tsneCode = tsneCode;
    }

    public String getUmapCode() {
        return umapCode;
    }

    public void setUmapCode(String umapCode) {
        this.umapCode = umapCode;
    }
}
