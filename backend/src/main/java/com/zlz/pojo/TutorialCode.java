package com.zlz.pojo;


import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Setter
@Getter
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

    // Getters and Setters
    @Column(name = "lda_code", columnDefinition = "TEXT")
    private String ldaCode;



    @Column(name = "tsne_code", columnDefinition = "TEXT")
    private String tsneCode;

    @Column(name = "umap_code", columnDefinition = "TEXT")
    private String umapCode;

}
