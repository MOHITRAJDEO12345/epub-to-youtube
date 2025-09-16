import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_chapters(epub_path):
    """
    Extracts chapters from an ePub file.
    Returns a list of tuples, where each tuple is (chapter_title, chapter_content).
    """
    print("📚 Reading ePub file...")
    book = epub.read_epub(epub_path)
    chapters = []
    
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = item.get_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract text, removing extra whitespace
        text = soup.get_text(strip=True, separator='\n')
        
        # Try to find a title, otherwise use a generic name
        title_tag = soup.find(['h1', 'h2', 'h3'])
        title = title_tag.get_text(strip=True) if title_tag else f"Chapter_{len(chapters) + 1}"
        
        if text.strip(): # Only add chapters with actual content
            chapters.append((title, text))
            print(f"  - Found Chapter: {title}")
            
    print(f"✅ Found {len(chapters)} chapters in total.")
    return chapters