package com.zlz.controller;

import com.zlz.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/student")
@CrossOrigin
public class StudentController {
    @Autowired
    private StudentService studentService;

    @PostMapping("/login")
    public Map<String, Object> login(@RequestBody Map<String, String> loginData) {
        String studentId = loginData.get("studentId");
        String password = loginData.get("password");
        boolean success = studentService.login(studentId, password);
        Map<String, Object> result = new HashMap<>();
        if (success) {
            result.put("code", 200);
            result.put("msg", "登录成功");
        } else {
            result.put("code", 401);
            result.put("msg", "学号或密码错误");
        }
        return result;
    }
}

