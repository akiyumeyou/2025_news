"""
情報収集ソースの設定
"""

# RSSフィードソース（生成AI特化）
RSS_SOURCES = [
    # 生成AI企業ブログ
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "category": "content_gen",
        "priority": "high"
    },
    {
        "name": "Google AI Blog",
        "url": "https://ai.googleblog.com/feeds/posts/default",
        "category": "content_gen",
        "priority": "high"
    },
    {
        "name": "Anthropic Blog",
        "url": "https://www.anthropic.com/feed.xml",
        "category": "content_gen",
        "priority": "high"
    },
    {
        "name": "Meta AI Blog",
        "url": "https://ai.meta.com/blog/rss/",
        "category": "content_gen",
        "priority": "high"
    },
    
    # プログラミング・開発
    {
        "name": "GitHub Blog",
        "url": "https://github.blog/feed/",
        "category": "code_gen",
        "priority": "high"
    },
    {
        "name": "Stack Overflow Blog",
        "url": "https://stackoverflow.blog/feed/",
        "category": "code_gen",
        "priority": "medium"
    },
    {
        "name": "Microsoft DevBlogs",
        "url": "https://devblogs.microsoft.com/feed/",
        "category": "code_gen",
        "priority": "medium"
    },
    
    # 技術ニュース
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "category": "general",
        "priority": "medium"
    },
    {
        "name": "VentureBeat",
        "url": "https://venturebeat.com/feed/",
        "category": "general",
        "priority": "medium"
    }
]

# APIソース（ニュースAPIなど）
API_SOURCES = [
    {
        "name": "NewsAPI",
        "base_url": "https://newsapi.org/v2/everything",
        "api_key_env": "NEWS_API_KEY",
        "params": {
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5
        },
        "keywords": [
            "code generation", "GitHub Copilot", "Claude Code", "Cursor",
            "DALL-E", "Midjourney", "Stable Diffusion", "Runway", "Sora",
            "business automation", "Microsoft Copilot", "AI in education",
            "AI safety", "AI regulation", "responsible AI"
        ]
    },
    # 日本語キーワードでNewsAPIを使用
    {
        "name": "NewsAPI Japan",
        "base_url": "https://newsapi.org/v2/everything",
        "api_key_env": "NEWS_API_KEY",
        "params": {
            "language": "ja",
            "sortBy": "publishedAt",
            "pageSize": 5
        },
        "keywords": [
            "コード生成", "GitHub Copilot", "Claude Code", "画像生成",
            "業務自動化", "教育AI", "AI安全性", "AI規制"
        ]
    }
]

# Webスクレイピング対象サイト（無料で利用可能）
SCRAPING_SOURCES = [
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/",
        "selector": "tr.athing",
        "title_selector": "span.titleline > a",
        "link_selector": "span.titleline > a",
        "category": "general",
        "priority": "high"
    },
    {
        "name": "Reddit r/artificial",
        "url": "https://www.reddit.com/r/artificial/",
        "selector": "div[data-testid='post-container']",
        "title_selector": "h3",
        "link_selector": "a[data-testid='post-title']",
        "category": "AI",
        "priority": "high"
    },
    {
        "name": "Reddit r/MachineLearning",
        "url": "https://www.reddit.com/r/MachineLearning/",
        "selector": "div[data-testid='post-container']",
        "title_selector": "h3",
        "link_selector": "a[data-testid='post-title']",
        "category": "AI",
        "priority": "high"
    }
]

# 追加の情報収集方法（生成AI特化）
ADDITIONAL_SOURCES = {
    # 学術論文（arXiv）
    "arxiv": {
        "name": "arXiv Generative AI Papers",
        "url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+(generative+OR+diffusion+OR+transformer)&sortBy=lastUpdatedDate&sortOrder=descending&max_results=5",
        "category": "content_gen",
        "priority": "high"
    },
    
    # GitHub Trending
    "github_trending": {
        "name": "GitHub Trending AI",
        "url": "https://github.com/trending?since=daily&q=AI",
        "category": "code_gen",
        "priority": "medium"
    },
    
    # 技術ブログ
    "tech_blogs": [
        {
            "name": "Towards Data Science",
            "url": "https://towardsdatascience.com/tagged/generative-ai",
            "category": "content_gen",
            "priority": "medium"
        },
        {
            "name": "Medium AI",
            "url": "https://medium.com/tag/generative-ai",
            "category": "content_gen",
            "priority": "medium"
        }
    ]
}

# 収集設定
COLLECTION_CONFIG = {
    "max_articles_per_source": 5,  # テスト用に5件に制限
    "min_date": "7 days ago",  # 過去7日間の記事のみ
    "duplicate_threshold": 0.8,  # 重複判定の閾値
    "language_filter": ["en", "ja"],  # 英語と日本語のみ
    "exclude_keywords": [
        "sponsored", "advertisement", "promoted",
        "clickbait", "fake news", "広告", "宣伝", "スポンサード"
    ]
} 