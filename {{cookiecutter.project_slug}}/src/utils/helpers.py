import os
import shutil
import zipfile
import base64
from datetime import datetime
from pypinyin import pinyin, Style
from typing import Any, Iterable, Callable
from typing_extensions import Annotated  # Python <3.10 使用 typing_extensions
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from config import *

try:
    import pyzipper  # 可选 AES 加密
except ImportError:
    pyzipper = None


# --------------------
# 自定义注解类型
# --------------------
class ParamInfo:
    """Parameter metadata for documentation and validation.
    参数元信息，用于文档和校验
    """

    def __init__(self, description: str = "", deprecated: bool = False):
        self.description = description
        self.deprecated = deprecated


# --------------------
# AES 加密（文件）
# --------------------
def aes_encrypt_file(
    input_path: Annotated[str, ParamInfo("Input file path / 输入文件路径")],
    output_path: Annotated[str, ParamInfo("Output encrypted file path / 输出加密文件路径")]
) -> None:
    """
    Encrypt file using AES-CBC.
    使用 AES-CBC 加密文件
    """
    # 读取原始文件
    with open(input_path, "rb") as f:
        plaintext = f.read()

    # 生成随机 IV（16 字节）
    iv = get_random_bytes(16)

    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    # 文件格式：IV + ciphertext
    with open(output_path, "wb") as f:
        f.write(iv + ciphertext)


# --------------------
# AES 解密（文件）
# --------------------
def aes_decrypt_file(
    input_path: Annotated[str, ParamInfo("Encrypted file path / 加密文件路径")],
    output_path: Annotated[str, ParamInfo("Output decrypted file path / 输出解密文件路径")]
) -> None:
    """
    Decrypt AES-CBC encrypted file.
    解密 AES-CBC 加密的文件
    """
    with open(input_path, "rb") as f:
        encrypted_data = f.read()

    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(output_path, "wb") as f:
        f.write(plaintext)


# --------------------
# AES 加密（字符串/字节）
# --------------------
def aes_encrypt_bytes(
    data: Annotated[bytes, ParamInfo("Raw bytes to encrypt / 待加密字节数据")]
) -> bytes:
    """
    Encrypt raw bytes with AES-CBC.
    使用 AES-CBC 加密字节数据
    """
    iv = get_random_bytes(16)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return iv + ciphertext


# --------------------
# AES 解密（字符串/字节）
# --------------------
def aes_decrypt_bytes(
    encrypted: Annotated[bytes, ParamInfo("Encrypted bytes / 加密字节数据")]
) -> bytes:
    """
    Decrypt AES-CBC encrypted bytes.
    解密 AES-CBC 加密的字节数据
    """
    iv = encrypted[:16]
    ciphertext = encrypted[16:]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)

# --------------------
# 名字转换
# --------------------
def fullname_cn2en(
        chinese_name: Annotated[str, ParamInfo("Chinese full name / 中文全名")]
) -> str:
    """Convert Chinese full name to English-style 'given.surname'. 中文名转英文名"""
    double_surname = {
        "欧阳", "太史", "端木", "上官", "司马", "东方", "独孤", "南宫",
        "万俟", "闻人", "夏侯", "诸葛", "尉迟", "公羊", "赫连", "皇甫",
        "宗政", "濮阳", "公冶", "太叔", "申屠", "公孙", "慕容", "仲孙",
        "钟离", "长孙", "宇文", "城池", "司徒", "司空", "亓官", "鲜于",
        "闾丘", "子车", "颛孙", "端木", "巫马", "公西", "漆雕", "乐正"
    }
    # 检查是否复姓
    if len(chinese_name) >= 2 and chinese_name[:2] in double_surname:
        surname = chinese_name[:2]
        given_name = chinese_name[2:]
    else:
        surname = chinese_name[0]
        given_name = chinese_name[1:]
    # 获取拼音
    surname_pinyin = pinyin(surname, style=Style.NORMAL)[0][0]
    given_name_pinyin = ''.join([p[0] for p in pinyin(given_name, style=Style.NORMAL)])
    # 组合成英文名
    english_name = f"{given_name_pinyin}.{surname_pinyin}"
    return english_name.lower()


# --------------------
# 文件/目录相关
# --------------------
def ensure_dir(path: Annotated[str, ParamInfo("Directory path to ensure / 待确保的目录路径")]) -> str:
    """Ensure directory exists, create if not exists. 确保目录存在，不存在则创建"""
    os.makedirs(path, exist_ok=True)
    return path


def remove_dir(path: Annotated[str, ParamInfo("Directory path to remove / 待删除的目录路径")]) -> None:
    """Remove directory and all its contents. 删除目录及其所有内容"""
    if os.path.exists(path):
        shutil.rmtree(path)


def list_files(
        path: Annotated[str, ParamInfo("Directory path / 目录路径")],
        suffix: Annotated[str, ParamInfo("Optional suffix filter / 可选后缀过滤")] = ""
) -> list[str]:
    """List files in a directory with optional suffix filter. 列出目录下的文件，可按后缀过滤"""
    return [f for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f)) and f.endswith(suffix)]


# --------------------
# 时间相关
# --------------------
def current_time_str(
        fmt: Annotated[str, ParamInfo("Time format string / 时间格式")] = "%Y-%m-%d %H:%M:%S"
) -> str:
    """Return current time as formatted string. 返回当前时间的格式化字符串"""
    return datetime.now().strftime(fmt)


