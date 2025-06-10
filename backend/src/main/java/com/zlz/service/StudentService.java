package com.zlz.service;

import com.zlz.dao.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class StudentService {
    private final StudentRepository studentRepository;

    public StudentService(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    public boolean login(String studentId, String password) {
        return studentRepository.findByStudentIdAndPassword(studentId, password).isPresent();
    }
}
