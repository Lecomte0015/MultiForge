import Link from 'next/link';
import { Sparkles, PlayCircle, BarChart3, Video } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">

      {/* Grid Background */}
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none"></div>
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none"></div>

      {/* Nav */}
      <nav className="relative z-10 flex justify-between items-center p-6 max-w-7xl mx-auto w-full">
        <div className="font-bold text-xl flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          MultiForge
        </div>
        <div className="flex gap-6 text-sm font-medium text-slate-300 items-center">
          <Link href="/auth" className="hover:text-white transition">Connexion</Link>
          <Link href="/auth" className="text-black bg-white px-5 py-2 rounded-lg font-bold hover:bg-slate-200 transition">
            Commencer Gratuitement
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <main className="relative z-10 flex-1 flex flex-col items-center justify-center text-center px-4 pt-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-900/30 border border-purple-500/50 text-purple-300 text-sm font-medium mb-8 animate-fade-in-up">
          <Sparkles className="w-4 h-4" />
          Nouvelle IA V2 : Vidéos sans visage automatiques
        </div>

        <h1 className="text-5xl md:text-7xl font-black tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white via-white to-slate-500 max-w-4xl mx-auto leading-tight">
          Transformez une idée en <br />
          <span className="text-purple-500">Vidéo Virale</span> en 1 clic.
        </h1>

        <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
          Générez des scripts, voix-off et montages dynamiques sans jamais montrer votre visage.
          La forge de contenu ultime pour TikTok, Shorts et Reels.
        </p>

        <div className="flex flex-col md:flex-row gap-4 items-center">
          <Link
            href="/auth"
            className="bg-white text-black px-8 py-4 rounded-xl font-bold text-lg hover:scale-105 transition-transform shadow-[0_0_40px_-10px_rgba(255,255,255,0.3)] flex items-center gap-2"
          >
            <Sparkles className="w-5 h-5" />
            Créer ma première vidéo
          </Link>
          <button className="px-8 py-4 rounded-xl font-bold text-lg text-white border border-slate-800 hover:bg-slate-800 transition flex items-center gap-2">
            <PlayCircle className="w-5 h-5" /> Voir la Démo
          </button>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 max-w-5xl w-full text-left">
          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl">
            <div className="w-10 h-10 bg-purple-900/50 rounded-lg flex items-center justify-center mb-4 text-purple-400">
              <Video className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-lg mb-2">Montage Automatique</h3>
            <p className="text-slate-400 text-sm">Notre IA assemble B-Rolls, images et transitions pour un rendu professionnel instantané.</p>
          </div>
          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl">
            <div className="w-10 h-10 bg-blue-900/50 rounded-lg flex items-center justify-center mb-4 text-blue-400">
              <BarChart3 className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-lg mb-2">Optimisé Viralité</h3>
            <p className="text-slate-400 text-sm">Scripts calibrés pour la rétention et formats verticaux (9:16) prêts pour les réseaux.</p>
          </div>
          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl">
            <div className="w-10 h-10 bg-green-900/50 rounded-lg flex items-center justify-center mb-4 text-green-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-lg mb-2">100% Faceless</h3>
            <p className="text-slate-400 text-sm">Lancez une chaîne YouTube ou TikTok sans caméra ni microphone.</p>
          </div>
        </div>

        {/* Dashboard Preview Mockup */}
        <div className="mt-20 relative w-full max-w-5xl mx-auto rounded-t-2xl overflow-hidden border border-slate-800 bg-slate-900/50 shadow-2xl">
          <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent z-10"></div>
          {/* Placeholder for actual screenshot */}
          <div className="aspect-[16/9] bg-slate-950 flex items-center justify-center text-slate-700">
            Aperçu de l'interface Dashboard
          </div>
        </div>
      </main>
    </div>
  );
}