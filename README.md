# MultiForge

AI-powered video generation SaaS platform with hybrid Pexels/Runway integration, GPT-4 script extraction, and ElevenLabs voice synthesis.

## 🚀 Features

- **Hybrid Video Generation**: Intelligent routing between Pexels (stock footage) and Runway Gen-4 (AI generation)
- **Smart Script Extraction**: GPT-4 automatically extracts voice scripts from complex prompts
- **Voice Synthesis**: High-quality text-to-speech with ElevenLabs
- **Professional Editing**: MoviePy-based video editing with subtitles
- **Lip-Sync Ready**: D-ID integration for talking avatars (optional)
- **Fast Backend**: FastAPI with lazy loading for instant startup
- **Modern Frontend**: Next.js with TypeScript and Tailwind CSS
- **Secure Auth**: Supabase authentication and storage

## 💰 Cost Efficiency

**Per 60-second video**:
- OpenAI (GPT-4): $0.03
- Runway (AI generation): $0.30
- ElevenLabs (voice): $0.05
- **Total**: ~$0.38/video

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **AI Services**: OpenAI GPT-4, Runway Gen-4, ElevenLabs, D-ID
- **Video Processing**: MoviePy, OpenCV, FFmpeg
- **ML**: PyTorch, librosa, numba
- **Database**: Supabase (PostgreSQL)

### Frontend
- **Framework**: Next.js 13+
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: Zustand
- **Auth**: Supabase Auth

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- FFmpeg
- Supabase account

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your API keys
```

Run backend:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
```

Create `.env.local`:
```bash
cp .env.local.example .env.local
# Edit .env.local with your Supabase credentials
```

Run frontend:
```bash
npm run dev
```

## 🔑 Required API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **ElevenLabs**: https://elevenlabs.io/
- **Pexels**: https://www.pexels.com/api/
- **Runway**: https://app.runwayml.com/ (optional)
- **D-ID**: https://studio.d-id.com/ (optional)
- **Supabase**: https://supabase.com/

## 📖 Usage

1. Navigate to `http://localhost:3000`
2. Sign up / Log in
3. Go to Studio
4. Enter your video topic or detailed prompt
5. Wait for generation (~2-5 minutes)
6. Download your video!

## 🎯 Roadmap

- [x] Hybrid video generation (Pexels + Runway)
- [x] Script extraction with GPT-4
- [x] Voice synthesis with ElevenLabs
- [x] Professional video editing
- [ ] Lip-sync with D-ID/Wav2Lip
- [ ] Video history dashboard
- [ ] Credit system
- [ ] Stripe integration
- [ ] Production deployment

## 📝 License

MIT

## 👨‍💻 Author

Dally Hermann (@Lecomte0015)

## 🙏 Acknowledgments

- OpenAI for GPT-4
- Runway for Gen-4 video generation
- ElevenLabs for voice synthesis
- Pexels for stock footage
- Supabase for backend infrastructure
