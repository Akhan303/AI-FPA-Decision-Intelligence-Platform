---
name: AI FP&A Decision Intelligence Platform
description: Executive finance dashboard design contract for a synthetic portfolio case study.
colors:
  foundations: ["bg/primary", "bg/secondary", "bg/tertiary", "border/light", "border/default", "text/primary", "text/secondary", "text/tertiary", "icon/accent"]
  charts: ["blue/500", "green/700", "purple/500"]
typography:
  family: "System Sans Variable"
  tokens: ["text/xs/normal", "text/xs/semibold", "text/sm/normal", "text/sm/medium", "heading/md/medium", "heading/2xl"]
spacing:
  tokens: ["space-12", "space-24"]
rounded:
  card: "corner-radius/cr-24"
surfaces:
  shell: "1140px"
  reading: "800px"
  top-bar: "48px"
  dashboard-padding: "24px"
components:
  top-bar: "compact artifact title and freshness"
  metric-card: "one headline KPI plus comparison"
  report-block: "governed narrative container"
  chart-block: "neutral chart title and decision context"
  table-list: "dense executive lookup"
  popover-menu: "source and evidence details"
implementation:
  runtime: "portable analytics artifact reader"
---

# AI FP&A Decision Intelligence Platform

## Overview

The dashboard is an executive decision surface: summary first, drivers second, actions third. It is labeled as a synthetic portfolio case study and keeps provenance accessible.

## Colors

Use bg/primary, bg/secondary, bg/tertiary, border/light, border/default, text/primary, text/secondary, text/tertiary, and icon/accent. Charts use blue/500, green/700 and purple/500. Color is never the only status encoding.

## Typography

System Sans Variable is the fallback. Use text/xs/normal and text/xs/semibold for metadata, text/sm/normal and text/sm/medium for copy, heading/md/medium for sections, and heading/2xl for the title.

## Layout

The shell is 1140px with an 800px reading column. The top bar is 48px, horizontal padding is 24px, and rhythm uses space-12 and space-24. KPI cards lead, followed by trend, decomposition, scenarios and controls.

## Elevation & Depth

Use elevation/01 only for the shell and true overlays. Borders and spacing create hierarchy.

## Shapes

Cards use corner-radius/cr-24. Compact controls use the shared small-radius role; badges use pills.

## Components

The top-bar keeps freshness accessible. Each metric-card carries one decision metric. A report-block contains grounded narrative, each chart-block answers one question, table-list supports exact review, and popover-menu exposes source details.

## Do's and Don'ts

Do preserve reconciled calculations, source notes and the human approval gate. Do keep synthetic assumptions explicit. Do customize drivers and scenarios through the generator. Do not claim real-company outcomes or publish unapproved narrative as fact.

