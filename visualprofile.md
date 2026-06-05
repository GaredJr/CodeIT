# CodeIT Visual Profile

CodeIT is a clean developer-focused discussion platform. It takes the familiar structure of Reddit, but shifts the visual identity closer to GitHub, VS Code, Linear, and Stack Overflow.

The goal is simple:

> A clean place where coders can ask questions, share code, post repositories, and build focused communities around languages and technologies.

CodeIT should feel practical, fast, readable, and pleasant to use.

---

## Core Visual Direction

CodeIT should feel like:

- Reddit structure
- GitHub clarity
- VS Code code presentation
- Modern developer tool polish

The interface should not feel like a generic social media app. It should feel like a proper workspace for developers.

The style should be:

- Clean
- Sharp
- Technical
- Calm
- Focused
- Straightforward

The UI should make long threads, code blocks, nested comments, tags, and repositories easy to scan.

---

## Brand Feel

The name **CodeIT** feels direct and command-like.

It should give this kind of feeling:

> Post it. Debug it. Ship it.

The tone should be useful and clear. Not overly playful. Not corporate.

Good tone words:

- Clean
- Technical
- Fast
- Focused
- Community-driven
- Practical
- No bullshit

Avoid making it look too much like Reddit. The concept can be similar, but the identity should lean more toward developer tools.

---

## Logo Direction

The logo should be simple. No mascot. No complex icon.

### Option 1: Bracket Mark

```txt
<CodeIT/>
```

or:

```txt
{C}
```

This is simple, but also a bit common.

### Option 2: Terminal Prompt

```txt
>_
```

Combined with the CodeIT wordmark:

```txt
> CodeIT
```

This gives a coding feel fast.

### Option 3: Comment Bubble + Code Bracket

A speech bubble with `</>` inside.

This is probably the strongest direction because CodeIT is about discussion around code.

### Option 4: Subcodeit Tree Symbol

Since CodeIT has subcodeits, the logo could use a small modular structure.

```txt
CodeIT
├─ javascript
├─ roblox
├─ python
└─ webdev
```

The icon could be a small tree, node, folder, or branching symbol.

---

## Recommended Logo Direction

The strongest direction is:

> A clean speech bubble combined with code brackets.

Example concept:

```txt
[ </> ]
CodeIT
```

It communicates:

- Coding
- Discussion
- Community
- Help
- Snippets

Keep it flat, simple, and readable at small sizes.

---

## Color Palette

CodeIT should be dark mode first.

Use a soft neutral background, clean cards, subtle borders, and one clear accent color.

### Main Dark Palette

```css
:root {
  --bg: #0D1117;
  --surface: #161B22;
  --surface-hover: #1F2630;
  --border: #30363D;

  --text: #E6EDF3;
  --text-muted: #8B949E;
  --text-soft: #6E7681;

  --accent: #3B82F6;
  --accent-hover: #60A5FA;

  --success: #22C55E;
  --warning: #F59E0B;
  --danger: #EF4444;

  --code-bg: #0B0F14;
  --code-border: #263040;
}
```

This palette feels natural for a coder app. It is GitHub-like, but not a direct copy.

### Recommended Accent

Blue is the safest and cleanest choice.

```css
--accent: #4F8CFF;
```

Purple is also good if the app should feel a bit more distinct.

```css
--accent: #7C5CFF;
```

Best choice:

```css
--accent: #4F8CFF;
```

Use one main accent. Let syntax highlighting add the extra color.

---

## Light Mode Palette

Light mode should exist, but dark mode should be the default.

```css
:root.light {
  --bg: #F6F8FA;
  --surface: #FFFFFF;
  --surface-hover: #F0F3F6;
  --border: #D0D7DE;

  --text: #24292F;
  --text-muted: #57606A;
  --text-soft: #6E7781;

  --accent: #2563EB;
  --accent-hover: #1D4ED8;

  --code-bg: #F6F8FA;
  --code-border: #D8DEE4;
}
```

---

## Typography

Use one clean UI font and one proper monospace font.

### UI Font

Recommended:

```css
font-family: Inter, Geist, system-ui, sans-serif;
```

Good options:

- Geist
- Inter
- IBM Plex Sans
- Satoshi

Best choice:

```css
--font-ui: "Geist", system-ui, sans-serif;
```

### Code Font

Recommended:

```css
font-family: "JetBrains Mono", "Fira Code", monospace;
```

Best choice:

```css
--font-code: "JetBrains Mono", monospace;
```

JetBrains Mono fits code snippets well and looks serious.

---

## Layout Style

The layout should feel familiar, but cleaner than Reddit.

