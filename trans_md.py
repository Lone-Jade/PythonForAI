def replace_symbols_in_md(file_path):
    try:
        with open(file_path, 'r', encoding='utf - 8') as file:
            content = file.read()
        new_content = content.replace('\\[', '$$').replace('\\]', '$$').replace('\\(', '$').replace('\\)', '$')
        with open(file_path, 'w', encoding='utf - 8') as file:
            file.write(new_content)
        print("替换成功")
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    file_path = input("请输入.md文件路径: ")
    replace_symbols_in_md(file_path)