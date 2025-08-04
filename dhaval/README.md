# Dhaval's Research Work

This folder contains Dhaval's research work on AI alignment critique and revision processes.

## Setup

### OpenAI API Key Setup

1. **Copy the template file:**

   ```bash
   cp env.template .env
   ```

2. **Add your OpenAI API key to `.env`:**

   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. **The `.env` file is already in `.gitignore`** - it will not be committed to the repository.

### Alternative: GitHub Secrets (Recommended for CI/CD)

For automated workflows, add your OpenAI API key as a GitHub Secret:

1. Go to your repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add a new repository secret named `OPENAI_API_KEY`
4. Paste your API key as the value

## Work Structure

- `env.template` - Template for environment variables
- `README.md` - This setup guide
- Additional research files will be added here

## Constitution

The project follows principles defined in `../constitution.json`:

- **Standard principles**: Ethical guidelines from CAI constitution
- **Weird principles**: Alternative evaluation criteria

## Security

- Never commit API keys or secrets to the repository
- Use environment variables for sensitive data
- The `.gitignore` file excludes common sensitive files