def time_diff_seconds(
        start: Annotated[datetime, ParamInfo("Start datetime / 开始时间")],
        end: Annotated[datetime, ParamInfo("End datetime / 结束时间")]
) -> float:
    """Return difference in seconds between two datetime objects. 计算两个 datetime 之间的秒数差"""
    return (end - start).total_seconds()


# --------------------
# 数学/安全计算
# --------------------
def safe_divide(
        a: Annotated[float, ParamInfo("Dividend / 被除数")],
        b: Annotated[float, ParamInfo("Divisor / 除数")],
        default: Annotated[float, ParamInfo("Default value if division fails / 除零返回值")] = 0.0
) -> float:
    """Safe division. Return default if division by zero. 安全除法，除零返回默认值"""
    try:
        return a / b
    except ZeroDivisionError:
        return default


def clamp(
        value: Annotated[float, ParamInfo("Value to clamp / 待限制的数值")],
        min_value: Annotated[float, ParamInfo("Minimum value / 最小值")],
        max_value: Annotated[float, ParamInfo("Maximum value / 最大值")]
) -> float:
    """Clamp value to be within min and max. 限制数值在最小值和最大值之间"""
    return max(min_value, min(max_value, value))


# --------------------
# 字符串处理
# --------------------
def truncate(
        text: Annotated[str, ParamInfo("String to truncate / 待截断字符串")],
        length: Annotated[int, ParamInfo("Maximum length / 最大长度")],
        suffix: Annotated[str, ParamInfo("Suffix if truncated / 截断后缀")] = "..."
) -> str:
    """Truncate string to a maximum length, append suffix if truncated. 截断字符串，超过长度添加后缀"""
    if len(text) <= length:
        return text
    return text[:length] + suffix


def safe_str(
        obj: Annotated[Any, ParamInfo("Object to convert / 待转换对象")],
        default: Annotated[str, ParamInfo("Default string if conversion fails / 转换失败默认值")] = ""
) -> str:
    """Convert object to string, return default if fails. 安全转换为字符串，失败返回默认值"""
    try:
        return str(obj)
    except Exception:
        return default


# --------------------
# 压缩/解压缩
# --------------------
def zip_dir(
        folder_path: Annotated[str, ParamInfo("Folder to compress / 待压缩文件夹")],
        zip_path: Annotated[str, ParamInfo("Output zip file path / 输出 zip 文件路径")],
        remove_source: Annotated[bool, ParamInfo("Delete source folder after compression / 是否删除源文件夹")] = False,
        password: Annotated[str | None, ParamInfo("Optional password / 可选密码")] = None
) -> None:
    """Compress folder into zip file. 可删除源文件或加密"""
    folder_path = os.path.abspath(folder_path)
    zip_path = os.path.abspath(zip_path)

    # AES 加密优先
    if password and pyzipper:
        with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode())
            for root, _, files in os.walk(folder_path):
                for file in files:
                    zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))
    else:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            if password:
                zf.setpassword(password.encode())
            for root, _, files in os.walk(folder_path):
                for file in files:
                    zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

    if remove_source:
        shutil.rmtree(folder_path)


def unzip_file(
        zip_path: Annotated[str, ParamInfo("Zip file path / 压缩包路径")],
        extract_dir: Annotated[str, ParamInfo("Directory to extract / 解压目录")],
        password: Annotated[str | None, ParamInfo("Optional password / 可选密码")] = None,
        remove_source: Annotated[bool, ParamInfo("Delete zip after extraction / 是否删除压缩包")] = False
) -> None:
    """Extract zip file. 可处理密码和删除压缩包"""
    zip_path = os.path.abspath(zip_path)
    extract_dir = os.path.abspath(extract_dir)
    ensure_dir(extract_dir)

    if password and pyzipper:
        with pyzipper.AESZipFile(zip_path, 'r') as zf:
            zf.setpassword(password.encode())
            zf.extractall(extract_dir)
    else:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            if password:
                zf.setpassword(password.encode())
            zf.extractall(extract_dir)

    if remove_source:
        os.remove(zip_path)


def make_archive(
        folder_path: Annotated[str, ParamInfo("Folder to compress / 待压缩文件夹")],
        archive_name: Annotated[str | None, ParamInfo("Zip file name / 压缩文件名")] = None,
        remove_source: Annotated[bool, ParamInfo("Delete source folder after compression / 是否删除源文件夹")] = False,
        password: Annotated[str | None, ParamInfo("Optional password / 可选密码")] = None
) -> str:
    """Compress folder and return zip path. 返回 zip 文件路径"""
    folder_path = os.path.abspath(folder_path)
    if archive_name is None:
        archive_name = os.path.basename(folder_path)
    zip_path = os.path.join(os.path.dirname(folder_path), f"{archive_name}.zip")
    zip_dir(folder_path, zip_path, remove_source=remove_source, password=password)
    return zip_path


# --------------------
# 函数工具
# --------------------
def retry(
        func: Annotated[Callable, ParamInfo("Function to retry / 待重试函数")],
        times: Annotated[int, ParamInfo("Retry times / 重试次数")] = 3,
        exceptions: Annotated[tuple, ParamInfo("Exceptions to catch / 捕获异常类型")] = (Exception,),
        delay: Annotated[float, ParamInfo("Delay seconds between retries / 重试间隔秒")] = 0
) -> Any:
    """Retry a function n times if exceptions occur. 遇到异常重试函数 n 次"""
    import time
    last_exception = None
    for _ in range(times):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if delay > 0:
                time.sleep(delay)
    raise last_exception
