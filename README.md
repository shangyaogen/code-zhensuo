代码诊所 Code Clinic Agent



基于通义千问的代码助手Agent，可以对Python代码做审查、重构、解释和测试生成。



功能：

\- 代码审查：分析代码质量、找Bug、找安全隐患

\- 重构建议：识别代码坏味道，给出重构方案和代码

\- 代码解释：解释代码逻辑，生成注释

\- 测试生成：自动生成单元测试



架构：

用户输入 -> 意图识别 -> ReAct循环(推理->工具调用->观察->循环) -> 最终回复



集成了3个工具：

\- FileReader：读本地代码文件

\- CodeExecutor：沙箱里跑Python代码

\- ASTAnalyzer：用ast模块做静态分析



怎么用：



1\. 装依赖

&#x20;  pip install -r requirements.txt



2\. 配置api key

复制.env.example文件重新命名为.env

&#x20;  在.env文件里写：

&#x20;  DASHSCOPE\_API\_KEY=你的key



3\. 命令行跑

&#x20;  python main.py



4\. 或者web界面

&#x20;  python web\_app.py

&#x20;  然后浏览器打开 http://localhost:7860



项目结构：

code-clinic-agent/

&#x20;   main.py              命令行入口

&#x20;   web\_app.py           web界面

&#x20;   agent/

&#x20;       \_\_init\_\_.py

&#x20;       core.py          agent核心循环

&#x20;       llm.py           llm调用封装

&#x20;       memory.py        上下文记忆

&#x20;       prompts.py       prompt模板

&#x20;       tools/

&#x20;           \_\_init\_\_.py

&#x20;           file\_reader.py    文件读取

&#x20;           code\_executor.py  代码执行

&#x20;           ast\_analyzer.py   ast分析

&#x20;   examples/

&#x20;       sample\_buggy.py   有bug的测试代码

&#x20;       sample\_clean.py   正常的测试代码

&#x20;   requirements.txt

&#x20;   README.md

&#x20;   Design.md



技术栈：

\- Python 3.10+

\- 通义千问 qwen-plus

\- Agent模式用的ReAct

\- web用的Gradio

\- 终端输出用的Rich