Desktop structure:

```txt
Left Sidebar        Main Feed              Right Panel
-------------------------------------------------------
Subcodeits          Posts/comments         Trending repos
Languages           Code snippets          Active users
Saved posts         Filters                Popular tags
```

### Top Navigation

```txt
Logo | Search | Create | Notifications | Profile
```

### Left Sidebar

```txt
Home
Following
Saved
/code/javascript
/code/python
/code/roblox
/code/react
Explore
```

### Main Feed

```txt
Hot | New | Top | Unanswered | Repos
```

### Right Sidebar

```txt
Trending subcodeits
Popular tags
Top contributors
GitHub repos
```

The **Unanswered** tab is important. It makes the platform useful, not just scrollable.

---

## Subcodeits

Do not copy Reddit naming too directly in the UI.

Use:

```txt
/code/javascript
/code/python
/code/roblox
/code/react
/code/linux
```

This feels developer-specific and different enough from Reddit.

Example:

```txt
/code/react
```

This is better than:

```txt
r/react
```

---

## Post Card Design

A post card should be clean and easy to scan.

Example:

```txt
[icon] /code/javascript      Posted by @user · 2h ago

How do I debounce this React input?

I have this component and it keeps rerendering...

[code snippet preview]

▲ 124   💬 38   🔗 Repo   #react #javascript #frontend
```

A more developer-focused example:

```txt
/code/react                         Question · Unsolved

How do I stop this component from rerendering?

I have a search input that calls the API every time I type.
What is the cleanest debounce pattern here?

[ App.tsx                                     TS  Copy ]
  const [query, setQuery] = useState("")
  useEffect(() => {
    fetch(`/api/search?q=${query}`)
  }, [query])

▲ 82   ▼   24 comments   #react #typescript #frontend
```

---

## Post Types

Post types should be clear and visible.

Suggested types:

- Question
- Snippet
- Repository
- Showcase
- Discussion
- Bug
- Tutorial
- Help Wanted

Example badges:

```txt
[Question]
[Bug]
[Repo]
[Snippet]
```

Keep badges small and outlined.

Suggested color meaning:

- Question: blue
- Bug: red
- Repo: purple
- Snippet: green
- Tutorial: amber

Do not overuse color. Badges should help scanning, not dominate the design.

---

## Code Blocks

Code blocks are one of the most important parts of CodeIT.

They should look excellent.

Features:

- Filename header
- Language label
- Copy button
- Line numbers
- Syntax highlighting
- Optional expand button
- Error line highlights
- Subtle border
- Slightly darker background than normal cards

Example:

```txt
app/components/PostCard.tsx                    TypeScript  Copy
────────────────────────────────────────────────────────────
1  export default function PostCard() {
2    return <article>...</article>
3  }
```

Recommended style:

```css
.code-block {
  background: var(--code-bg);
  border: 1px solid var(--code-border);
  border-radius: 12px;
  font-family: var(--font-code);
}
```

Code blocks should feel embedded into the platform, not pasted in as an afterthought.

---

## Cards and Borders

Avoid heavy shadows.

Use borders, contrast, and spacing instead.

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
}
```

Hover state:

```css
.card:hover {
  background: var(--surface-hover);
  border-color: var(--accent);
}
```

Keep hover states subtle. Do not make the whole site flash blue.

---

## Buttons

Buttons should be clean and tool-like.

Primary buttons:

- Post
- Ask Question
- Create Subcodeit

Secondary buttons:

- Save
- Share
- Follow

Primary style:

```css
.button-primary {
  background: var(--accent);
  color: white;
  border-radius: 10px;
  font-weight: 600;
}
```

Secondary buttons should usually be transparent with a border.

---

## Visual Identity Details

Use small developer-focused details across the UI.

Good details:

- Language icons
- Repo cards
- Commit-style timestamps
- Markdown preview
- Terminal-like empty states
- Syntax-colored accents
- Inline tags
- Copy buttons
- File names above code blocks
- Solved state for questions

Example empty state:

```txt
No posts found.
Try creating /code/rust
```

Another option:

```txt
Nothing here yet.
Be the first to push a post.
```

---

## Profile Pages

Profiles should feel like GitHub mixed with Reddit.

Suggested profile content:

```txt
@username
Frontend dev · Roblox scripter · Python enjoyer

