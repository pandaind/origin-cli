# Origin Hub Asset Bundling

Bundling is the process of packaging an asset directory into an `.originpkg` file before publishing to the Hub. The `origin hub publish` command handles this **automatically**.

## How Bundling Works

The bundle is just a standard `.tar.gz` archive with a custom `.originpkg` extension. When you run `origin hub publish`, the CLI internally performs the following steps:

1. **Reads `hub-manifest.json`** — validates required fields (`name`, `version`, `type`).
2. **Archives the Directory** — tars the entire directory (excluding `.git` and hidden system files) into a `<name>-<version>.originpkg` file.
3. **Uploads** — pushes the bundle to the Hub Registry via a multipart file upload.
4. **Cleans up** — deletes the temporary bundle file from your local machine.

## Step-by-Step Guide for Asset Authors

**1. Structure your asset folder:**
Create a folder containing all the files you want to publish.
```
my-asset/
├── hub-manifest.json        ← Required
├── my-expert.agent.md
└── my-instructions.md
```

**2. Write your `hub-manifest.json`:**
This file tells the Registry and the CLI how to handle your asset.
```json
{
  "name": "my-expert-agent",
  "version": "1.0.0",
  "type": "skill",
  "description": "A helpful expert agent",
  "tags": ["python", "fastapi"],
  "files": ["my-expert.agent.md", "my-instructions.md"]
}
```

### Manifest Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Unique asset name (used for install) |
| `version` | ✅ | Semantic version string (e.g., 1.0.0) |
| `type` | ✅ | Must be one of: `skill`, `agent`, `instruction`, `workflow`, or `extension` |
| `description` | No | Short summary of what the asset does |
| `tags` | No | Tech stack tags for auto-discovery (e.g., `react`, `python`) |
| `files` | No | Explicit list of files to extract upon installation |

**3. Publish (bundling is automatic):**
```bash
origin hub login   # if not already logged in
origin hub publish ./my-asset/
```

The CLI will print `✔ Successfully published my-expert-agent v1.0.0!` when done.

**4. Verify it's live:**
```bash
origin hub search my-expert-agent
```

That's all there is to it! The bundling itself is completely transparent — just focus on creating your files and writing a valid manifest.
