-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- PROFILES TABLE (Extends Supabase Auth)
create table profiles (
  id uuid references auth.users on delete cascade not null primary key,
  email text,
  full_name text,
  avatar_url text,
  credits integer default 10,
  tier text default 'free', -- 'free', 'pro', 'agency'
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- RLS for Profiles
alter table profiles enable row level security;
create policy "Public profiles are viewable by everyone." on profiles for select using ( true );
create policy "Users can insert their own profile." on profiles for insert with check ( auth.uid() = id );
create policy "Users can update own profile." on profiles for update using ( auth.uid() = id );

-- PROJECTS TABLE
create table projects (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references profiles(id) on delete cascade not null,
  title text not null,
  status text default 'draft', -- 'draft', 'generating_script', 'generating_audio', 'rendering', 'completed', 'failed'
  
  -- Project Data (JSONB for flexibility)
  script_content text,
  video_settings jsonb default '{}'::jsonb, -- { "voice_id": "...", "style": "cinematic" }
  
  -- Results
  result_video_url text,
  thumbnail_url text,
  
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- RLS for Projects
alter table projects enable row level security;
create policy "Users can view own projects." on projects for select using ( auth.uid() = user_id );
create policy "Users can insert own projects." on projects for insert with check ( auth.uid() = user_id );
create policy "Users can update own projects." on projects for update using ( auth.uid() = user_id );
create policy "Users can delete own projects." on projects for delete using ( auth.uid() = user_id );

-- TRIGGERS
-- Function to handle new user signup
create or replace function public.handle_new_user() 
returns trigger as $$
begin
  insert into public.profiles (id, email, full_name, avatar_url)
  values (new.id, new.email, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
  return new;
end;
$$ language plpgsql security definer;

-- Trigger the function
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
