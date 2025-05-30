package com.zlz.controller;

import com.zlz.pojo.PcaTutorialProgress;
import com.zlz.service.PcaTutorialService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/tutorial/pca")
@CrossOrigin(origins = "*") // 允许前端跨域访问
public class PcaTutorialController {

    @Autowired
    private PcaTutorialService pcaTutorialService;

    /**
     * 获取用户教程进度
     * @param userId 用户ID
     * @return 用户的教程进度数据
     */
    @GetMapping("/progress/{userId}")
    public ResponseEntity<?> getUserProgress(@PathVariable String userId) {
        try {
            PcaTutorialProgress progress = pcaTutorialService.getUserProgress(userId);
            return ResponseEntity.ok(progress);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("message", "获取用户进度失败: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    /**
     * 保存用户教程进度
     * @param progressData 包含进度信息的对象
     * @return 保存结果
     */
    @PostMapping("/progress")
    public ResponseEntity<?> saveUserProgress(@RequestBody PcaTutorialProgress progressData) {
        try {
            PcaTutorialProgress savedProgress = pcaTutorialService.saveUserProgress(progressData);
            return ResponseEntity.ok(savedProgress);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("message", "保存用户进度失败: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    /**
     * 更新特定章节的回答
     * @param requestData 包含用户ID、章节ID和回答的请求数据
     * @return 更新结果
     */
    @PatchMapping("/progress/answer")
    public ResponseEntity<?> updateSegmentAnswer(@RequestBody Map<String, String> requestData) {
        try {
            String userId = requestData.get("userId");
            String segmentId = requestData.get("segmentId");
            String answer = requestData.get("answer");

            boolean updated = pcaTutorialService.updateSegmentAnswer(userId, segmentId, answer);

            Map<String, Object> response = new HashMap<>();
            response.put("success", updated);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("message", "更新章节回答失败: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    /**
     * 标记章节为已完成
     * @param requestData 包含用户ID和章节ID的请求数据
     * @return 更新结果
     */
    @PatchMapping("/progress/complete")
    public ResponseEntity<?> markSegmentComplete(@RequestBody Map<String, String> requestData) {
        try {
            String userId = requestData.get("userId");
            String segmentId = requestData.get("segmentId");

            boolean updated = pcaTutorialService.markSegmentComplete(userId, segmentId);

            Map<String, Object> response = new HashMap<>();
            response.put("success", updated);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("message", "标记章节完成失败: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }
}