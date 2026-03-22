import json
import re

# ── Badge helpers ────────────────────────────────────────────────────────────
# Keys must be lowercase — matched against tech.lower().strip() from JSON
# Format: "key": ("Badge Label", "HEX color", "simple-icons logo name", "logo color")

TECH_BADGES = {
    # ── Frontend Frameworks ──────────────────────────────────────────────────
    "angular":          ("Angular",           "DD0031", "angular",            "white"),
    "angular js":       ("AngularJS",         "E23237", "angularjs",          "white"),
    "react":            ("React",             "20232A", "react",              "61DAFB"),
    "vue":              ("Vue.js",            "4FC08D", "vue.js",             "white"),
    "vue.js":           ("Vue.js",            "4FC08D", "vue.js",             "white"),
    "svelte":           ("Svelte",            "FF3E00", "svelte",             "white"),
    "next.js":          ("Next.js",           "000000", "next.js",            "white"),
    "nextjs":           ("Next.js",           "000000", "next.js",            "white"),
    "remix":            ("Remix",             "000000", "remix",              "white"),
    "astro":            ("Astro",             "BC52EE", "astro",              "white"),
    "analog.js":        ("AnalogJS",          "0F172A", "angular",            "white"),
    "analogjs":         ("AnalogJS",          "0F172A", "angular",            "white"),
    "scully":           ("Scully",            "FF6B6B", "angular",            "white"),
    "single-spa":       ("Single--SPA",       "E91E63", "single-spa",         "white"),
    "tanstack":         ("TanStack",          "FF4154", "react-query",        "white"),
    # ── Languages ────────────────────────────────────────────────────────────
    "javascript":       ("JavaScript",        "F7DF1E", "javascript",         "black"),
    "typescript":       ("TypeScript",        "3178C6", "typescript",         "white"),
    "coffeescript":     ("CoffeeScript",      "2F2625", "coffeescript",       "white"),
    "es6":              ("ES6",               "F7DF1E", "javascript",         "black"),
    "esnext":           ("ESNext",            "1F6FEB", "javascript",         "white"),
    "python":           ("Python",            "3776AB", "python",             "white"),
    "go":               ("Go",                "00ADD8", "go",                 "white"),
    "golang":           ("Go",                "00ADD8", "go",                 "white"),
    "rust":             ("Rust",              "000000", "rust",               "white"),
    "ruby":             ("Ruby",              "CC342D", "ruby",               "white"),
    "c":                ("C",                 "A8B9CC", "c",                  "black"),
    "c++":              ("C++",               "00599C", "c%2B%2B",            "white"),
    # ── State Management ─────────────────────────────────────────────────────
    "rxjs":             ("RxJS",              "B7178C", "reactivex",          "white"),
    "ngrx":             ("NgRx",              "BA2BD2", "reactivex",          "white"),
    "redux":            ("Redux",             "764ABC", "redux",              "white"),
    "redux saga":       ("Redux_Saga",        "999999", "redux-saga",         "white"),
    "redux thunk":      ("Redux_Thunk",       "764ABC", "redux",              "white"),
    "mobx":             ("MobX",              "FF9955", "mobx",               "white"),
    # ── Styling ──────────────────────────────────────────────────────────────
    "html":             ("HTML5",             "E34F26", "html5",              "white"),
    "html5":            ("HTML5",             "E34F26", "html5",              "white"),
    "css":              ("CSS3",              "1572B6", "css3",               "white"),
    "css3":             ("CSS3",              "1572B6", "css3",               "white"),
    "sass":             ("Sass",              "CC6699", "sass",               "white"),
    "scss":             ("Sass",              "CC6699", "sass",               "white"),
    "tailwind":         ("Tailwind_CSS",      "06B6D4", "tailwind-css",       "white"),
    "tailwind css":     ("Tailwind_CSS",      "06B6D4", "tailwind-css",       "white"),
    "tailwindcss":      ("Tailwind_CSS",      "06B6D4", "tailwind-css",       "white"),
    "bootstrap":        ("Bootstrap",         "7952B3", "bootstrap",          "white"),
    "material":         ("Angular+Material",  "757575", "angular",            "white"),
    "angular material": ("Angular+Material",  "757575", "angular",            "white"),
    "d3.js":            ("D3.js",             "F9A03C", "d3.js",              "white"),
    "d3":               ("D3.js",             "F9A03C", "d3.js",              "white"),
    "webassembly":      ("WebAssembly",       "654FF0", "webassembly",        "white"),
    "wasm":             ("WebAssembly",       "654FF0", "webassembly",        "white"),
    # ── Backend ──────────────────────────────────────────────────────────────
    "node js":          ("Node.js",           "5FA04E", "node.js",            "white"),
    "node.js":          ("Node.js",           "5FA04E", "node.js",            "white"),
    "nodejs":           ("Node.js",           "5FA04E", "node.js",            "white"),
    "express":          ("Express",           "000000", "express",            "white"),
    "express.js":       ("Express",           "000000", "express",            "white"),
    "nestjs":           ("NestJS",            "E0234E", "nestjs",             "white"),
    "graphql":          ("GraphQL",           "E10098", "graphql",            "white"),
    "deno":             ("Deno",              "000000", "deno",               "white"),
    "django":           ("Django",            "092E20", "django",             "white"),
    "rails":            ("Ruby_on_Rails",     "D30001", "ruby-on-rails",      "white"),
    "ruby on rails":    ("Ruby_on_Rails",     "D30001", "ruby-on-rails",      "white"),
    # ── Databases ────────────────────────────────────────────────────────────
    "mongodb":          ("MongoDB",           "47A248", "mongodb",            "white"),
    "postgresql":       ("PostgreSQL",        "4169E1", "postgresql",         "white"),
    "postgres":         ("PostgreSQL",        "4169E1", "postgresql",         "white"),
    "mysql":            ("MySQL",             "4479A1", "mysql",              "white"),
    "redis":            ("Redis",             "DC382D", "redis",              "white"),
    "firebase":         ("Firebase",          "FFCA28", "firebase",           "black"),
    "sqlite":           ("SQLite",            "003B57", "sqlite",             "white"),
    # ── Mobile ───────────────────────────────────────────────────────────────
    "ionic":            ("Ionic",             "3880FF", "ionic",              "white"),
    "react native":     ("React_Native",      "20232A", "react",              "61DAFB"),
    "flutter":          ("Flutter",           "02569B", "flutter",            "white"),
    # ── Cloud & DevOps ───────────────────────────────────────────────────────
    "aws":              ("AWS",               "232F3E", "amazon-aws",         "white"),
    "gcp":              ("Google_Cloud",      "4285F4", "google-cloud",       "white"),
    "google cloud":     ("Google_Cloud",      "4285F4", "google-cloud",       "white"),
    "heroku":           ("Heroku",            "430098", "heroku",             "white"),
    "docker":           ("Docker",            "2496ED", "docker",             "white"),
    "jenkins":          ("Jenkins",           "D24939", "jenkins",            "white"),
    "terraform":        ("Terraform",         "7B42BC", "terraform",          "white"),
    "nginx":            ("Nginx",             "009639", "nginx",              "white"),
    "git":              ("Git",               "F05032", "git",                "white"),
    "github actions":   ("GitHub_Actions",    "2088FF", "github-actions",     "white"),
    "nx":               ("Nx",                "143055", "nx",                 "white"),
    "linux":            ("Linux",             "FCC624", "linux",              "black"),
    "bash":             ("Bash",              "4EAA25", "gnu-bash",           "white"),
    # ── Testing ──────────────────────────────────────────────────────────────
    "jest":             ("Jest",              "C21325", "jest",               "white"),
    "vitest":           ("Vitest",            "6E9F18", "vitest",             "white"),
    "jasmine":          ("Jasmine",           "8A4182", "jasmine",            "white"),
    "karma":            ("Karma",             "56C0A7", "karma",              "white"),
    "postman":          ("Postman",           "FF6C37", "postman",            "white"),
    # ── Tools & Build ────────────────────────────────────────────────────────
    "webpack":          ("Webpack",           "8DD6F9", "webpack",            "black"),
    "babel":            ("Babel",             "F9DC3E", "babel",              "black"),
    "gulp":             ("Gulp",              "CF4647", "gulp",               "white"),
    "npm":              ("npm",               "CB3837", "npm",                "white"),
    "yarn":             ("Yarn",              "2C8EBB", "yarn",               "white"),
    "pnpm":             ("pnpm",              "F69220", "pnpm",               "white"),
    "bun":              ("Bun",               "000000", "bun",                "white"),
    "vscode":           ("VS_Code",           "007ACC", "visual-studio-code", "white"),
    "vs code":          ("VS_Code",           "007ACC", "visual-studio-code", "white"),
    "figma":            ("Figma",             "F24E1E", "figma",              "white"),
    "eslint":           ("ESLint",            "4B32C3", "eslint",             "white"),
    "mermaid":          ("Mermaid",           "FF3670", "mermaid",            "white"),
}

