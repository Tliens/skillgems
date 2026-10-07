#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkillGems catalog — single source of truth.
Every entry below was verified via the GitHub API on VERIFIED_DATE
(full_name + stargazers_count + description fetched live; 404s dropped).
Adds/moves stars daily -> rerun:  python3 scripts/gen_cards.py
Regenerates (do NOT hand-edit these regions in index.html):
  - static cards        <!--CARDS:START/END-->
  - JSON data island    /*DATA:START*/ ... /*DATA:END*/
  - stats               <!--STATS:START/END-->
  - ItemList JSON-LD    <!--JSONLDLIST:START/END-->
  - data/catalog.json, llms.txt
Also rewrites the entry/category counts inside the hero stats and dirSub copy.
"""

import json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
SITE = "https://skillgems.kuige.me"
VERIFIED = "2026-10-07"
CATS = ["official","collections","dev","writing","design","science","security","business","toolbox"]

def S(id, n, a, repo, st, c, de, dz, h, hz, t, f=False, xh=None):
    return {"id": id, "n": n, "a": a, "u": "https://github.com/" + repo, "st": st, "c": c,
            "de": de, "dz": dz, "h": h, "hz": hz, "t": t, "f": f, "xh": xh, "x": None}

SKILLS = [
S("anthropic-skills","Anthropic Skills","anthropics","anthropics/skills",179993,"official",
  "The official Anthropic skills repo: document powerhouses (docx, pptx, xlsx, pdf), skill-creator for authoring your own, mcp-builder, frontend-design, web-artifacts-builder, canvas-design and more — installable as a plugin marketplace.",
  "Anthropic 官方技能仓库：文档四件套（Word/PPT/Excel/PDF）、自己写技能用的 skill-creator、mcp-builder、frontend-design、web-artifacts-builder、canvas-design 等，可作为插件市场一键安装。",
  "Install via the Claude Code plugin marketplace (anthropics/skills), or copy any skill folder into your skills directory.",
  "用 Claude Code 插件市场安装（anthropics/skills），或把任意技能文件夹复制进你的技能目录。",
  "docx pptx xlsx pdf skill-creator mcp-builder frontend-design official 官方 文档",f=True,xh=None),

S("superpowers","Superpowers","obra · Jesse Vincent","obra/superpowers",296190,"dev",
  "Jesse Vincent's agentic skills framework and software development methodology: TDD, debugging, planning and collaboration skills that turn Claude Code into a disciplined engineer. The project that kicked off the skills boom.",
  "Jesse Vincent 的智能体技能框架与软件开发方法论：TDD、调试、计划、协作等技能，把 Claude Code 变成守纪律的工程师——引爆整个技能生态的项目。",
  "Install as a Claude Code plugin from its marketplace (see README).",
  "作为 Claude Code 插件从其市场安装（见 README）。",
  "tdd debugging planning methodology framework 工程化 方法论",f=True,xh="obra"),

S("agent-reach","Agent-Reach","Panniantong","Panniantong/Agent-Reach",92933,"dev",
  "Give your agent eyes on the whole internet: read and search Twitter/X, Reddit, YouTube, GitHub, Bilibili and more from one skill, with content delivered in a form agents can reason over.",
  "让你的智能体看见整个互联网：一个技能打通 Twitter/X、Reddit、YouTube、GitHub、B站等平台的读取与搜索，把内容变成智能体能推理的形态。",
  "Follow the repo setup to connect platform credentials, then ask your agent to read or search any supported site.",
  "按仓库说明配置各平台凭据，然后直接让智能体去读或搜索目标平台。",
  "twitter reddit youtube bilibili search research 检索 资讯",f=True,xh=None),

S("graphify","Graphify","Graphify-Labs","Graphify-Labs/graphify",124530,"dev",
  "Turn any codebase — docs, SQL schemas, configs, PDFs — into a queryable knowledge graph via a /graphify skill, so agents can navigate large systems instead of guessing.",
  "用 /graphify 技能把任意代码库（文档、SQL schema、配置、PDF）变成可查询的知识图谱，让智能体真正看懂大型系统而不是靠猜。",
  "Install the /graphify skill, point it at a repository and query the generated graph.",
  "安装 /graphify 技能，指向代码库即可生成并查询知识图谱。",
  "knowledge graph codebase architecture 知识图谱 代码库",f=True,xh=None),

S("archify","Archify","tt-a1i","tt-a1i/archify",78955,"dev",
  "Turn any idea, plan or codebase into beautiful interactive diagrams. An agent skill for Claude Code, Codex and beyond — great for architecture docs and READMEs.",
  "把任何想法、计划或代码库变成精美的交互式图表——面向 Claude Code、Codex 等的智能体技能，写架构文档和 README 的利器。",
  "Copy the skill folder into your skills directory and ask your agent to archify a plan or repo.",
  "把技能文件夹复制进技能目录，让智能体 archify 你的计划或代码库。",
  "diagram visualization architecture 图表 可视化 架构图",f=True,xh=None),

S("awesome-claude-skills","Awesome Claude Skills","ComposioHQ","ComposioHQ/awesome-claude-skills",76641,"collections",
  "One of the largest curated lists of Claude skills, resources and tools — the fastest way to survey the whole ecosystem from one README.",
  "规模最大的 Claude 技能精选列表之一：技能、资源、工具一站看全，是从一份 README 通览整个生态的最快方式。",
  "Browse the README and jump into any listed skill repo.",
  "浏览 README，点进任意技能仓库。",
  "awesome list curated 合集 导航",f=True,xh=None),

S("marketing-skills","Marketing Skills","coreyhaines31","coreyhaines31/marketingskills",53533,"business",
  "Marketing skills for Claude Code and AI agents: CRO, copywriting, SEO, analytics and growth engineering — a full growth team in skill form.",
  "面向 Claude Code 与 AI 智能体的营销技能包：CRO、文案、SEO、数据分析、增长工程——一套技能顶一个增长团队。",
  "Copy the skill folders you need into your skills directory.",
  "把需要的技能文件夹复制进技能目录。",
  "marketing cro copywriting seo growth 营销 增长 文案",f=True,xh=None),

S("academic-research","Academic Research Skills","Imbad0202","Imbad0202/academic-research-skills",50736,"science",
  "Academic research skills for Claude Code covering the full loop: research → write → review → revise → finalize. Built for literature-heavy, citation-disciplined work.",
  "覆盖学术研究全流程的 Claude Code 技能：检索 → 写作 → 评审 → 修改 → 定稿，为重文献、守引用规范的研究而生。",
  "Copy the skills into ~/.claude/skills/ and ask your agent to run the research pipeline.",
  "把技能复制进 ~/.claude/skills/，让智能体按流程跑研究管线。",
  "academic research paper thesis 学术 论文 文献",f=True,xh=None),

S("scientific-agent-skills","Scientific Agent Skills","K-Dense-AI","K-Dense-AI/scientific-agent-skills",47847,"science",
  "Turn any AI agent into an AI scientist: the top skills library for science — literature review, bioinformatics, analysis pipelines — used by 250,000+ researchers.",
  "把任意智能体变成 AI 科学家：科学领域第一大技能库，覆盖文献综述、生物信息、分析管线，超过 25 万科研人员在用。",
  "Install the collection and invoke domain skills (e.g. literature review, protein analysis) per task.",
  "安装合集后按任务调用领域技能（文献综述、蛋白分析等）。",
  "science bioinformatics literature research 科学 科研 生物信息",f=True,xh=None),

S("cybersecurity-skills","Cybersecurity Skill Pack","mukul975","mukul975/Anthropic-Cybersecurity-Skills",33882,"security",
  "817 structured cybersecurity skills for AI agents, mapped to 6 frameworks including MITRE ATT&CK and NIST CSF 2.0 — defensive coverage you can audit.",
  "817 个结构化网络安全技能，映射到 MITRE ATT&CK、NIST CSF 2.0 等 6 大框架——可审计的防御知识库。",
  "Copy the framework-aligned skill folders you need into your skills directory.",
  "把所需框架对应的技能文件夹复制进技能目录。",
  "cybersecurity mitre nist defense 网络安全 防御 红线蓝队",xh=None),

S("book-to-skill","Book to Skill","virgiliojr94","virgiliojr94/book-to-skill",34020,"toolbox",
  "Turn any technical book PDF into a Claude Code skill — ready to study, reference and use while you work. Books stop gathering dust.",
  "把任何技术书 PDF 变成 Claude Code 技能——边工作边随时调用、随时查阅，让买过的书不再吃灰。",
  "Feed it a book PDF; it generates a study-ready skill folder.",
  "喂给它一本书的 PDF，自动生成可学习的技能文件夹。",
  "book pdf learning study 读书 学习 转技能",xh=None),

S("hallmark","Hallmark","Nutlope","Nutlope/hallmark",29711,"design",
  "An anti-AI-slop design skill for Claude Code, Cursor and Codex: opinionated design taste so generated UI stops looking generated.",
  "面向 Claude Code、Cursor、Codex 的反 AI 味设计技能：内置主见的设计品味，让生成的 UI 不再一眼假。",
  "Add the skill to your agent's skills directory; design rules apply to every UI task.",
  "把技能加入智能体技能目录，之后所有 UI 任务自动带上设计规则。",
  "design ui taste anti-slop 设计 审美",f=True,xh=None),

S("cloudflare-security-audit","Cloudflare Security Audit","cloudflare","cloudflare/security-audit-skill",25591,"official",
  "Cloudflare's official coding-agent skill for multi-phase security audits, with independently verified, machine-readable findings.",
  "Cloudflare 官方的编码智能体安全审计技能：多阶段审计，产出可独立验证、机器可读的结果。",
  "Install the skill, then ask your agent to audit a repo or diff.",
  "安装技能后，让智能体对仓库或 diff 做安全审计。",
  "security audit vulnerability 安全 审计 漏洞",xh=None),

S("game-studios","Claude Code Game Studios","Donchitos","Donchitos/Claude-Code-Game-Studios",25844,"dev",
  "Turn Claude Code into a full game dev studio: 49 AI agents, 72 workflow skills and a complete coordination system for shipping games.",
  "把 Claude Code 变成完整的游戏工作室：49 个 AI 智能体、72 个工作流技能和一整套协作调度系统。",
  "Install the collection and assign studio roles (design, code, art, QA) to your agent.",
  "安装合集后，给智能体分配工作室角色（策划/程序/美术/QA）。",
  "game dev unity godot studio 游戏 开发 工作室",xh=None),

S("planning-with-files","Planning with Files","OthmanAdi","OthmanAdi/planning-with-files",27315,"dev",
  "Persistent file-based planning for AI coding agents: crash-proof markdown plans, session memory and long-running task state that survives restarts.",
  "面向 AI 编码智能体的持久化文件规划：防崩溃的 markdown 计划、会话记忆与长任务状态，重启也不丢。",
  "Copy into your skills directory; plans live in markdown files next to your code.",
  "复制进技能目录；计划以 markdown 文件形式与代码同库存放。",
  "planning tasks memory plan 计划 任务管理",xh=None),

S("claude-skills-pack","Claude Skills Mega-Pack","alirezarezvani","alirezarezvani/claude-skills",27800,"collections",
  "A mega-pack of 380 Claude Code skills plus 30+ agents and 70+ custom commands — breadth first, ideal for assembling your own toolkit.",
  "380 个 Claude Code 技能 + 30 多个 agent + 70 多个自定义命令的超大合集——广度优先，适合自己攒工具箱。",
  "Browse categories and copy the skills you want into your skills directory.",
  "按分类浏览，把想要的技能复制进技能目录。",
  "mega pack collection 大合集 插件",xh=None),

S("huashu-design","Huashu Design","alchaincyf · 花叔","alchaincyf/huashu-design",24641,"design",
  "Huashu's HTML-native design skill for Claude Code: high-fidelity prototypes, slides and animation pages generated as pure HTML — a community favorite for beautiful output.",
  "花叔的 Claude Code HTML 原生设计技能：高保真原型、幻灯片、动效页直接产出纯 HTML——社区公认的高颜值输出。",
  "Copy into ~/.claude/skills/ and ask for prototypes, slides or poster pages in HTML.",
  "复制进 ~/.claude/skills/，直接要求产出 HTML 原型、幻灯片或海报页。",
  "design html prototype slides 设计 原型 幻灯片 高颜值",f=True,xh="alchaincyf"),

S("khazix-skills","Khazix Skills","KKKKhazix · 数字生命卡兹克","KKKKhazix/khazix-skills",21215,"collections",
  "Khazix's open-source AI skills collection: leader (goal definition), neat-freak, hv-analysis, khazix-writer and more — practical Chinese-community favorites.",
  "数字生命卡兹克开源的 AI 技能合集：leader（帮你定义目标）、neat-freak 洁癖、hv-analysis、khazix-writer 等，中文圈实测好用的口碑之作。",
  "Copy the skills you want into your skills directory (README in Chinese).",
  "把想要的技能复制进技能目录（README 为中文）。",
  "collection chinese writer analysis 合集 中文 写作",xh=None),

S("notebooklm-py","NotebookLM Py","teng-lin","teng-lin/notebooklm-py",19634,"toolbox",
  "Unofficial Python API and agentic skill for Google NotebookLM: full programmatic access to notebooks, sources and generated content.",
  "Google NotebookLM 的非官方 Python API 与智能体技能：笔记本、来源与生成内容全量可编程操控。",
  "pip install the package, then use the bundled agent skill to drive NotebookLM.",
  "pip 安装后，用附带的智能体技能驱动 NotebookLM。",
  "notebooklm google api python",xh=None),

S("skillspector","SkillSpector","NVIDIA","NVIDIA/SkillSpector",19604,"security",
  "NVIDIA's security scanner for AI agent skills: detects vulnerabilities, malicious patterns, prompt injection and risky code before you install a SKILL.md.",
  "NVIDIA 出品的技能安全扫描器：在安装任何 SKILL.md 之前，检出漏洞、恶意模式、提示词注入与危险代码。",
  "Run SkillSpector against any skill folder or collection before installing it.",
  "安装前对任意技能文件夹或合集跑一遍 SkillSpector。",
  "security scanner audit safety 安全 扫描 审计",xh=None),

S("humanizer-zh","Humanizer-zh","op7418 · 歸藏","op7418/Humanizer-zh",19042,"writing",
  "Guizang's Chinese edition of Humanizer, the Claude Code skill that strips AI-generated traces from text — rhythm, vocabulary and structure all de-slopped.",
  "歸藏汉化的 Humanizer：Claude Code 技能，专治文本里的 AI 味——从节奏、用词到结构逐层去机器感。",
  "Copy into ~/.claude/skills/, then ask your agent to humanize a draft.",
  "复制进 ~/.claude/skills/，让智能体 humanize 你的稿子。",
  "humanizer chinese writing de-ai 去AI味 中文 写作 润色",xh="op7418"),

S("claude-seo","Claude SEO","AgriciDaniel","AgriciDaniel/claude-seo",18459,"business",
  "Universal SEO skill for Claude Code: 26 sub-skills and 19 sub-agents covering technical SEO, E-E-A-T, schema and content optimization.",
  "通用 SEO 技能：26 个子技能 + 19 个子 agent，覆盖技术 SEO、E-E-A-T、结构化数据与内容优化。",
  "Install the skill pack and ask for audits, keyword plans or schema markup.",
  "安装技能包后，直接要求站点审计、关键词规划或 schema 标记。",
  "seo schema eeat keywords 搜索优化 关键词",xh=None),

S("skillopt","SkillOpt","microsoft · MSR","microsoft/SkillOpt",18095,"toolbox",
  "Microsoft Research's text-space optimizer that trains reusable natural-language skills for frozen LLM agents — the science of making skills better.",
  "微软研究院的文本空间优化器：为冻结参数的 LLM 智能体训练可复用的自然语言技能——把「技能怎么变强」变成科学。",
  "Research toolkit: clone, prepare your task set and optimize skills per the repo guide.",
  "研究工具箱：克隆仓库，按指南准备任务集并优化技能。",
  "optimization research training 优化 训练 研究",xh=None),

S("aris-research","ARIS Research","wanshuiyin","wanshuiyin/Auto-claude-code-research-in-sleep",17076,"science",
  "ARIS (Auto-Research-In-Sleep): markdown-only skills for autonomous ML research — cross-model review and experiment loops that run while you sleep.",
  "ARIS（睡着也能做科研）：纯 markdown 的自主科研技能——跨模型评审与实验循环，睡前挂机、醒来看结果。",
  "Install the ARIS skills and launch an overnight research loop.",
  "安装 ARIS 技能后，启动过夜科研循环。",
  "autonomous ml research experiment 自动 科研 实验",xh=None),

S("awesome-claude-skills-travis","Awesome Claude Skills · travisvn","travisvn","travisvn/awesome-claude-skills",15301,"collections",
  "A well-maintained curated list of awesome Claude skills, resources and tools with clear category navigation.",
  "维护良好的 Claude 技能精选列表：分类清晰、收录讲究的技能/资源/工具导航。",
  "Browse the README by category and follow links out to each skill.",
  "按分类浏览 README，点进具体技能。",
  "awesome list curated 合集 导航",xh=None),

S("skill-seekers","Skill Seekers","yusufkaraaslan","yusufkaraaslan/Skill_Seekers",15111,"toolbox",
  "Convert documentation sites, GitHub repos and PDFs into Claude-ready skills automatically, with conflict detection when merging sources.",
  "把文档站、GitHub 仓库和 PDF 自动转成 Claude 技能，合并多来源时还能自动检测冲突。",
  "Run the converter against a docs URL, repo or PDF to emit a skill folder.",
  "对文档 URL、仓库或 PDF 跑转换脚本，产出技能文件夹。",
  "converter docs pdf scrape 转换 文档 抓取",xh=None),

S("prompt-master","Prompt Master","nidhinjs","nidhinjs/prompt-master",14134,"writing",
  "A skill that writes accurate prompts for any AI tool — full context assembly with zero tokens wasted on guesswork.",
  "帮任何 AI 工具写准提示词的技能：完整上下文组装，不浪费一个 token 在瞎猜上。",
  "Install the skill and ask it to draft or fix a prompt.",
  "安装技能后，让它起草或修复你的提示词。",
  "prompt engineering 提示词 工程",xh=None),

S("ai-guide","AI Guide · 程序员鱼皮","liyupi","liyupi/ai-guide",20773,"collections",
  "Yupi's AI resource compendium plus zero-basics vibe coding tutorials: model playbooks, OpenClaw walkthroughs and skills guidance for Chinese developers.",
  "程序员鱼皮的 AI 资源大全 + Vibe Coding 零基础教程：大模型玩法、OpenClaw 保姆级教程与技能使用指南，中文开发者友好。",
  "Read the guide; follow its curated links into tools and skills.",
  "直接阅读指南，按其精选链接进入各工具与技能。",
  "tutorial chinese guide resources 教程 资源 中文",xh=None),

S("microsoft-skills","Microsoft Skills","microsoft","microsoft/skills",3088,"official",
  "Microsoft's official skills, MCP servers, custom agents and AGENTS.md templates for grounding coding agents across their SDKs and developer stack.",
  "微软官方出品：技能、MCP 服务器、自定义 agent 与 AGENTS.md 模板，为其 SDK 与开发者工具链的编码智能体提供接地能力。",
  "Browse the catalog and follow per-skill install instructions.",
  "浏览目录，按各技能说明安装。",
  "mcp agents templates microsoft 微软 官方",xh=None),

S("swiftui-expert","SwiftUI Expert Skill","AvdLee","AvdLee/SwiftUI-Agent-Skill",3665,"dev",
  "Expert SwiftUI best-practices guidance in the open Agent Skills format — keeping generated Swift code production-grade.",
  "以开放 Agent Skills 格式提供的 SwiftUI 专家级最佳实践——让生成的 Swift 代码达到生产级水准。",
  "Copy the swiftui-expert-skill folder into your agent's skills directory.",
  "把 swiftui-expert-skill 文件夹复制进智能体技能目录。",
  "swiftui ios swift mobile 苹果 移动开发",xh=None),

S("awesome-design-skills","Awesome Design Skills","bergside","bergside/awesome-design-skills",3071,"design",
  "67 curated DESIGN.md and SKILL.md design files for agentic tools — aesthetic families you can mix into any UI project.",
  "67 个精选 DESIGN.md / SKILL.md 设计文件——按美学族系归类，可混搭进任何 UI 项目。",
  "Pick a design file and drop it into your project as a skill or design context.",
  "挑一个设计文件，作为技能或设计上下文放进项目。",
  "design aesthetics ui 设计 美学 风格",xh=None),

S("sepia","Sepia","Nanako0129","Nanako0129/sepia",3009,"writing",
  "De-AI writing skill compatible with 77+ Agent Skills agents (native plugins for Claude and more): repairs narrative structure and humanizes prose.",
  "兼容 77+ 智能体的去 AI 味写作技能（Claude 等有原生插件）：修复叙事结构，让文字读起来像人写的。",
  "Install via its CLI or copy the skill folder; works across many agents.",
  "用其 CLI 安装或直接复制技能文件夹，多智能体通用。",
  "writing fiction prose de-ai 写作 小说 文学 去AI味",xh=None),

S("angular-skills","Angular Skills","angular","angular/skills",670,"official",
  "The Angular team's official agent skills — framework-accurate guidance for building and modernizing Angular apps with coding agents.",
  "Angular 团队官方智能体技能——用编码智能体开发/升级 Angular 应用时，给出与框架精确对齐的指导。",
  "Follow the repo instructions to add angular-developer and angular-new-app skills.",
  "按仓库说明安装 angular-developer 与 angular-new-app 技能。",
  "angular frontend web 前端 官方",xh=None),

S("frontend-toolkit","Frontend Design Toolkit","wilwaldon","wilwaldon/Claude-Code-Frontend-Design-Toolkit",1173,"design",
  "A battle-tested bundle of skills, plugins and MCP servers that measurably improve Claude Code's frontend output.",
  "经过实战检验的技能/插件/MCP 组合包，实打实提升 Claude Code 的前端产出质量。",
  "Install components à la carte per the README.",
  "按 README 挑选需要的组件安装。",
  "frontend design toolkit 前端 设计 工具箱",xh=None),

S("awesome-claude-design","Awesome Claude Design","rohitg00","rohitg00/awesome-claude-design",1123,"design",
  "DESIGN.md prompt packs organized by aesthetic family, plus remix recipes, skills and video teardowns for design-minded agent work.",
  "按美学族系组织的 DESIGN.md 提示词包，附混搭配方、技能与视频拆解，面向有设计追求的智能体工作流。",
  "Copy a DESIGN.md aesthetic into your project or install the accompanying skills.",
  "把心仪的 DESIGN.md 美学复制进项目，或安装随附技能。",
  "design aesthetics prompts 设计 美学 风格",xh=None),

S("gamedev-skills","Gamedev Agent Skills","gamedev-skills","gamedev-skills/awesome-gamedev-agent-skills",1348,"dev",
  "74 game-dev skills for AI coding agents: Godot, Unity, Unreal, Phaser, PixiJS, three.js, Bevy, pygame, LÖVE and more.",
  "74 个游戏开发技能：Godot、Unity、Unreal、Phaser、PixiJS、three.js、Bevy、pygame、LÖVE 等引擎全覆盖。",
  "Copy the engine-specific skills you need into your skills directory.",
  "把对应引擎的技能复制进技能目录。",
  "godot unity unreal phaser threejs 游戏引擎 游戏开发",xh=None),

S("self-learning","Self-Learning Skills","Kulaxyz","Kulaxyz/self-learning-skills",960,"dev",
  "A self-improving skill: recognize hard-won golden paths while coding and persist them as reusable skills for the next run.",
  "会自我进化的技能：编码中识别来之不易的黄金路径，沉淀成可复用技能，越用越顺手。",
  "Install the skill; it captures lessons automatically as you work.",
  "安装后它会随你的工作自动沉淀经验。",
  "self-improving memory learning 自我进化 记忆 学习",xh=None),

S("video-spec-builder","Video Spec Builder","feicaiclub","feicaiclub/video-spec-builder",1015,"dev",
  "Turns 'I want a video' into a second-precise storyboard spec (video-spec.md) for HyperFrames to render — one command installs it into Claude Code / Cursor / Codex.",
  "把「我想做个视频」逼成精确到秒的分镜脚本 video-spec.md，交给 HyperFrames 渲染——一条命令装进 Claude Code / Cursor / Codex。",
  "One-line install command from the README, then describe the video you want.",
  "README 里一行命令安装，然后直接描述你想要的视频。",
  "video storyboard spec 视频 分镜 脚本",xh=None),

S("huashu-md-html","Huashu md↔html","alchaincyf · 花叔","alchaincyf/huashu-md-html",908,"writing",
  "Huashu's bidirectional md/html pipeline: anything → markdown, markdown → beautiful HTML, HTML → markdown — wrapping markitdown, Pandoc and html-to-markdown.",
  "花叔的 md/html 双向流水线：万物→md、md→精美 HTML、HTML→md 一站式，封装 markitdown、Pandoc 与 html-to-markdown。",
  "Install the skill and ask for format conversions in conversation.",
  "安装技能后，对话里直接要求格式转换。",
  "markdown html convert pandoc 转换 排版",xh="alchaincyf"),

S("lambdatest-agent-skills","LambdaTest Agent Skills","LambdaTest","LambdaTest/agent-skills",377,"official",
  "LambdaTest's official collection of 50+ testing skills: Playwright, Selenium, Cypress, Appium, pytest, Jest and more, wired to their cloud test platform.",
  "LambdaTest 官方 50+ 测试技能合集：Playwright、Selenium、Cypress、Appium、pytest、Jest 等，直连其云测试平台。",
  "Pick framework skills from the repo and follow per-skill setup.",
  "从仓库挑选框架技能，按各自说明接入。",
  "testing playwright selenium cypress 测试 自动化",xh=None),

S("courier-notifications","Courier Notifications","trycourier","trycourier/courier-skills",14,"official",
  "Courier's official skill for building production-ready notifications across email, SMS, push, in-app, Slack and Teams.",
  "Courier 官方技能：构建覆盖邮件、短信、推送、应用内、Slack 与 Teams 的生产级通知系统。",
  "Install the skill and describe the notification flow you need.",
  "安装技能后，直接描述你要的通知流程。",
  "notifications email push slack 通知 邮件 推送",xh=None),

S("charlie-cfo","Charlie CFO Skill","EveryInc","EveryInc/charlie-cfo-skill",324,"business",
  "A Claude Code skill for bootstrapped CFO work — financial modeling, runway and unit economics discipline, named after Charlie Munger.",
  "面向精益创业的 CFO 技能：财务建模、现金流跑道与单位经济性纪律，以 Charlie Munger 命名。",
  "Copy into your skills directory and ask CFO questions with your numbers.",
  "复制进技能目录，带上你的数据直接问财务问题。",
  "cfo finance startup runway 财务 创业 现金流",xh=None),
]

# ---------- derived ----------
def fmt_k(n):
    if n >= 1e6: return ("%.2f" % (n/1e6)).rstrip("0").rstrip(".") + "M"
    if n >= 1000: return ("%.1f" % (n/1e3)).rstrip("0").rstrip(".") + "k"
    return str(n)

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def assert_sub(html, pat, label):
    if not re.search(pat, html):
        raise SystemExit("PATTERN MISSING (%s): %r" % (label, pat[:80]))

def build_card(s):
    cls = " feat" if s["f"] else ""
    feat = '<span class="c-feat" title="Featured">★</span>' if s["f"] else ""
    xchip = ""
    if s["xh"]:
        xchip = ' <a class="xchip" href="https://x.com/%s" target="_blank" rel="noopener" title="https://x.com/%s">𝕏 @%s</a>' % (s["xh"], s["xh"], s["xh"])
    stars = "{:,}".format(s["st"])
    return f'''<article class="card{cls}" data-id="{s["id"]}">
  <div class="c-top"><h3>{esc(s["n"])}{feat}</h3><span class="c-cat" data-cat="{s["c"]}"></span></div>
  <p class="c-desc" data-zh="{esc(s["dz"])}">{esc(s["de"])}</p>
  <p class="c-how"><b>⚙</b> <span data-zh="{esc(s["hz"])}">{esc(s["h"])}</span></p>
  <div class="c-meta"><span>{esc(s["a"])}</span>{xchip}<span class="stars" title="{stars}">★ {fmt_k(s["st"])}</span></div>
  <div class="c-actions"><a class="btn pri" href="{s["u"]}" target="_blank" rel="noopener">⭐ <span class="gh-t">GitHub</span> ↗</a></div>
</article>'''

def main():
    total = sum(s["st"] for s in SKILLS)
    n = len(SKILLS)
    ncats = len({s["c"] for s in SKILLS})
    ordered = sorted(SKILLS, key=lambda s: (not s["f"], -s["st"]))

    html = open(INDEX, encoding="utf-8").read()

    # cards
    m = re.search(r"(<!--CARDS:START-->)(.*?)(<!--CARDS:END-->)", html, re.S)
    assert m, "CARDS markers missing"
    html = html[:m.start(2)] + "\n" + "\n".join(build_card(s) for s in ordered) + "\n" + html[m.end(2):]

    # data island (content only — the object braces live outside the markers in index.html)
    payload = json.dumps({"d": VERIFIED, "s": [{k: s[k] for k in ("id","n","a","u","st","c","de","dz","h","hz","t","f","xh","x")} for s in SKILLS]}, ensure_ascii=False, separators=(",",":")).replace("</", "<\\/")
    payload = payload[1:-1]
    m = re.search(r"(/\*DATA:START\*/)(.*?)(/\*DATA:END\*/)", html, re.S)
    assert m, "DATA markers missing"
    html = html[:m.start(2)] + payload + html[m.end(2):]

    # stats
    m = re.search(r"(<!--STATS:START-->)(.*?)(<!--STATS:END-->)", html, re.S)
    assert m, "STATS markers missing"
    stats = ('<div class="stats">\n'
             f'      <div class="stat"><b id="stSkills">{n}</b><span data-i18n="statSkills">Skills &amp; collections</span></div>\n'
             f'      <div class="stat"><b id="stCats">{ncats}</b><span data-i18n="statCats">Categories</span></div>\n'
             f'      <div class="stat"><b id="stStars">{fmt_k(total)}</b><span data-i18n="statStars">Combined GitHub stars</span></div>\n'
             f'      <div class="stat"><b id="stDate">{VERIFIED}</b><span data-i18n="statVerified">Links verified</span></div>\n'
             '    </div>')
    html = html[:m.start(2)] + stats + html[m.end(2):]

    # counts inside copy (prefill + dictionaries)
    for pat, rep in [
        (r"42 entries across 9 categories", f"{n} entries across {ncats} categories"),
        (r"42 个条目、9 个分类", f"{n} 个条目、{ncats} 个分类"),
        (r'<b id="cnt">42</b>', f'<b id="cnt">{n}</b>'),
        (r'<b id="cntAll">42</b>', f'<b id="cntAll">{n}</b>'),
    ]:
        assert_sub(html, pat, pat[:30])
        html = re.sub(pat, rep, html)

    # ItemList JSON-LD
    items = [{"@type":"ListItem","position":i+1,"name":s["n"],"url":s["u"]} for i, s in enumerate(ordered)]
    ld = json.dumps({"@context":"https://schema.org","@type":"ItemList","name":"SkillGems catalog",
                     "numberOfItems":n,"itemListElement":items}, ensure_ascii=False)
    m = re.search(r"(<!--JSONLDLIST:START-->)(.*?)(<!--JSONLDLIST:END-->)", html, re.S)
    assert m, "JSONLD markers missing"
    html = html[:m.start(2)] + '\n<script type="application/ld+json">\n' + ld + "\n</script>\n" + html[m.end(2):]

    open(INDEX, "w", encoding="utf-8").write(html)

    # machine-readable catalog for AI agents
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    catalog = {
        "site": SITE, "generated": datetime.date.today().isoformat(), "verified": VERIFIED,
        "count": n, "total_stars": total,
        "skills": [{"id": s["id"], "name": s["n"], "author": s["a"], "url": s["u"], "stars": s["st"],
                    "category": s["c"], "description_en": s["de"], "description_zh": s["dz"],
                    "how_en": s["h"], "how_zh": s["hz"], "tags": s["t"].split(),
                    "featured": s["f"],
                    **({"x_profile": "https://x.com/" + s["xh"]} if s["xh"] else {}),
                    **({"x_post": s["x"]} if s.get("x") else {})} for s in SKILLS]}
    with open(os.path.join(ROOT, "data", "catalog.json"), "w", encoding="utf-8") as fp:
        json.dump(catalog, fp, ensure_ascii=False, indent=1)

    # llms.txt (llmstxt.org style)
    L = [f"# SkillGems", "",
         f"> Curated, link-verified directory of {n} AI agent skills (SKILL.md format): official releases from Anthropic, Microsoft, Cloudflare, Angular, LambdaTest plus the strongest community collections. Every link verified {VERIFIED}. Agents: fetch {SITE}/data/catalog.json for the full machine-readable catalog.", "",
         "## Quick start for agents", "",
         f"1. Fetch {SITE}/data/catalog.json (JSON: id, name, author, url, stars, category, bilingual descriptions, install hints).",
         "2. Filter by `category` (official/collections/dev/writing/design/science/security/business/toolbox) or search `tags`.",
         "3. Open the entry's GitHub `url` and follow its README for the exact install path (default: copy the skill folder to `~/.claude/skills/`).",
         "4. Treat skills as code: review contents and license before installing.", ""]
    for c in CATS:
        entries = [s for s in SKILLS if s["c"] == c]
        if not entries: continue
        L.append(f"## {c.capitalize()} ({len(entries)})")
        L.append("")
        for s in sorted(entries, key=lambda x: -x["st"]):
            L.append(f"- [{s['n']}]({s['u']}): {s['de']} (★{fmt_k(s['st'])})")
        L.append("")
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(L))

    print(f"OK: {n} skills, {ncats} cats, total stars {total:,} ({fmt_k(total)}) -> index.html, data/catalog.json, llms.txt")

if __name__ == "__main__":
    main()
