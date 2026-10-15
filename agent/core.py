import re
from .llm import LLMClient
from .memory import ConversationMemory
from .prompts import (
    SYSTEM_PROMPT,
    REVIEW_PROMPT,
    REFACTOR_PROMPT,
    EXPLAIN_PROMPT,
    TEST_PROMPT,
)
from .tools import FileReaderTool, CodeExecutorTool, ASTAnalyzerTool


class CodeClinicAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.memory = ConversationMemory()
        self.tools = {
            "read_file": FileReaderTool(),
            "execute_code": CodeExecutorTool(),
            "analyze_ast": ASTAnalyzerTool(),
        }
        self.max_tool_rounds = 5

    def _detect_mode(self, user_input):
        input_lower = user_input.lower()
        if any(kw in input_lower for kw in ["审查", "review", "体检", "检查", "bug", "问题"]):
            return "review"
        elif any(kw in input_lower for kw in ["重构", "refactor", "优化", "改进", "处方"]):
            return "refactor"
        elif any(kw in input_lower for kw in ["解释", "explain", "解读", "说明", "注释"]):
            return "explain"
        elif any(kw in input_lower for kw in ["测试", "test", "化验", "单元测试", "用例"]):
            return "test"
        return "general"

    def _get_mode_prompt(self, mode):
        prompts = {
            "review": REVIEW_PROMPT,
            "refactor": REFACTOR_PROMPT,
            "explain": EXPLAIN_PROMPT,
            "test": TEST_PROMPT,
        }
        return prompts.get(mode, "")

    def _parse_tool_calls(self, response):
        pattern = r'\[TOOL_CALL\]\s*tool:\s*(\w+)\s*arg:\s*(.*?)\s*\[/TOOL_CALL\]'
        matches = re.findall(pattern, response, re.DOTALL)
        return [(name.strip(), arg.strip()) for name, arg in matches]

    def _execute_tool(self, tool_name, arg):
        if tool_name not in self.tools:
            return f"[错误] 未知工具: {tool_name}，可用: {list(self.tools.keys())}"
        tool = self.tools[tool_name]
        return tool.execute(arg)

    def chat(self, user_input):
        mode = self._detect_mode(user_input)
        mode_prompt = self._get_mode_prompt(mode)

        mode_labels = {
            "review": "代码审查",
            "refactor": "代码重构",
            "explain": "代码解释",
            "test": "测试生成",
            "general": "综合对话",
        }
        print(f"\n  [分诊] {mode_labels.get(mode, '综合对话')}")

        enhanced_input = user_input
        if mode_prompt:
            enhanced_input = f"{mode_prompt}\n\n用户输入：{user_input}"

        self.memory.add("user", enhanced_input)

        for round_num in range(self.max_tool_rounds):
            messages = self.memory.get_messages(SYSTEM_PROMPT)
            response = self.llm.chat(messages)

            tool_calls = self._parse_tool_calls(response)

            if not tool_calls:
                self.memory.add("assistant", response)
                return response

            print(f"  [工具调用] 第{round_num + 1}轮:")
            tool_results = []
            for tool_name, arg in tool_calls:
                print(f"    -> {tool_name}({arg[:50]}{'...' if len(arg) > 50 else ''})")
                result = self._execute_tool(tool_name, arg)
                tool_results.append(f"工具 {tool_name} 返回:\n{result}")

            observation = "\n\n".join(tool_results)
            clean_response = re.sub(
                r'\[TOOL_CALL\].*?\[/TOOL_CALL\]', '', response, flags=re.DOTALL
            ).strip()

            self.memory.add("assistant", clean_response if clean_response else "(正在分析...)")
            self.memory.add("user", f"[工具执行结果]\n{observation}\n\n请根据以上工具结果继续分析，给出最终回复。")

        messages = self.memory.get_messages(SYSTEM_PROMPT)
        final = self.llm.chat(messages)
        self.memory.add("assistant", final)
        return final

    def reset(self):
        self.memory.clear()
        print("  对话已重置")