import json
import re

# ── Badge helpers ────────────────────────────────────────────────────────────

TECH_BADGES = {
    "single-spa":  ("Single--SPA",  "E91E63", "single-spa",      "white"),
    "angular":     ("Angular",      "DD0031", "angular",         "white"),
    "angular js":  ("AngularJS",    "E23237", "angularjs",       "white"),
    "react":       ("React",        "20232A", "react",           "61DAFB"),
    "vue":         ("Vue.js",       "4FC08D", "vue.js",          "white"),
    "svelte":      ("Svelte",       "FF3E00", "svelte",          "white"),
    "javascript":  ("JavaScript",   "F7DF1E", "javascript",      "black"),
    "typescript":  ("TypeScript",   "3178C6", "typescript",      "white"),
    "css":         ("CSS3",         "1572B6", "css3",            "white"),
    "docker":      ("Docker",       "2496ED", "docker",          "white"),
    "node js":     ("Node.js",      "5FA04E", "node.js",         "white"),
    "material":    ("Angular+Material", "757575", "angular",     "white"),
    "es6":         ("ES6",          "F7DF1E", "javascript",      "black"),
    "bootstrap":   ("Bootstrap",    "7952B3", "bootstrap",       "white"),
    "rust":        ("Rust",         "000000", "rust",            "white"),
    "ruby":        ("Ruby",         "CC342D", "ruby",            "white"),
    "npm":         ("npm",          "CB3837", "npm",             "white"),
    "webassembly": ("WebAssembly",  "654FF0", "webassembly",     "white"),
}

def make_badge(tech):
    key = tech.lower().strip()
    if key in TECH_BADGES:
        label, color, logo, logo_color = TECH_BADGES[key]
        return (f'<img src="https://img.shields.io/badge/{label}-{color}'
                f'?style=flat-square&logo={logo}&logoColor={logo_color}" alt="{tech}"/>')
    # fallback — grey badge, no logo
    safe = tech.replace(" ", "_").replace("-", "--")
    return (f'<img src="https://img.shields.io/badge/{safe}-555555'
            f'?style=flat-square&logoColor=white" alt="{tech}"/>')


# ── Featured Projects ────────────────────────────────────────────────────────

def build_featured_projects(projects):
    lines = []
    lines.append("<!-- FEATURED_PROJECTS_START -->")
    lines.append("")
    lines.append("## 🚀 &nbsp;Featured Projects")
    lines.append("")
    lines.append('<div align="center">')
    lines.append("")

    for p in projects:
        badges = " ".join(make_badge(t) for t in p["techStack"])
        has_demo = p["liveDemoUrl"] not in ("N/A", "", None)

        demo_btn = ""
        if has_demo:
            demo_btn = (f'&nbsp;<a href="{p["liveDemoUrl"]}" target="_blank">'
                        f'<img src="https://img.shields.io/badge/🌐 Live Demo-FF5722?style=for-the-badge" alt="Live Demo"/></a>')

        lines.append(
            f'<table width="100%"><tr><td valign="top" width="100%">\n'
            f'\n'
            f'### [{p["name"]}]({p["gitHubUrl"]})\n'
            f'\n'
            f'{p["description"]}\n'
            f'\n'
            f'<p>{badges}</p>\n'
            f'\n'
            f'<a href="{p["gitHubUrl"]}" target="_blank">'
            f'<img src="https://img.shields.io/badge/📂 View Repo-181717?style=for-the-badge&logo=github&logoColor=white" alt="View Repo"/></a>'
            f'{demo_btn}\n'
            f'\n'
            f'</td></tr></table>\n'
            f'\n'
            f'<br/>\n'
        )

    lines.append("</div>")
    lines.append("")
    lines.append("<!-- FEATURED_PROJECTS_END -->")
    return "\n".join(lines)


# ── Open Source ──────────────────────────────────────────────────────────────

def build_open_source(repos):
    lines = []
    lines.append("<!-- OPEN_SOURCE_START -->")
    lines.append("")
    lines.append("## 🌍 &nbsp;Open Source")
    lines.append("")
    lines.append('<div align="center">')
    lines.append("")
    lines.append('<table width="100%">')
    lines.append("  <tr>")

    for i, r in enumerate(repos):
        # detect host for badge color
        url = r["url"]
        if "github.com" in url:
            host_badge = ('https://img.shields.io/badge/GitHub-181717'
                          '?style=flat-square&logo=github&logoColor=white')
            host_label = "GitHub"
        elif "npmjs.com" in url:
            host_badge = ('https://img.shields.io/badge/npm-CB3837'
                          '?style=flat-square&logo=npm&logoColor=white')
            host_label = "npm"
        elif "rubygems.org" in url:
            host_badge = ('https://img.shields.io/badge/RubyGems-CC342D'
                          '?style=flat-square&logo=ruby&logoColor=white')
            host_label = "RubyGems"
        else:
            host_badge = ('https://img.shields.io/badge/View-555555'
                          '?style=flat-square&logoColor=white')
            host_label = "View"

        lines.append(f'    <td valign="top" width="33%">')
        lines.append(f'      <h4><a href="{url}" target="_blank">{r["name"]}</a></h4>')
        lines.append(f'      <p>{r["description"]}</p>')
        lines.append(f'      <a href="{url}" target="_blank">'
                     f'<img src="{host_badge}" alt="{host_label}"/></a>')
        lines.append(f'    </td>')

        # close row and open new one every 3 items
        if (i + 1) % 3 == 0 and i + 1 < len(repos):
            lines.append("  </tr>")
            lines.append("  <tr>")

    lines.append("  </tr>")
    lines.append("</table>")
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append("<!-- OPEN_SOURCE_END -->")
    return "\n".join(lines)


# ── Inject into README ───────────────────────────────────────────────────────

def inject(readme, start_marker, end_marker, new_content):
    pattern = rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
    if re.search(pattern, readme, flags=re.DOTALL):
        return re.sub(pattern, new_content, readme, flags=re.DOTALL)
    return readme   # markers not found — caller will append


# ── Main ─────────────────────────────────────────────────────────────────────

with open("data/featured_projects.json") as f:
    projects = json.load(f)

with open("data/open_source_projects.json") as f:
    oss = json.load(f)

with open("README.md") as f:
    readme = f.read()

fp_block = build_featured_projects(projects)
os_block = build_open_source(oss)

# inject / replace sections
readme = inject(readme,
                "<!-- FEATURED_PROJECTS_START -->",
                "<!-- FEATURED_PROJECTS_END -->",
                fp_block)

readme = inject(readme,
                "<!-- OPEN_SOURCE_START -->",
                "<!-- OPEN_SOURCE_END -->",
                os_block)

with open("README.md", "w") as f:
    f.write(readme)

print("✅ README.md updated successfully.")