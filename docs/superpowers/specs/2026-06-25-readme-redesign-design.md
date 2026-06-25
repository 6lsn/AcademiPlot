# README Redesign Design Spec

**Date:** 2026-06-25
**Status:** Approved
**Scope:** Visual redesign of README.md for AcademiPlot v0.2.0

---

## 1. Goals

- Visual beautification: badges, TOC, icons, dividers, centered layout
- Structure reorganization: feature-first flow (attract → engage → convert)
- Add content: installation, contributing hints, navigation links
- Bilingual Chinese + English maintained
- Target audience: academic researchers, math modeling competitors, general developers

## 2. Approach

Feature Showcase — visual impact first, technical details after.

## 3. Section Structure

### §1 Hero (centered)
- Large title with emoji
- Tagline (bilingual)
- 4 badges: PyPI version, Python version, License, Downloads
- Navigation links: Quick Start • Gallery • API • Installation

### §2 Why AcademiPlot + Quick Start
- Before/After comparison table (existing images)
- 4 feature bullet points with emoji icons (引用块格式)
- Quick Start: 3 code examples (lineplot, suggest, auto_plot)

### §3 Gallery
- Top navigation: Basic • Statistical • Advanced • 3D • Multi-panel
- Basic: Line, Bar, Scatter, Area (4 per row)
- Statistical: Heatmap, Box Plot, Radar, Histogram, Violinplot (5 per row)
- Advanced: Pareto, Contour, Waterfall, Dumbbell, Bullet (5 per row)
- 3D: Surface, Scatter, Bar (3 per row)
- Multi-panel: 2p, 3p, 4p, 6p (4 per row)

### §4 Features + Usage
- Features table with emoji: 3 themes, smart suggest, quality review, 17 charts, multi-panel, bilingual, multi-format, CLI
- Usage: 4 core scenarios (suggest, themes, review, multi-panel) — 2-4 lines each

### §5 API Reference
- Two `<details>` collapsible sections: Chart Functions (17) + Smart Functions
- Reduces scrolling significantly

### §6 Installation
- pip install acadp
- From source (git clone + pip install -e .)

### §7 Comparison
- Table with ❌/✅ icons: matplotlib vs seaborn vs AcademiPlot
- Rows: academic styles, smart selection, quality review, chart types, CLI review

### §8 Footer
- Centered: MIT License • GitHub • PyPI

## 4. Visual Elements

- Emoji section headers: 🎨 🚀 ⚡ 📊 ✨ 📖 🔍 📦 📈
- `<div align="center">` for hero and footer
- `<details>` for collapsible API reference
- Navigation links in hero
- Badge shields: PyPI, Python, License, Downloads
- `<table>` for Before/After comparison
- `<b>` bold for feature names in tables

## 5. Content Changes

- Remove: duplicate "核心优势" list (merged into §2 quote block)
- Remove: sections 1-8 of old Usage Guide (replaced by 4 compact scenarios)
- Remove: `README_CN.md` link (bilingual is built-in)
- Add: Downloads badge
- Add: Navigation links in hero
- Add: From source installation
- Add: Gallery category navigation
- Add: `<details>` collapsible API sections
- Add: Centered footer

## 6. File Changes

- Modify: `README.md` — complete rewrite
- No other files change
