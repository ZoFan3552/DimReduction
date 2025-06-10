package com.zlz.controller;


import com.zlz.pojo.AlgorithmCodeResponse;
import com.zlz.pojo.SaveCodeRequest;
import com.zlz.service.CodeService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/tutorial")
@CrossOrigin(origins = "*")
public class CodeController {

    private final CodeService tutorialService;

    public CodeController(CodeService tutorialService) {
        this.tutorialService = tutorialService;
    }

    /**
     * 获取用户保存的代码
     */
    @GetMapping("/user-code")
    @Operation(summary = "获取用户保存记录")
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
    @Operation(summary = "获取标准算法")
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
    @Operation(summary = "保存用户代码")
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
    @Setter
    @Getter
    public static class SaveResponse {
        private boolean success;
        private String message;

        public SaveResponse(boolean success, String message) {
            this.success = success;
            this.message = message;
        }

    }
}
