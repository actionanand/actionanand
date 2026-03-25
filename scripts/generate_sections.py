import json
import re
from urllib.parse import quote

# ═══════════════════════════════════════════════════════════════════════════════
# TECH BADGE DICTIONARY
# Key = lowercase tech name from JSON
# Value = (Badge Label, HEX color, simple-icons logo name, logo color)
# ═══════════════════════════════════════════════════════════════════════════════
TECH_BADGES = {
    # Frontend Frameworks
    "angular":           ("Angular",              "DD0031", "angular",              "white"),
    "angular js":        ("AngularJS",             "E23237", "angularjs",            "white"),
    "angularjs":         ("AngularJS",             "E23237", "angularjs",            "white"),
    "react":             ("React",                 "20232A", "react",                "61DAFB"),
    "vue":               ("Vue.js",                "4FC08D", "vue.js",               "white"),
    "vue.js":            ("Vue.js",                "4FC08D", "vue.js",               "white"),
    "svelte":            ("Svelte",                "FF3E00", "svelte",               "white"),
    "next.js":           ("Next.js",               "000000", "next.js",              "white"),
    "nextjs":            ("Next.js",               "000000", "next.js",              "white"),
    "remix":             ("Remix",                 "000000", "remix",                "white"),
    "astro":             ("Astro",                 "BC52EE", "astro",                "white"),
    "analog.js":         ("AnalogJS",              "0F172A", "angular",              "white"),
    "analogjs":          ("AnalogJS",              "0F172A", "angular",              "white"),
    "scully":            ("Scully",                "FF6B6B", "angular",              "white"),
    "single-spa":        ("Single--SPA",           "E91E63", "single-spa",           "white"),
    "tanstack":          ("TanStack",              "FF4154", "react-query",          "white"),
    "mean stack":        ("MEAN_Stack",            "00BCD4", "angular",              "white"),
    "mern stack":        ("MERN_Stack",            "61DAFB", "react",                "black"),
    "jam stack":         ("JAMstack",              "F0047F", "jamstack",             "white"),
    "jamstack":          ("JAMstack",              "F0047F", "jamstack",             "white"),
    "pwa":               ("PWA",                   "5A0FC8", "pwa",                  "white"),
    "web components":    ("Web_Components",        "29ABE2", "webcomponents",        "white"),
    "three.js":          ("Three.js",              "000000", "three.js",             "white"),
    "threejs":           ("Three.js",              "000000", "three.js",             "white"),
    "handlebars":        ("Handlebars.js",         "000000", "handlebarsdotjs",      "white"),
    "ejs":               ("EJS",                   "B4CA65", "ejs",                  "black"),
    "pug":               ("Pug",                   "A86454", "pug",                  "white"),
    # Languages
    "javascript":        ("JavaScript",            "F7DF1E", "javascript",           "black"),
    "typescript":        ("TypeScript",            "3178C6", "typescript",           "white"),
    "coffeescript":      ("CoffeeScript",          "2F2625", "coffeescript",         "white"),
    "es6":               ("ES6",                   "F7DF1E", "javascript",           "black"),
    "esnext":            ("ESNext",                "1F6FEB", "javascript",           "white"),
    "python":            ("Python",                "3776AB", "python",               "white"),
    "go":                ("Go",                    "00ADD8", "go",                   "white"),
    "golang":            ("Go",                    "00ADD8", "go",                   "white"),
    "rust":              ("Rust",                  "000000", "rust",                 "white"),
    "ruby":              ("Ruby",                  "CC342D", "ruby",                 "white"),
    "c":                 ("C",                     "A8B9CC", "c",                    "black"),
    "c++":               ("C++",                   "00599C", "c%2B%2B",              "white"),
    # State Management
    "rxjs":              ("RxJS",                  "B7178C", "reactivex",            "white"),
    "ngrx":              ("NgRx",                  "BA2BD2", "reactivex",            "white"),
    "redux":             ("Redux",                 "764ABC", "redux",                "white"),
    "redux saga":        ("Redux_Saga",            "999999", "redux-saga",           "white"),
    "redux thunk":       ("Redux_Thunk",           "764ABC", "redux",                "white"),
    "mobx":              ("MobX",                  "FF9955", "mobx",                 "white"),
    # Styling
    "html":              ("HTML5",                 "E34F26", "html5",                "white"),
    "html5":             ("HTML5",                 "E34F26", "html5",                "white"),
    "css":               ("CSS3",                  "1572B6", "css3",                 "white"),
    "css3":              ("CSS3",                  "1572B6", "css3",                 "white"),
    "sass":              ("Sass",                  "CC6699", "sass",                 "white"),
    "scss":              ("Sass",                  "CC6699", "sass",                 "white"),
    "tailwind":          ("Tailwind_CSS",          "06B6D4", "tailwind-css",         "white"),
    "tailwind css":      ("Tailwind_CSS",          "06B6D4", "tailwind-css",         "white"),
    "tailwindcss":       ("Tailwind_CSS",          "06B6D4", "tailwind-css",         "white"),
    "bootstrap":         ("Bootstrap",             "7952B3", "bootstrap",            "white"),
    "material":          ("Angular+Material",      "757575", "angular",              "white"),
    "angular material":  ("Angular+Material",      "757575", "angular",              "white"),
    "d3.js":             ("D3.js",                 "F9A03C", "d3.js",                "white"),
    "d3":                ("D3.js",                 "F9A03C", "d3.js",                "white"),
    "webassembly":       ("WebAssembly",           "654FF0", "webassembly",          "white"),
    "wasm":              ("WebAssembly",           "654FF0", "webassembly",          "white"),
    # Backend
    "node js":           ("Node.js",               "5FA04E", "node.js",              "white"),
    "node.js":           ("Node.js",               "5FA04E", "node.js",              "white"),
    "nodejs":            ("Node.js",               "5FA04E", "node.js",              "white"),
    "express":           ("Express",               "000000", "express",              "white"),
    "express.js":        ("Express",               "000000", "express",              "white"),
    "nestjs":            ("NestJS",                "E0234E", "nestjs",               "white"),
    "graphql":           ("GraphQL",               "E10098", "graphql",              "white"),
    "deno":              ("Deno",                  "000000", "deno",                 "white"),
    "django":            ("Django",                "092E20", "django",               "white"),
    "rails":             ("Ruby_on_Rails",         "D30001", "ruby-on-rails",        "white"),
    "ruby on rails":     ("Ruby_on_Rails",         "D30001", "ruby-on-rails",        "white"),
    # Databases
    "mongodb":           ("MongoDB",               "47A248", "mongodb",              "white"),
    "postgresql":        ("PostgreSQL",            "4169E1", "postgresql",           "white"),
    "postgres":          ("PostgreSQL",            "4169E1", "postgresql",           "white"),
    "mysql":             ("MySQL",                 "4479A1", "mysql",                "white"),
    "redis":             ("Redis",                 "DC382D", "redis",                "white"),
    "firebase":          ("Firebase",              "FFCA28", "firebase",             "black"),
    "sqlite":            ("SQLite",                "003B57", "sqlite",               "white"),
    # Mobile
    "ionic":             ("Ionic",                 "3880FF", "ionic",                "white"),
    "react native":      ("React_Native",          "20232A", "react",                "61DAFB"),
    "flutter":           ("Flutter",               "02569B", "flutter",              "white"),
    # Cloud & DevOps
    "aws":               ("AWS",                   "232F3E", "amazon-aws",           "white"),
    "gcp":               ("Google_Cloud",          "4285F4", "google-cloud",         "white"),
    "google cloud":      ("Google_Cloud",          "4285F4", "google-cloud",         "white"),
    "heroku":            ("Heroku",                "430098", "heroku",               "white"),
    "docker":            ("Docker",                "2496ED", "docker",               "white"),
    "jenkins":           ("Jenkins",               "D24939", "jenkins",              "white"),
    "spinnaker":         ("Spinnaker",             "139BB4", "spinnaker",            "white"),
    "terraform":         ("Terraform",             "7B42BC", "terraform",            "white"),
    "airflow":           ("Airflow",               "017CEE", "apache-airflow",       "white"),
    "rundeck":           ("Rundeck",               "F73F39", "rundeck",              "white"),
    "backstage io":      ("Backstage",             "9BF0E1", "backstage",            "black"),
    "backstage":         ("Backstage",             "9BF0E1", "backstage",            "black"),
    "nginx":             ("Nginx",                 "009639", "nginx",                "white"),
    "git":               ("Git",                   "F05032", "git",                  "white"),
    "github actions":    ("GitHub_Actions",        "2088FF", "github-actions",       "white"),
    "nx":                ("Nx",                    "143055", "nx",                   "white"),
    "linux":             ("Linux",                 "FCC624", "linux",                "black"),
    "bash":              ("Bash",                  "4EAA25", "gnu-bash",             "white"),
    "wsl":               ("WSL",                   "0a97f5", "linux",                "white"),
    # Testing
    "jest":              ("Jest",                  "C21325", "jest",                 "white"),
    "vitest":            ("Vitest",                "6E9F18", "vitest",               "white"),
    "jasmine":           ("Jasmine",               "8A4182", "jasmine",              "white"),
    "karma":             ("Karma",                 "56C0A7", "karma",                "white"),
    "postman":           ("Postman",               "FF6C37", "postman",              "white"),
    # Tools & Build
    "webpack":           ("Webpack",               "8DD6F9", "webpack",              "black"),
    "babel":             ("Babel",                 "F9DC3E", "babel",                "black"),
    "gulp":              ("Gulp",                  "CF4647", "gulp",                 "white"),
    "nvm":               ("NVM",                   "F4DD4B", "node.js",              "black"),
    "npm":               ("npm",                   "CB3837", "npm",                  "white"),
    "yarn":              ("Yarn",                  "2C8EBB", "yarn",                 "white"),
    "pnpm":              ("pnpm",                  "F69220", "pnpm",                 "white"),
    "bun":               ("Bun",                   "000000", "bun",                  "white"),
    "vscode":            ("VS_Code",               "007ACC", "visual-studio-code",   "white"),
    "vs code":           ("VS_Code",               "007ACC", "visual-studio-code",   "white"),
    "figma":             ("Figma",                 "F24E1E", "figma",                "white"),
    "invision":          ("InVision",              "FF3366", "invision",             "white"),
    "eslint":            ("ESLint",                "4B32C3", "eslint",               "white"),
    "biome":             ("Biome",                 "60A5FA", "biome",                "white"),
    "mermaid":           ("Mermaid",               "FF3670", "mermaid",              "white"),
    "miniconda":         ("Miniconda",             "44A833", "anaconda",             "white"),
    "katex":             ("KaTeX",                 "008080", "katex",                "white"),
    "prism js":          ("PrismJS",               "2D2D2D", "prisma",               "white"),
    "prismjs":           ("PrismJS",               "2D2D2D", "prisma",               "white"),
    "shiki":             ("Shiki",                 "4FC08D", "shiki",                "white"),
    # AI & ML
    "openai":            ("OpenAI",                "412991", "openai",               "white"),
    "langchain":         ("LangChain",             "1C3C3C", "langchain",            "white"),
    "ollama":            ("Ollama",                "000000", "ollama",               "white"),
    "hugging face":      ("Hugging_Face",          "FFD21E", "huggingface",          "black"),
    "claude code":       ("Claude_Code",           "6B3DF5", "anthropic",            "white"),
    "opencode":          ("OpenCode",              "000000", "terminal",             "white"),
    "openai codex":      ("OpenAI_Codex",          "10A37F", "openai",               "white"),
    "github copilot":    ("GitHub_Copilot",        "181717", "github",               "white"),
    "rag":               ("RAG",                   "00B4D8", "databricks",           "white"),
    "ai agents":         ("AI_Agents",             "7C3AED", "probot",               "white"),
    "llm":               ("LLMs",                  "10A37F", "openai",               "white"),
    "vector db":         ("Vector_DB",             "4A154B", "pinecone",             "white"),
    "chatgpt":           ("ChatGPT",               "10A37F", "openai",               "white"),
    "qwen ai":           ("Qwen_AI",               "FF6A00", "alibabadotcom",        "white"),
    "deepseek":          ("DeepSeek",              "1E90FF", "deepseek",             "white"),
    "gemini ai":              ("Gemini_AI",              "4285F4", "google",          "white"),
    # AI Tools & Concepts
    "pi coding agent":        ("PI_Coding_Agent",        "FF4F00", "probot",          "white"),
    "gemini cli":             ("Gemini_CLI",             "4285F4", "google",          "white"),
    "antigravity":            ("Antigravity",            "4285F4", "google",          "white"),
    "ai assisted development":("AI_Assisted_Dev",        "6A5ACD", "probot",          "white"),
    "prompt engineering":     ("Prompt_Engineering",     "FF6F00", "openai",          "white"),
    "ai pair programming":    ("AI_Pair_Programming",    "7C3AED", "github",          "white"),
}

