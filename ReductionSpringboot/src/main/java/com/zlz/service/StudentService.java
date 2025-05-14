package com.zlz.service;

import com.zlz.Dao.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class StudentService {
    @Autowired
    private StudentRepository studentRepository;

    public boolean login(String studentId, String password) {
        return studentRepository.findByStudentIdAndPassword(studentId, password).isPresent();
    }
}
