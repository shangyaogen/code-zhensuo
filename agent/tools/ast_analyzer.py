import ast
import json


class ASTAnalyzerTool:
    name = "analyze_ast"
    description = "分析Python代码的AST结构，提取类、函数、复杂度等信息"

    @staticmethod
    def execute(code):
        try:
            code = code.strip()
            tree = ast.parse(code)

            analysis = {
                "总行数": len(code.splitlines()),
                "导入模块": [],
                "类定义": [],
                "函数定义": [],
                "全局变量": [],
                "代码异味检测": [],
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["导入模块"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    analysis["导入模块"].append(
                        f"from {node.module} import ..."
                    )
                elif isinstance(node, ast.ClassDef):
                    methods = [
                        n.name
                        for n in node.body
                        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    ]
                    analysis["类定义"].append(
                        {"类名": node.name, "方法数": len(methods), "方法列表": methods}
                    )
                elif isinstance(node, ast.FunctionDef) or isinstance(
                    node, ast.AsyncFunctionDef
                ):
                    complexity = 1
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                            complexity += 1
                        elif isinstance(child, ast.BoolOp):
                            complexity += len(child.values) - 1

                    params = [arg.arg for arg in node.args.args]
                    func_info = {
                        "函数名": node.name,
                        "参数": params,
                        "行数": (node.end_lineno or 0) - node.lineno + 1,
                        "圈复杂度": complexity,
                        "有docstring": (
                            isinstance(node.body[0], ast.Expr)
                            and isinstance(node.body[0].value, (ast.Str, ast.Constant))
                            if node.body
                            else False
                        ),
                    }
                    analysis["函数定义"].append(func_info)

                    if complexity > 10:
                        analysis["代码异味检测"].append(
                            f"函数 '{node.name}' 圈复杂度={complexity}，过于复杂"
                        )
                    if len(params) > 5:
                        analysis["代码异味检测"].append(
                            f"函数 '{node.name}' 参数过多({len(params)}个)"
                        )
                    line_count = (node.end_lineno or 0) - node.lineno + 1
                    if line_count > 50:
                        analysis["代码异味检测"].append(
                            f"函数 '{node.name}' 过长({line_count}行)"
                        )

            if not analysis["代码异味检测"]:
                analysis["代码异味检测"].append("未检测到明显代码异味")

            return json.dumps(analysis, ensure_ascii=False, indent=2)

        except SyntaxError as e:
            return f"[语法错误] 无法解析代码: 第{e.lineno}行 - {e.msg}"
        except Exception as e:
            return f"[错误] AST分析失败: {e}"