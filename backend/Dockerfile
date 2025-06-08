# 使用官方 Maven 镜像进行构建，包含 JDK 17，可按需更换版本
FROM maven:3.9.6-eclipse-temurin-11 AS builder

# 设置国内 Maven 镜像源
COPY settings.xml /root/.m2/settings.xml

# 将源码复制到容器中
WORKDIR /app
COPY . .

# 使用 Maven 打包 Spring Boot 项目
RUN mvn clean package -DskipTests

# 使用更小的 JDK 运行环境
FROM eclipse-temurin:11-jdk-alpine

# 创建目录用于运行
WORKDIR /app

# 从构建阶段复制打包后的 jar 文件（假设只生成一个 jar）
COPY --from=builder /app/target/*.jar app.jar

# 暴露应用运行端口
EXPOSE 8080

# 启动 Spring Boot 应用
ENTRYPOINT ["java", "-jar", "app.jar"]
