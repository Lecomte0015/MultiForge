import { create } from 'zustand';

interface JobState {
  jobId: string | null;
  status: 'IDLE' | 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  progress: number;
  currentStep: string;
  logs: string[];
  resultVideoUrl: string | null;

  // Wizard Data
  topic: string;
  scriptContent: string;
  visualStyle: 'cinematic' | 'minimalist' | 'chaos' | 'corporate';
  platform: 'tiktok' | 'youtube' | 'instagram';

  // Actions
  setJobId: (id: string) => void;
  updateStatus: (data: Partial<JobState>) => void;
  setWizardData: (key: keyof JobState, value: any) => void;
  reset: () => void;
}

export const useJobStore = create<JobState>((set) => ({
  jobId: null,
  status: 'IDLE',
  progress: 0,
  currentStep: '',
  logs: [],
  resultVideoUrl: null,

  topic: '',
  scriptContent: '',
  visualStyle: 'cinematic',
  platform: 'tiktok',

  setJobId: (id) => set({ jobId: id, status: 'PENDING' }),

  updateStatus: (data) => set((state) => ({ ...state, ...data })),

  setWizardData: (key, value) => set((state) => ({ ...state, [key]: value })),

  reset: () => set({
    jobId: null,
    status: 'IDLE',
    progress: 0,
    logs: [],
    resultVideoUrl: null,
    topic: '',
    scriptContent: ''
  })
}));