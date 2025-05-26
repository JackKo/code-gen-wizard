import os

def generate_assertion_class(class_name: str, locators: dict, output_dir: str):
    assertions_dir = os.path.join(output_dir, "Assertions")
    os.makedirs(assertions_dir, exist_ok=True)
    file_path = os.path.join(assertions_dir, f"{class_name}Assertions.cs")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("using FluentAssertions;using Microsoft.Playwright;")
        f.write(f"public class {class_name}Assertions {{")
        f.write("    private readonly IPage page;")
        f.write(f"    public {class_name}Assertions(IPage page) {{")
        f.write("        this.page = page;")
        f.write("    }")

        for loc_name, selector in locators.items():
            method_name = f"Assert{loc_name.capitalize()}Visible"
            f.write(f"    public async Task {method_name}() {{")
            f.write(f"        var visible = await page.Locator(\"+{selector}\").IsVisibleAsync();")
            f.write(f"        visible.Should().BeTrue(\"{selector} should be visible\");")
            f.write("    }")
        f.write("}")