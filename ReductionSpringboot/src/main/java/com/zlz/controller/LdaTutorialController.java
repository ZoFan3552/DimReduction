package com.zlz.controller;

import com.zlz.pojo.LdaTutorialProgress;
import com.zlz.service.LdaTutorialService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/lda-tutorial")
@CrossOrigin(origins = "*") // 允许前端访问
public class LdaTutorialController {

    @Autowired
    private LdaTutorialService ldaTutorialService;

    /**
     * 获取用户的LDA教程学习进度
     */
    @GetMapping("/progress/{userId}")
    public ResponseEntity<?> getUserProgress(@PathVariable String userId) {
        try {
            Map<String, Object> progress = ldaTutorialService.getUserProgress(userId);
            return ResponseEntity.ok(progress);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("获取用户进度失败: " + e.getMessage());
        }
    }

    /**
     * 保存用户的LDA教程学习进度
     */
    @PostMapping("/progress")
    public ResponseEntity<?> saveUserProgress(@RequestBody LdaTutorialProgress progressData) {
        try {
            ldaTutorialService.saveUserProgress(progressData);
            return ResponseEntity.ok("用户进度保存成功");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("保存用户进度失败: " + e.getMessage());
        }
    }

    /**
     * 保存用户对特定章节的回答
     */
    @PostMapping("/answer")
    public ResponseEntity<?> saveUserAnswer(@RequestBody Map<String, String> answerData) {
        try {
            String userId = answerData.get("userId");
            String sectionId = answerData.get("sectionId");
            String answer = answerData.get("answer");

            ldaTutorialService.saveUserAnswer(userId, sectionId, answer);
            return ResponseEntity.ok("用户回答保存成功");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("保存用户回答失败: " + e.getMessage());
        }
    }

    /**
     * 标记章节为已完成
     */
    @PostMapping("/complete-section")
    public ResponseEntity<?> markSectionComplete(@RequestBody Map<String, String> completionData) {
        try {
            String userId = completionData.get("userId");
            String sectionId = completionData.get("sectionId");

            ldaTutorialService.markSectionComplete(userId, sectionId);
            return ResponseEntity.ok("章节标记为已完成");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("标记章节完成失败: " + e.getMessage());
        }
    }
}