def make_badge(tech, style="flat-square"):
    key = tech.lower().strip()
    if key in TECH_BADGES:
        label, color, logo, logo_color = TECH_BADGES[key]
        return (f'<img src="https://img.shields.io/badge/{label}-{color}'
                f'?style={style}&logo={logo}&logoColor={logo_color}" alt="{tech}"/>')
    # fallback — grey badge, no logo
    safe = tech.replace(" ", "_").replace("-", "--")
    return (f'<img src="https://img.shields.io/badge/{safe}-555555'
            f'?style={style}&logoColor=white" alt="{tech}"/>')


# ── Featured Projects ────────────────────────────────────────────────────────

def build_featured_projects(projects):
    lines = []
    lines.append("<!-- FEATURED_PROJECTS_START -->")
    lines.append("")
    lines.append("## 🚀 &nbsp;Featured Projects")
    lines.append("")

    for p in projects:
        badges = "&nbsp;".join(make_badge(t) for t in p["techStack"])
        has_demo = p["liveDemoUrl"] not in ("N/A", "", None)

        demo_btn = ""
        if has_demo:
            demo_btn = (
                f'&nbsp;&nbsp;<a href="{p["liveDemoUrl"]}" target="_blank">'
                f'<img src="https://img.shields.io/badge/🌐%20Live%20Demo-FF5722'
                f'?style=for-the-badge" alt="Live Demo"/></a>'
            )

        # Single full-width table, td has align=center — no outer div needed
        lines.append('<table width="100%"><tr><td align="center" width="100%">')
        lines.append("")
        lines.append(f'### [{p["name"]}]({p["gitHubUrl"]})')
        lines.append("")
        lines.append(f'{p["description"]}')
        lines.append("")
        lines.append(f'<p>{badges}</p>')
        lines.append("")
        lines.append(
            f'<a href="{p["gitHubUrl"]}" target="_blank">'
            f'<img src="https://img.shields.io/badge/📂%20View%20Repo-181717'
            f'?style=for-the-badge&logo=github&logoColor=white" alt="View Repo"/></a>'
            f'{demo_btn}'
        )
        lines.append("")
        lines.append('</td></tr></table>')
        lines.append("")
        lines.append('<br/>')
        lines.append("")

    lines.append("<!-- FEATURED_PROJECTS_END -->")
    return "\n".join(lines)


