#!/usr/bin/env python3
"""
Auto Translation Script for Blog Posts

This script helps to automatically translate Chinese blog posts to English.
Usage:
1. python3 bin/auto-translate.py [post_directory]  # Translate specific post
2. python3 bin/auto-translate.py --all             # Translate all posts without English version
3. python3 bin/auto-translate.py --latest          # Translate the latest post

Examples:
python3 bin/auto-translate.py content/posts/my-new-post/
python3 bin/auto-translate.py --all
python3 bin/auto-translate.py --latest
"""

import os
import sys
import re
import argparse
import openai
from pathlib import Path
from datetime import datetime
import yaml
import time

class BlogTranslator:
    def __init__(self):
        # You can set your OpenAI API key here or use environment variable
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("❌ Error: Please set OPENAI_API_KEY environment variable")
            print("   Example: export OPENAI_API_KEY='your-api-key'")
            sys.exit(1)
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        self.content_dir = Path("content/posts")
        
    def find_posts_to_translate(self):
        """Find all posts that have Chinese version but no English version"""
        posts_to_translate = []
        
        for post_dir in self.content_dir.iterdir():
            if not post_dir.is_dir():
                continue
                
            chinese_file = post_dir / "index.md"
            english_file = post_dir / "index.en.md"
            
            if chinese_file.exists() and not english_file.exists():
                posts_to_translate.append(post_dir)
                
        return sorted(posts_to_translate, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def get_latest_post(self):
        """Get the latest Chinese post directory"""
        posts = []
        for post_dir in self.content_dir.iterdir():
            if not post_dir.is_dir():
                continue
            chinese_file = post_dir / "index.md"
            if chinese_file.exists():
                posts.append((post_dir, chinese_file.stat().st_mtime))
        
        if not posts:
            return None
            
        # Sort by modification time and return the latest
        posts.sort(key=lambda x: x[1], reverse=True)
        return posts[0][0]
    
    def parse_frontmatter(self, content):
        """Parse frontmatter from markdown content"""
        if not content.startswith('---'):
            return {}, content
            
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content
            
        try:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return frontmatter, body
        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML frontmatter: {e}")
            return {}, content
    
    def translate_text(self, text, context="blog post"):
        """Translate Chinese text to English using OpenAI GPT"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # You can change to gpt-3.5-turbo for lower cost
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a professional technical translator specializing in DevOps, AI, and software development content. 
                        
                        Translate the following Chinese {context} to English:
                        - Keep technical terms accurate and consistent
                        - Maintain markdown formatting
                        - Keep code blocks unchanged
                        - Use professional but readable English
                        - Preserve the original meaning and tone
                        - Keep URLs and links unchanged
                        - For technical terms, use commonly accepted English equivalents
                        - Maintain the structure and formatting of the original text
                        
                        Only return the translation, no explanations."""
                    },
                    {
                        "role": "user", 
                        "content": text
                    }
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Translation error: {e}")
            return None
    
    def translate_frontmatter(self, frontmatter):
        """Translate frontmatter fields"""
        translated = frontmatter.copy()
        
        # Translate title
        if 'title' in translated:
            print(f"   📝 Translating title: {translated['title'][:50]}...")
            translated_title = self.translate_text(translated['title'], "title")
            if translated_title:
                translated['title'] = translated_title
        
        # Translate summary if exists
        if 'summary' in translated:
            print("   📄 Translating summary...")
            translated_summary = self.translate_text(translated['summary'], "summary")
            if translated_summary:
                translated['summary'] = translated_summary
        
        # Adjust date for English version (one day earlier to show Chinese first)
        if 'date' in translated:
            try:
                original_date = datetime.fromisoformat(str(translated['date']).replace('Z', '+00:00'))
                # Set English version date one day earlier
                english_date = original_date.replace(day=original_date.day - 1)
                translated['date'] = english_date.strftime('%Y-%m-%d')
            except:
                pass
        
        return translated
    
    def translate_post(self, post_dir):
        """Translate a single post"""
        chinese_file = post_dir / "index.md"
        english_file = post_dir / "index.en.md"
        
        if not chinese_file.exists():
            print(f"❌ Chinese file not found: {chinese_file}")
            return False
            
        if english_file.exists():
            print(f"⚠️  English version already exists: {english_file}")
            return False
        
        print(f"🔄 Translating: {post_dir.name}")
        
        try:
            # Read Chinese content
            with open(chinese_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter and body
            frontmatter, body = self.parse_frontmatter(content)
            
            # Translate frontmatter
            translated_frontmatter = self.translate_frontmatter(frontmatter)
            
            # Split body into chunks for better translation
            print("   🔄 Translating content...")
            chunks = self.split_content(body)
            translated_chunks = []
            
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    print(f"      Translating chunk {i+1}/{len(chunks)}...")
                    translated_chunk = self.translate_text(chunk, "content")
                    if translated_chunk:
                        translated_chunks.append(translated_chunk)
                    else:
                        translated_chunks.append(chunk)  # Fallback to original
                    time.sleep(1)  # Rate limiting
                else:
                    translated_chunks.append(chunk)
            
            translated_body = '\n\n'.join(translated_chunks)
            
            # Create English version
            english_content = self.create_english_content(translated_frontmatter, translated_body)
            
            # Write English file
            with open(english_file, 'w', encoding='utf-8') as f:
                f.write(english_content)
            
            print(f"✅ Successfully created: {english_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error translating {post_dir.name}: {e}")
            return False
    
    def split_content(self, content, max_chunk_size=2000):
        """Split content into smaller chunks for translation"""
        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def create_english_content(self, frontmatter, body):
        """Create English markdown content"""
        # Convert frontmatter to YAML
        yaml_content = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        
        return f"---\n{yaml_content}---\n\n{body}\n"
    
    def run(self, args):
        """Main execution method"""
        if args.all:
            # Translate all posts
            posts = self.find_posts_to_translate()
            if not posts:
                print("✅ All posts already have English versions!")
                return
            
            print(f"📚 Found {len(posts)} posts to translate:")
            for post in posts[:5]:  # Show first 5
                print(f"   - {post.name}")
            if len(posts) > 5:
                print(f"   ... and {len(posts) - 5} more")
            
            confirm = input(f"\n🤔 Translate all {len(posts)} posts? (y/N): ").lower()
            if confirm != 'y':
                print("❌ Translation cancelled")
                return
            
            success_count = 0
            for i, post in enumerate(posts, 1):
                print(f"\n📖 [{i}/{len(posts)}] Processing: {post.name}")
                if self.translate_post(post):
                    success_count += 1
                
            print(f"\n🎉 Translation complete! {success_count}/{len(posts)} posts translated successfully.")
            
        elif args.latest:
            # Translate latest post
            latest_post = self.get_latest_post()
            if not latest_post:
                print("❌ No posts found!")
                return
                
            print(f"📖 Latest post: {latest_post.name}")
            english_file = latest_post / "index.en.md"
            if english_file.exists():
                print("⚠️  English version already exists!")
                return
                
            self.translate_post(latest_post)
            
        elif args.post_directory:
            # Translate specific post
            post_dir = Path(args.post_directory)
            if not post_dir.exists():
                print(f"❌ Directory not found: {post_dir}")
                return
                
            self.translate_post(post_dir)
        else:
            print("❌ Please specify --all, --latest, or a post directory")

def main():
    parser = argparse.ArgumentParser(description='Auto translate Chinese blog posts to English')
    parser.add_argument('post_directory', nargs='?', help='Specific post directory to translate')
    parser.add_argument('--all', action='store_true', help='Translate all posts without English version')
    parser.add_argument('--latest', action='store_true', help='Translate the latest post')
    
    args = parser.parse_args()
    
    if not any([args.all, args.latest, args.post_directory]):
        parser.print_help()
        return
    
    print("🚀 Blog Auto Translator")
    print("=" * 50)
    
    translator = BlogTranslator()
    translator.run(args)

if __name__ == "__main__":
    main()
