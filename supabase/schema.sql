-- ====================================================================
-- FORMPILOT AI — PRODUCTION SUPABASE POSTGRESQL SCHEMA & RLS POLICIES
-- Tagline: Understand. Fill. Verify. Apply.
-- ====================================================================

-- 1. Profiles Table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT DEFAULT 'applicant',
    language_pref TEXT DEFAULT 'en',
    theme_pref TEXT DEFAULT 'dark',
    profile_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS on profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

-- 2. Documents Table
CREATE TABLE IF NOT EXISTS public.documents (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size_bytes BIGINT DEFAULT 0,
    file_type TEXT DEFAULT 'pdf',
    doc_category TEXT DEFAULT 'unclassified',
    doc_category_confidence TEXT DEFAULT '0.0',
    page_count INTEGER DEFAULT 1,
    extracted_text TEXT DEFAULT '',
    is_blank_form BOOLEAN DEFAULT FALSE,
    is_filled_form BOOLEAN DEFAULT FALSE,
    is_guideline BOOLEAN DEFAULT FALSE,
    metadata_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own documents"
    ON public.documents FOR ALL
    USING (auth.uid() = user_id);

-- 3. Form Analyses Table
CREATE TABLE IF NOT EXISTS public.form_analyses (
    id BIGSERIAL PRIMARY KEY,
    document_id BIGINT REFERENCES public.documents(id) ON DELETE SET NULL,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    mode TEXT DEFAULT 'analyzer',
    document_title TEXT DEFAULT 'Document',
    detected_type TEXT DEFAULT 'Application Form',
    total_fields INTEGER DEFAULT 0,
    mandatory_fields_count INTEGER DEFAULT 0,
    optional_fields_count INTEGER DEFAULT 0,
    summary_en TEXT DEFAULT '',
    summary_ta TEXT DEFAULT '',
    sections JSONB DEFAULT '[]'::jsonb,
    fields JSONB DEFAULT '[]'::jsonb,
    declarations JSONB DEFAULT '[]'::jsonb,
    issues_and_errors JSONB DEFAULT '[]'::jsonb,
    eligibility_info JSONB DEFAULT '{}'::jsonb,
    generated_pdf_path TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.form_analyses ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own analyses"
    ON public.form_analyses FOR ALL
    USING (auth.uid() = user_id);

-- 4. Applications Tracker Table
CREATE TABLE IF NOT EXISTS public.applications (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    category TEXT DEFAULT 'Scholarship',
    deadline TEXT,
    status TEXT DEFAULT 'Draft',
    progress_percent INTEGER DEFAULT 15,
    portal_url TEXT,
    notes TEXT DEFAULT '',
    checklist JSONB DEFAULT '[]'::jsonb,
    reminder_date TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.applications ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own applications"
    ON public.applications FOR ALL
    USING (auth.uid() = user_id);

-- 5. Chat Messages Table
CREATE TABLE IF NOT EXISTS public.chat_messages (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    document_id BIGINT REFERENCES public.documents(id) ON DELETE SET NULL,
    role TEXT DEFAULT 'user',
    content TEXT NOT NULL,
    language TEXT DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.chat_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own chat history"
    ON public.chat_messages FOR ALL
    USING (auth.uid() = user_id);

-- Create Indexes for fast querying
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON public.documents(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_user_id ON public.applications(user_id);
CREATE INDEX IF NOT EXISTS idx_form_analyses_user_id ON public.form_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON public.chat_messages(user_id);
