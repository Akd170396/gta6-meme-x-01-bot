// Entry for make.fun's "Post a GTA 6 meme on X" bounty (gta6-meme-x-01).
//
// The entry is the X post itself; this repository only hands the house the
// post's address. POST.json at the repo root names the post, and this
// program copies it to the output directory. That is all it does: no
// network, no clock, no files outside the repository, and the same bytes
// on every run.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// Read the post file first and check it names an X post, so a malformed
// POST.json fails here instead of entering a dead address.
const postPath = join(botDir, "POST.json");
const post = JSON.parse(readFileSync(postPath, "utf8"));
const postUrl = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+$/;
if (typeof post.url !== "string" || !postUrl.test(post.url)) {
  throw new Error(`POST.json does not name an X post: ${post.url}`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(postPath, join(outputDir, "POST.json"));
