import tokenize
import io
import os

def is_docstring(prev_tok, tok):
    """
    判断给定的 STRING token 是否为文档字符串（docstring）
    判定规则：
    1. 模块级 docstring：文件开头紧跟 ENCODING 的第一个 STRING
    2. 函数 / 类的 docstring：STRING 紧跟在 INDENT 之后
    """
    if prev_tok and prev_tok.type == tokenize.ENCODING:
        return True
    if prev_tok and prev_tok.type == tokenize.INDENT:
        return True
    return False


def remove_comments_and_docstring(code):
    """
    处理内容：
    - 移除所有 # 注释
    - 移除 docstring（模块/类/函数开头的 STRING）
    - 保留变量多行字符串
    - 删除所有空行（无论原始是否存在）
    """
    result = []
    code_bytes = io.BytesIO(code.encode("utf-8"))

    prev_tok = None
    tokens = list(tokenize.tokenize(code_bytes.readline))

    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            continue

        if tok.type == tokenize.STRING:
            if is_docstring(prev_tok, tok):
                prev_tok = tok
                continue

        result.append((tok.type, tok.string))
        prev_tok = tok

    cleaned = tokenize.untokenize(result).decode("utf-8")

    # 删除所有空行
    return "\n".join(line for line in cleaned.splitlines() if line.strip())


def process_file(in_file, out_file):
    """处理单文件：读取 → 清洗 → 写入"""
    with open(in_file, "r", encoding="utf-8") as f:
        code = f.read()

    new_code = remove_comments_and_docstring(code)

    # 输出目录不存在则创建
    os.makedirs(os.path.dirname(out_file), exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(new_code)


def process_directory_recursive(src_root, out_root, exclude_suffixes):
    """
    递归扫描 src_root 下所有文件与目录
    按相同路径结构输出到 out_root
    """
    for root, dirs, files in os.walk(src_root):
        for filename in files:
            if any(filename.endswith(s) for s in exclude_suffixes):
                print(f"跳过: {filename}")
                continue

            if filename.endswith(".py"):
                abs_in_path = os.path.join(root, filename)

                # 计算相对路径
                rel_path = os.path.relpath(abs_in_path, src_root)

                # 输出路径镜像到 output 目录
                abs_out_path = os.path.join(out_root, rel_path.replace(".py", ".py"))

                process_file(abs_in_path, abs_out_path)
                print(f"{abs_in_path} -> {abs_out_path}")


if __name__ == "__main__":
    # 当前脚本所在目录，例如 project_root/scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # scripts 上一层目录，即 project_root
    project_root = os.path.dirname(script_dir)

    # 指向与 scripts 同级的 src
    target_dir = os.path.join(project_root, "src")

    # 输出目录 scripts/output
    output_dir = os.path.join(project_root, "output\\clean_code_comments")

    # 添加要排除的文件
    exclude = []

    process_directory_recursive(target_dir, output_dir, exclude)
