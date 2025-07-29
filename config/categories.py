"""
AI情報のカテゴリ定義
"""

CATEGORIES = {
    "breakthrough": {
        "name": "🚀 AI技術ブレークスルー",
        "description": "革新的なAI技術、研究成果、新手法など",
        "keywords": [
            "breakthrough", "research", "paper", "arxiv", "new model",
            "algorithm", "neural network", "transformer", "diffusion",
            "language model", "multimodal", "AGI", "artificial general intelligence",
            "GPT", "LLM", "foundation model", "vision transformer"
        ]
    },
    "llm_chatbot": {
        "name": "🤖 主要LLMアップデート",
        "description": "ChatGPT、Claude、Geminiなどの言語モデルとチャットボット",
        "keywords": [
            "ChatGPT", "GPT-4", "Claude", "Gemini", "Bard", 
            "language model", "LLM", "chatbot", "conversational AI",
            "OpenAI", "Anthropic", "Google AI", "dialogue system",
            "prompt engineering", "in-context learning"
        ]
    },
    "design_ai": {
        "name": "🎨 デザイン・UI/UX AI",
        "description": "エンジニア向けUI/UXデザイン支援、プロトタイピング、デザインシステム",
        "keywords": [
            "Figma AI", "Framer", "v0", "Galileo AI", "Uizard",
            "UI generation", "UX design", "prototype", "wireframe",
            "design system", "component library", "design tokens",
            "responsive design", "mobile design", "web design",
            "user interface", "user experience", "accessibility",
            "design automation", "layout generation", "color palette",
            "typography", "icon generation", "design handoff",
            "React components", "Vue components", "CSS generation",
            "Tailwind CSS", "styled-components", "design to code"
        ]
    },
    "generative_ai": {
        "name": "🖼️ 画像・動画生成AI",
        "description": "画像・動画・音楽生成、クリエイティブAIツール",
        "keywords": [
            "DALL-E", "Midjourney", "Stable Diffusion", "Sora", "Runway",
            "image generation", "video generation", "music generation",
            "text-to-image", "text-to-video", "creative AI", "art AI",
            "generative model", "diffusion model", "GAN",
            "image synthesis", "video synthesis", "audio synthesis",
            "multimodal generation", "content creation", "creative tools"
        ]
    },
    "programming_tools": {
        "name": "💻 プログラミングツール・開発環境",
        "description": "エンジニア向けの開発ツール、IDE、フレームワーク、ライブラリのアップデートや新機能",
        "keywords": [
            "GitHub Copilot", "Cursor", "Claude Code", "Codeium", "Tabnine",
            "VS Code", "JetBrains", "Replit", "CodeSandbox", "Vercel",
            "Next.js", "React", "Vue", "Angular", "Node.js", "Python",
            "Docker", "Kubernetes", "Git", "GitHub", "GitLab",
            "pricing", "subscription", "free tier", "enterprise",
            "version update", "new features", "beta", "stable release",
            "IDE extension", "plugin", "developer experience", "DX",
            "code completion", "AI assistant", "pair programming",
            "debugging tools", "testing framework", "CI/CD"
        ]
    },
    "ai_coding": {
        "name": "🤖 AIコーディング・開発支援",
        "description": "AI搭載のコード生成、プログラミング支援、自動化ツール",
        "keywords": [
            "code generation", "AI coding", "programming assistant",
            "automated coding", "code review", "refactoring",
            "unit test generation", "documentation generation",
            "code explanation", "code completion", "intelligent search",
            "bug detection", "security scanning", "performance optimization"
        ]
    },
    "business_enterprise": {
        "name": "🏢 ビジネス・企業AI",
        "description": "企業のAI導入、業務自動化、AIエージェント",
        "keywords": [
            "enterprise AI", "business AI", "automation", "AI agent",
            "workflow", "productivity", "Microsoft Copilot", "ChatGPT Enterprise",
            "AI assistant", "customer service", "analytics", "insights"
        ]
    },
    "hardware_chip": {
        "name": "🔧 AIハードウェア・チップ",
        "description": "GPU、TPU、AI専用チップ、エッジAI",
        "keywords": [
            "GPU", "TPU", "AI chip", "NVIDIA", "hardware", "edge AI",
            "inference", "training", "compute", "semiconductor",
            "accelerator", "neural processing unit", "NPU"
        ]
    },
    "regulation_ethics": {
        "name": "⚖️ AI規制・倫理・安全性",
        "description": "AI規制、倫理問題、安全性、バイアス対策",
        "keywords": [
            "AI regulation", "ethics", "bias", "fairness", "safety",
            "responsible AI", "AI governance", "policy", "law",
            "privacy", "security", "alignment", "AI safety"
        ]
    },
    "ai_trends": {
        "name": "📊 AI業界トレンド・総括",
        "description": "AI業界全体の動向、市場分析、将来予測、業界レポート",
        "keywords": [
            "AI market", "industry trend", "market analysis", "forecast",
            "adoption rate", "AI transformation", "enterprise adoption",
            "AI investment", "market size", "growth prediction",
            "AI strategy", "competitive landscape", "industry report",
            "technology roadmap", "emerging trends", "AI maturity",
            "industry survey", "benchmark", "AI readiness"
        ]
    },
    "startups_funding": {
        "name": "💰 AIスタートアップ・資金調達",
        "description": "AI関連の投資、資金調達、新興企業、事業支援",
        "keywords": [
            "funding", "investment", "startup", "venture capital",
            "IPO", "acquisition", "merger", "valuation",
            "AI company", "unicorn", "series A", "series B"
        ]
    }
}

# 重要度評価の基準（生成AI特化）
IMPORTANCE_CRITERIA = {
    "high": {
        "score": 3,
        "description": "生成AI研究者が必ず知っておくべき重要な情報",
        "indicators": [
            "生成AIのブレークスルー技術", "OpenAI、Google、Metaの重要な発表",
            "学術的な重要な発見", "コード生成・コンテンツ生成の革新的技術",
            "新しい生成モデルの発表", "大規模言語モデルの重要なアップデート"
        ]
    },
    "medium": {
        "score": 2,
        "description": "生成AI研究者が知っておくと良い情報",
        "indicators": [
            "生成AI技術の進歩", "新しい生成AIツール・サービス",
            "コード生成・コンテンツ生成の市場動向", "生成AI関連の投資・資金調達",
            "生成AIの実用応用事例", "生成AIの倫理・安全性に関する議論"
        ]
    },
    "low": {
        "score": 1,
        "description": "参考程度の情報",
        "indicators": [
            "一般的なAIニュース", "軽微なアップデート",
            "生成AIの一般的な動向", "エンターテイメント分野でのAI活用"
        ]
    }
} 