def make_badge(tech, style="for-the-badge"):
    """tech can be a plain string or a dict with 'name' and optional 'url'."""
    if isinstance(tech, dict):
        name = tech["name"]
        url  = tech.get("url", "").strip()
    else:
        name = tech
        url  = ""

    key = name.lower().strip()
    if key in TECH_BADGES:
        label, color, logo, logo_color = TECH_BADGES[key]
        img = (f'<img src="https://img.shields.io/badge/{label}-{color}'
               f'?style={style}&logo={logo}&logoColor={logo_color}" alt="{name}"/>')
    else:
        # fallback — grey badge with tech name, no logo
        safe = name.replace(" ", "_").replace("-", "--")
        img  = (f'<img src="https://img.shields.io/badge/{safe}-555555'
                f'?style={style}&logoColor=white" alt="{name}"/>')

    # wrap in <a> only when a URL is provided
    if url:
        return f'<a href="{url}" target="_blank">{img}</a>'
    return img


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER & TYPING SECTION  (data/profile.json)
# ═══════════════════════════════════════════════════════════════════════════════

def build_header(profile):
    name      = profile["name"]
    role      = profile["role"]
    p_url     = profile["portfolio_url"]
    p_disp    = profile["portfolio_display"]
    # readme-typing-svg requires: single lines= param, raw ; as separator, + for spaces
    # Do NOT use quote() — %20 spaces and %3B semicolons both break the service
    def _encode_line(line):
        return (line
                .replace(" ", "+")
                .replace("|", "%7C")
                .replace("•", "%E2%80%A2")
                .replace("&", "%26")
                .replace("?", "%3F")
                .replace("#", "%23"))
    lines_param = "lines=" + ";".join(_encode_line(l) for l in profile["typing_lines"])
    name_enc  = quote(name, safe="")
    desc_enc  = quote(role, safe="")

    return f"""<!-- HEADER_START -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text={name_enc}&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=32&desc={desc_enc}&descSize=18&descAlignY=52&descAlign=50" width="100%" alt="Header"/>
</div>

<!-- Typing SVG -->
<div align="center">
  <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=3178C6&center=true&vCenter=true&repeat=true&random=false&width=650&height=50&{lines_param}" alt="Typing SVG" /></a>
</div>

<br/>

<!-- Profile Badges -->
<div align="center">
  <a href="{p_url}" target="_blank"><img src="https://img.shields.io/badge/🌐%20Portfolio-{p_disp.replace('-', '--')}-FF5722?style=for-the-badge" alt="Portfolio"/></a>

  <br/><br/>

  <img src="https://komarev.com/ghpvc/?username=actionanand&label=Profile%20Views&color=0e75b6&style=for-the-badge" alt="Profile views"/>
  &nbsp;
  <a href="https://github.com/actionanand?tab=followers"><img src="https://img.shields.io/github/followers/actionanand?label=Followers&style=for-the-badge&color=236ad3&labelColor=1155ba&logo=github" alt="GitHub followers"/></a>
  &nbsp;
  <a href="https://linkedin.com/in/anand-ns" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
</div>
<!-- HEADER_END -->"""


