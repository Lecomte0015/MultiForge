import { GetServerSideProps } from 'next'
import { createPagesServerClient } from '../../lib/supabase/server-pages'
import Head from 'next/head'
import Link from 'next/link'
import { Sparkles, Plus, Video, Calendar } from 'lucide-react'

interface Project {
    id: string
    title: string
    status: string
    created_at: string
}

interface DashboardProps {
    projects: Project[]
    user: any
}

export const getServerSideProps: GetServerSideProps = async (context) => {
    const supabase = createPagesServerClient(context)

    const { data: { user } } = await supabase.auth.getUser()

    if (!user) {
        return {
            redirect: {
                destination: '/auth',
                permanent: false,
            },
        }
    }

    // Fetch projects
    const { data: projects } = await supabase
        .from('projects')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })

    return {
        props: {
            projects: projects || [],
            user
        },
    }
}

export default function Dashboard({ projects, user }: DashboardProps) {
    return (
        <div className="min-h-screen bg-black text-white">
            <Head>
                <title>Dashboard - MultiForge</title>
            </Head>

            {/* Navbar */}
            <nav className="border-b border-slate-800 p-4 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
                <div className="max-w-7xl mx-auto flex justify-between items-center">
                    <div className="flex items-center gap-2 font-black text-xl tracking-tighter">
                        <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                            <Sparkles className="w-5 h-5 text-white" />
                        </div>
                        MultiForge
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="text-sm text-slate-400 hidden md:block">
                            {user.email}
                        </div>
                        <Link href="/studio">
                            <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition-colors">
                                <Plus className="w-4 h-4" />
                                Nouveau Projet
                            </button>
                        </Link>
                    </div>
                </div>
            </nav>

            <main className="max-w-7xl mx-auto p-6 md:p-10">
                <div className="flex justify-between items-end mb-8">
                    <h1 className="text-3xl font-bold">Mes Projets</h1>
                </div>

                {projects.length === 0 ? (
                    <div className="border border-dashed border-slate-800 rounded-2xl p-12 flex flex-col items-center justify-center text-center bg-slate-900/20">
                        <div className="w-16 h-16 bg-slate-800/50 rounded-full flex items-center justify-center mb-4">
                            <Video className="w-8 h-8 text-slate-500" />
                        </div>
                        <h3 className="text-xl font-semibold mb-2">Aucun projet pour le moment</h3>
                        <p className="text-slate-400 max-w-md mb-6">
                            Commencez à créer des vidéos virales en quelques secondes grâce à l'IA.
                        </p>
                        <Link href="/studio">
                            <button className="bg-white text-black px-6 py-3 rounded-lg font-bold hover:bg-slate-200 transition-colors flex items-center gap-2">
                                <Sparkles className="w-4 h-4" />
                                Créer ma première vidéo
                            </button>
                        </Link>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {projects.map((project) => (
                            <div key={project.id} className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden hover:border-purple-500/50 transition-all group">
                                <div className="aspect-video bg-slate-950 relative flex items-center justify-center">
                                    {/* Thumbnail placeholder */}
                                    <Video className="w-12 h-12 text-slate-800" />
                                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                        <button className="bg-white text-black px-4 py-2 rounded-lg font-bold text-sm transform scale-95 group-hover:scale-100 transition-transform">
                                            Ouvrir
                                        </button>
                                    </div>
                                </div>
                                <div className="p-4">
                                    <h3 className="font-semibold truncate">{project.title}</h3>
                                    <div className="flex justify-between items-center mt-2 text-xs text-slate-400">
                                        <span className={`px-2 py-1 rounded-full ${project.status === 'completed' ? 'bg-green-500/10 text-green-500' : 'bg-slate-800 text-slate-400'
                                            }`}>
                                            {project.status.toUpperCase()}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Calendar className="w-3 h-3" />
                                            {new Date(project.created_at).toLocaleDateString()}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    )
}
