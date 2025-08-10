# Blog Translation Scripts

This directory contains scripts to help translate Chinese blog posts to English automatically or create templates for manual translation.

## Setup

Install required dependencies:
```bash
make setup
# or
pip3 install -r requirements.txt
```

## Translation Methods

### Auto Translation (Recommended)

Uses OpenAI GPT to automatically translate Chinese posts to English.

**Prerequisites:**
- OpenAI API key
- Set environment variable: `export OPENAI_API_KEY='your-api-key'`

**Commands:**
```bash
# Translate all posts without English versions
make translate

# Translate only the latest post
make translate-latest

# Translate a specific post
make translate-post POST=content/posts/my-post-directory/
```

**Features:**
- Automatically translates title, summary, and content
- Maintains markdown formatting and code blocks
- Sets English post date one day earlier than Chinese version
- Handles large content by splitting into chunks
- Rate limiting to avoid API limits

## File Structure

After running the scripts, your post directory will look like:
```
content/posts/my-post/
├── index.md       # Original Chinese version
├── index.en.md    # Generated English version
└── ...            # Other assets
```

## Script Details

### auto-translate.py
- Full automatic translation using OpenAI GPT-4
- Handles frontmatter and content translation
- Smart content chunking for large posts
- Error handling and rate limiting

## Examples

### Auto-translate the latest post
```bash
export OPENAI_API_KEY='sk-...'
make translate-latest
```

### Translate a specific post
```bash
make translate-post POST=content/posts/jenkins-concurrent-build/
```

## Tips

1. **Cost Management**: Auto-translation uses OpenAI API which has costs. Use template method for large batches if preferred.

2. **Quality Check**: Always review auto-translated content for accuracy, especially technical terms.

3. **Batch Processing**: The auto-translate script processes posts one by one with rate limiting to avoid API errors.

4. **Backup**: The scripts never modify original Chinese files, only create new English versions.

## Troubleshooting

### OpenAI API Issues
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Test API connection
python3 -c "import openai; client = openai.OpenAI(); print('API key is valid')"
```

### Missing Dependencies
```bash
# Reinstall requirements
pip3 install -r requirements.txt --force-reinstall
```

### Permission Issues
```bash
# Fix script permissions
chmod +x bin/auto-translate.py
```