Cred
Top languages
Pinned posts
GitHub repositories
Badges
Recent activity
```

Useful stats:

```txt
Answers helped: 42
Repos shared: 8
Snippets posted: 19
```

Do not call the score karma. That feels too much like Reddit.

Better names:

- Cred
- Score
- Rep

Best choice:

```txt
Cred
```

Example:

```txt
1,284 Cred
```

---

## Naming System

Avoid copying Reddit terms directly where possible.

| Reddit Term | CodeIT Version |
|---|---|
| Subreddit | Subcodeit |
| r/javascript | /code/javascript |
| Karma | Cred |
| Members | Devs |
| Mods | Maintainers |
| Flair | Tags |
| OP | Author |
| Post | Post |
| Upvote | Upvote |

“Maintainers” is a strong replacement for mods because it fits coding culture.

---

## Post Composer

The composer should feel like GitHub issues mixed with a clean forum editor.

It should support Markdown well.

Tabs:

```txt
Write | Preview
```

Quick insert buttons:

```txt
Code block
Inline code
Link repo
Add image
Add tags
```

The composer should support:

- Markdown
- Syntax-highlighted code blocks
- GitHub repo links
- Images
- Tags
- Post type selection
- Subcodeit selection
- Preview mode

---

## Repository Posts

A repository post should feel like a small GitHub card.

Example:

```txt
gardegeheime / cool-project

A simple weather app using Next.js and OpenWeather

★ 24    Forks 3    TypeScript    Updated 2d ago
```

Useful repo data:

- Repo name
- Owner
- Description
- Stars
- Forks
- Main language
- Last updated date
- Open issues
- License
- GitHub link

---

## Question Posts

Question posts should show whether they are solved.

Example:

```txt
[Solved] How do I fix this Lua table bug?
```

Solved answers should have a green check.

Useful states:

- Unsolved
- Solved
- Needs more info
- Duplicate
- Archived

The solved state makes CodeIT more useful than normal Reddit threads.

---

## Search Design

Search should be a major feature.

Placeholder:

```txt
Search posts, errors, repos, snippets...
```

Filters:

- Language
- Post type
- Solved / Unsolved
- Date
- Subcodeit
- Has repo
- Has code
- Author
- Tags

This makes the platform useful as a knowledge base, not just a feed.

---

## Microcopy

Keep UI text short and dev-like.

Good:

```txt
Ask a question
Post a snippet
Link a repo
Create subcodeit
Mark as solved
Copy code
```

Avoid:

```txt
Join the conversation!
Share your amazing thoughts!
Build community together!
```

That sounds fake.

---

## Feed Tabs

Recommended feed tabs:

```txt
Hot
New
Top
Unanswered
Repos
Snippets
```

Optional:

```txt
Solved
Following
```

The most important ones are:

- Hot
- New
- Unanswered
- Repos
- Snippets

---

## Comment Design

Comments should support nested discussion, but avoid becoming messy.

Important features:

- Clear nesting lines
- Collapse thread button
- Code block support
- Inline code support
- Accepted answer marker
- Reply button
- Upvote/downvote
- Author labels
- Maintainer labels

Example:

```txt
@devuser · 14 min ago

You need to memoize the callback, not the whole component.

[code block]

▲ 18   Reply   Copy link
```

---

## Tags

Tags should be small and clean.

Example:

```txt
#react #typescript #frontend
```

Style:

```css
.tag {
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-muted);
  border-radius: 999px;
  padding: 2px 8px;
}
```

Tags should not look like big buttons.

---

## Icons

Use simple line icons.

Good icon libraries:

- Lucide
- Phosphor Icons
- Heroicons

Best choice:

```txt
Lucide
```

It fits clean developer tools well.

Use icons for:

- Question
- Bug
- Repository
- Snippet
- Solved
- Copy
- Save
- Share
- Search
- Notifications

---

## Motion

Animations should be subtle.

Use motion for:

- Card hover
- Button hover
- Dropdowns
- Copy feedback
- New comment appearing
- Vote count changing
- Sidebar opening on mobile

Avoid flashy animations. CodeIT should feel fast and focused.

Recommended transition:

```css
transition: 120ms ease;
```

---

## Mobile Design

Mobile should keep the same clean feel.

Recommended structure:

- Top bar with logo and search
- Feed as full-width cards
- Bottom nav
- Drawer for subcodeits
- Floating create button

Bottom nav:

```txt
Home | Search | Create | Saved | Profile
```

Keep code blocks horizontally scrollable on mobile.

---

## Final Visual Direction

CodeIT should be defined like this:

> CodeIT is a clean dark-mode coding forum with GitHub-style clarity, Reddit-style discussion flow, and VS Code-style code presentation. The interface should feel practical, fast, and focused. The brand should use a dark neutral palette, one blue accent, crisp typography, subtle borders, and strong code block design.

This gives the project a clear identity without copying Reddit too closely.
