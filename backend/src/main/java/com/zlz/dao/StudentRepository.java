package com.zlz.dao;

import com.zlz.pojo.Student;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface StudentRepository extends JpaRepository<Student, String> {
    Optional<Student> findByStudentIdAndPassword(String studentId, String password);
}
