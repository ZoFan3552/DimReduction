package com.zlz.pojo;


import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Setter
@Getter
@Entity
@Table(name = "algorithm_code")
public class AlgorithmCode {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "pca_code", columnDefinition = "TEXT")
    private String pcaCode;

    @Column(name = "lda_code", columnDefinition = "TEXT")
    private String ldaCode;

    @Column(name = "tsne_code", columnDefinition = "TEXT")
    private String tsneCode;

    @Column(name = "umap_code", columnDefinition = "TEXT")
    private String umapCode;

    // Getters and Setters

}