# ═══════════════════════════════════════════════════════════════════════════════
# ABOUT ME  (data/profile.json)
# ═══════════════════════════════════════════════════════════════════════════════

def build_about_me(profile):
    fa     = profile["focus_areas"]
    goals  = "\n".join(f"  - {g}" for g in profile["current_goals"])
    open_to = profile.get("open_to", [])
    open_to_line = f"\nopen_to: [{', '.join(open_to)}]" if open_to else ""
    # ── open_to examples — copy the list you want into data/profile.json ────
    # Actively looking:
    #   "open_to": ["Open to new opportunities", "Full-time roles", "Freelance projects"]
    #   "open_to": ["Actively job hunting", "Full-time", "Remote-friendly roles"]
    #   "open_to": ["Looking for new role", "Full-time", "Open Source Collaboration"]
    #
    # Passively open:
    #   "open_to": ["Open to interesting opportunities", "Freelance", "Consulting"]
    #   "open_to": ["Not actively looking, but open to great opportunities"]
    #   "open_to": ["Selectively open", "Senior / Lead roles only", "Remote preferred"]
    #
    # Not looking:
    #   "open_to": ["Currently employed, not looking"]
    #   "open_to": ["Happy where I am, but open to exceptional offers"]
    #   "open_to": ["Not available for hire"]
    #
    # Freelance / Contract:
    #   "open_to": ["Available for Freelance", "Contract work", "Open Source"]
    #   "open_to": ["Part-time Consulting", "Freelance Angular projects"]
    #
    # Current (active):
    #   "open_to": ["Freelance", "Full-time", "Open Source Collaboration"]
    #
    # To hide the field entirely, set:  "open_to": []
    # ────────────────────────────────────────────────────────────────────────

    return f"""<!-- ABOUT_ME_START -->
## <img src="https://media2.giphy.com/media/QssGEmpkyEOhBCb7e1/giphy.gif?cid=ecf05e47a0n3gi1bfqntqmob8g9aid1oyj2wr3ds3mg700bl&rid=giphy.gif" width="25"> &nbsp;About Me

<img align="right" src="https://media.giphy.com/media/SWoSkN6DxTszqIKEqv/giphy.gif" alt="Coder GIF" width="320">

```yaml
name: {profile["name"]}
location: {profile["location"]}
role: {profile["role"]}
experience: {profile["experience"]}

focus_areas:
  primary: {fa["primary"]}
  frontend: [{", ".join(fa["frontend"])}]
  backend: [{", ".join(fa["backend"])}]
  mobile: [{", ".join(fa["mobile"])}]

current_goals:
{goals}

fun_fact: >
  {profile["fun_fact"]}{open_to_line}
```

<br clear="both"/>
<!-- ABOUT_ME_END -->"""


