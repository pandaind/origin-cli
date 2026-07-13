# Origin Hub Registry

The `origin hub` command group allows you to manage, discover, publish, and install AI assets (like Agent Forge templates, prompts, and Spec Kit workflows) directly from your terminal.

## Overview of Commands

```bash
origin hub [COMMAND]
```

| Command | Description |
|---------|-------------|
| `set-url` | Configure a persistent custom Hub URL |
| `login` | Register and authenticate with the Origin Hub |
| `whoami` | Show the currently authenticated user |
| `search` | Search the Hub for assets |
| `create` | Scaffold a new Hub asset with boilerplate files |
| `publish` | Package and publish an asset to the Hub |
| `install` | Download and install an asset from the Hub |
| `discover`| Scan the project and auto-install recommended assets |
| `logout` | Remove stored Hub credentials |

---

## 1. Configuration & Authentication

Before interacting with the Hub, you must point the CLI to a running Hub Server and authenticate.

**Set the Hub URL (Optional):**
By default, the CLI points to `http://127.0.0.1:8000`. If your Hub Registry is hosted elsewhere, you can configure it globally:
```bash
origin hub set-url https://my-hub-registry.com
```
*(Note: You can also use the `ORIGIN_HUB_URL` environment variable if you prefer not to save it to disk).*

**Login / Register:**
To publish assets, you need an API key. 
```bash
origin hub login
```
You will be prompted for a username and email. The server will issue a secure API key and save it to your local machine (`~/.origin/hub_credentials.json`).

**Check Status:**
```bash
origin hub whoami
```

---

## 2. Discovering & Installing Assets

There are two ways to fetch AI templates from the Hub: **Auto-Discovery** and **Manual Search**.

### Auto-Discovery (Recommended)
When you enter a new codebase, you can ask the CLI to automatically detect your tech stack (Java, Python, React, Go, etc.) and recommend the best agents for your exact environment.

```bash
cd my-react-project/
origin hub discover
```
- The CLI will instantly scan your `package.json`, `pom.xml`, `pyproject.toml`, etc.
- It will display a rich table of recommended assets based on your stack.
- You can type the numbers of the assets you want, and they will be automatically downloaded and installed into your project (e.g., to `.github/prompts/`).

### Manual Search
If you know what you're looking for, you can query the Hub registry:
```bash
origin hub search "frontend"
```

### Manual Install
If you have the exact name of an asset, you can install it directly:
```bash
origin hub install forge-react-expert
```

---

## 3. Publishing Your Own Assets

If you have built an incredible Agent Forge persona, skill, or a useful set of instructions, you can publish it to the Hub for others to use!

### Step 1: Scaffold your Asset

Use the `create` command to automatically generate a boilerplate asset directory:
```bash
origin hub create forge-react-expert --type agent
```
This will create a `forge-react-expert/` directory with a standard `hub-manifest.json` and a boilerplate markdown file. 

The `hub-manifest.json` will look something like this:
```json
{
  "name": "forge-react-expert",
  "version": "1.0.0",
  "type": "agent",
  "description": "An expert-level React Agent persona",
  "author": "your_username"
}
```

### Step 2: Publish

Once you have filled out your asset files, point the publish command at your directory:
```bash
origin hub publish ./forge-react-expert/
```

**Magic Under the Hood:** You do not need to manually list your files in the manifest! The CLI's packager will automatically detect all the files in your directory, inject them into the manifest's `files` array on-the-fly, bundle them into a `.originpkg` archive, and upload it to the server!

---

## Agent-Driven Integration

The Origin Hub is natively integrated into **Agent Forge**. 

If you use `/forge-create` or `/forge-analyze` in your Copilot Chat to scaffold an agent architecture, the AI is explicitly instructed to execute `origin hub search` and `origin hub install` in your terminal *before* writing boilerplate code from scratch. This guarantees that your agents are always using the best, community-vetted templates!
