# Privacy Policy for CodeIT

*Last updated: 09.06.2026*

CodeIT is an exam project and prototype for a code-focused social platform. This privacy policy explains what data the project may collect, why it is used, and how it is handled.

This document is written for project documentation and demonstration purposes. Before using CodeIT as a real public service, the privacy policy should be reviewed and adapted for production use.

---

## 1. Who is responsible

CodeIT is developed as an exam project by the project owner.

For questions about privacy or data handling, contact:

```text
TODO: Add contact email or GitHub profile
```

---

## 2. What data CodeIT collects

CodeIT may collect and store the following information:

### Account data

If a user logs in with GitHub, CodeIT may store:

- GitHub user ID or Supabase user ID
- GitHub username
- Display name
- Avatar URL
- Basic profile metadata returned through GitHub/Supabase Auth

CodeIT does not store GitHub passwords.

### Content data

When users interact with the platform, CodeIT may store:

- Posts
- Code snippets
- Post titles and descriptions
- Tags
- GitHub repository links added to posts
- Comments
- Upvotes
- Profile text such as bio, if this feature is enabled

### Technical data

The server and third-party providers may process technical data such as:

- IP address
- Browser/user agent
- Request URLs
- Login redirect data
- Basic server logs
- Error logs

This is used for security, debugging and keeping the service available.

---

## 3. Why the data is used

CodeIT uses data to:

- Show posts, comments and code snippets
- Let users create and interact with content
- Connect posts to GitHub repositories
- Let users log in with GitHub
- Show user profiles
- Prevent basic misuse
- Debug errors during development
- Demonstrate fullstack functionality for the exam project

---

## 4. GitHub login

CodeIT uses GitHub login through Supabase Auth.

When a user chooses to log in with GitHub:

```text
CodeIT -> Supabase Auth -> GitHub -> Supabase Auth -> CodeIT
```

GitHub confirms the user's identity, and Supabase returns an authentication session to CodeIT. CodeIT then stores only the information needed to identify the user inside the app.

CodeIT does not receive or store the user's GitHub password.

---

## 5. Supabase

CodeIT uses Supabase for:

- PostgreSQL database
- Authentication
- API access to stored data

Supabase stores application data such as profiles, posts, comments and votes. Access to this data should be protected with database rules such as Row Level Security.

Supabase's own privacy and security documentation applies to their handling of data as a service provider.

---

## 6. Cloudflare

CodeIT may use Cloudflare Tunnel to make the app available online from the server PC.

Cloudflare may process technical traffic data needed to route requests, provide security features and keep the tunnel working.

Cloudflare's own privacy policy applies to their handling of traffic and service data.

---

## 7. Legal basis

For a real public deployment, CodeIT should define a clear legal basis for processing personal data.

For this exam prototype, the intended legal bases would likely be:

- User consent, when logging in or submitting content
- Legitimate interest, for basic security, debugging and service operation

TODO: Review this section before production use.

---

## 8. Data sharing

CodeIT does not sell user data.

Data may be processed by these service providers:

| Provider | Purpose |
|---|---|
| Supabase | Database, authentication and API |
| GitHub | OAuth login |
| Cloudflare | Tunnel, routing and security |

If CodeIT becomes a real public service, the project should review each provider's data processing terms and subprocessors.

---

## 9. Data retention

CodeIT keeps user-generated content while the project is active, unless it is deleted manually or removed by the project owner.

For a production version, CodeIT should define:

- How long logs are stored
- How users can delete their accounts
- How users can delete posts/comments
- How backups are handled

TODO: Add exact retention periods before production use.

---

## 10. User rights

Depending on applicable law, users may have rights to:

- Request access to their personal data
- Correct inaccurate data
- Request deletion of data
- Object to certain processing
- Request a copy of their data

For this exam prototype, these requests must currently be handled manually by the project owner.

TODO: Add a real contact method and process if the project goes public.

---

## 11. Security

CodeIT uses or plans to use:

- GitHub OAuth instead of storing passwords
- Supabase Auth for authentication
- Environment variables for secrets
- `.env` ignored from Git
- Supabase Row Level Security for database access control
- Cloudflare Tunnel instead of exposing the server directly through port forwarding

Known limitations:

- The project is still a prototype.
- It does not yet have full moderation tools.
- It does not yet have automated privacy/account deletion flows.
- Logging and retention policies are not production-ready.

---

## 12. Children's privacy

CodeIT is not intentionally designed for children or for collecting data from children.

If the project becomes public, the intended audience and age requirements should be clarified.

---

## 13. Changes to this policy

This privacy policy may be updated as the project changes.

For the exam version, changes should be documented in the project log or Git history.

---

## 14. Useful provider links

- Supabase Privacy Policy: https://supabase.com/privacy
- Supabase Security Docs: https://supabase.com/docs/guides/security
- GitHub Privacy Statement: https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement
- Cloudflare Privacy Policy: https://www.cloudflare.com/policies/privacy/
