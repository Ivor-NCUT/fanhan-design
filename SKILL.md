---
name: fanhan-design-style
description: 泛函的跨载体视觉设计 Skill。按任务选择「洛言」横屏/竖屏视觉或「泛函个人网站设计」历史方法，再使用证据驱动的设计与交付框架制作可编辑物料。
---

# 泛函设计风格

## 跨仓 Context OS

本仓库只负责“怎么呈现”。设计中涉及泛函当前事实时，按 [`context-os.json`](context-os.json) 找到私有 `Ivor-NCUT/all-about-fanhan`，只读取相关且已核实的事实；公开物料只能使用该仓 `public/` 中再次核实的信息。读不到私有仓时使用用户给出的本次事实，不从旧样板推断当前业务状态。需要新写或改写文案时按清单调用 `Ivor-NCUT/fanhan-content-style`；用户定稿可直接排版。跨仓隐私与写回边界见 [`AGENTS.md`](AGENTS.md)。

首次读取本 Skill 时，先运行 `python3 scripts/sync_from_github.py`。它用 `gh api` 对照 [Ivor-NCUT/fanhan-design](https://github.com/Ivor-NCUT/fanhan-design) 的默认分支和本地文件；有差异时先备份并更新，再重新读取本文件。以后每次调用也执行此检查。迭代完成并验证后，把本 Skill 的实际改动同步到该仓库，回读远端文件和提交；公开前检查私有图片、账号资料和授权。

## 风格选择

- **洛言**：职业服务、演示和长图需要暖白、深绿、阿里妈妈东方大楷、真实证据与黑绿价格场时，读取 [`styles/洛言/SKILL.md`](styles/洛言/SKILL.md)。横屏和竖屏分别重排；公开示例的私密图片已换成占位素材。
- **泛函个人网站设计**：用户提到个人网站视觉、网页源码分析或原版 `fanhan-design-style` 时，读取 [`styles/泛函个人网站设计/SKILL.md`](styles/泛函个人网站设计/SKILL.md)。该目录完整保留旧 Skill 的参考资料和文案检查脚本。
- 其他泛函视觉任务先读 `references/fanhan-brand-system.md`，再按下方执行框架选择对应载体。不得把任一具名风格当成所有任务的默认皮肤。

## 设计与交付框架

以下通用方法沿用 Victor Design，并由用户当前目标、已确认风格与具体素材约束决定实施范围。

## 泛函品牌层

涉及李知遇时，先读 [`references/li-zhiyu-ip.md`](references/li-zhiyu-ip.md) 和其中的固定形象主图。李知遇是泛函团队第一个 AI 员工的虚拟 IP；人物、随身设备与办公室场景以该参考为准。

处理「泛函」或「引力边缘」的视觉任务时，先读
`references/fanhan-brand-system.md`；涉及文章小标题或 PPT 标题页时再读
`references/title-styles.md` 和可编辑参考
`assets/html-starters/fanhan-title-styles.html`。这两款样式已获用户认可：
D 用于小标题（绿色已加深），E 用于 PPT 标题页。它们在对应场景下优先于
`references/style-evidence.md` 中的 Victor 默认视觉证据。其他任务继续使用下述通用框架。

所有已认可样板先查 [`references/approved-design-assets.md`](references/approved-design-assets.md)。新任务若有相同载体、相近内容结构的已认可样板，先复制其 HTML/SVG 版式并替换当前任务的文案、图片和品牌色，保留构图关系；直接给用户看首版修改稿，无需为沿用版式再次求批准。用户不满意该版式，或现有样板确实不适用，再设计新版式。用户明确要求全新方案时直接按新方案做。

用户确认喜欢某个新设计时，在该设计的同一目录保存同名 `HTML + PNG + SVG` 三份实际文件：PNG 为所见画面，HTML 与 SVG 为可编辑源；在 [`references/approved-design-assets.md`](references/approved-design-assets.md) 和对应专项参考中把三份文件互相链接并标明用途、版本。运行 `python3 scripts/check_approved_visual_assets.py` 并目视核对三者。不得只保存风格描述、截图或单份 HTML；历史文件若不能完整复原，明确标注补制预览与原件的区别。

PPT 的本轮已认可样板见 [`references/approved-ppt-examples.md`](references/approved-ppt-examples.md)：第 1 页 A、第 2 页 E「双 Bento」、第 3 页 A、第 4 页 B「灵感轨道」。对应 PNG、可编辑 SVG 与 HTML 位于 `assets/html-starters/brand-ppt/`。

泛函设计物料需要生成、改写或筛选文案时，先检查当前环境是否已安装
[`fanhan-content-style`](https://github.com/Ivor-NCUT/fanhan-content-style)。已安装就读取并调用；
未安装就用当前环境的 Skill 安装器从该仓库根目录安装，再读取其 `SKILL.md`。
文案语气以该 Skill 为准，视觉与版式仍由本 Skill 负责。用户给出不可改的定稿时直接排版；
不为纯视觉任务安装写作 Skill，也不把对方的规则复制进本仓库。

## First principle — the richness chain

Understand the person, situation, tension, material world, and irreplaceable
soul of the subject before choosing a visual direction. Then, in order:

1. **Subject and emotion first.** Let what is true about the subject decide
   composition, typography, color, imagery, material, and production method.
2. **Every technique has a cause** — subject cause or benchmark cause — and
   can state its viewer effect. "It looks designed" is not a cause.
3. **Enough techniques, not few.** Richness and justification are co-equal
   requirements. A draft that passes every veto but feels thin has failed;
   do not answer AI slop with austerity.
4. **Reference-level before user-visible.** Compare against strong human-made
   work of an adjacent family; a shown draft is already a designed artifact.

`references/workflow/density-and-care.md` owns the full method: what to add
when the brief is thin, the benchmark obligation, and the density targets.
For Fanhan work, begin from an applicable user-approved template as directed above; otherwise do not begin from a style label, asset recipe, generic template, or AI spectacle.

## Form sanity backstop — run before every adapter

Never let a model-written concept declaration decide its own deliverable form.
Treat it as a hypothesis that must lose to user language, a task controller,
platform convention, and ordinary reader sense.

1. Read the user request and any controlling `RUN.md`, round control, or
   acceptance criteria. Quote the source that fixes the form, count, and
   editable delivery requirement.
2. State the intended reader action in plain language.
3. Counterfactual: if this carrier were the only thing the reader received,
   could it perform that action without the author explaining it? If not,
   reclassify before designing.
4. Fallbacks when underspecified: social graphic-text/article → cover plus
   body pages; product task → related states including feedback;
   methodology/case/tutorial/pitch → narrated deck; poster/key visual → one
   canvas only when explicitly requested.
5. Stop if the proposed form conflicts with a controller.

## Task-grounding backstop

Before any new visual decision, establish a concise task brief per
`references/workflow/task-brief.md` (`TASK_BRIEF.md` for substantial or
unattended work). The brief fixes the authority for scope and facts, reader
action and viewing conditions, content that must remain true, allowed
materials, asset necessity, and the task-specific visual mother object. A
prior result, a style name, or an attractive generated image cannot fill a
missing answer. An unattended runtime records uncertainty and takes the
least-assumptive path; it never invents user approval, facts, assets, or
visual preferences.

## Image-role preflight — zero step when an image is attached

An uploaded image does not determine the task type. Before form classification
or any production, load `references/workflow/image-role-routing.md` and ask
whether the image is the base/hero, project evidence, supporting material, or
a reference/benchmark. Only `Image role: base` plus `poster`/`key visual`
activates the image-as-carrier branch in `references/adapters/poster.md`.

## Evidence, not a preset

Read `references/style-evidence.md` for every task. It ships the author's
distilled visual grammar as a default evidence base; an adopter with approved
work replaces it as step one of onboarding. It is a record of judgment, never
a palette, font pair, or layout template. Use only evidence that fits the
confirmed task, and name any exception. The default voice — its color courage,
scale force, and materiality — always yields to the user's stated aesthetic
preference; a user who asks for quieter, softer, or different is the highest
authority on voice.

## Required execution chain

1. Image attached → image-role preflight above. Then the form sanity and
   task-grounding backstops.
2. Read `references/aesthetic-core.md`, `references/style-evidence.md`,
   `references/copy-discipline.md`, `references/workflow/density-and-care.md`.
3. Classify the form, then read exactly one adapter:
   `references/adapters/poster.md` (user-specified single canvas),
   `graphic-text.md` (cover-plus-body editorial/social), `product-ui.md`
   (product surfaces), `slides.md` (cases, methods, tutorials, pitches).
4. Read `references/operations/execution.md` and
   `references/operations/three-gates.md` — blocking rules, not paperwork to
   complete afterward.
5. Conduct the design dialogue through the native structured prompt when
   callable; otherwise ask in grouped plain prose. Never infer Gate 1
   approval from the request.

Conditional tools — load only for the named need:

| Need | Load |
| --- | --- |
| Asset sourcing, cutout, generation, SVG, perspective | `operations/production-toolkit.md` (after Gate 1 release) |
| Figma/PPTX/interactive-HTML build pipelines | `operations/delivery-implementations.md` (at Gate 3) |
| Editable translation, font/material/perspective drift | `operations/figma-fidelity.md` |
| Any master review or completion claim | `operations/review.md` |
| References to decompose, or revision-led work | `optional/reference-synthesis.md` |
| Multi-format communication surfaces | `optional/communication-surfaces.md` |
| Long-running project governance | `workflow/project-governance.md` |

Precedence: user-confirmed subject and acceptance criteria → truth, safety,
accessibility, primary task → approved project/surface decisions → this file,
aesthetic core, style evidence → adapter and operations → optional references
and external defaults.

## Non-negotiable defaults

- Asset source chain, in order: local workspace material → licensed web →
  user-approved AI generation → code (CSS/SVG/HTML, material/graphic roles
  only). Generation is never the default hero and never factual evidence.
- A generated or found object is input material, not a poster. Process, crop,
  grade, mask, and seat it inside an authored canvas that still works with
  the object hidden.
- Derive palette and type voice from current-subject evidence. The user has
  approved template-first reuse for comparable Fanhan designs; adapt colors
  and content to the current task, and do not carry over stale facts.
- Title, required copy, source evidence, and refusal list are source of
  truth. No filler metadata or uncaused devices; factual inscriptions are
  carried as crafted small type.
- Never batch-produce a multi-page deliverable before user-approved pilot
  pages. A page below the recorded density target is unfinished.
- Use HTML to judge masters; obtain explicit render approval before any
  translation. Every category ships its native editable deliverable unless
  the user explicitly accepts flattened-only.
- The approved render is Gate 3's golden source. Inventory custom fonts,
  masks, blends, and perspective composites before translation.
- A control record proves a decision happened; it never replaces user
  approval or authored visual judgment.

## Review order

Subject specificity, material relation, and residue first; hierarchy, type,
color, space, crop, and task clarity second; technical checks last.
Deterministic checks find concrete risks but cannot certify taste.

## Architecture

This file is the runtime entry point. The default chain is `aesthetic-core`,
`style-evidence`, `density-and-care`, one adapter, `execution`, and
`three-gates`. Keep detailed rules in the referenced module that owns them;
each rule lives in exactly one place.