# ═══════════════════════════════════════════════════════════════════════════════
# TECH STACK  (data/tech_stack.json)
# ═══════════════════════════════════════════════════════════════════════════════

def build_tech_stack(sections):
    lines = []
    lines.append("<!-- TECH_STACK_START -->")
    lines.append("")
    lines.append('## <img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="25"> &nbsp;Tech Stack')
    lines.append("")
    for sec in sections:
        badges = "\n  ".join(make_badge(item) for item in sec["items"])
        lines.append("<details open>")
        lines.append(f'<summary><b>{sec["section"]}</b></summary>')
        lines.append("<br/>")
        lines.append('<p align="center">')
        lines.append(f'  {badges}')
        lines.append("</p>")
        lines.append("</details>")
        lines.append("")
    lines.append("<!-- TECH_STACK_END -->")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# STACK OVERFLOW — top tags driven by profile.json
# ═══════════════════════════════════════════════════════════════════════════════

def build_stackoverflow(profile):
    so       = profile["stackoverflow"]
    uid      = so["user_id"]
    uname    = so["username"]
    so_url   = f"https://stackoverflow.com/users/{uid}/{uname}"
    so_json  = f"https://raw.githubusercontent.com/actionanand/actionanand/main/stackoverflow-stats.json"

    top_tags = "\n  ".join(
        f'<img src="https://img.shields.io/badge/Top%20Tag-{t["tag"].replace(" ", "%20")}-{t["color"]}'
        f'?style=flat-square&logo={t["logo"]}&logoColor={t["logoColor"]}" alt="Top Tag: {t["tag"]}"/>'
        for t in so["top_tags"]
    )

    return f"""<!-- STACKOVERFLOW_START -->
## <img src="https://img.shields.io/badge/-stackoverflow-F58025?style=flat&logo=stackoverflow&logoColor=white" height="25" alt="Stack Overflow"/> &nbsp;Stack Overflow

<div align="center">

  <!-- Stack Overflow Flair (official, auto-updates with reputation & badges) -->
  <a href="{so_url}" target="_blank"><img src="https://stackoverflow.com/users/flair/{uid}.png?theme=dark" width="208" height="58" alt="Stack Overflow profile for {profile["name"]}" title="Stack Overflow profile for {profile["name"]}"/></a>

  <br/>

  <!-- SO Stats badges — auto-updated daily by GitHub Action: stackoverflow-stats.yml -->
  <!-- Reputation: dynamic via shields.io stackexchange API -->
  <a href="{so_url}" target="_blank"><img src="https://img.shields.io/stackexchange/stackoverflow/r/{uid}?style=for-the-badge&logo=stackoverflow&logoColor=white&label=Reputation&color=F58025" alt="Stack Overflow Reputation"/></a>&nbsp;
  <!-- Questions & Answers: dynamic via shields.io JSON badge reading from stackoverflow-stats.json -->
  <a href="{so_url}?tab=questions" target="_blank"><img src="https://img.shields.io/badge/dynamic/json?url={quote(so_json, safe='')}&query=%24.question_count&label=Questions&style=for-the-badge&logo=stackoverflow&logoColor=white&color=1E88E5" alt="Stack Overflow Questions"/></a>&nbsp;
  <a href="{so_url}?tab=answers" target="_blank"><img src="https://img.shields.io/badge/dynamic/json?url={quote(so_json, safe='')}&query=%24.answer_count&label=Answers&style=for-the-badge&logo=stackoverflow&logoColor=white&color=43A047" alt="Stack Overflow Answers"/></a>

  <br/>

  <!-- Top Tags — editable via data/profile.json -->
  {top_tags}

</div>
<!-- STACKOVERFLOW_END -->"""


