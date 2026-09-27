# 泛函｜引力边缘设计体系

本仓库沿用 Victor Design 的目录与执行框架；泛函的品牌判断和已确认样式以以下文件为准：

- [视觉设计体系（文字版 v2）](references/fanhan-brand-system.md)：品牌情绪、排版、字体角色、颜色 token、摄影和四类载体规则。
- [已选标题样式](references/title-styles.md)：D 小标题与 E PPT 标题页的适用场景和颜色。
- [两款可编辑 HTML 参考](assets/html-starters/fanhan-title-styles.html)：D 已加深“去前沿”；E 为 16:9 PPT 版式。

设计物料需要创作或修改文案时，调用 [泛函内容风格 Skill](https://github.com/Ivor-NCUT/fanhan-content-style)；当前环境未安装时，先从该仓库根目录安装。两套规则各自在原仓库维护。

新任务先以这些已确认的品牌材料为依据。下方保留上游 Victor Design 的通用框架说明。

## 上游框架

Victor Design 原项目：[victorzhang016-code/victor-design](https://github.com/victorzhang016-code/victor-design)。本仓库的安装地址应使用 `Ivor-NCUT/fanhan-design`；下方原项目安装示例仅用于说明来源。

# Victor Design

Victor Design is a human-centered visual design workflow for AI agents. It understands the subject and the task first, then chooses the form, content, and visual language before delivering work that can be reviewed and edited.

In a recorded four-track evaluation, it outperformed most of seven world-class design skills and received a first-place public-vote finish.

## Use it for

- Posters and key visuals
- Social media graphics
- Product UI
- Presentations and decks

## What makes it different

1. **Form before styling** — A design brief is classified before production: one poster, a graphic set, a multi-state UI flow, or a presentation.
2. **Real material first** — Workspace material and project facts come before generation. Generated images are approved supplemental material, never a substitute for authored structure.
3. **A complete production and review chain** — Layout constraints, three hard delivery gates, and visual review keep the output accountable. Built-in guardrails also reject generic AI visual and copy patterns.
4. **Editable delivery** — Posters and graphic sets ship as editable Figma frames by default; product UI keeps its HTML interaction flow.
5. **HTML to Figma** — The companion DOM Migrate v3 plugin converts Victor Design's controlled UI HTML into editable Figma Frames, Auto Layout, Grid, Text, Image, components, and valid Hug / Fill / Fixed sizing. Complex CSS effects are rasterized only at the smallest necessary layer while the main structure stays editable.

DOM Migrate v3 is designed for controlled Victor Design UI HTML. It does not promise lossless migration for arbitrary websites.

## Install

```bash
git clone https://github.com/victorzhang016-code/victor-design.git ~/.agents/skills/victor-design
```

Windows PowerShell:

```powershell
git clone https://github.com/victorzhang016-code/victor-design.git "$HOME\.agents\skills\victor-design"
```

The entry point is `SKILL.md`. MIT License.

## First run

The skill ships with the author's default style evidence, so it has a real
voice immediately. If you have approved work of your own, open
`references/style-evidence.md` and replace the default base with evidence
from your own finished pieces — the "Make it yours" section walks through
it. Teams adopting the system should treat this swap as onboarding step one,
not an advanced option.

## SkillHub release

The repository includes development and test files. Prepare a clean SkillHub source directory first:

```bash
python scripts/prepare_skillhub_release.py --output /tmp/victor-design-skillhub
```

Then pass that directory to `redskillhub-upload` for dry-run, review, and submission.
