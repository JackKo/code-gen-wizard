import re
import os
from typing import List, Tuple, Dict
from assertion_generator import generate_assertion_class

def extract_blocks(code: str) -> List[Tuple[str, str, List[str]]]:
    pattern = re.compile(r'// <# (\w+)\.(\w+) #>(.*?)// </#>', re.DOTALL)
    matches = pattern.finditer(code)

    blocks = []
    for match in matches:
        class_name = match.group(1)
        method_name = match.group(2)
        block_content = match.group(3).strip().splitlines()
        cleaned_lines = [line.strip() for line in block_content if line.strip()]
        blocks.append((class_name, method_name, cleaned_lines))
    return blocks

def extract_locators(lines: List[str]) -> Dict[str, str]:
    locators = {}
    count = 1
    for line in lines:
        match = re.search(r'page\.\w+Async\("([^"]+)"', line)
        if match:
            selector = match.group(1)
            variable_name = f"locator{count}"
            locators[variable_name] = selector
            count += 1
    return locators

def generate_page_objects(code: str, output_dir: str) -> Dict[str, Dict[str, str]]:
    pages_dir = os.path.join(output_dir, "Pages")
    os.makedirs(pages_dir, exist_ok=True)

    blocks = extract_blocks(code)
    class_methods = {}
    class_locators = {}

    for class_name, method_name, lines in blocks:
        if class_name not in class_methods:
            class_methods[class_name] = []
            class_locators[class_name] = {}

        locators = extract_locators(lines)
        class_locators[class_name].update(locators)

        method_lines = []
        for line in lines:
            for loc_name, selector in locators.items():
                if selector in line:
                    line = line.replace(f'"{selector}"', loc_name)
            method_lines.append("        " + line)

        method_body = f"    public async Task {method_name}() {{" + "".join(method_lines) + "}"
        class_methods[class_name].append(method_body)

    for class_name, methods in class_methods.items():
        file_path = os.path.join(pages_dir, f"{class_name}.cs")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"public class {class_name} {{")
            f.write("    private readonly IPage page;")
            for loc_name, selector in class_locators[class_name].items():
                f.write(f'    private ILocator {loc_name} => page.Locator("{selector}");')
            f.write(f"public {class_name}(IPage page) {{")
            f.write("        this.page = page;")
            f.write("    }")
            f.write("".join(methods))
            f.write("}")

    return class_locators

def generate_test_class(class_name: str, methods: List[str], output_dir: str):
    tests_dir = os.path.join(output_dir, "Tests")
    os.makedirs(tests_dir, exist_ok=True)
    file_path = os.path.join(tests_dir, f"{class_name}Test.cs")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("using Microsoft.Playwright;using System.Threading.Tasks;")
        f.write(f"public class {class_name}Test {{")
        f.write("    private IPage page;")
        f.write(f"    private {class_name} pageObject;")
        f.write("    public async Task Setup(IPage page) {")
        f.write("        this.page = page;")
        f.write(f"        this.pageObject = new {class_name}(page);")
        f.write("    }")
        for method in methods:
            f.write(f"    public async Task Test_{method}() {{")
            f.write(f"        await pageObject.{method}();")
            f.write("    }")
        f.write("}")

def generate_all(code: str, output_dir: str):
    locators_per_class = generate_page_objects(code, output_dir)
    blocks = extract_blocks(code)
    grouped = {}
    for class_name, method_name, _ in blocks:
        if class_name not in grouped:
            grouped[class_name] = []
        grouped[class_name].append(method_name)
    for cls, methods in grouped.items():
        generate_test_class(cls, methods, output_dir)
        generate_assertion_class(cls, locators_per_class.get(cls, {}), output_dir)