# ═══════════════════════════════════════════════════════════════════════════════
# CONNECT WITH ME  (data/social_links.json)
# ═══════════════════════════════════════════════════════════════════════════════

def build_connect(links):
    badges = "&nbsp;\n  ".join(
        f'<a href="{l["url"]}" target="_blank">'
        f'<img src="https://img.shields.io/badge/{l["label"]}-{l["color"]}'
        f'?style=for-the-badge&logo={l["logo"]}&logoColor={l["logoColor"]}" alt="{l["label"]}"/></a>'
        for l in links
    )
    return f"""<!-- CONNECT_START -->
## <img src="https://media.giphy.com/media/LnQjpWaON8nhr21vNW/giphy.gif" width="25"> &nbsp;Connect with Me

<div align="center">
  {badges}
</div>
<!-- CONNECT_END -->"""


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURED PROJECTS  (data/featured_projects.json)
# ═══════════════════════════════════════════════════════════════════════════════

def build_featured_projects(projects):
    lines = []
    lines.append("<!-- FEATURED_PROJECTS_START -->")
    lines.append("")
    lines.append("## 🚀 &nbsp;Featured Projects")
    lines.append("")
    for p in projects:
        badges   = "&nbsp;".join(make_badge(t, "flat-square") for t in p["techStack"])
        has_demo = p["liveDemoUrl"] not in ("N/A", "", None)
        demo_btn = (
            f'&nbsp;&nbsp;<a href="{p["liveDemoUrl"]}" target="_blank">'
            f'<img src="https://img.shields.io/badge/🌐%20Live%20Demo-FF5722?style=for-the-badge" alt="Live Demo"/></a>'
        ) if has_demo else ""
        lines.append('<table width="100%"><tr><td align="center" width="100%">')
        lines.append("")
        lines.append(f'### [{p["name"]}]({p["gitHubUrl"]})')
        lines.append("")
        lines.append(p["description"])
        lines.append("")
        lines.append(f'<p>{badges}</p>')
        lines.append("")
        lines.append(
            f'<a href="{p["gitHubUrl"]}" target="_blank">'
            f'<img src="https://img.shields.io/badge/📂%20View%20Repo-181717'
            f'?style=for-the-badge&logo=github&logoColor=white" alt="View Repo"/></a>{demo_btn}'
        )
        lines.append("")
        lines.append('</td></tr></table>')
        lines.append("")
        lines.append('<br/>')
        lines.append("")
    lines.append("<!-- FEATURED_PROJECTS_END -->")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# OPEN SOURCE  (data/open_source_projects.json)
