package com.zlz.pojo;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Setter
@Getter
@Entity
@Table(name = "student")
public class Student {
    @Id
    private String studentId;

    private String password;

    private String name; // 可选

    // Getter, Setter

}
