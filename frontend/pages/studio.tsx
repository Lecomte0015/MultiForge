import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { useJobStore } from '../state/jobStore';
import { Sparkles, Video, CheckCircle2, FileText, Palette, Smartphone, Youtube, Instagram, Wand2, ArrowRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// --- MOCK AI FUNCTION ---
const generateMockScript = (topic: string) => {
  return `**Titre:** ${topic} : La Vérité Cachée 🤫

**Accroche (0-3s):**
Vous ne devinerez jamais ce qui se cache derrière ${topic}. C'est hallucinant.

**Corps (3-40s):**
La plupart des gens pensent que c'est compliqué. Mais en fait, il suffit de connaître cette astuce simple.
Regardez ça : c'est exactement pour ça que les experts ne veulent pas que vous sachiez.

**Appel à l'action (40-60s):**
Abonne-toi pour la partie 2, je vais tout révéler !`;
};

// --- COMPONENTS ---

// 1. Topic & Platform
const StepTopic = ({ onNext }: { onNext: () => void }) => {
  const { setWizardData, topic, platform } = useJobStore();

  const handleGenerate = () => {
    if (!topic) return;
    // Simulate AI generation delay
    setTimeout(() => {
      const mockScript = generateMockScript(topic);
      setWizardData('scriptContent', mockScript);
      onNext();
    }, 800);
  };

  return (
    <div className="max-w-3xl mx-auto mt-20 text-center">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-4xl md:text-6xl font-black mb-4 bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-500">
          La Forge
        </h1>
        <p className="text-xl text-slate-400 mb-10">Quel sujet voulez-vous explorer aujourd'hui ?</p>

        {/* Platform Selection */}
        <div className="flex justify-center gap-4 mb-8">
          {[
            { id: 'tiktok', icon: Smartphone, label: 'TikTok' },
            { id: 'youtube', icon: Youtube, label: 'Shorts' },
            { id: 'instagram', icon: Instagram, label: 'Reels' }
          ].map((p) => (
            <button
              key={p.id}
              onClick={() => setWizardData('platform', p.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl border-2 transition-all ${platform === p.id
                ? 'border-purple-500 bg-purple-500/10 text-white'
                : 'border-slate-800 bg-slate-900 text-slate-400 hover:border-slate-700'
                }`}
            >
              <p.icon className="w-5 h-5" />
              <span className="font-bold">{p.label}</span>
            </button>
          ))}
        </div>

        <div className="relative group max-w-2xl mx-auto">
          <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
          <div className="relative flex bg-slate-900 rounded-lg p-2">
            <input
              type="text"
              value={topic}
              onChange={(e) => setWizardData('topic', e.target.value)}
              placeholder="Ex: Les 5 secrets de la productivité..."
              className="flex-1 bg-transparent text-white p-4 text-lg outline-none placeholder-slate-500"
              onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
            />
            <button
              onClick={handleGenerate}
              className="bg-white text-black px-8 py-2 rounded font-bold hover:bg-slate-200 transition-colors flex items-center gap-2"
            >
              <Wand2 className="w-5 h-5" />
              Générer
            </button>
          </div>
        </div>

        <div className="flex gap-3 mt-6 justify-center flex-wrap">
          {["Faits Historiques", "Motivation Sport", "Tech News", "Voyage"].map(tag => (
            <button
              key={tag}
              onClick={() => setWizardData('topic', tag)}
              className="px-4 py-2 rounded-full bg-slate-800 hover:bg-slate-700 text-sm text-slate-300 transition-colors border border-slate-700"
            >
              {tag}
            </button>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

// 2. Script Editor
const StepScript = ({ onNext, onBack }: { onNext: () => void, onBack: () => void }) => {
  const { scriptContent, setWizardData } = useJobStore();

  return (
    <div className="max-w-4xl mx-auto mt-10 h-[calc(100vh-200px)] flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-3xl font-bold">Éditeur de Script</h2>
          <p className="text-slate-400">Vérifiez et ajustez le contenu généré par l'IA.</p>
        </div>
        <button onClick={onNext} className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-bold flex items-center gap-2">
          Validé <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      <div className="flex-1 bg-slate-900 rounded-xl border border-slate-800 p-6 shadow-2xl overflow-hidden flex flex-col">
        <textarea
          value={scriptContent}
          onChange={(e) => setWizardData('scriptContent', e.target.value)}
          className="flex-1 bg-transparent text-slate-200 text-lg leading-relaxed outline-none resize-none font-medium"
          placeholder="Le script apparaîtra ici..."
        />
      </div>

      <button onClick={onBack} className="mt-4 text-slate-500 hover:text-white self-start">
        ← Retour
      </button>
    </div>
  );
};

// 3. Visual Style
const StepVisuals = ({ onNext, onBack }: { onNext: () => void, onBack: () => void }) => {
  const { setWizardData, visualStyle } = useJobStore();

  const styles = [
    { id: 'cinematic', label: 'Cinématique', desc: 'Haut contraste, images épiques, lent.' },
    { id: 'minimalist', label: 'Minimaliste', desc: 'Ultra-propre, blanc/noir, moderne.' },
    { id: 'chaos', label: 'Chaos (TikTok)', desc: 'Rapide, glitchs, saturé, viral.' },
    { id: 'corporate', label: 'Corporate', desc: 'Professionnel, stock business, bleu.' },
  ];

  return (
    <div className="max-w-4xl mx-auto mt-16 text-center">
      <h2 className="text-3xl font-bold mb-2">Style Visuel</h2>
      <p className="text-slate-400 mb-10">Quelle ambiance pour votre vidéo ?</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
        {styles.map((s) => (
          <div
            key={s.id}
            onClick={() => setWizardData('visualStyle', s.id)}
            className={`p-6 border-2 rounded-xl cursor-pointer text-left transition-all bg-slate-900 ${visualStyle === s.id
              ? 'border-purple-500 ring-2 ring-purple-500/20'
              : 'border-slate-800 hover:border-slate-700'
              }`}
          >
            <h3 className="text-xl font-bold mb-1">{s.label}</h3>
            <p className="text-sm text-slate-400">{s.desc}</p>
          </div>
        ))}
      </div>

      <div className="flex gap-4 justify-center">
        <button onClick={onBack} className="px-8 py-3 rounded-lg font-bold border border-slate-700 text-slate-300 hover:bg-slate-800">
          Retour
        </button>
        <button onClick={onNext} className="px-10 py-3 bg-white text-black rounded-lg font-bold hover:bg-slate-200 flex items-center gap-2">
          <Video className="w-5 h-5" />
          Lancer la Production
        </button>
      </div>
    </div>
  );
};


// 4. Loading (Compatible with existing polling)
const StepLoading = () => {
  const { logs, progress, currentStep } = useJobStore();

  return (
    <div className="max-w-2xl mx-auto mt-20">
      <div className="bg-slate-950 border border-slate-800 rounded-lg p-6 font-mono text-sm min-h-[300px] flex flex-col relative overflow-hidden shadow-2xl shadow-purple-900/20">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-purple-500/5 to-transparent opacity-20 pointer-events-none animate-pulse-slow" />

        <div className="flex-1 space-y-2 z-10">
          {logs.map((log, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="text-green-400"
            >
              {`> ${log}`}
            </motion.div>
          ))}
          <motion.div
            animate={{ opacity: [0, 1, 0] }}
            transition={{ repeat: Infinity, duration: 0.8 }}
            className="text-purple-500"
          >
            _
          </motion.div>
        </div>

        <div className="mt-6 pt-4 border-t border-slate-800 z-10">
          <div className="flex justify-between mb-2 text-xs text-slate-400 uppercase tracking-widest">
            <span>Status: {currentStep}</span>
            <span>{progress}%</span>
          </div>
          <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-purple-500"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>
      <p className="text-center text-slate-500 mt-6 text-sm">MultiForge assemble votre contenu. Ne fermez pas cet onglet.</p>
    </div>
  );
};

// 5. Result
const StepResult = () => {
  const { resultVideoUrl } = useJobStore();

  // Handle relative static paths from backend
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const fullUrl = resultVideoUrl?.startsWith('http')
    ? resultVideoUrl
    : `${apiUrl}${resultVideoUrl}`;

  return (
    <div className="flex flex-col items-center justify-center p-10 text-center">
      <h2 className="text-3xl font-bold mb-6">Vidéo Terminée !</h2>
      <div className="bg-black border border-slate-800 rounded-2xl overflow-hidden shadow-2xl max-w-md w-full">
        {fullUrl ? (
          <video src={fullUrl} controls className="w-full" autoPlay loop />
        ) : (
          <div className="p-10 text-slate-500">Erreur vidéo</div>
        )}
      </div>
      <div className="mt-8 flex gap-4">
        <button onClick={() => window.location.reload()} className="px-6 py-2 bg-slate-800 rounded-lg text-white hover:bg-slate-700">Nouveau Projet</button>
        <button
          onClick={() => window.open(fullUrl, '_blank')}
          className="px-6 py-2 bg-purple-600 rounded-lg text-white font-bold hover:bg-purple-700 flex items-center gap-2"
        >
          <Video className="w-4 h-4" />
          Télécharger
        </button>
      </div>
    </div>
  )
}

// --- MAIN PAGE ---

export default function Studio() {
  const [step, setStep] = useState<number>(1);
  const {
    jobId, status, setJobId, updateStatus,
    topic, scriptContent, visualStyle, platform, reset
  } = useJobStore();

  // Polling Logic
  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (jobId && status !== 'COMPLETED' && status !== 'FAILED') {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/jobs/${jobId}`);
          const data = await res.json();

          updateStatus({
            status: data.status,
            progress: data.progress,
            currentStep: data.current_step,
            logs: data.logs,
            resultVideoUrl: data.result_video_url,
          });

          if (data.status === 'COMPLETED') {
            setStep(5);
          }
        } catch (err) {
          console.error("Polling error", err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [jobId, status, updateStatus]);

  const startGeneration = async () => {
    setStep(4);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/create-video`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic,
          script: scriptContent, // We send the edited script now!
          visual_style: visualStyle,
          platform: platform,
          avatar_id: 'none', // Faceless override
          voice_id: 'pNInz6obpgDQGcFmaJgB', // Adam Voice ID
        })
      });
      const data = await res.json();
      setJobId(data.job_id);
    } catch (err) {
      console.error("Failed to start job", err);
      setStep(3);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-purple-500/30">
      <Head>
        <title>MultiForge Studio</title>
      </Head>

      <header className="border-b border-slate-800 p-4 flex justify-between items-center bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2 font-black text-xl tracking-tighter">
          <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          MultiForge
        </div>
        {step !== 1 && (
          <div className="text-sm font-mono text-slate-500">
            STEP {step}/4
          </div>
        )}
      </header>

      <main className="p-4">
        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.div key="1" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <StepTopic onNext={() => setStep(2)} />
            </motion.div>
          )}
          {step === 2 && (
            <motion.div key="2" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <StepScript onNext={() => setStep(3)} onBack={() => setStep(1)} />
            </motion.div>
          )}
          {step === 3 && (
            <motion.div key="3" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <StepVisuals onNext={startGeneration} onBack={() => setStep(2)} />
            </motion.div>
          )}
          {step === 4 && (
            <motion.div key="4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <StepLoading />
            </motion.div>
          )}
          {step === 5 && (
            <motion.div key="5" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <StepResult />
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}