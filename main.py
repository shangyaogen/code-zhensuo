from rich.console import Console
from rich.panel import Panel
from agent import CodeClinicAgent

console = Console()


def print_banner():
    console.print()
    console.print("  代码诊所 Code Clinic", style="bold cyan")
    console.print("  功能: 代码审查 | 重构建议 | 代码解释 | 测试生成", style="dim")
    console.print("  输入 /help 查看帮助, /quit 退出", style="dim")
    console.print("  多行输入时，最后单独输一行 end 表示结束", style="dim")
    console.print()


def print_help():
    console.print()
    console.print("  使用方法:", style="bold")
    console.print("    直接输入需求即可，会自动识别你想做什么")
    console.print("    如果要粘贴多行代码，粘贴完后单独输一行 end 再按回车")
    console.print()
    console.print("  示例:", style="bold")
    console.print('    "帮我审查这段代码"   -> 代码审查')
    console.print('    "帮我重构优化"       -> 重构建议')
    console.print('    "解释这段代码"       -> 代码解释')
    console.print('    "生成单元测试"       -> 测试生成')
    console.print()
    console.print("  你可以直接粘贴代码，也可以指定文件路径")
    console.print("  比如: 帮我审查 ./examples/sample_buggy.py")
    console.print()
    console.print("  命令:", style="bold")
    console.print("    /help  - 帮助")
    console.print("    /reset - 重置对话")
    console.print("    /quit  - 退出")
    console.print()


def get_user_input():
    first_line = console.input("[bold green]你: [/]").strip()

    if not first_line or first_line.startswith("/"):
        return first_line

    lines = [first_line]

    while True:
        try:
            line = input("... ")
            if line.strip().lower() == "end":
                break
            lines.append(line)
        except EOFError:
            break

    return "\n".join(lines)


def main():
    print_banner()
    agent = CodeClinicAgent()

    while True:
        try:
            console.print()
            user_input = get_user_input()

            if not user_input:
                continue

            if user_input == "/quit":
                console.print("\n  再见!\n", style="cyan")
                break
            elif user_input == "/help":
                print_help()
                continue
            elif user_input == "/reset":
                agent.reset()
                continue

            console.print()
            with console.status("分析中...", spinner="dots"):
                response = agent.chat(user_input)

            console.print()
            console.print(Panel(response, title="回复", border_style="blue", padding=(1, 2)))

        except KeyboardInterrupt:
            console.print("\n\n  再见!\n", style="cyan")
            break
        except Exception as e:
            console.print(f"\n  出错了: {e}\n", style="bold red")


if __name__ == "__main__":
    main()