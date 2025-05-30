package com.zlz.controller;


import com.zlz.pojo.AlgorithmCodeResponse;
import com.zlz.pojo.SaveCodeRequest;
import com.zlz.service.CodeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/tutorial")
public class CodeController {

    @Autowired
    private CodeService tutorialService;

    /**
     * 获取用户保存的代码
     */
    @GetMapping("/user-code")
    public ResponseEntity<AlgorithmCodeResponse> getUserCode(
            @RequestParam String userId,
            @RequestParam String algorithmType) {

        String code = tutorialService.getUserCode(userId, algorithmType);

        AlgorithmCodeResponse response = new AlgorithmCodeResponse();
        response.setCode(code);

        return ResponseEntity.ok(response);
    }

    /**
     * 获取标准算法代码
     */
    @GetMapping("/standard-code")
    public ResponseEntity<AlgorithmCodeResponse> getStandardCode(
            @RequestParam String algorithmType) {

        String code = tutorialService.getStandardCode(algorithmType);

        AlgorithmCodeResponse response = new AlgorithmCodeResponse();
        response.setCode(code);

        return ResponseEntity.ok(response);
    }

    /**
     * 保存用户代码
     */
    @PostMapping("/save-code")
    public ResponseEntity<?> saveUserCode(@RequestBody SaveCodeRequest request) {
        boolean success = tutorialService.saveUserCode(
                request.getUserId(),
                request.getAlgorithmType(),
                request.getCode()
        );

        if (success) {
            return ResponseEntity.ok().body(new SaveResponse(true, "代码保存成功"));
        } else {
            return ResponseEntity.badRequest().body(new SaveResponse(false, "代码保存失败"));
        }
    }

    // 保存响应内部类
    public static class SaveResponse {
        private boolean success;
        private String message;

        public SaveResponse(boolean success, String message) {
            this.success = success;
            this.message = message;
        }

        public boolean isSuccess() {
            return success;
        }

        public void setSuccess(boolean success) {
            this.success = success;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }
    }
}
