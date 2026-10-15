import subprocess
import tempfile
import os


class CodeExecutorTool:
    name = "execute_code"
    description = "在沙箱中执行Python代码并返回结果"

    TIMEOUT = 10
    BLOCKED_KEYWORDS = [
        "os.system",
        "subprocess",
        "shutil.rmtree",
        "__import__('os')",
        "eval(",
        "exec(",
        "rm -rf",
    ]

    @staticmethod
    def execute(code):
        try:
            code = code.strip()

            for keyword in CodeExecutorTool.BLOCKED_KEYWORDS:
                if keyword in code:
                    return f"[拦截] 代码包含危险操作: {keyword}"

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            ) as f:
                f.write(code)
                tmp_path = f.name

            try:
                result = subprocess.run(
                    ["python", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=CodeExecutorTool.TIMEOUT,
                    cwd=tempfile.gettempdir(),
                )

                output = ""
                if result.stdout:
                    output += f"标准输出:\n{result.stdout}"
                if result.stderr:
                    output += f"\n错误输出:\n{result.stderr}"
                if not output.strip():
                    output = "代码执行成功，无输出"

                return output.strip()

            except subprocess.TimeoutExpired:
                return f"[超时] 代码执行超过{CodeExecutorTool.TIMEOUT}秒"
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            return f"[错误] 代码执行失败: {e}"