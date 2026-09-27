#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";

const rules = [
  ["对比强调", /不是.{0,30}而是|不是关键.{0,20}才是/g],
  ["背景引入", /在.{0,30}的浪潮下|随着.{0,30}的发展/g],
  ["空泛强调", /重中之重|关键所在|是.{0,24}的核心/g],
  ["手段目的", /通过.{0,40}实现|以.{0,24}为抓手|赋能/g],
  ["模板总结", /首先|其次|然后|最后|因此|然而|综上所述|总而言之/g],
  ["未定义缩写", /\bAI\b|\bSaaS\b/g],
];

function visibleText(source) {
  return source
    .replace(/<[^>]*>/g, " ")
    .replaceAll("&amp;", "&")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replace(/\s+/g, " ")
    .trim();
}

function scan(text, keywords = []) {
  const issues = [];
  for (const [name, pattern] of rules) {
    pattern.lastIndex = 0;
    for (const match of text.matchAll(pattern)) {
      issues.push(`${name}: ${match[0]}`);
    }
  }
  for (const keyword of keywords.filter(Boolean)) {
    const positions = [];
    for (let from = 0; ; ) {
      const index = text.indexOf(keyword, from);
      if (index < 0) break;
      positions.push(index);
      from = index + keyword.length;
    }
    for (let i = 1; i < positions.length; i += 1) {
      if (positions[i] - positions[i - 1] < 100) {
        issues.push(`关键词重复: ${keyword}（间隔 ${positions[i] - positions[i - 1]} 字）`);
      }
    }
  }
  return issues;
}

function selfTest() {
  assert.equal(scan("在技术的浪潮下，我们赋能团队。").length, 2);
  assert.equal(scan("语音留下细节，语音继续流动。", ["语音"]).length, 1);
  assert.deepEqual(scan("周宁确认价格，首版方案周四发出。", ["语音"]), []);
  console.log("self-test passed");
}

const args = process.argv.slice(2);
if (args.includes("--self-test")) {
  selfTest();
  process.exit(0);
}

const keywordArg = args.find((arg) => arg.startsWith("--keywords="));
const keywords = keywordArg ? keywordArg.slice("--keywords=".length).split(",") : [];
const files = args.filter((arg) => !arg.startsWith("--"));
if (!files.length) {
  console.error("usage: node scripts/check-copy.mjs <file...> [--keywords=词1,词2]");
  process.exit(2);
}

let failed = false;
for (const file of files) {
  const issues = scan(visibleText(fs.readFileSync(file, "utf8")), keywords);
  if (issues.length) {
    failed = true;
    console.error(`${file}:`);
    for (const issue of issues) console.error(`  - ${issue}`);
  }
}

if (failed) process.exit(1);
console.log(`copy check passed: ${files.length} file(s)`);
