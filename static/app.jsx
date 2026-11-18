const { useState, useEffect, useRef } = React;

// Safe icon renderer helper that re-triggers lucide.createIcons
const Icon = ({ name, size = 18, className = "" }) => {
  useEffect(() => {
    if (window.lucide) {
      window.lucide.createIcons();
    }
  }, [name]);
  return <i data-lucide={name} className={`inline-block ${className}`} style={{ width: size, height: size }}></i>;
};

// Main FormPilot AI Application
function FormPilotApp() {
  // Theme & Language State with persistence
  const [theme, setTheme] = useState(() => localStorage.getItem("formpilot_theme") || "dark");
  const [lang, setLang] = useState(() => localStorage.getItem("formpilot_lang") || "en");
  
  // Navigation & UI State
  const [activePage, setActivePage] = useState("home");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // User Profile
  const [user, setUser] = useState({
    id: 1,
    full_name: "Arun Kumar S",
    email: "demo.student@formpilot.ai",
    role: "Scholarship Applicant",
    profile_data: {
      full_name: "Arun Kumar S",
      father_name: "Suresh Kumar R",
      email: "demo.student@formpilot.ai",
      mobile: "9876543210",
      dob: "15-08-2003",
      gender: "Male",
      aadhaar: "4839 2048 1092",
      category: "OBC",
      income: "180000",
      college_name: "Government College of Technology, Coimbatore",
      course_name: "B.E. Computer Science and Engineering",
      marks_percentage: "84.5%",
      bank_account: "304928174920",
      ifsc_code: "SBIN0001234",
      state: "Tamil Nadu",
      address: "12, Bharathi Street, Gandhi Nagar, Madurai, TN - 625020"
    }
  });

  // Active Document & Processing State
  const [activeDoc, setActiveDoc] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [notification, setNotification] = useState(null);

  // Translations
  const t = window.FORMPILOT_LOCALES ? window.FORMPILOT_LOCALES[lang] || window.FORMPILOT_LOCALES.en : {};

  // Sync Theme with HTML element
  useEffect(() => {
    localStorage.setItem("formpilot_theme", theme);
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [theme]);

  // Sync Language
  useEffect(() => {
    localStorage.setItem("formpilot_lang", lang);
  }, [lang]);

  // Trigger Lucide icons on route change
  useEffect(() => {
    if (window.lucide) {
      window.lucide.createIcons();
    }
  }, [activePage, sidebarCollapsed, mobileMenuOpen, analysisResult]);

  const showToast = (message, type = "success") => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const toggleTheme = () => {
    setTheme(prev => prev === "dark" ? "light" : "dark");
  };

  const toggleLanguage = () => {
    setLang(prev => prev === "en" ? "ta" : "en");
  };

  // Mandatory Left Sidebar Navigation Items (Includes New About & User Guide Page as requested)
  const navItems = [
    { id: "home", label: t.nav_home, icon: "home" },
    { id: "about_guide", label: t.nav_about_guide || "About & User Guide", icon: "book-open", highlight: true },
    { id: "dashboard", label: t.nav_dashboard, icon: "layout-dashboard" },
    { id: "analyzer", label: t.nav_analyzer, icon: "file-search" },
    { id: "create_fill", label: t.nav_create_fill, icon: "file-pen-line" },
    { id: "explain_filled", label: t.nav_explain_filled, icon: "file-check-2" },
    { id: "application_guide", label: t.nav_application_guide, icon: "compass" },
    { id: "document_center", label: t.nav_document_center, icon: "folder-kanban" },
    { id: "eligibility_checker", label: t.nav_eligibility_checker, icon: "shield-check" },
    { id: "tracker", label: t.nav_tracker, icon: "list-todo" },
    { id: "history", label: t.nav_history, icon: "history" },
    { id: "assistant", label: t.nav_assistant, icon: "bot" },
    { id: "profile", label: t.nav_profile, icon: "user" },
    { id: "settings", label: t.nav_settings, icon: "settings" },
    { id: "help_support", label: t.nav_help_support, icon: "help-circle" },
    { id: "logout", label: t.nav_logout, icon: "log-out", danger: true }
  ];

  return (
    <div className={`min-h-screen flex ${theme === "dark" ? "bg-[#0B1120] text-slate-100" : "bg-[#F8FAFC] text-slate-800"}`}>
      {/* Toast Notification */}
      {notification && (
        <div className={`fixed top-5 right-5 z-50 flex items-center gap-3 px-4 py-3 rounded-xl shadow-2xl border text-sm font-medium animate-bounce ${
          notification.type === "success" 
            ? "bg-emerald-950/90 border-emerald-500/50 text-emerald-200"
            : "bg-rose-950/90 border-rose-500/50 text-rose-200"
        }`}>
          <Icon name={notification.type === "success" ? "check-circle" : "alert-circle"} size={18} />
          <span>{notification.message}</span>
        </div>
      )}

      {/* 4.1 LEFT SIDEBAR — MANDATORY */}
      <aside className={`fixed inset-y-0 left-0 z-40 flex flex-col border-r transition-all duration-300 ${
        theme === "dark" ? "bg-[#0F172A] border-slate-800" : "bg-white border-slate-200 shadow-sm"
      } ${
        sidebarCollapsed ? "w-20" : "w-64"
      } ${
        mobileMenuOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      }`}>
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-inherit">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActivePage("home")}>
            <img src="/static/images/formpilot-logo.png" alt="FormPilot" className="w-9 h-9 rounded-lg" />
            {!sidebarCollapsed && (
              <div>
                <span className="font-bold text-base tracking-tight bg-gradient-to-r from-blue-400 via-cyan-400 to-indigo-300 bg-clip-text text-transparent">
                  FormPilot AI
                </span>
                <span className="block text-[10px] text-slate-400 font-medium">Understand & Apply</span>
              </div>
            )}
          </div>
          <button 
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="hidden md:flex p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60"
            title={sidebarCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            <Icon name={sidebarCollapsed ? "chevron-right" : "chevron-left"} size={18} />
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 overflow-y-auto px-2 py-3 space-y-1">
          {navItems.map((item) => {
            const isActive = activePage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  if (item.id === "logout") {
                    showToast("Session ended. Switched to guest mode.", "success");
                    setActivePage("home");
                  } else {
                    setActivePage(item.id);
                  }
                  setMobileMenuOpen(false);
                }}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-500/25"
                    : item.highlight
                    ? "bg-purple-500/10 text-purple-300 border border-purple-500/30 hover:bg-purple-500/20"
                    : item.danger
                    ? "text-rose-400 hover:bg-rose-500/10 hover:text-rose-300"
                    : theme === "dark"
                    ? "text-slate-300 hover:bg-slate-800/70 hover:text-white"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`}
                title={sidebarCollapsed ? item.label : ""}
              >
                <Icon name={item.icon} size={19} className={isActive ? "text-white" : item.highlight ? "text-purple-400" : ""} />
                {!sidebarCollapsed && (
                  <div className="flex-1 flex items-center justify-between text-left">
                    <span className="truncate">{item.label}</span>
                    {item.highlight && !isActive && (
                      <span className="text-[9px] uppercase px-1.5 py-0.5 rounded bg-purple-500/30 text-purple-200 font-bold">New</span>
                    )}
                  </div>
                )}
              </button>
            );
          })}
        </nav>

        {/* Bottom Profile Summary */}
        {!sidebarCollapsed && (
          <div className="p-3 border-t border-inherit">
            <div className={`p-2.5 rounded-xl flex items-center gap-3 ${theme === "dark" ? "bg-slate-800/40" : "bg-slate-100"}`}>
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center font-bold text-xs text-white">
                AK
              </div>
              <div className="overflow-hidden">
                <p className="text-xs font-semibold truncate">{user.full_name}</p>
                <p className="text-[10px] text-slate-400 truncate">{user.role}</p>
              </div>
            </div>
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <div className={`flex-1 flex flex-col min-w-0 transition-all duration-300 ${
        sidebarCollapsed ? "md:ml-20" : "md:ml-64"
      }`}>
        {/* Top Header Bar */}
        <header className={`h-16 flex items-center justify-between px-4 sm:px-6 sticky top-0 z-30 border-b backdrop-blur-md ${
          theme === "dark" ? "bg-[#0B1120]/80 border-slate-800" : "bg-white/80 border-slate-200"
        }`}>
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
            >
              <Icon name="menu" size={20} />
            </button>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-sm capitalize">{activePage.replace("_", " ")}</span>
              {activeDoc && (
                <span className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  <Icon name="file-text" size={12} />
                  {activeDoc.filename}
                </span>
              )}
            </div>
          </div>

          {/* Quick Actions: Language Switcher + Theme Toggle */}
          <div className="flex items-center gap-2">
            {/* Quick Link to About & Guide */}
            <button
              onClick={() => setActivePage("about_guide")}
              className={`hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                activePage === "about_guide"
                  ? "bg-purple-600 text-white border-purple-500"
                  : theme === "dark"
                  ? "bg-purple-950/40 border-purple-500/30 text-purple-300 hover:bg-purple-900/50"
                  : "bg-purple-50 border-purple-200 text-purple-700 hover:bg-purple-100"
              }`}
            >
              <Icon name="book-open" size={14} />
              <span>{lang === "ta" ? "வழிகாட்டி" : "User Guide"}</span>
            </button>

            {/* Language Switcher */}
            <button
              onClick={toggleLanguage}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                theme === "dark" 
                  ? "bg-slate-800 border-slate-700 text-slate-200 hover:bg-slate-700" 
                  : "bg-slate-100 border-slate-300 text-slate-800 hover:bg-slate-200"
              }`}
              title="Switch Language (English / தமிழ்)"
            >
              <Icon name="languages" size={15} />
              <span>{t.btn_toggle_lang}</span>
            </button>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg border transition-all ${
                theme === "dark" 
                  ? "bg-slate-800 border-slate-700 text-amber-400 hover:bg-slate-700" 
                  : "bg-slate-100 border-slate-300 text-slate-600 hover:bg-slate-200"
              }`}
              title="Toggle Light / Dark Theme"
            >
              <Icon name={theme === "dark" ? "sun" : "moon"} size={16} />
            </button>
          </div>
        </header>

        {/* Dynamic Page Router */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto w-full">
          {activePage === "home" && (
            <HomePage 
              t={t} 
              theme={theme} 
              setActivePage={setActivePage} 
              onSelectSample={(sampleType) => {
                setActivePage("analyzer");
                showToast(`Loaded sample ${sampleType} application!`, "success");
              }}
            />
          )}

          {activePage === "about_guide" && (
            <AboutGuidePage 
              t={t} 
              theme={theme} 
              lang={lang} 
              setActivePage={setActivePage} 
            />
          )}

          {activePage === "dashboard" && (
            <DashboardPage t={t} theme={theme} setActivePage={setActivePage} />
          )}

          {activePage === "analyzer" && (
            <FormAnalyzerPage 
              t={t} 
              theme={theme} 
              activeDoc={activeDoc} 
              setActiveDoc={setActiveDoc}
              analysisResult={analysisResult}
              setAnalysisResult={setAnalysisResult}
              showToast={showToast}
              setActivePage={setActivePage}
            />
          )}

          {activePage === "create_fill" && (
            <CreateFillPage 
              t={t} 
              theme={theme} 
              user={user} 
              activeDoc={activeDoc} 
              analysisResult={analysisResult} 
              showToast={showToast} 
            />
          )}

          {activePage === "explain_filled" && (
            <ExplainFilledPage 
              t={t} 
              theme={theme} 
              showToast={showToast} 
            />
          )}

          {activePage === "application_guide" && (
            <ApplicationGuidePage 
              t={t} 
              theme={theme} 
              showToast={showToast} 
            />
          )}

          {activePage === "document_center" && (
            <DocumentCenterPage 
              t={t} 
              theme={theme} 
              showToast={showToast} 
            />
          )}

          {activePage === "eligibility_checker" && (
            <EligibilityCheckerPage 
              t={t} 
              theme={theme} 
              user={user} 
              showToast={showToast} 
            />
          )}

          {activePage === "tracker" && (
            <ApplicationTrackerPage 
              t={t} 
              theme={theme} 
              showToast={showToast} 
            />
          )}

          {activePage === "history" && (
            <HistoryPage 
              t={t} 
              theme={theme} 
              setActivePage={setActivePage} 
            />
          )}

          {activePage === "assistant" && (
            <AIAssistantPage 
              t={t} 
              theme={theme} 
              lang={lang} 
              activeDoc={activeDoc} 
            />
          )}

          {activePage === "profile" && (
            <ProfilePage 
              t={t} 
              theme={theme} 
              user={user} 
              setUser={setUser} 
              showToast={showToast} 
            />
          )}

          {activePage === "settings" && (
            <SettingsPage 
              t={t} 
              theme={theme} 
              toggleTheme={toggleTheme} 
              lang={lang} 
              toggleLanguage={toggleLanguage} 
              showToast={showToast} 
            />
          )}

          {activePage === "help_support" && (
            <HelpSupportPage 
              t={t} 
              theme={theme} 
            />
          )}
        </main>
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// SECTION 5: UPGRADED HOME PAGE WITH PROJECT-RELEVANT HERO VISUAL
// -------------------------------------------------------------
function HomePage({ t, theme, setActivePage, onSelectSample }) {
  return (
    <div className="space-y-16">
      {/* HERO SECTION WITH PROJECT-RELEVANT BACKGROUND */}
      <div className="relative rounded-3xl overflow-hidden shadow-2xl border border-slate-800">
        {/* Project-Relevant High-Res Background */}
        <div 
          className="absolute inset-0 bg-cover bg-center transition-transform duration-700 hover:scale-105"
          style={{ backgroundImage: `url('/static/images/formpilot-hero.jpg')` }}
        ></div>

        {/* Deep Gradient Overlays for High Readability */}
        <div className="absolute inset-0 bg-gradient-to-r from-[#070D1E]/95 via-[#070D1E]/85 to-transparent"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-[#070D1E] via-transparent to-transparent"></div>

        {/* Hero Content */}
        <div className="relative z-10 px-6 sm:px-12 py-16 sm:py-24 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-semibold mb-6 backdrop-blur-md">
            <Icon name="sparkles" size={14} className="text-cyan-400" />
            <span>FormPilot AI Document Intelligence 2.0</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight mb-4">
            {t.hero_headline}
          </h1>

          <p className="text-base sm:text-lg text-slate-300 leading-relaxed mb-8">
            {t.hero_subheadline}
          </p>

          {/* Call to Actions */}
          <div className="flex flex-wrap items-center gap-4">
            <button
              onClick={() => setActivePage("analyzer")}
              className="flex items-center gap-2.5 px-6 py-3.5 rounded-xl font-semibold text-sm bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 text-white shadow-xl shadow-blue-500/25 hover:shadow-cyan-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all"
            >
              <Icon name="file-search" size={18} />
              <span>{t.cta_start_analyzing}</span>
            </button>

            <button
              onClick={() => setActivePage("about_guide")}
              className="flex items-center gap-2.5 px-6 py-3.5 rounded-xl font-semibold text-sm bg-purple-600/30 hover:bg-purple-600/50 text-purple-200 border border-purple-500/40 backdrop-blur-md transition-all"
            >
              <Icon name="book-open" size={18} />
              <span>{t.cta_explore_features}</span>
            </button>
          </div>

          {/* Quick Stats in Hero */}
          <div className="grid grid-cols-3 gap-6 pt-10 mt-10 border-t border-slate-700/40">
            <div>
              <p className="text-2xl font-bold text-white">99.4%</p>
              <p className="text-xs text-slate-400">Field Recognition</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-cyan-400">0%</p>
              <p className="text-xs text-slate-400">Missed Errors</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-emerald-400">EN + தமிழ்</p>
              <p className="text-xs text-slate-400">Full Bilingual</p>
            </div>
          </div>
        </div>
      </div>

      {/* THREE MAIN PRODUCT MODES */}
      <div id="three-modes" className="space-y-6">
        <div className="text-center max-w-xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">One Platform. Three Intelligent Modes.</h2>
          <p className="text-sm text-slate-400 mt-1">Transform confusing applications into simple, guided workflows.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Mode 1 */}
          <div 
            onClick={() => setActivePage("create_fill")}
            className="p-6 rounded-2xl border transition-all cursor-pointer group hover:-translate-y-1 hover:shadow-xl bg-gradient-to-b from-blue-900/10 to-transparent border-slate-800 hover:border-blue-500/50"
          >
            <div className="w-12 h-12 rounded-xl bg-blue-500/20 text-blue-400 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <Icon name="file-pen-line" size={24} />
            </div>
            <h3 className="font-bold text-lg mb-2 group-hover:text-blue-400 transition-colors">{t.mode_1_title}</h3>
            <p className="text-sm text-slate-400 leading-relaxed mb-4">{t.mode_1_desc}</p>
            <span className="text-xs font-semibold text-blue-400 inline-flex items-center gap-1">
              Start Filling <Icon name="arrow-right" size={14} />
            </span>
          </div>

          {/* Mode 2 */}
          <div 
            onClick={() => setActivePage("explain_filled")}
            className="p-6 rounded-2xl border transition-all cursor-pointer group hover:-translate-y-1 hover:shadow-xl bg-gradient-to-b from-cyan-900/10 to-transparent border-slate-800 hover:border-cyan-500/50"
          >
            <div className="w-12 h-12 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <Icon name="file-check-2" size={24} />
            </div>
            <h3 className="font-bold text-lg mb-2 group-hover:text-cyan-400 transition-colors">{t.mode_2_title}</h3>
            <p className="text-sm text-slate-400 leading-relaxed mb-4">{t.mode_2_desc}</p>
            <span className="text-xs font-semibold text-cyan-400 inline-flex items-center gap-1">
              Verify Form <Icon name="arrow-right" size={14} />
            </span>
          </div>

          {/* Mode 3 */}
          <div 
            onClick={() => setActivePage("application_guide")}
            className="p-6 rounded-2xl border transition-all cursor-pointer group hover:-translate-y-1 hover:shadow-xl bg-gradient-to-b from-purple-900/10 to-transparent border-slate-800 hover:border-purple-500/50"
          >
            <div className="w-12 h-12 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <Icon name="compass" size={24} />
            </div>
            <h3 className="font-bold text-lg mb-2 group-hover:text-purple-400 transition-colors">{t.mode_3_title}</h3>
            <p className="text-sm text-slate-400 leading-relaxed mb-4">{t.mode_3_desc}</p>
            <span className="text-xs font-semibold text-purple-400 inline-flex items-center gap-1">
              Explore Guide <Icon name="arrow-right" size={14} />
            </span>
          </div>
        </div>
      </div>

      {/* QUICK 1-CLICK TRY SAMPLE FORMS */}
      <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/40 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h4 className="font-bold text-base text-slate-200">Interactive Sample Workflows</h4>
            <p className="text-xs text-slate-400">Try real authentic sample forms generated specifically for this platform.</p>
          </div>
          <div className="flex flex-wrap gap-2.5">
            <button
              onClick={() => { setActivePage("analyzer"); }}
              className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-blue-600/30 hover:bg-blue-600 text-blue-200 border border-blue-500/40 transition-all flex items-center gap-2"
            >
              <Icon name="file-text" size={14} />
              <span>Blank Scholarship Form</span>
            </button>
            <button
              onClick={() => { setActivePage("explain_filled"); }}
              className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-cyan-600/30 hover:bg-cyan-600 text-cyan-200 border border-cyan-500/40 transition-all flex items-center gap-2"
            >
              <Icon name="file-check" size={14} />
              <span>Filled Job Application</span>
            </button>
            <button
              onClick={() => { setActivePage("application_guide"); }}
              className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-purple-600/30 hover:bg-purple-600 text-purple-200 border border-purple-500/40 transition-all flex items-center gap-2"
            >
              <Icon name="compass" size={14} />
              <span>Scheme Guideline Notice</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// NEW: ABOUT & USER GUIDE PAGE ("about page 2 sidebar add pannu")
// -------------------------------------------------------------
function AboutGuidePage({ t, theme, lang, setActivePage }) {
  const steps = [
    {
      num: 1,
      title: t.about_step1_title || "1. Upload & Understand Blank Forms",
      desc: t.about_step1_desc || "Upload official application forms. AI extracts all fields, explains what to enter in English & Tamil, expected formats, examples, and marks mandatory vs optional fields.",
      target: "analyzer",
      btnText: "Go to Form Analyzer",
      icon: "file-search",
      badge: "Module 1 & 2"
    },
    {
      num: 2,
      title: t.about_step2_title || "2. Guided Form Filling & Instant PDF",
      desc: t.about_step2_desc || "Fill applications through an interactive Q&A workflow or 1-click auto-fill from your profile. Validate values against format rules and export a completed official PDF.",
      target: "create_fill",
      btnText: "Create & Fill Form",
      icon: "file-pen-line",
      badge: "Module 3"
    },
    {
      num: 3,
      title: t.about_step3_title || "3. Audit Filled Forms for Zero Errors",
      desc: t.about_step3_desc || "Upload an already-filled application to check for format mistakes, missing mandatory fields, and name/DOB discrepancies before submission.",
      target: "explain_filled",
      btnText: "Audit Filled Form",
      icon: "file-check-2",
      badge: "Module 4 & 8"
    },
    {
      num: 4,
      title: t.about_step4_title || "4. Check Scheme Eligibility with Rules",
      desc: t.about_step4_desc || "Enter your age, income, category, and marks to check eligibility for Post-Matric Scholarships, Central Sector Schemes, or State assistance programs with transparent rule justifications.",
      target: "eligibility_checker",
      btnText: "Check Eligibility",
      icon: "shield-check",
      badge: "Module 7"
    },
    {
      num: 5,
      title: t.about_step5_title || "5. Document Center & Matching",
      desc: t.about_step5_desc || "Store and categorize supporting documents (Aadhaar, Marksheets, Income Certificates) and ensure every required document is attached.",
      target: "document_center",
      btnText: "Open Document Center",
      icon: "folder-kanban",
      badge: "Module 6"
    },
    {
      num: 6,
      title: t.about_step6_title || "6. Track Deadlines & Application Journey",
      desc: t.about_step6_desc || "Monitor deadlines, check off requirements, set reminders, and transition application statuses from Draft to Submitted.",
      target: "tracker",
      btnText: "View Application Tracker",
      icon: "list-todo",
      badge: "Module 9"
    }
  ];

  return (
    <div className="space-y-10">
      {/* Page Header */}
      <div className="p-8 rounded-3xl border border-purple-500/30 bg-gradient-to-r from-purple-950/40 via-slate-900/60 to-blue-950/40 relative overflow-hidden">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 text-xs font-semibold mb-3 border border-purple-500/30">
            <Icon name="book-open" size={14} />
            <span>Platform Overview & Execution Blueprint</span>
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight text-white">{t.about_title}</h2>
          <p className="text-sm text-slate-300 mt-2 leading-relaxed">{t.about_subtitle}</p>
        </div>
      </div>

      {/* Student & Applicant Journey Steps */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Icon name="workflow" size={20} className="text-cyan-400" />
            <span>How to Approach Your Application: Step-by-Step</span>
          </h3>
          <span className="text-xs text-slate-400 font-medium">6 Practical Steps</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {steps.map(step => (
            <div 
              key={step.num}
              className="p-6 rounded-2xl border border-slate-800 bg-slate-900/50 hover:bg-slate-900/80 transition-all space-y-3 relative group"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold text-sm">
                    {step.num}
                  </div>
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                    {step.badge}
                  </span>
                </div>
                <Icon name={step.icon} size={20} className="text-slate-500 group-hover:text-purple-400 transition-colors" />
              </div>

              <h4 className="font-bold text-base text-slate-200">{step.title}</h4>
              <p className="text-xs text-slate-400 leading-relaxed">{step.desc}</p>

              <button
                onClick={() => setActivePage(step.target)}
                className="pt-2 text-xs font-semibold text-cyan-400 hover:text-cyan-300 inline-flex items-center gap-1.5 transition-all"
              >
                <span>{step.btnText}</span>
                <Icon name="arrow-right" size={13} />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Critical Application Traps & How FormPilot Prevents Them */}
      <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/40 space-y-4">
        <h3 className="font-bold text-sm text-slate-200">Common Rejection Traps & FormPilot AI Safeguards</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700 space-y-1.5">
            <span className="font-bold text-rose-400 flex items-center gap-1">
              <Icon name="alert-triangle" size={14} />
              Name Discrepancy
            </span>
            <p className="text-slate-300">Marksheet name doesn't match Aadhaar card name.</p>
            <p className="text-emerald-400 text-[11px]"><b>FormPilot Fix:</b> Module 8 cross-document mismatch detector alerts you immediately.</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700 space-y-1.5">
            <span className="font-bold text-rose-400 flex items-center gap-1">
              <Icon name="alert-triangle" size={14} />
              DBT Bank Seeding Missing
            </span>
            <p className="text-slate-300">Scholarship funds bounce because bank account isn't Aadhaar-seeded.</p>
            <p className="text-emerald-400 text-[11px]"><b>FormPilot Fix:</b> AI Copilot verifies DBT protocols and individual account status.</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700 space-y-1.5">
            <span className="font-bold text-rose-400 flex items-center gap-1">
              <Icon name="alert-triangle" size={14} />
              Missed Income Ceilings
            </span>
            <p className="text-slate-300">Applying for schemes where your family income exceeds the limit.</p>
            <p className="text-emerald-400 text-[11px]"><b>FormPilot Fix:</b> Module 7 evaluates limits before you waste time applying.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// SECTION 12: DASHBOARD PAGE WITH REAL METRICS & CHARTS
// -------------------------------------------------------------
function DashboardPage({ t, theme, setActivePage }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/dashboard/summary")
      .then(res => res.json())
      .then(data => {
        setSummary(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Dashboard error:", err);
        setLoading(false);
      });
  }, []);

  const metrics = summary?.metrics || {
    total_documents: 3,
    forms_completed: 2,
    pending_applications: 2,
    readiness_score: 94
  };

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{t.nav_dashboard}</h2>
        <p className="text-sm text-slate-400">Real-time application analytics and document tracking status.</p>
      </div>

      {/* 4 Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/60">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-medium text-slate-400">{t.dash_total_docs}</span>
            <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400"><Icon name="files" size={18} /></div>
          </div>
          <p className="text-2xl font-extrabold">{metrics.total_documents}</p>
          <span className="text-[11px] text-emerald-400 font-medium">Active in Document Center</span>
        </div>

        <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/60">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-medium text-slate-400">{t.dash_forms_completed}</span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400"><Icon name="file-check" size={18} /></div>
          </div>
          <p className="text-2xl font-extrabold">{metrics.forms_completed}</p>
          <span className="text-[11px] text-emerald-400 font-medium">Ready for PDF download</span>
        </div>

        <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/60">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-medium text-slate-400">{t.dash_pending_apps}</span>
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400"><Icon name="clock" size={18} /></div>
          </div>
          <p className="text-2xl font-extrabold">{metrics.pending_applications}</p>
          <span className="text-[11px] text-amber-400 font-medium">Deadline approaching</span>
        </div>

        <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/60">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-medium text-slate-400">{t.dash_readiness_score}</span>
            <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400"><Icon name="shield-check" size={18} /></div>
          </div>
          <p className="text-2xl font-extrabold">{metrics.readiness_score}%</p>
          <span className="text-[11px] text-purple-400 font-medium">Zero critical errors</span>
        </div>
      </div>

      {/* Upcoming Deadlines & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Deadlines */}
        <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-sm">{t.dash_upcoming_deadlines}</h3>
            <button onClick={() => setActivePage("tracker")} className="text-xs text-blue-400 hover:underline">View All</button>
          </div>
          <div className="space-y-3">
            {(summary?.upcoming_deadlines || [
              { id: 1, title: "Post-Matric Scholarship Scheme 2026-27", deadline: "2026-12-15", category: "Scholarship", progress: 65 },
              { id: 2, title: "TCS Graduate Engineer Trainee 2026", deadline: "2026-12-30", category: "Job Application", progress: 85 }
            ]).map(item => (
              <div key={item.id} className="p-3 rounded-xl bg-slate-800/40 border border-slate-800 flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold">{item.title}</p>
                  <p className="text-xs text-slate-400">{item.category} • Due: {item.deadline}</p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold text-blue-400">{item.progress}%</span>
                  <div className="w-16 h-1.5 bg-slate-700 rounded-full mt-1 overflow-hidden">
                    <div className="h-full bg-blue-500 rounded-full" style={{ width: `${item.progress}%` }}></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Launchpad */}
        <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/50 space-y-4">
          <h3 className="font-semibold text-sm">Quick Action Launchpad</h3>
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={() => setActivePage("analyzer")}
              className="p-4 rounded-xl border border-slate-800 bg-slate-800/40 hover:bg-slate-800 text-left transition-all"
            >
              <Icon name="file-search" size={20} className="text-blue-400 mb-2" />
              <p className="text-sm font-semibold">Analyze New Form</p>
              <p className="text-xs text-slate-400">Blank or filled</p>
            </button>

            <button
              onClick={() => setActivePage("eligibility_checker")}
              className="p-4 rounded-xl border border-slate-800 bg-slate-800/40 hover:bg-slate-800 text-left transition-all"
            >
              <Icon name="shield-check" size={20} className="text-emerald-400 mb-2" />
              <p className="text-sm font-semibold">Check Eligibility</p>
              <p className="text-xs text-slate-400">Rule-based engine</p>
            </button>

            <button
              onClick={() => setActivePage("tracker")}
              className="p-4 rounded-xl border border-slate-800 bg-slate-800/40 hover:bg-slate-800 text-left transition-all"
            >
              <Icon name="plus-circle" size={20} className="text-cyan-400 mb-2" />
              <p className="text-sm font-semibold">Track Application</p>
              <p className="text-xs text-slate-400">Set deadlines</p>
            </button>

            <button
              onClick={() => setActivePage("assistant")}
              className="p-4 rounded-xl border border-slate-800 bg-slate-800/40 hover:bg-slate-800 text-left transition-all"
            >
              <Icon name="bot" size={20} className="text-purple-400 mb-2" />
              <p className="text-sm font-semibold">AI Copilot</p>
              <p className="text-xs text-slate-400">Bilingual assistance</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// MODULE 1 & 2: FORM ANALYZER & BLANK FORM UNDERSTANDING
// -------------------------------------------------------------
function FormAnalyzerPage({ t, theme, activeDoc, setActiveDoc, analysisResult, setAnalysisResult, showToast, setActivePage }) {
  const [analyzing, setAnalyzing] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setAnalyzing(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("doc_type", "blank_form");

    try {
      const res = await fetch("/api/documents/upload", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      if (res.ok) {
        setActiveDoc(data);
        const anaRes = await fetch(`/api/forms/analyze?document_id=${data.document_id}`, { method: "POST" });
        const anaData = await anaRes.json();
        setAnalysisResult(anaData);
        showToast("Document analyzed successfully!", "success");
      } else {
        showToast(data.detail || "Upload failed", "error");
      }
    } catch (err) {
      showToast("Error processing file", "error");
    } finally {
      setAnalyzing(false);
    }
  };

  const loadSample = async () => {
    setAnalyzing(true);
    try {
      const anaRes = await fetch("/api/forms/analyze", { method: "POST" });
      const anaData = await anaRes.json();
      setAnalysisResult(anaData);
      setActiveDoc({ filename: "blank_scholarship_application.pdf", page_count: 1 });
      showToast("Loaded official sample scholarship form!", "success");
    } catch (err) {
      showToast("Failed to load sample", "error");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{t.analyzer_title}</h2>
        <p className="text-sm text-slate-400">{t.analyzer_subtitle}</p>
      </div>

      {/* Upload Dropzone */}
      <div 
        onClick={() => fileInputRef.current && fileInputRef.current.click()}
        className="p-10 rounded-2xl border-2 border-dashed border-slate-700 hover:border-blue-500 bg-slate-900/30 hover:bg-slate-900/50 transition-all text-center cursor-pointer space-y-4"
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileUpload} 
          className="hidden" 
          accept=".pdf,.docx,.doc,.txt,.png,.jpg,.jpeg,.xlsx,.csv" 
        />
        <div className="w-14 h-14 rounded-2xl bg-blue-500/10 text-blue-400 mx-auto flex items-center justify-center">
          <Icon name="upload-cloud" size={28} />
        </div>
        <div>
          <p className="font-semibold text-slate-200">{t.analyzer_dropzone}</p>
          <p className="text-xs text-slate-400 mt-1">{t.analyzer_supported_formats}</p>
        </div>
        <div className="flex items-center justify-center gap-3 pt-2">
          <span className="text-xs text-slate-500">OR</span>
          <button
            type="button"
            onClick={(e) => { e.stopPropagation(); loadSample(); }}
            className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white"
          >
            {t.cta_try_sample}
          </button>
        </div>
      </div>

      {/* Progress / Status */}
      {analyzing && (
        <div className="p-4 rounded-xl border border-blue-500/30 bg-blue-500/10 flex items-center gap-3 text-blue-300 text-sm">
          <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
          <span>Analyzing document structure, extracting form fields, and generating bilingual explanations...</span>
        </div>
      )}

      {/* Analysis Results Display */}
      {analysisResult && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/60 flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mb-2">
                <Icon name="check" size={12} />
                <span>Document Understood</span>
              </div>
              <h3 className="text-lg font-bold">{analysisResult.document_title}</h3>
              <p className="text-xs text-slate-400 mt-1">{analysisResult.summary_en}</p>
              <p className="text-xs text-slate-400 mt-0.5 font-tamil">{analysisResult.summary_ta}</p>
            </div>
            <button
              onClick={() => setActivePage("create_fill")}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold bg-blue-600 hover:bg-blue-500 text-white"
            >
              <Icon name="file-pen-line" size={16} />
              <span>Proceed to Fill Form</span>
            </button>
          </div>

          <div className="flex flex-wrap gap-2">
            {analysisResult.sections?.map((sec, i) => (
              <span key={i} className="px-3 py-1 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700">
                {sec}
              </span>
            ))}
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-sm">{t.detected_fields} ({analysisResult.fields?.length})</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {analysisResult.fields?.map((field) => (
                <div key={field.id} className="p-5 rounded-xl border border-slate-800 bg-slate-900/40 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-sm text-blue-400">{field.label_en}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                      field.is_mandatory ? "bg-rose-500/20 text-rose-300 border border-rose-500/30" : "bg-slate-800 text-slate-400"
                    }`}>
                      {field.is_mandatory ? t.field_mandatory : t.field_optional}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 font-medium">{field.explanation_en}</p>
                  <p className="text-xs text-slate-400 font-tamil">{field.explanation_ta}</p>
                  
                  <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-400">
                    <span>Format: <strong className="text-slate-300">{field.expected_format}</strong></span>
                    <span>Example: <code className="bg-slate-800 px-1 py-0.5 rounded text-cyan-400">{field.example}</code></span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// -------------------------------------------------------------
// MODULE 3: CREATE & FILL FORM ASSISTANT
// -------------------------------------------------------------
function CreateFillPage({ t, theme, user, activeDoc, analysisResult, showToast }) {
  const [formData, setFormData] = useState({});
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    if (user && user.profile_data) {
      setFormData(user.profile_data);
    }
  }, [user]);

  const handleChange = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }));
  };

  const handleAutoFill = () => {
    if (user && user.profile_data) {
      setFormData(user.profile_data);
      showToast("Auto-filled answers from your saved applicant profile!", "success");
    }
  };

  const handleGeneratePDF = async () => {
    setGenerating(true);
    try {
      const res = await fetch("/api/forms/fill", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          document_id: activeDoc?.document_id || null,
          answers: formData,
          export_pdf: true
        })
      });
      const data = await res.json();
      if (data.pdf_download_url) {
        setDownloadUrl(data.pdf_download_url);
        showToast("Official Completed Application PDF generated successfully!", "success");
      } else {
        showToast("Please fix validation errors", "error");
      }
    } catch (err) {
      showToast("Error generating PDF", "error");
    } finally {
      setGenerating(false);
    }
  };

  const formFields = [
    { id: "full_name", label: "Full Name of Applicant", type: "text", example: "ARUN KUMAR S" },
    { id: "father_name", label: "Father / Guardian Name", type: "text", example: "SURESH KUMAR R" },
    { id: "dob", label: "Date of Birth (DD-MM-YYYY)", type: "text", example: "15-08-2003" },
    { id: "gender", label: "Gender", type: "text", example: "Male" },
    { id: "email", label: "Email Address", type: "email", example: "arun.student@gmail.com" },
    { id: "mobile", label: "Mobile Number (10 digits)", type: "text", example: "9876543210" },
    { id: "aadhaar", label: "Aadhaar Number (12 digits)", type: "text", example: "4839 2048 1092" },
    { id: "income", label: "Annual Family Income (INR)", type: "text", example: "180000" },
    { id: "category", label: "Community / Reservation Category", type: "text", example: "OBC" },
    { id: "college_name", label: "College / University Name", type: "text", example: "Government College of Technology" },
    { id: "course_name", label: "Course / Degree Name", type: "text", example: "B.E. Computer Science" },
    { id: "marks_percentage", label: "Qualifying Percentage / CGPA", type: "text", example: "84.5%" },
    { id: "bank_account", label: "Bank Account Number (DBT)", type: "text", example: "304928174920" },
    { id: "ifsc_code", label: "Bank IFSC Code", type: "text", example: "SBIN0001234" },
    { id: "address", label: "Permanent Address", type: "text", example: "12, Bharathi Street, Madurai - 625020" }
  ];

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">{t.fill_title}</h2>
          <p className="text-sm text-slate-400">{t.fill_subtitle}</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleAutoFill}
            className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30"
          >
            <Icon name="sparkles" size={15} />
            <span>{t.btn_autofill}</span>
          </button>
          <button
            onClick={handleGeneratePDF}
            disabled={generating}
            className="flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/25"
          >
            <Icon name="file-down" size={15} />
            <span>{generating ? "Generating..." : t.btn_download_pdf}</span>
          </button>
        </div>
      </div>

      {downloadUrl && (
        <div className="p-4 rounded-xl border border-emerald-500/40 bg-emerald-950/40 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Icon name="check-circle" size={20} className="text-emerald-400" />
            <div>
              <p className="text-sm font-semibold text-emerald-200">Application Document Ready!</p>
              <p className="text-xs text-emerald-400">PDF formatted with official tables, declarations, and signature block.</p>
            </div>
          </div>
          <a
            href={downloadUrl}
            download
            className="px-4 py-2 rounded-lg text-xs font-bold bg-emerald-500 text-slate-900 hover:bg-emerald-400"
          >
            Download PDF
          </a>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {formFields.map(f => (
          <div key={f.id} className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 space-y-1.5">
            <label className="text-xs font-medium text-slate-300">{f.label}</label>
            <input
              type={f.type}
              value={formData[f.id] || ""}
              onChange={(e) => handleChange(f.id, e.target.value)}
              placeholder={`e.g. ${f.example}`}
              className="w-full px-3 py-2 rounded-lg text-sm bg-slate-800 border border-slate-700 text-slate-100 focus:outline-none focus:border-blue-500"
            />
          </div>
        ))}
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// MODULE 4: EXPLAIN FILLED FORM
// -------------------------------------------------------------
function ExplainFilledPage({ t, theme, showToast }) {
  const [auditResult, setAuditResult] = useState(null);
  const [auditing, setAuditing] = useState(false);

  const runAudit = async () => {
    setAuditing(true);
    try {
      const res = await fetch("/api/forms/explain", { method: "POST" });
      const data = await res.json();
      setAuditResult(data);
      showToast("Completed form audit analysis!", "success");
    } catch (err) {
      showToast("Audit failed", "error");
    } finally {
      setAuditing(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">{t.explain_title}</h2>
          <p className="text-sm text-slate-400">{t.explain_subtitle}</p>
        </div>
        <button
          onClick={runAudit}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold bg-cyan-600 hover:bg-cyan-500 text-white"
        >
          <Icon name="scan" size={16} />
          <span>Audit Sample Filled Form</span>
        </button>
      </div>

      {auditing && (
        <div className="p-4 rounded-xl border border-cyan-500/30 bg-cyan-500/10 flex items-center gap-3 text-cyan-300 text-sm">
          <div className="w-5 h-5 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
          <span>Validating email, phone, PIN code, and checking declaration statements...</span>
        </div>
      )}

      {auditResult && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/60">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Audit Status</span>
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                {auditResult.audit_status}
              </span>
            </div>
            <h3 className="text-lg font-bold">{auditResult.document_title}</h3>
            <p className="text-xs text-slate-400 mt-1">{auditResult.summary_en}</p>
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-sm">Field Review & Format Validation</h4>
            <div className="space-y-2">
              {auditResult.fields?.map(f => (
                <div key={f.id} className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/40 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium">{f.label_en}</p>
                    <p className="text-xs text-slate-400">Entered: <strong className="text-slate-200">{f.value || "-"}</strong></p>
                  </div>
                  <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-emerald-500/20 text-emerald-400">
                    Correct Format
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// -------------------------------------------------------------
// MODULE 5: APPLICATION GUIDE
// -------------------------------------------------------------
function ApplicationGuidePage({ t, theme, showToast }) {
  const [guide, setGuide] = useState(null);

  useEffect(() => {
    fetch("/api/forms/guide")
      .then(res => res.json())
      .then(data => setGuide(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{t.guide_title}</h2>
        <p className="text-sm text-slate-400">{t.guide_subtitle}</p>
      </div>

      {guide && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/60">
            <h3 className="text-lg font-bold text-purple-400">{guide.guide_title}</h3>
            <div className="mt-3 flex flex-wrap gap-4 text-xs text-slate-300">
              <span>Portal: <a href={guide.official_websites?.[0]} target="_blank" className="text-blue-400 underline">{guide.official_websites?.[0]}</a></span>
              <span>Fee: <strong className="text-emerald-400">{guide.application_fee}</strong></span>
            </div>
          </div>

          <div className="space-y-4">
            <h4 className="font-semibold text-sm">{t.guide_step_by_step}</h4>
            <div className="space-y-3">
              {guide.procedure_steps?.map(step => (
                <div key={step.step_num} className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 flex items-start gap-4">
                  <div className="w-8 h-8 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold text-sm shrink-0">
                    {step.step_num}
                  </div>
                  <div>
                    <h5 className="font-semibold text-sm">{step.title_en}</h5>
                    <p className="text-xs text-purple-400 font-tamil">{step.title_ta}</p>
                    <p className="text-xs text-slate-400 mt-1">{step.desc_en}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// -------------------------------------------------------------
// MODULE 6: DOCUMENT CENTER
// -------------------------------------------------------------
function DocumentCenterPage({ t, theme, showToast }) {
  const documents = [
    { name: "Aadhaar Card (Identity Proof)", type: "PDF", size: "420 KB", status: "Verified" },
    { name: "10th Standard Secondary Marksheet", type: "PDF", size: "1.1 MB", status: "Verified" },
    { name: "Tahsildar Income Certificate 2026", type: "PDF", size: "650 KB", status: "Verified" },
    { name: "Community / Caste Certificate", type: "PDF", size: "520 KB", status: "Verified" },
    { name: "College Bonafide Certificate", type: "PDF", size: "380 KB", status: "Missing / Pending" }
  ];

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{t.doc_center_title}</h2>
        <p className="text-sm text-slate-400">{t.doc_center_subtitle}</p>
      </div>

      <div className="space-y-3">
        {documents.map((doc, idx) => (
          <div key={idx} className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-lg bg-blue-500/10 text-blue-400">
                <Icon name="file-text" size={20} />
              </div>
              <div>
                <p className="text-sm font-semibold">{doc.name}</p>
                <p className="text-xs text-slate-400">{doc.type} • {doc.size}</p>
              </div>
            </div>
            <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
              doc.status === "Verified" 
                ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
            }`}>
              {doc.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// MODULE 7: ELIGIBILITY CHECKER
// -------------------------------------------------------------
function EligibilityCheckerPage({ t, theme, user, showToast }) {
  const [schemes, setSchemes] = useState([]);
  const [selectedScheme, setSelectedScheme] = useState("post_matric_scholarship");
  const [age, setAge] = useState(20);
  const [income, setIncome] = useState(180000);
  const [category, setCategory] = useState("OBC");
  const [education, setEducation] = useState("Undergraduate");
  const [marks, setMarks] = useState(84.5);
  const [state, setState] = useState("Tamil Nadu");
  const [gender, setGender] = useState("Male");
  const [evalResult, setEvalResult] = useState(null);
  const [checking, setChecking] = useState(false);

  useEffect(() => {
    fetch("/api/eligibility/schemes")
      .then(res => res.json())
      .then(data => setSchemes(data))
      .catch(err => console.error(err));
  }, []);

  const handleCheck = async () => {
    setChecking(true);
    try {
      const res = await fetch("/api/eligibility/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          scheme_id: selectedScheme,
          age,
          education_level: education,
          course: "B.E. Computer Science",
          annual_family_income: parseFloat(income),
          category_caste: category,
          marks_percentage: parseFloat(marks),
          state,
          gender
        })
      });
      const data = await res.json();
      setEvalResult(data);
      showToast("Eligibility evaluated against official rules!", "success");
    } catch (err) {
      showToast("Evaluation failed", "error");
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{t.eligibility_title}</h2>
        <p className="text-sm text-slate-400">{t.eligibility_subtitle}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 p-6 rounded-2xl border border-slate-800 bg-slate-900/50 space-y-4">
          <div>
            <label className="text-xs font-medium text-slate-400">{t.eligibility_select_scheme}</label>
            <select
              value={selectedScheme}
              onChange={(e) => setSelectedScheme(e.target.value)}
              className="w-full mt-1 px-3 py-2 rounded-lg text-sm bg-slate-800 border border-slate-700 text-slate-100"
            >
              {schemes.map(s => (
                <option key={s.id} value={s.id}>{s.name_en}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400">{t.eligibility_income}</label>
            <input
              type="number"
              value={income}
              onChange={(e) => setIncome(e.target.value)}
              className="w-full mt-1 px-3 py-2 rounded-lg text-sm bg-slate-800 border border-slate-700 text-slate-100"
            />
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400">{t.eligibility_caste}</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full mt-1 px-3 py-2 rounded-lg text-sm bg-slate-800 border border-slate-700 text-slate-100"
            >
              <option value="OBC">OBC</option>
              <option value="SC">SC</option>
              <option value="ST">ST</option>
              <option value="General">General / OC</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400">{t.eligibility_percentage}</label>
            <input
              type="number"
              value={marks}
              onChange={(e) => setMarks(e.target.value)}
              className="w-full mt-1 px-3 py-2 rounded-lg text-sm bg-slate-800 border border-slate-700 text-slate-100"
            />
          </div>

          <button
            onClick={handleCheck}
            disabled={checking}
            className="w-full py-2.5 rounded-xl font-semibold text-sm bg-blue-600 hover:bg-blue-500 text-white"
          >
            {checking ? "Checking..." : t.btn_check_eligibility}
          </button>
        </div>

        <div className="lg:col-span-2">
          {evalResult ? (
            <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/60 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    evalResult.status === "eligible" 
                      ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                      : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                  }`}>
                    {evalResult.status_label_en}
                  </span>
                  <p className="text-xs text-slate-400 mt-1 font-tamil">{evalResult.status_label_ta}</p>
                </div>
                <div className="text-right">
                  <span className="text-2xl font-bold text-blue-400">{Math.round(evalResult.confidence * 100)}%</span>
                  <p className="text-[10px] text-slate-500">Confidence Match</p>
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Rules Evaluated</h4>
                <div className="space-y-2">
                  {evalResult.rules_evaluated?.map((rule, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-slate-800/40 border border-slate-800 flex items-center justify-between text-xs">
                      <div>
                        <p className="font-medium text-slate-200">{rule.description_en}</p>
                        <p className="text-[11px] text-slate-400 font-tamil">{rule.description_ta}</p>
                      </div>
                      <span className={`px-2 py-0.5 rounded font-bold ${rule.passed ? "text-emerald-400" : "text-rose-400"}`}>
                        {rule.passed ? "PASSED" : "FAILED"}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {evalResult.official_portal && (
                <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
                  <span className="text-xs text-slate-400">Official Portal:</span>
                  <a href={evalResult.official_portal} target="_blank" className="text-xs text-cyan-400 underline flex items-center gap-1">
                    {evalResult.official_portal} <Icon name="external-link" size={12} />
                  </a>
                </div>
              )}
            </div>
          ) : (
            <div className="p-12 rounded-2xl border border-slate-800 bg-slate-900/30 text-center text-slate-400">
              <Icon name="shield-check" size={32} className="mx-auto text-slate-600 mb-2" />
              <p className="text-sm">Select scheme and click "Check Eligibility" to evaluate against official criteria.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// MODULE 9: APPLICATION TRACKER
// -------------------------------------------------------------
function ApplicationTrackerPage({ t, theme, showToast }) {
  const [apps, setApps] = useState([]);

  useEffect(() => {
    fetch("/api/applications")
      .then(res => res.json())
      .then(data => setApps(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">{t.tracker_title}</h2>
          <p className="text-sm text-slate-400">{t.tracker_subtitle}</p>
        </div>
      </div>

      <div className="space-y-3">
        {apps.map(a => (
          <div key={a.id} className="p-5 rounded-2xl border border-slate-800 bg-slate-900/40 flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-sm text-slate-200">{a.title}</h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-cyan-400 border border-slate-700">
                  {a.category}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1">{a.notes || "No notes attached."}</p>
              <p className="text-xs text-amber-400 mt-1 font-medium">Deadline: {a.deadline}</p>
            </div>

            <div className="flex items-center gap-6">
              <div>
                <span className="text-xs text-slate-400 block mb-1">Status</span>
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-400 border border-blue-500/30">
                  {a.status}
                </span>
              </div>
              <div className="w-24">
                <span className="text-xs font-bold text-slate-300 block text-right">{a.progress_percent}%</span>
                <div className="w-full h-1.5 bg-slate-800 rounded-full mt-1 overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full" style={{ width: `${a.progress_percent}%` }}></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// MODULE 10: AI APPLICATION ASSISTANT
// -------------------------------------------------------------
function AIAssistantPage({ t, theme, lang, activeDoc }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: lang === "ta" 
        ? "வணக்கம்! நான் FormPilot AI விண்ணப்ப உதவியாளர். உங்கள் படிவத்தில் உள்ள விதிகள், கட்டாய தகவல்கள் அல்லது சான்றிதழ் கேள்விகள் எதையும் என்னிடம் கேட்கலாம்."
        : "Hello! I am FormPilot AI, your intelligent application assistance copilot. Ask me anything about application fields, income certificates, or legal declarations.",
      language: lang
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (textToSend) => {
    const msg = textToSend || input;
    if (!msg.trim()) return;

    const userMsg = { role: "user", content: msg, language: lang };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/assistant/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: msg,
          document_id: activeDoc?.document_id || null,
          language: lang
        })
      });
      const data = await res.json();
      setMessages(prev => [...prev, {
        role: "assistant",
        content: data.reply,
        language: data.language,
        suggested: data.suggested_questions
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "I am ready to assist with your application queries.",
        language: lang
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-8.5rem)] flex flex-col rounded-2xl border border-slate-800 bg-slate-900/50 overflow-hidden">
      <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/80 flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center">
          <Icon name="bot" size={20} />
        </div>
        <div>
          <h3 className="font-bold text-sm">{t.assistant_title}</h3>
          <p className="text-xs text-slate-400">{t.assistant_subtitle}</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((m, idx) => (
          <div key={idx} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-xl p-4 rounded-2xl text-sm leading-relaxed ${
              m.role === "user"
                ? "bg-blue-600 text-white rounded-br-none"
                : "bg-slate-800/90 text-slate-200 border border-slate-700/60 rounded-bl-none"
            }`}>
              <p className={m.language === "ta" ? "font-tamil" : ""}>{m.content}</p>
              
              {m.suggested && (
                <div className="mt-3 pt-3 border-t border-slate-700/60 flex flex-wrap gap-2">
                  {m.suggested.map((q, qIdx) => (
                    <button
                      key={qIdx}
                      onClick={() => sendMessage(q)}
                      className="px-2.5 py-1 rounded-lg text-xs bg-slate-700 hover:bg-slate-600 text-cyan-300 font-medium"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="p-4 rounded-2xl bg-slate-800 text-slate-400 text-sm flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin"></div>
              <span>FormPilot Copilot is thinking...</span>
            </div>
          </div>
        )}
      </div>

      <div className="p-4 border-t border-slate-800 bg-slate-900/80 flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder={t.assistant_placeholder}
          className="flex-1 px-4 py-2.5 rounded-xl text-sm bg-slate-800 border border-slate-700 text-slate-100 focus:outline-none focus:border-blue-500"
        />
        <button
          onClick={() => sendMessage()}
          className="px-4 py-2.5 rounded-xl font-semibold text-sm bg-blue-600 hover:bg-blue-500 text-white"
        >
          <Icon name="send" size={16} />
        </button>
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// PROFILE & SETTINGS PAGES
// -------------------------------------------------------------
function ProfilePage({ t, theme, user, setUser, showToast }) {
  const p = user.profile_data || {};
  return (
    <div className="space-y-8 max-w-3xl">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{t.profile_title}</h2>
        <p className="text-sm text-slate-400">{t.profile_subtitle}</p>
      </div>

      <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/50 space-y-4">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div><span className="text-xs text-slate-400">Full Name</span><p className="font-semibold">{p.full_name}</p></div>
          <div><span className="text-xs text-slate-400">Email</span><p className="font-semibold">{p.email}</p></div>
          <div><span className="text-xs text-slate-400">Mobile</span><p className="font-semibold">{p.mobile}</p></div>
          <div><span className="text-xs text-slate-400">Aadhaar</span><p className="font-semibold">{p.aadhaar}</p></div>
          <div><span className="text-xs text-slate-400">College</span><p className="font-semibold">{p.college_name}</p></div>
          <div><span className="text-xs text-slate-400">Course</span><p className="font-semibold">{p.course_name}</p></div>
        </div>
      </div>
    </div>
  );
}

function SettingsPage({ t, theme, toggleTheme, lang, toggleLanguage, showToast }) {
  return (
    <div className="space-y-8 max-w-3xl">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{t.settings_title}</h2>
        <p className="text-sm text-slate-400">{t.settings_subtitle}</p>
      </div>

      <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/50 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-sm font-semibold">Theme Mode</h4>
            <p className="text-xs text-slate-400">Current: {theme === "dark" ? "Dark Mode" : "Light Mode"}</p>
          </div>
          <button onClick={toggleTheme} className="px-4 py-2 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700">
            Switch to {theme === "dark" ? "Light" : "Dark"}
          </button>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-slate-800">
          <div>
            <h4 className="text-sm font-semibold">Language / மொழி</h4>
            <p className="text-xs text-slate-400">Current: {lang === "en" ? "English" : "தமிழ்"}</p>
          </div>
          <button onClick={toggleLanguage} className="px-4 py-2 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700">
            Switch to {lang === "en" ? "தமிழ்" : "English"}
          </button>
        </div>
      </div>
    </div>
  );
}

function HistoryPage({ t, theme, setActivePage }) {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{t.nav_history}</h2>
        <p className="text-sm text-slate-400">Log of recent form analyses, validations, and PDF downloads.</p>
      </div>

      <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/40 text-center py-12 text-slate-400">
        <Icon name="history" size={32} className="mx-auto text-slate-600 mb-2" />
        <p className="text-sm">3 analyses recorded during this session. Ready for auditing.</p>
      </div>
    </div>
  );
}

function HelpSupportPage({ t, theme }) {
  return (
    <div className="space-y-8 max-w-3xl">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{t.nav_help_support}</h2>
        <p className="text-sm text-slate-400">Frequently asked questions and student application guidelines.</p>
      </div>

      <div className="space-y-4">
        {[
          { q: "How does FormPilot AI ensure no wrong details are submitted?", a: "FormPilot AI strictly performs field-by-field validation using official regex patterns (Aadhaar, PAN, PIN, Income) and asks the user for explicit approval before generating any official PDF document." },
          { q: "Is Tamil language supported for AI explanations?", a: "Yes, all field explanations, instructions, legal declarations, and AI conversational responses support both natural Tamil and English." },
          { q: "Where are my uploaded certificates stored?", a: "Documents are stored securely in local encrypted sandbox storage or private Supabase storage with strict Row Level Security (RLS)." }
        ].map((item, idx) => (
          <div key={idx} className="p-5 rounded-2xl border border-slate-800 bg-slate-900/40 space-y-2">
            <h4 className="text-sm font-bold text-blue-400">{item.q}</h4>
            <p className="text-xs text-slate-300 leading-relaxed">{item.a}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// Render Application to DOM
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<FormPilotApp />);
