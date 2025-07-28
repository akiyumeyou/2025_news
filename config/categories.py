"""
AI情報のカテゴリ定義（5グループ連動型カテゴリ設計）
"""

CATEGORIES = {
    "code_gen": {
        "name": "🚀 コード生成・開発支援",
        "description": "Claude CodeやGitHub Copilotなどによるコード生成、自動補完、AIペアプロなど",
        "keywords": [
            "code generation", "GitHub Copilot", "Claude Code", "Cursor", 
            "AI coding", "pair programming", "code completion", "code assistant", 
            "IDE", "Tabnine", "Codeium", "LLM for coding", "programming assistant",
            "autocomplete", "development tools", "code review", "debugging assistant",
            "vibecode", "vibe code", "software development", "coding AI"
        ]
    },
    "content_gen": {
        "name": "🎨 コンテンツ生成（テキスト・画像・音声・動画）",
        "description": "テキストから画像・動画・音楽などを生成するAI。MidjourneyやRunwayなどの活用例を含む",
        "keywords": [
            "DALL-E", "Midjourney", "Stable Diffusion", "Runway", "Sora", 
            "text-to-image", "text-to-video", "audio generation", "creative AI", 
            "generative art", "prompt art", "image synthesis", "video synthesis",
            "music generation", "content creation", "creative tools", "art AI",
            "diffusion model", "GAN", "generative model", "multimodal generation"
        ]
    },
    "business_ai": {
        "name": "🏢 ビジネス業務支援AI",
        "description": "CopilotやZapier、Notion AIなど、業務自動化や生産性向上に寄与するAI技術・導入事例",
        "keywords": [
            "business automation", "Microsoft Copilot", "AI assistant", 
            "ChatGPT Enterprise", "workflow automation", "CRM AI", "sales AI", 
            "productivity", "task automation", "RPA", "Zapier", "n8n",
            "business intelligence", "enterprise AI", "workflow optimization",
            "Notion AI", "automation tools", "business process"
        ]
    },
    "edu_ai": {
        "name": "📘 教育・専門特化型AI",
        "description": "教育現場、リスキリング、専門スキル習得のためのAI活用。教育特化LLMや教材生成など",
        "keywords": [
            "AI in education", "personalized learning", "tutor bot", "EdTech", 
            "Socratic", "Khanmigo", "adaptive learning", "curriculum generation", 
            "skill assessment", "AI教材", "教育AI", "learning assistant",
            "educational technology", "training AI", "knowledge transfer",
            "Khan Academy", "Coursera AI", "learning platform"
        ]
    },
    "ai_safety": {
        "name": "🔐 セキュリティ・倫理・AIガバナンス",
        "description": "AIの安全性・倫理・規制に関する動向（規制動向・バイアス・フェイク生成リスク含む）",
        "keywords": [
            "AI safety", "alignment", "hallucination", "bias", "fairness", 
            "AI ethics", "AI regulation", "responsible AI", "EU AI Act", 
            "GPT risk", "AI misuse", "deepfake", "misinformation", 
            "AI governance", "policy", "privacy", "security", "AI Act",
            "regulatory", "compliance", "transparency"
        ]
    }
}

# 重要度評価の基準（5グループ連動型に特化）
IMPORTANCE_CRITERIA = {
    "high": {
        "score": 3,
        "description": "AI開発者・研究者が必ず知っておくべき重要な情報",
        "indicators": [
            "コード生成・開発支援の革新的技術", "コンテンツ生成の画期的進歩",
            "ビジネス業務支援AIの重要な導入事例", "教育AI分野の重要な進展",
            "AI安全性・倫理・規制の重要な動向", "大手企業の重要発表"
        ]
    },
    "medium": {
        "score": 2,
        "description": "AI開発者・研究者が知っておくと良い情報",
        "indicators": [
            "新しいAI開発ツール・サービス", "コンテンツ生成技術の改善",
            "ビジネスAIの実用応用事例", "教育AI技術の進歩",
            "AI倫理・安全性に関する議論", "市場動向・投資情報"
        ]
    },
    "low": {
        "score": 1,
        "description": "参考程度の情報",
        "indicators": [
            "一般的なAIニュース", "軽微なアップデート",
            "AI分野の一般的な動向", "エンターテイメント分野でのAI活用"
        ]
    }
}