import gradio as gr
from agent import CodeClinicAgent

agent = CodeClinicAgent()


def respond(message, history):
    if message.strip() == "/reset":
        agent.reset()
        return "对话已重置"
    response = agent.chat(message)
    return response


def create_app():
    with gr.Blocks(
        title="代码诊所",
        theme=gr.themes.Soft(),
    ) as app:
        gr.Markdown("# 代码诊所 Code Clinic\n支持代码审查、重构建议、代码解释、测试生成")

        chatbot = gr.ChatInterface(
            fn=respond,
            examples=[
                "帮我审查以下代码：\ndef add(a,b):\n  return a-b",
                "帮我解释Python装饰器的工作原理",
                "帮我给以下函数生成单元测试：\ndef factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n-1)",
                "帮我重构这段代码：\ndef f(x):\n  if x==1:\n    return 'one'\n  elif x==2:\n    return 'two'\n  else:\n    return 'other'",
            ],
            retry_btn="重试",
            undo_btn="撤销",
            clear_btn="清空",
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)