# ── Open Source ──────────────────────────────────────────────────────────────

def get_host_badge(url):
    """Return (badge_img_url, label) based on the URL host."""
    if "github.com" in url:
        return ('https://img.shields.io/badge/GitHub-181717'
                '?style=flat-square&logo=github&logoColor=white', "GitHub")
    elif "npmjs.com" in url:
        return ('https://img.shields.io/badge/npm-CB3837'
                '?style=flat-square&logo=npm&logoColor=white', "npm")
    elif "rubygems.org" in url:
        return ('https://img.shields.io/badge/RubyGems-CC342D'
                '?style=flat-square&logo=ruby&logoColor=white', "RubyGems")
    elif "hub.docker.com" in url:
        return ('https://img.shields.io/badge/Docker%20Hub-2496ED'
                '?style=flat-square&logo=docker&logoColor=white', "Docker Hub")
    else:
        return ('https://img.shields.io/badge/View-555555'
                '?style=flat-square&logoColor=white', "View")


def build_open_source(repos):
    lines = []
    lines.append("<!-- OPEN_SOURCE_START -->")
    lines.append("")
    lines.append("## 🌍 &nbsp;Open Source")
    lines.append("")
    lines.append('<table width="100%">')
    lines.append("  <tr>")

    for i, r in enumerate(repos):
        host_badge, host_label = get_host_badge(r["url"])

        lines.append(f'    <td align="center" valign="top" width="33%">')
        lines.append(f'      <h4><a href="{r["url"]}" target="_blank">{r["name"]}</a></h4>')
        lines.append(f'      <p>{r["description"]}</p>')
        lines.append(
            f'      <a href="{r["url"]}" target="_blank">'
            f'<img src="{host_badge}" alt="{host_label}"/></a>'
        )
        lines.append(f'    </td>')

        if (i + 1) % 3 == 0 and i + 1 < len(repos):
            lines.append("  </tr>")
            lines.append("  <tr>")

    lines.append("  </tr>")
    lines.append("</table>")
    lines.append("")
    lines.append("<!-- OPEN_SOURCE_END -->")
    return "\n".join(lines)


# ── Inject into README ───────────────────────────────────────────────────────

def inject(readme, start_marker, end_marker, new_content):
    pattern = rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
    if re.search(pattern, readme, flags=re.DOTALL):
        return re.sub(pattern, new_content, readme, flags=re.DOTALL)
    return readme


# ── Main ─────────────────────────────────────────────────────────────────────

with open("data/featured_projects.json") as f:
    projects = json.load(f)

with open("data/open_source_projects.json") as f:
    oss = json.load(f)

with open("README.md") as f:
    readme = f.read()

# inject / replace sections
readme = inject(readme,
                "<!-- FEATURED_PROJECTS_START -->",
                "<!-- FEATURED_PROJECTS_END -->",
                build_featured_projects(projects))

readme = inject(readme,
                "<!-- OPEN_SOURCE_START -->",
                "<!-- OPEN_SOURCE_END -->",
                build_open_source(oss))

with open("README.md", "w") as f:
    f.write(readme)

print("✅ README.md updated successfully.")