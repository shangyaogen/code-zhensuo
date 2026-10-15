import os


class FileReaderTool:
    name = "read_file"
    description = "读取指定路径的代码文件，返回带行号的内容"

    @staticmethod
    def execute(file_path):
        try:
            file_path = file_path.strip().strip("'\"")
            if not os.path.exists(file_path):
                return f"[错误] 文件不存在: {file_path}"

            if os.path.getsize(file_path) > 100 * 1024:
                return "[错误] 文件过大，超过100KB"

            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            numbered = []
            for i, line in enumerate(lines, 1):
                numbered.append(f"{i:4d} | {line.rstrip()}")

            return f"文件: {file_path} ({len(lines)}行)\n" + "\n".join(numbered)

        except Exception as e:
            return f"[错误] 读取文件失败: {e}"