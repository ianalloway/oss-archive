---
name: portfolio-ship-week
description: "A comprehensive workflow for launching and optimizing personal portfolios, including DNS fixes, SEO infrastructure, and job search outreach. Use for: fixing broken portfolio domains, adding SEO/meta tags to React sites, and preparing job application materials."
---

# Portfolio Ship Week

This skill provides a structured workflow for the final push to launch a professional portfolio and initiate a job search.

## Core Workflow

### 1. DNS Diagnosis & Fix
- **Check Records**: Use `dig <domain> ANY +short` and `whois <domain>` to identify the current DNS state and name servers.
- **Identify Hosting**: Determine if the site is on Vercel, Netlify, GitHub Pages, etc.
- **Generate Guide**: Use the `DNS_FIX_GUIDE.md.template` to provide the user with specific A and CNAME records.

### 2. SEO Infrastructure
- **Install Dependencies**: Ensure `react-helmet-async` is installed in the project.
- **Implement SEO Component**: Use `SEO.tsx.template` to create a reusable meta-tag component.
- **Update Routing**: Wrap the application in `HelmetProvider` and add `<SEO />` to each route in `App.tsx` or `Router.tsx`.
- **Static Files**: Create `robots.txt` and `sitemap.xml` in the `public/` directory.

### 3. GitHub Integration
- **Locate Repo**: Use `gh repo list <username>` to find the active portfolio repository.
- **Apply Changes**: Clone the repo, implement the SEO/Routing fixes, and push directly to the main branch.
- **Verify Build**: Check for common deployment triggers (e.g., Vercel/Netlify automatic builds).

### 4. Job Search Outreach
- **Draft Emails**: Create tailored outreach for specific roles (e.g., HN "Who is hiring", direct recruiter emails).
- **Master Checklist**: Provide a clear "Today / This Week / Done" checklist to keep the user organized.

## Bundled Resources

### Templates
- `SEO.tsx.template`: React component for Open Graph, Twitter cards, and JSON-LD.
- `DNS_FIX_GUIDE.md.template`: Markdown guide for resolving domain issues.

## Best Practices
- **Ship Beats Perfect**: Focus on getting the site reachable and the emails sent first.
- **Direct Action**: Whenever possible, push code directly to GitHub rather than just providing snippets.
- **Clear Instructions**: For tasks requiring user login (like DNS), provide the exact values to copy-paste.
