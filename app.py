import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# 读取环境变量
load_dotenv()

# 页面设置
st.set_page_config(page_title="Resume JD Copilot", page_icon="🧠")

st.title("🧠 简历 / JD Copilot")
st.write("粘贴你的简历和岗位 JD，系统会自动分析匹配度、优化简历，并生成面试题。")

# 读取 API Key
api_key = os.getenv("ZAI_API_KEY")

if not api_key:
    st.error("没有读取到 ZAI_API_KEY，请检查 .env 文件。")
    st.stop()

# 创建智谱客户端（OpenAI 兼容接口）
client = OpenAI(
    api_key=api_key,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

MODEL_NAME = "glm-5"

# 统一的模型调用函数
def run_agent(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# 三个角色的提示词
JD_ANALYST_PROMPT = """
你是一名资深招聘分析师。
请阅读候选人简历和目标岗位 JD，输出以下内容：

1. 岗位核心技能关键词
2. 匹配度评分（0-100）
3. 候选人的优势
4. 候选人的短板
5. 风险点
6. 修改建议

要求：
- 用中文回答
- 简洁直接
- 不允许编造候选人没有的经历
"""

RESUME_EDITOR_PROMPT = """
你是一名专业技术简历顾问。
请根据候选人的真实简历内容和岗位 JD，对简历进行改写优化。

输出必须包含：
1. 重写后的个人简介
2. 推荐的项目标题
3. 4 条更适合岗位的项目 bullet
4. 8 个 ATS 关键词

要求：
- 只能基于已有信息改写
- 不能编造项目、奖项、公司、数字成果
- 风格简洁、专业、面向技术岗位
"""

INTERVIEW_COACH_PROMPT = """
你是一名技术面试辅导教练。
请基于候选人简历、岗位 JD、岗位分析结果和改写结果，输出：

1. 10 个高频面试问题
2. 每个问题的回答提纲
3. 5 个候选人可反问面试官的问题

要求：
- 用中文输出
- 问题尽量贴近目标岗位
- 回答提纲要具体，不要空泛
"""

# 页面输入区
resume_text = st.text_area("请粘贴你的简历内容", height=260)
jd_text = st.text_area("请粘贴目标岗位 JD", height=260)

# 按钮
if st.button("开始生成"):
    if not resume_text.strip():
        st.warning("请先输入简历内容。")
        st.stop()

    if not jd_text.strip():
        st.warning("请先输入岗位 JD。")
        st.stop()

    # 第一步：岗位分析
    with st.spinner("JD Analyst 正在分析岗位匹配度..."):
        analysis_result = run_agent(
            JD_ANALYST_PROMPT,
            f"候选人简历：\n{resume_text}\n\n目标岗位 JD：\n{jd_text}"
        )

    # 第二步：简历优化
    with st.spinner("Resume Editor 正在优化简历..."):
        rewrite_result = run_agent(
            RESUME_EDITOR_PROMPT,
            f"候选人简历：\n{resume_text}\n\n目标岗位 JD：\n{jd_text}\n\n岗位分析结果：\n{analysis_result}"
        )

    # 第三步：面试准备
    with st.spinner("Interview Coach 正在生成面试问题..."):
        interview_result = run_agent(
            INTERVIEW_COACH_PROMPT,
            f"候选人简历：\n{resume_text}\n\n目标岗位 JD：\n{jd_text}\n\n岗位分析结果：\n{analysis_result}\n\n简历改写结果：\n{rewrite_result}"
        )

    # 展示结果
    tab1, tab2, tab3 = st.tabs(["岗位分析", "简历改写", "面试准备"])

    with tab1:
        st.markdown(analysis_result)

    with tab2:
        st.markdown(rewrite_result)

    with tab3:
        st.markdown(interview_result)
    final_output = f"""
# 一、岗位分析
        {analysis_result}

---

# 二、简历改写
        {rewrite_result}

---

# 三、面试准备
        {interview_result}
"""

    st.download_button(
        label="下载完整结果（Markdown）",
        data=final_output,
        file_name="resume_jd_copilot_result.md",
        mime="text/markdown"
    )