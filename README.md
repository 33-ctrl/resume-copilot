# 🧠 Resume / JD Copilot

一个基于 **智谱 AI OpenAI 兼容接口** 和 **Streamlit** 开发的简历 / 岗位分析助手。

用户输入自己的简历内容和目标岗位 JD 后，系统会自动完成：

- 岗位匹配度分析
- 简历优化建议
- 项目 bullet 改写
- ATS 关键词提取
- 面试问题与回答提纲生成

---

## 功能介绍

这个项目将任务拆分为 3 个角色模块：

### 1. JD Analyst
负责分析岗位要求，输出：

- 岗位核心技能关键词
- 匹配度评分
- 候选人优势
- 候选人短板
- 风险点
- 修改建议

### 2. Resume Editor
负责根据岗位要求优化简历，输出：

- 重写后的个人简介
- 推荐项目标题
- 更适合岗位的项目 bullet
- ATS 关键词

### 3. Interview Coach
负责生成面试准备内容，输出：

- 高频面试问题
- 每个问题的回答提纲
- 可反问面试官的问题

---

## 技术栈

- Python
- Streamlit
- OpenAI Python SDK
- 智谱 AI OpenAI 兼容接口
- python-dotenv

---

## 项目结构

```text
resume-copilot/
├─ app.py
├─ README.md
├─ requirements.txt
├─ .gitignore
└─ .env