# ═══════════════════════════════════════════════════════════════════════════════

def get_host_badge(url):
    if "github.com"     in url: return ('https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white',        "GitHub")
    elif "npmjs.com"    in url: return ('https://img.shields.io/badge/npm-CB3837?style=flat-square&logo=npm&logoColor=white',               "npm")
    elif "rubygems.org" in url: return ('https://img.shields.io/badge/RubyGems-CC342D?style=flat-square&logo=ruby&logoColor=white',         "RubyGems")
    elif "hub.docker.com" in url: return ('https://img.shields.io/badge/Docker%20Hub-2496ED?style=flat-square&logo=docker&logoColor=white', "Docker Hub")
    else:                       return ('https://img.shields.io/badge/View-555555?style=flat-square&logoColor=white',                       "View")

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
        lines.append(f'      <a href="{r["url"]}" target="_blank"><img src="{host_badge}" alt="{host_label}"/></a>')
        lines.append(f'    </td>')
        if (i + 1) % 3 == 0 and i + 1 < len(repos):
            lines.append("  </tr>")
            lines.append("  <tr>")
    lines.append("  </tr>")
    lines.append("</table>")
    lines.append("")
    lines.append("<!-- OPEN_SOURCE_END -->")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# INJECT HELPER
# ═══════════════════════════════════════════════════════════════════════════════

