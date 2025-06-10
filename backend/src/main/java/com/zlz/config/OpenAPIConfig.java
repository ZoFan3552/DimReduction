package com.zlz.config;

import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.OpenAPI;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenAPIConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("合肥工业大学降维算法教育系统后端 API 文档")
                        .version("1.0")
                        .description(" backend 模块的 API 接口相关"));
    }
}
