import { useState } from 'react'
import { createClient } from '../lib/supabase/client'
import { useRouter } from 'next/router'
import Head from 'next/head'
import { Sparkles } from 'lucide-react'

export default function Auth() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [isSignUp, setIsSignUp] = useState(false)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const router = useRouter()
    const supabase = createClient()

    const handleAuth = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError(null)

        try {
            if (isSignUp) {
                const { error } = await supabase.auth.signUp({
                    email,
                    password,
                    options: {
                        emailRedirectTo: `${location.origin}/auth/callback`,
                    },
                })
                if (error) throw error
                alert('Check your email for the confirmation link!')
            } else {
                const { error } = await supabase.auth.signInWithPassword({
                    email,
                    password,
                })
                if (error) throw error
                router.push('/dashboard')
            }
        } catch (err: any) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-4">
            <Head>
                <title>Authentification - MultiForge</title>
            </Head>

            <div className="w-full max-w-md bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl">
                <div className="flex items-center gap-2 font-black text-2xl tracking-tighter mb-8 justify-center">
                    <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                        <Sparkles className="w-6 h-6 text-white" />
                    </div>
                    MultiForge
                </div>

                <h2 className="text-xl font-bold mb-6 text-center">
                    {isSignUp ? 'Créer un compte' : 'Connexion'}
                </h2>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded-lg mb-4 text-sm">
                        {error}
                    </div>
                )}

                <form onSubmit={handleAuth} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-1 text-slate-400">Email</label>
                        <input
                            type="email"
                            required
                            className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 focus:border-purple-500 outline-none transition-colors"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium mb-1 text-slate-400">Mot de passe</label>
                        <input
                            type="password"
                            required
                            className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 focus:border-purple-500 outline-none transition-colors"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? 'Chargement...' : (isSignUp ? "S'inscrire" : 'Se connecter')}
                    </button>
                </form>

                <div className="mt-6 text-center text-sm text-slate-400">
                    {isSignUp ? 'Déjà un compte ?' : "Pas encore de compte ?"}
                    <button
                        onClick={() => setIsSignUp(!isSignUp)}
                        className="text-purple-400 hover:text-purple-300 ml-2 font-medium"
                    >
                        {isSignUp ? 'Se connecter' : "S'inscrire"}
                    </button>
                </div>
            </div>
        </div>
    )
}