def inject(readme, start_marker, end_marker, new_content):
    pattern = rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
    if re.search(pattern, readme, flags=re.DOTALL):
        return re.sub(pattern, new_content, readme, flags=re.DOTALL)
    return readme


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

with open("data/profile.json")              as f: profile  = json.load(f)
with open("data/tech_stack.json")           as f: tech     = json.load(f)
with open("data/social_links.json")         as f: socials  = json.load(f)
with open("data/featured_projects.json")    as f: projects = json.load(f)
with open("data/open_source_projects.json") as f: oss      = json.load(f)

with open("README.md") as f:
    readme = f.read()

readme = inject(readme, "<!-- HEADER_START -->",            "<!-- HEADER_END -->",            build_header(profile))
readme = inject(readme, "<!-- ABOUT_ME_START -->",          "<!-- ABOUT_ME_END -->",          build_about_me(profile))
readme = inject(readme, "<!-- TECH_STACK_START -->",        "<!-- TECH_STACK_END -->",        build_tech_stack(tech))
readme = inject(readme, "<!-- STACKOVERFLOW_START -->",     "<!-- STACKOVERFLOW_END -->",     build_stackoverflow(profile))
readme = inject(readme, "<!-- CONNECT_START -->",           "<!-- CONNECT_END -->",           build_connect(socials))
readme = inject(readme, "<!-- FEATURED_PROJECTS_START -->", "<!-- FEATURED_PROJECTS_END -->", build_featured_projects(projects))
readme = inject(readme, "<!-- OPEN_SOURCE_START -->",       "<!-- OPEN_SOURCE_END -->",       build_open_source(oss))

with open("README.md", "w") as f:
    f.write(readme)

print("✅ README.md updated successfully.")