# react_app.py - نسخه کامل با همه صفحات

REACT_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - مسیرینو</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/react@18.2.0/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18.2.0/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
        * { font-family: 'Vazirmatn', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
        body { direction: rtl; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; }
        .dark { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
        .light { background: linear-gradient(135deg, #f5f7fa, #e4e8f0); }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(255,255,255,0.1); border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: #6c63ff; border-radius: 10px; }
        .animate-spin-slow { animation: spin 3s linear infinite; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel" data-presets="react">
        const { useState, useEffect, useCallback, useRef, createContext, useContext } = React;
        
        // ========== Context برای مدیریت وضعیت جهانی ==========
        const AppContext = createContext();
        
        const useApp = () => useContext(AppContext);
        
        // ========== Session ID ==========
        const sessionId = "{session_id}";
        
        // ========== API Helper ==========
        const apiCall = async (url, options = {}) => {
            try {
                const res = await fetch(url, options);
                return await res.json();
            } catch(e) {
                console.error('API Error:', e);
                return { error: e.message };
            }
        };
        
        // ========== کامپوننت‌های صفحات ==========
        
        // 1. صفحه اصلی (داشبورد)
        const HomePage = () => {
            const features = [
                { icon: "💬", title: "چت هوشمند", desc: "مشاوره تحصیلی با هوش مصنوعی", path: "chat", color: "from-purple-500 to-pink-500" },
                { icon: "🎯", title: "انتخاب رشته", desc: "تحلیل علمی 5 معیاره", path: "track", color: "from-blue-500 to-cyan-500" },
                { icon: "📉", title: "پیش‌بینی افت", desc: "بررسی 12 فاکتور خطر", path: "risk", color: "from-red-500 to-orange-500" },
                { icon: "🧠", title: "آزمون هالند", desc: "شناسایی تیپ شخصیت", path: "holland", color: "from-green-500 to-teal-500" },
                { icon: "🍅", title: "پومودورو", desc: "مدیریت زمان مطالعه", path: "pomodoro", color: "from-yellow-500 to-orange-500" },
                { icon: "🎯", title: "اهداف SMART", desc: "هدف‌گذاری هوشمند", path: "goals", color: "from-indigo-500 to-purple-500" },
                { icon: "📝", title: "تولید سوال", desc: "سوالات تستی و تشریحی", path: "exam", color: "from-pink-500 to-rose-500" },
                { icon: "🎯", title: "چالش روزانه", desc: "امتیاز و گواهی", path: "challenges", color: "from-amber-500 to-yellow-500" },
                { icon: "📅", title: "تقویم آموزشی", desc: "برنامه و رویدادها", path: "calendar", color: "from-emerald-500 to-green-500" },
                { icon: "👥", title: "گروه‌های مطالعه", desc: "یادگیری گروهی", path: "groups", color: "from-violet-500 to-purple-500" },
            ];
            
            const { setCurrentPage, theme } = useApp();
            
            return (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                    {features.map((f, i) => (
                        <div 
                            key={i}
                            onClick={() => setCurrentPage(f.path)}
                            className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 cursor-pointer transition-all duration-300 hover:scale-105 hover:bg-white/20 border border-white/10"
                        >
                            <div className={`text-5xl mb-4 bg-gradient-to-r ${f.color} bg-clip-text text-transparent`}>
                                {f.icon}
                            </div>
                            <h3 className="text-xl font-bold mb-2">{f.title}</h3>
                            <p className="text-white/60 text-sm">{f.desc}</p>
                        </div>
                    ))}
                </div>
            );
        };
        
        // 2. صفحه چت بات (تکمیل شده)
        const ChatPage = () => {
            const [messages, setMessages] = useState([
                { text: 'سلام! 🌟 من مسیرینو هستم، مشاور تحصیلی هوشمند. چطور می‌تونم بهت کمک کنم؟', type: 'bot' }
            ]);
            const [input, setInput] = useState('');
            const [loading, setLoading] = useState(false);
            const messagesEndRef = useRef(null);
            
            const scrollToBottom = () => {
                messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
            };
            
            useEffect(() => {
                scrollToBottom();
            }, [messages]);
            
            const sendMessage = async () => {
                if (!input.trim()) return;
                const userMsg = input.trim();
                setMessages(prev => [...prev, { text: userMsg, type: 'user' }]);
                setInput('');
                setLoading(true);
                
                const data = await apiCall('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userMsg, session_id: sessionId })
                });
                
                setMessages(prev => [...prev, { text: data.response || 'متاسفانه خطایی رخ داد', type: 'bot' }]);
                setLoading(false);
            };
            
            return (
                <div className="flex flex-col h-[550px]">
                    <div className="flex-1 overflow-y-auto space-y-3 mb-4 p-2">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-3 rounded-2xl ${
                                    msg.type === 'user' 
                                        ? 'bg-gradient-to-r from-purple-600 to-pink-500 text-white' 
                                        : 'bg-white/20 text-white'
                                }`}>
                                    {msg.text}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-white/20 p-3 rounded-2xl">
                                    <div className="flex gap-1">
                                        <span className="w-2 h-2 bg-white rounded-full animate-bounce"></span>
                                        <span className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></span>
                                        <span className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                            placeholder="سوال خود را بپرسید..."
                            className="flex-1 p-3 rounded-full bg-white/20 text-white placeholder-white/50 outline-none focus:ring-2 focus:ring-purple-500"
                        />
                        <button
                            onClick={sendMessage}
                            className="px-6 py-3 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 text-white hover:opacity-90 transition"
                        >
                            ارسال
                        </button>
                    </div>
                </div>
            );
        };
        
        // 3. صفحه پومودورو (تکمیل شده)
        const PomodoroPage = () => {
            const [timeLeft, setTimeLeft] = useState(25 * 60);
            const [isRunning, setIsRunning] = useState(false);
            const [isWorkMode, setIsWorkMode] = useState(true);
            const [pomodoroCount, setPomodoroCount] = useState(0);
            
            useEffect(() => {
                let interval;
                if (isRunning && timeLeft > 0) {
                    interval = setInterval(() => {
                        setTimeLeft(prev => prev - 1);
                    }, 1000);
                } else if (timeLeft === 0) {
                    if (isWorkMode) {
                        setPomodoroCount(prev => prev + 1);
                        setIsWorkMode(false);
                        setTimeLeft(5 * 60);
                    } else {
                        setIsWorkMode(true);
                        setTimeLeft(25 * 60);
                    }
                    setIsRunning(false);
                    alert(isWorkMode ? '🎉 پومودورو کامل شد! وقت استراحت' : '⏰ استراحت تمام شد! وقت مطالعه');
                }
                return () => clearInterval(interval);
            }, [isRunning, timeLeft, isWorkMode]);
            
            const formatTime = (seconds) => {
                const mins = Math.floor(seconds / 60);
                const secs = seconds % 60;
                return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            };
            
            return (
                <div className="text-center py-8">
                    <div className={`text-8xl font-mono mb-6 ${isWorkMode ? 'text-green-400' : 'text-orange-400'}`}>
                        {formatTime(timeLeft)}
                    </div>
                    <div className="text-xl mb-6">{isWorkMode ? '📚 زمان مطالعه' : '☕ زمان استراحت'}</div>
                    <div className="flex gap-4 justify-center mb-8">
                        <button onClick={() => setIsRunning(true)} className="px-8 py-3 rounded-full bg-green-500 text-white hover:bg-green-600 transition text-lg">▶ شروع</button>
                        <button onClick={() => setIsRunning(false)} className="px-8 py-3 rounded-full bg-yellow-500 text-white hover:bg-yellow-600 transition text-lg">⏸ توقف</button>
                        <button onClick={() => { setIsRunning(false); setTimeLeft(25*60); setIsWorkMode(true); }} className="px-8 py-3 rounded-full bg-red-500 text-white hover:bg-red-600 transition text-lg">🔄 ریست</button>
                    </div>
                    <div className="text-white/70 text-lg">✅ پومودوروهای امروز: {pomodoroCount}</div>
                </div>
            );
        };
        
        // 4. صفحه چالش‌ها (تکمیل شده)
        const ChallengesPage = () => {
            const [challenges, setChallenges] = useState([]);
            const [points, setPoints] = useState({ total: 0, weekly: 0 });
            const [level, setLevel] = useState('آسان');
            
            useEffect(() => {
                loadChallenges();
            }, [level]);
            
            const loadChallenges = async () => {
                const data = await apiCall('/get-challenges?session_id=' + sessionId + '&level=' + level);
                setChallenges(data.challenges || []);
                setPoints({ total: data.total_points || 0, weekly: data.weekly_points || 0 });
            };
            
            const completeChallenge = async (challengeId) => {
                const data = await apiCall('/complete-challenge', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, challenge_id: challengeId, level: level })
                });
                if (data.status === 'ok') {
                    alert('🎉 تبریک! ' + data.points + ' امتیاز گرفتی');
                    loadChallenges();
                }
            };
            
            return (
                <div>
                    <div className="flex gap-3 justify-center mb-6">
                        {['آسان', 'متوسط', 'سخت'].map(l => (
                            <button
                                key={l}
                                onClick={() => setLevel(l)}
                                className={`px-5 py-2 rounded-full transition ${level === l ? 'bg-gradient-to-r from-purple-600 to-pink-500 text-white' : 'bg-white/20 text-white hover:bg-white/30'}`}
                            >
                                {l === 'آسان' && '😊 '}{l === 'متوسط' && '🤔 '}{l === 'سخت' && '💪 '}{l}
                            </button>
                        ))}
                    </div>
                    <div className="grid grid-cols-2 gap-4 mb-6">
                        <div className="bg-white/10 rounded-xl p-4 text-center">
                            <div className="text-3xl font-bold text-yellow-400">{points.total}</div>
                            <div className="text-sm">⭐ امتیاز کل</div>
                        </div>
                        <div className="bg-white/10 rounded-xl p-4 text-center">
                            <div className="text-3xl font-bold text-yellow-400">{points.weekly}</div>
                            <div className="text-sm">📅 این هفته</div>
                        </div>
                    </div>
                    <div className="space-y-3">
                        {challenges.map((ch, idx) => (
                            <div key={idx} className="bg-white/10 rounded-xl p-4 flex justify-between items-center">
                                <div>
                                    <div className="font-bold text-lg">{ch.icon} {ch.title}</div>
                                    <div className="text-sm text-white/60">{ch.description}</div>
                                    <div className="text-xs text-yellow-400 mt-1">⭐ {ch.points} امتیاز</div>
                                </div>
                                {ch.status !== 'completed' && (
                                    <button onClick={() => completeChallenge(ch.challenge_id)} className="px-5 py-2 rounded-full bg-green-500 text-white hover:bg-green-600 transition">
                                        انجام دادم
                                    </button>
                                )}
                                {ch.status === 'completed' && (
                                    <span className="px-5 py-2 rounded-full bg-white/20 text-white/60">✅ انجام شد</span>
                                )}
                            </div>
                        ))}
                        {challenges.length === 0 && (
                            <div className="text-center py-8 text-white/60">✨ امروز همه چالش‌ها رو انجام دادی! فردا دوباره بیا ✨</div>
                        )}
                    </div>
                </div>
            );
        };
        
        // 5. صفحه گروه‌ها (تکمیل شده)
        const GroupsPage = () => {
            const [myGroups, setMyGroups] = useState([]);
            const [availableGroups, setAvailableGroups] = useState([]);
            const [showCreateModal, setShowCreateModal] = useState(false);
            const [newGroupName, setNewGroupName] = useState('');
            const [newGroupDesc, setNewGroupDesc] = useState('');
            const [selectedGroup, setSelectedGroup] = useState(null);
            
            useEffect(() => {
                loadGroups();
            }, []);
            
            const loadGroups = async () => {
                const data = await apiCall('/get-groups?session_id=' + sessionId);
                setMyGroups(data.my_groups || []);
                setAvailableGroups(data.available_groups || []);
            };
            
            const createGroup = async () => {
                if (!newGroupName.trim()) return;
                await apiCall('/create-group', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, name: newGroupName, description: newGroupDesc, is_private: 0 })
                });
                setShowCreateModal(false);
                setNewGroupName('');
                setNewGroupDesc('');
                loadGroups();
            };
            
            const joinGroup = async (groupId) => {
                await apiCall('/join-group', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, group_id: groupId })
                });
                loadGroups();
            };
            
            const showGroupDetail = async (groupId) => {
                const data = await apiCall('/get-group-detail?session_id=' + sessionId + '&group_id=' + groupId);
                setSelectedGroup(data);
            };
            
            return (
                <div>
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xl font-bold">📚 گروه‌های من</h3>
                        <button onClick={() => setShowCreateModal(true)} className="px-5 py-2 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 text-white hover:opacity-90 transition">
                            ➕ گروه جدید
                        </button>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                        {myGroups.map(g => (
                            <div key={g.id} onClick={() => showGroupDetail(g.id)} className="bg-white/10 rounded-xl p-4 cursor-pointer hover:bg-white/20 transition">
                                <div className="font-bold text-lg">👥 {g.name}</div>
                                <div className="text-sm text-white/60">👤 {g.member_count} عضو | 🏆 {g.total_points} امتیاز</div>
                                <div className="text-sm text-white/40 mt-1">{g.description}</div>
                            </div>
                        ))}
                        {myGroups.length === 0 && <div className="text-white/60 text-center p-8 col-span-2">هنوز عضوی از گروهی نیستی. یک گروه بساز یا به گروهی بپیوند!</div>}
                    </div>
                    
                    <h3 className="text-xl font-bold mb-4">🌍 گروه‌های عمومی</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {availableGroups.map(g => (
                            <div key={g.id} className="bg-white/10 rounded-xl p-4 flex justify-between items-center">
                                <div>
                                    <div className="font-bold">{g.name}</div>
                                    <div className="text-sm text-white/60">👤 {g.member_count} عضو</div>
                                </div>
                                <button onClick={() => joinGroup(g.id)} className="px-4 py-2 rounded-full bg-green-500 text-white hover:bg-green-600 transition text-sm">
                                    پیوستن
                                </button>
                            </div>
                        ))}
                        {availableGroups.length === 0 && <div className="text-white/60 text-center p-8 col-span-2">گروه عمومی دیگری موجود نیست</div>}
                    </div>
                    
                    {showCreateModal && (
                        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
                            <div className="bg-gray-800 rounded-2xl p-6 w-96">
                                <h3 className="text-xl font-bold mb-4">ایجاد گروه جدید</h3>
                                <input
                                    type="text"
                                    placeholder="نام گروه"
                                    value={newGroupName}
                                    onChange={(e) => setNewGroupName(e.target.value)}
                                    className="w-full p-3 rounded-lg bg-gray-700 text-white mb-3 outline-none focus:ring-2 focus:ring-purple-500"
                                />
                                <textarea
                                    placeholder="توضیحات (اختیاری)"
                                    value={newGroupDesc}
                                    onChange={(e) => setNewGroupDesc(e.target.value)}
                                    className="w-full p-3 rounded-lg bg-gray-700 text-white mb-4 outline-none focus:ring-2 focus:ring-purple-500"
                                    rows="3"
                                />
                                <div className="flex gap-3">
                                    <button onClick={createGroup} className="flex-1 py-2 rounded-full bg-purple-600 text-white hover:bg-purple-700 transition">ایجاد</button>
                                    <button onClick={() => setShowCreateModal(false)} className="flex-1 py-2 rounded-full bg-gray-600 text-white hover:bg-gray-700 transition">انصراف</button>
                                </div>
                            </div>
                        </div>
                    )}
                    
                    {selectedGroup && (
                        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
                            <div className="bg-gray-800 rounded-2xl p-6 w-[600px] max-h-[80vh] overflow-y-auto">
                                <h3 className="text-xl font-bold mb-2">👥 {selectedGroup.group?.name}</h3>
                                <p className="text-white/60 mb-4">{selectedGroup.group?.description}</p>
                                <div className="border-t border-white/10 pt-4 mb-4">
                                    <h4 className="font-bold mb-2">👤 اعضا ({selectedGroup.members?.length || 0})</h4>
                                    {selectedGroup.members?.map((m, i) => (
                                        <div key={i} className="flex justify-between py-2 border-b border-white/10">
                                            <span>{i+1}. {m.user_name}</span>
                                            <span className="text-yellow-400">⭐ {m.points}</span>
                                        </div>
                                    ))}
                                </div>
                                <button onClick={() => setSelectedGroup(null)} className="w-full py-2 rounded-full bg-purple-600 text-white hover:bg-purple-700 transition">بستن</button>
                            </div>
                        </div>
                    )}
                </div>
            );
        };
        
        // 6. صفحه انتخاب رشته (جدید - React)
        const TrackPage = () => {
            const [step, setStep] = useState(1);
            const [formData, setFormData] = useState({
                firstName: '', lastName: '', age: '', gradeLevel: 'هفتم-نهم',
                dominant_think: 'تحلیلی', average_grade: 15, track: ''
            });
            const [subjects, setSubjects] = useState([]);
            const [subjectScores, setSubjectScores] = useState({});
            const [result, setResult] = useState(null);
            const [loading, setLoading] = useState(false);
            
            const gradeLevels = ['ابتدایی', 'هفتم-نهم', 'دهم-دوازدهم', 'دانشگاه'];
            const thinkStyles = [
                { value: 'تحلیلی', icon: '🔍', desc: 'منطقی، حل مسئله' },
                { value: 'خلاق', icon: '🎨', desc: 'ایده‌پرداز، هنری' },
                { value: 'انسانی', icon: '📖', desc: 'اجتماعی، ادبیات' },
                { value: 'تکنولوژی/پروژه', icon: '💻', desc: 'فنی، پروژه‌محور' },
                { value: 'کارآفرین', icon: '🚀', desc: 'رهبر، کسب‌وکار' }
            ];
            
            const updateForm = (field, value) => {
                setFormData(prev => ({ ...prev, [field]: value }));
                if (field === 'gradeLevel' && value !== 'دهم-دوازدهم' && value !== 'دانشگاه') {
                    setFormData(prev => ({ ...prev, track: '' }));
                }
            };
            
            const fetchSubjects = async () => {
                if (step === 2) {
                    let subs = [];
                    const isAdvanced = formData.gradeLevel === 'دهم-دوازدهم' || formData.gradeLevel === 'دانشگاه';
                    if (isAdvanced && formData.track) {
                        const trackSubjects = {
                            'علوم تجربی': ['زیست‌شناسی', 'شیمی', 'فیزیک', 'ریاضی', 'ادبیات فارسی', 'زبان انگلیسی'],
                            'ریاضی فیزیک': ['ریاضی', 'فیزیک', 'شیمی', 'ادبیات فارسی', 'زبان انگلیسی', 'حسابان'],
                            'علوم انسانی': ['ادبیات فارسی', 'عربی', 'تاریخ', 'جغرافیا', 'فلسفه و منطق', 'زبان انگلیسی'],
                            'هنر': ['مبانی هنر', 'خلاقیت', 'تاریخ هنر', 'ادبیات فارسی', 'طراحی', 'زبان انگلیسی']
                        };
                        subs = trackSubjects[formData.track] || [];
                    } else {
                        const basicSubjects = {
                            'ابتدایی': ['ریاضی', 'فارسی', 'علوم', 'قرآن', 'مطالعات اجتماعی'],
                            'هفتم-نهم': ['ریاضی', 'علوم', 'ادبیات فارسی', 'زبان انگلیسی', 'دینی/قرآن', 'مطالعات اجتماعی', 'عربی']
                        };
                        subs = basicSubjects[formData.gradeLevel] || [];
                    }
                    setSubjects(subs);
                    const initialScores = {};
                    subs.forEach(s => {
                        initialScores[s] = { understanding: 3, performance: 3, interest: 3 };
                    });
                    setSubjectScores(initialScores);
                }
            };
            
            useEffect(() => {
                fetchSubjects();
            }, [step, formData.track, formData.gradeLevel]);
            
            const updateScore = (subject, field, value) => {
                setSubjectScores(prev => ({
                    ...prev,
                    [subject]: { ...prev[subject], [field]: parseInt(value) }
                }));
            };
            
            const submitTrack = async () => {
                setLoading(true);
                const body = new FormData();
                Object.entries(formData).forEach(([k, v]) => body.append(k, v));
                Object.entries(subjectScores).forEach(([subject, scores]) => {
                    const key = subject.replace(/ /g, '_');
                    body.append(`${key}__understanding`, scores.understanding);
                    body.append(`${key}__performance`, scores.performance);
                    body.append(`${key}__interest`, scores.interest);
                });
                body.append('step', step + 1);
                
                const res = await fetch('/track-submit', { method: 'POST', body });
                if (res.redirected) {
                    window.location.href = res.url;
                }
                setLoading(false);
            };
            
            if (result) {
                return (
                    <div className="text-center">
                        <div className="animate-spin-slow text-6xl mb-4">⚙️</div>
                        <p className="text-white/60">در حال بارگذاری نتایج...</p>
                    </div>
                );
            }
            
            if (step === 1) {
                return (
                    <div>
                        <h3 className="text-xl font-bold mb-6">📋 مرحله ۱: اطلاعات پایه</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <input type="text" placeholder="نام (اختیاری)" value={formData.firstName} onChange={(e) => updateForm('firstName', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white placeholder-white/50 outline-none focus:ring-2 focus:ring-purple-500" />
                            <input type="text" placeholder="نام خانوادگی (اختیاری)" value={formData.lastName} onChange={(e) => updateForm('lastName', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white placeholder-white/50 outline-none focus:ring-2 focus:ring-purple-500" />
                            <input type="number" placeholder="سن" value={formData.age} onChange={(e) => updateForm('age', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white placeholder-white/50 outline-none focus:ring-2 focus:ring-purple-500" />
                            <select value={formData.gradeLevel} onChange={(e) => updateForm('gradeLevel', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white outline-none focus:ring-2 focus:ring-purple-500">
                                {gradeLevels.map(g => <option key={g} value={g}>{g}</option>)}
                            </select>
                            <select value={formData.dominant_think} onChange={(e) => updateForm('dominant_think', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white outline-none focus:ring-2 focus:ring-purple-500">
                                {thinkStyles.map(t => <option key={t.value} value={t.value}>{t.icon} {t.value} - {t.desc}</option>)}
                            </select>
                            <input type="number" step="0.1" min="0" max="20" placeholder="معدل تقریبی" value={formData.average_grade} onChange={(e) => updateForm('average_grade', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white placeholder-white/50 outline-none focus:ring-2 focus:ring-purple-500" />
                        </div>
                        {(formData.gradeLevel === 'دهم-دوازدهم' || formData.gradeLevel === 'دانشگاه') && (
                            <select value={formData.track} onChange={(e) => updateForm('track', e.target.value)} className="w-full p-3 rounded-xl bg-white/20 text-white outline-none focus:ring-2 focus:ring-purple-500 mb-6">
                                <option value="">رشته تحصیلی خود را انتخاب کنید</option>
                                <option value="ریاضی فیزیک">⚡ ریاضی فیزیک</option>
                                <option value="علوم تجربی">🔬 علوم تجربی</option>
                                <option value="علوم انسانی">📖 علوم انسانی</option>
                                <option value="هنر">🎨 هنر</option>
                            </select>
                        )}
                        <button onClick={() => setStep(2)} className="w-full py-3 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 text-white font-bold hover:opacity-90 transition">
                            بعدی ➡️
                        </button>
                    </div>
                );
            }
            
            return (
                <div>
                    <h3 className="text-xl font-bold mb-6">📚 مرحله ۲: ارزیابی دروس</h3>
                    <div className="space-y-6">
                        {subjects.map(sub => (
                            <div key={sub} className="bg-white/10 rounded-xl p-4">
                                <h4 className="font-bold text-lg mb-3">{sub}</h4>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <div>
                                        <label className="text-sm text-white/60 block mb-1">📖 فهم و درک (1-5)</label>
                                        <input type="number" min="1" max="5" value={subjectScores[sub]?.understanding || 3} onChange={(e) => updateScore(sub, 'understanding', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white outline-none focus:ring-2 focus:ring-purple-500" />
                                    </div>
                                    <div>
                                        <label className="text-sm text-white/60 block mb-1">📝 عملکرد در آزمون (1-5)</label>
                                        <input type="number" min="1" max="5" value={subjectScores[sub]?.performance || 3} onChange={(e) => updateScore(sub, 'performance', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white outline-none focus:ring-2 focus:ring-purple-500" />
                                    </div>
                                    <div>
                                        <label className="text-sm text-white/60 block mb-1">❤️ علاقه به درس (1-5)</label>
                                        <input type="number" min="1" max="5" value={subjectScores[sub]?.interest || 3} onChange={(e) => updateScore(sub, 'interest', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white outline-none focus:ring-2 focus:ring-purple-500" />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                    <button onClick={submitTrack} disabled={loading} className="w-full mt-6 py-3 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 text-white font-bold hover:opacity-90 transition disabled:opacity-50">
                        {loading ? '⏳ در حال ارسال...' : 'مشاهده نتایج پیشرفته 🎯'}
                    </button>
                </div>
            );
        };
        
        // 7. صفحه پیش‌بینی افت (جدید - React)
        const RiskPage = () => {
            const [formData, setFormData] = useState({
                firstName: '', lastName: '', age: '', gradeLevel: 'هفتم-نهم',
                study_hours_rating: 3, study_days_week_rating: 3, study_mode: 'منظم',
                distract_rating: 3, has_review: 'دارم (منظم)', start_days_before_exam: '30+',
                sleep_status: 'خوب', stress_rating: 3, main_weakness_area: 'محاسباتی / تمرین',
                can_execute_plan: 3, has_tutor: 'ندارم', tutor_sessions_week: 0,
                family_support: 'خوب', previous_fail: 'ندارم', test_anxiety: 3
            });
            const [loading, setLoading] = useState(false);
            
            const updateForm = (field, value) => {
                setFormData(prev => ({ ...prev, [field]: value }));
            };
            
            const submitRisk = async () => {
                setLoading(true);
                const body = new FormData();
                Object.entries(formData).forEach(([k, v]) => body.append(k, v));
                const res = await fetch('/risk-submit', { method: 'POST', body });
                if (res.redirected) {
                    window.location.href = res.url;
                }
                setLoading(false);
            };
            
            const riskOptions = {
                study_mode: ['منظم', 'نیمه‌منظم', 'ضربتی'],
                has_review: ['دارم (منظم)', 'بعضی وقت‌ها', 'تقریباً نه'],
                start_days_before_exam: ['30+', '10–20', '3–7', 'از روز امتحان!'],
                sleep_status: ['خوب', 'متوسط', 'کم'],
                main_weakness_area: ['محاسباتی / تمرین', 'مفهومی (درک)', 'تشریحی / نگارش', 'زمان کم می‌آورم', 'بی‌دقتی'],
                has_tutor: ['ندارم', 'تا حدی', 'دارم (کلاس/معلم خصوصی)'],
                family_support: ['خوب', 'متوسط', 'ضعیف'],
                previous_fail: ['ندارم', 'دارم']
            };
            
            return (
                <div>
                    <h3 className="text-xl font-bold mb-6">📉 پیش‌بینی افت نمره</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                        <input type="text" placeholder="نام (اختیاری)" value={formData.firstName} onChange={(e) => updateForm('firstName', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white placeholder-white/50 outline-none focus:ring-2 focus:ring-purple-500" />
                        <input type="text" placeholder="نام خانوادگی" value={formData.lastName} onChange={(e) => updateForm('lastName', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white placeholder-white/50 outline-none focus:ring-2 focus:ring-purple-500" />
                        <input type="number" placeholder="سن" value={formData.age} onChange={(e) => updateForm('age', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white placeholder-white/50 outline-none focus:ring-2 focus:ring-purple-500" />
                        <select value={formData.gradeLevel} onChange={(e) => updateForm('gradeLevel', e.target.value)} className="p-3 rounded-xl bg-white/20 text-white outline-none focus:ring-2 focus:ring-purple-500">
                            <option value="هفتم-نهم">هفتم-نهم</option>
                            <option value="دهم-دوازدهم">دهم-دوازدهم</option>
                            <option value="دانشگاه">دانشگاه</option>
                        </select>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                        <div><label className="text-sm text-white/60">ساعت مطالعه روزانه (1-5)</label><input type="number" min="1" max="5" value={formData.study_hours_rating} onChange={(e) => updateForm('study_hours_rating', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white" /></div>
                        <div><label className="text-sm text-white/60">روزهای مطالعه در هفته (1-7)</label><input type="number" min="1" max="7" value={formData.study_days_week_rating} onChange={(e) => updateForm('study_days_week_rating', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white" /></div>
                        <div><label className="text-sm text-white/60">شیوه مطالعه</label><select value={formData.study_mode} onChange={(e) => updateForm('study_mode', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white">{riskOptions.study_mode.map(o => <option key={o}>{o}</option>)}</select></div>
                        <div><label className="text-sm text-white/60">حواس‌پرتی (1-5)</label><input type="number" min="1" max="5" value={formData.distract_rating} onChange={(e) => updateForm('distract_rating', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white" /></div>
                        <div><label className="text-sm text-white/60">مرور بعد از یادگیری</label><select value={formData.has_review} onChange={(e) => updateForm('has_review', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white">{riskOptions.has_review.map(o => <option key={o}>{o}</option>)}</select></div>
                        <div><label className="text-sm text-white/60">شروع مطالعه قبل از امتحان</label><select value={formData.start_days_before_exam} onChange={(e) => updateForm('start_days_before_exam', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white">{riskOptions.start_days_before_exam.map(o => <option key={o}>{o}</option>)}</select></div>
                        <div><label className="text-sm text-white/60">کیفیت خواب</label><select value={formData.sleep_status} onChange={(e) => updateForm('sleep_status', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white">{riskOptions.sleep_status.map(o => <option key={o}>{o}</option>)}</select></div>
                        <div><label className="text-sm text-white/60">استرس قبل امتحان (1-5)</label><input type="number" min="1" max="5" value={formData.stress_rating} onChange={(e) => updateForm('stress_rating', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white" /></div>
                        <div><label className="text-sm text-white/60">ناحیه ضعف اصلی</label><select value={formData.main_weakness_area} onChange={(e) => updateForm('main_weakness_area', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white">{riskOptions.main_weakness_area.map(o => <option key={o}>{o}</option>)}</select></div>
                        <div><label className="text-sm text-white/60">اجرای برنامه (1-5)</label><input type="number" min="1" max="5" value={formData.can_execute_plan} onChange={(e) => updateForm('can_execute_plan', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white" /></div>
                        <div><label className="text-sm text-white/60">معلم خصوصی</label><select value={formData.has_tutor} onChange={(e) => updateForm('has_tutor', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white">{riskOptions.has_tutor.map(o => <option key={o}>{o}</option>)}</select></div>
                        <div><label className="text-sm text-white/60">جلسات پشتیبان در هفته</label><input type="number" min="0" max="7" value={formData.tutor_sessions_week} onChange={(e) => updateForm('tutor_sessions_week', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white" /></div>
                        <div><label className="text-sm text-white/60">حمایت خانواده</label><select value={formData.family_support} onChange={(e) => updateForm('family_support', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white">{riskOptions.family_support.map(o => <option key={o}>{o}</option>)}</select></div>
                        <div><label className="text-sm text-white/60">سابقه افت نمره</label><select value={formData.previous_fail} onChange={(e) => updateForm('previous_fail', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white">{riskOptions.previous_fail.map(o => <option key={o}>{o}</option>)}</select></div>
                        <div><label className="text-sm text-white/60">اضطراب امتحان (1-5)</label><input type="number" min="1" max="5" value={formData.test_anxiety} onChange={(e) => updateForm('test_anxiety', e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white" /></div>
                    </div>
                    
                    <button onClick={submitRisk} disabled={loading} className="w-full py-3 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 text-white font-bold hover:opacity-90 transition disabled:opacity-50">
                        {loading ? '⏳ در حال ارسال...' : 'محاسبه دقیق ریسک افت نمره 📊'}
                    </button>
                </div>
            );
        };
        
        // 8. صفحه آزمون هالند (جدید - React)
        const HollandPage = () => {
            const [currentQ, setCurrentQ] = useState(0);
            const [answers, setAnswers] = useState(Array(45).fill(null));
            const [showResult, setShowResult] = useState(false);
            const [result, setResult] = useState(null);
            
            const questions = [
                "من کار با ابزار و ماشین‌آلات را دوست دارم.", "من فردی عملی و واقع‌گرا هستم.", "من تعمیر وسایل برقی و مکانیکی را بلدم.",
                "من از کارهای فیزیکی و بیرون از دفتر لذت می‌برم.", "من رانندگی و کار با ماشین‌آلات را دوست دارم.", "من به طبیعت و حیوانات علاقه دارم.",
                "من از کارهای علمی و تحقیقاتی لذت می‌برم.", "من حل مسائل ریاضی و علمی را دوست دارم.", "من به کشف و یادگیری چیزهای جدید علاقه دارم.",
                "من فردی تحلیلی و منطقی هستم.", "من کار در آزمایشگاه را دوست دارم.", "من به مطالعه کتاب‌های علمی و تخصصی علاقه دارم.",
                "من هنرمند و خلاق هستم.", "من طراحی و نقاشی را دوست دارم.", "من موسیقی یا تئاتر را دوست دارم.",
                "من نوشتن داستان یا شعر را دوست دارم.", "من از کارهای هنری و خلاقانه لذت می‌برم.", "من ایده‌های جدید و نوآورانه دارم.",
                "من به کمک به دیگران علاقه دارم.", "من تدریس و آموزش را دوست دارم.", "من مشاوره و راهنمایی دیگران را دوست دارم.",
                "من کار در حوزه سلامت و پزشکی را دوست دارم.", "من از ارتباط با مردم لذت می‌برم.", "من کار تیمی و گروهی را ترجیح می‌دهم.",
                "من رهبری و مدیریت تیم را دوست دارم.", "من فروش و مذاکره را دوست دارم.", "من به کسب‌وکار و کارآفرینی علاقه دارم.",
                "من سخنرانی در جمع را دوست دارم.", "من متقاعد کردن دیگران را بلدم.", "من ریسک‌پذیر و جسور هستم.",
                "من سازماندهی و برنامه‌ریزی را دوست دارم.", "من کار با کامپیوتر و نرم‌افزار را دوست دارم.", "من به امور مالی و حسابداری علاقه دارم.",
                "من جزئیات را دقیق رعایت می‌کنم.", "من بایگانی و نظم‌دهی اطلاعات را دوست دارم.", "من از کارهای دفتری و اداری لذت می‌برم.",
                "من کار در بانک یا موسسه مالی را دوست دارم.", "من قوانین و مقررات را دقیق رعایت می‌کنم.", "من تحقیق و جستجوی اطلاعات را دوست دارم.",
                "من سفر و ماجراجویی را دوست دارم.", "من ورزش و فعالیت بدنی را دوست دارم.", "من یادگیری زبان خارجی را دوست دارم.",
                "من کارآفرینی و راه‌اندازی کسب‌وکار را دوست دارم.", "من به سیاست و مسائل اجتماعی علاقه دارم.", "من برنامه‌نویسی و کدنویسی را دوست دارم."
            ];
            
            const types = [
                { name: "واقع‌گرا", icon: "🔧", desc: "عملی، فنی، مکانیکی - مناسب برای مهندسی، تعمیرات", jobs: "مهندسی مکانیک، برق، عمران، معماری" },
                { name: "پژوهشی", icon: "🔬", desc: "تحلیلی، علمی - مناسب برای پزشکی، داروسازی، تحقیق", jobs: "پزشکی، دندانپزشکی، داروسازی، بیوتکنولوژی" },
                { name: "هنری", icon: "🎨", desc: "خلاق، ایده‌پرداز - مناسب برای هنر، طراحی، موسیقی", jobs: "گرافیک، انیمیشن، طراحی داخلی، موسیقی" },
                { name: "اجتماعی", icon: "🤝", desc: "یاری‌رسان، آموزشی - مناسب برای معلمی، روانشناسی", jobs: "روانشناسی، مشاوره، مددکاری، معلمی" },
                { name: "متهور", icon: "🚀", desc: "رهبر، مدیر - مناسب برای مدیریت، حقوق، فروش", jobs: "مدیریت بازرگانی، حقوق، فروش، کارآفرینی" },
                { name: "سازمانی", icon: "📊", desc: "دقیق، اداری - مناسب برای حسابداری، امور مالی", jobs: "حسابداری، امور مالی، مدیریت اداری" }
            ];
            
            const answerQuestion = (val) => {
                const newAnswers = [...answers];
                newAnswers[currentQ] = val;
                setAnswers(newAnswers);
                if (currentQ < 44) {
                    setCurrentQ(currentQ + 1);
                } else {
                    calculateResults(newAnswers);
                }
            };
            
            const calculateResults = (finalAnswers) => {
                const scores = [0, 0, 0, 0, 0, 0];
                const ranges = [[0,7], [8,14], [15,21], [22,28], [29,35], [36,44]];
                for (let i = 0; i < 45; i++) {
                    for (let t = 0; t < 6; t++) {
                        if (i >= ranges[t][0] && i <= ranges[t][1]) {
                            scores[t] += (finalAnswers[i] || 3);
                            break;
                        }
                    }
                }
                const maxScore = Math.max(...scores);
                const primaryIndex = scores.indexOf(maxScore);
                const percentages = scores.map(s => Math.round((s / 45) * 100));
                setResult({ primary: types[primaryIndex], percentages, scores: types.map((t, i) => ({ ...t, percent: percentages[i] })) });
                setShowResult(true);
                
                apiCall('/save-holland-test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, scores, primary_type: types[primaryIndex].name, percentages })
                });
            };
            
            if (showResult && result) {
                return (
                    <div className="text-center">
                        <div className="text-8xl mb-4">{result.primary.icon}</div>
                        <h3 className="text-2xl font-bold mb-2">{result.primary.name}</h3>
                        <p className="text-white/70 mb-4">{result.primary.desc}</p>
                        <div className="bg-white/10 rounded-xl p-4 mb-6">
                            <p className="font-bold mb-2">💼 پیشنهاد شغلی:</p>
                            <p>{result.primary.jobs}</p>
                        </div>
                        <div className="space-y-2 mb-6">
                            {result.scores.map((t, i) => (
                                <div key={i} className="flex items-center gap-3">
                                    <span className="w-24">{t.icon} {t.name}</span>
                                    <div className="flex-1 h-3 bg-white/20 rounded-full overflow-hidden">
                                        <div className="h-full bg-gradient-to-r from-purple-600 to-pink-500 rounded-full" style={{ width: `${t.percent}%` }}></div>
                                    </div>
                                    <span className="w-12">{t.percent}%</span>
                                </div>
                            ))}
                        </div>
                        <button onClick={() => { setCurrentQ(0); setAnswers(Array(45).fill(null)); setShowResult(false); setResult(null); }} className="px-6 py-2 rounded-full bg-purple-600 text-white">🔄 شروع مجدد</button>
                    </div>
                );
            }
            
            return (
                <div>
                    <div className="mb-4 flex justify-between items-center">
                        <span className="text-sm text-white/60">سوال {currentQ + 1} از 45</span>
                        <div className="flex-1 mx-4 h-2 bg-white/20 rounded-full overflow-hidden">
                            <div className="h-full bg-gradient-to-r from-purple-600 to-pink-500 rounded-full" style={{ width: `${((currentQ + 1) / 45) * 100}%` }}></div>
                        </div>
                    </div>
                    <div className="bg-white/10 rounded-2xl p-6 mb-6">
                        <p className="text-lg mb-6">{questions[currentQ]}</p>
                        <div className="grid grid-cols-5 gap-2">
                            {[1, 2, 3, 4, 5].map(val => (
                                <button key={val} onClick={() => answerQuestion(val)} className="py-2 rounded-full bg-white/20 hover:bg-purple-600 transition">
                                    {val} {val === 1 ? 'خیلی کم' : val === 2 ? 'کم' : val === 3 ? 'متوسط' : val === 4 ? 'زیاد' : 'خیلی زیاد'}
                                </button>
                            ))}
                        </div>
                    </div>
                    <div className="flex gap-3">
                        <button onClick={() => currentQ > 0 && setCurrentQ(currentQ - 1)} disabled={currentQ === 0} className="flex-1 py-2 rounded-full bg-white/20 disabled:opacity-50">قبلی</button>
                        <button onClick={() => answers[currentQ] !== null && currentQ < 44 && setCurrentQ(currentQ + 1)} disabled={answers[currentQ] === null} className="flex-1 py-2 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 disabled:opacity-50">بعدی</button>
                    </div>
                </div>
            );
        };
        
        // 9. صفحه اهداف SMART (جدید - React)
        const GoalsPage = () => {
            const [goals, setGoals] = useState([]);
            const [showModal, setShowModal] = useState(false);
            const [showProgressModal, setShowProgressModal] = useState(false);
            const [selectedGoal, setSelectedGoal] = useState(null);
            const [formData, setFormData] = useState({ title: '', measurable: '', achievable: '', relevant: '', deadline: '', priority: 'medium', category: 'تحصیلی' });
            const [progressValue, setProgressValue] = useState(0);
            const [progressNote, setProgressNote] = useState('');
            
            useEffect(() => { loadGoals(); }, []);
            
            const loadGoals = async () => {
                const data = await apiCall('/get-goals?session_id=' + sessionId);
                setGoals(data.goals || []);
            };
            
            const createGoal = async () => {
                await apiCall('/create-goal', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, ...formData })
                });
                setShowModal(false);
                setFormData({ title: '', measurable: '', achievable: '', relevant: '', deadline: '', priority: 'medium', category: 'تحصیلی' });
                loadGoals();
            };
            
            const updateProgress = async () => {
                await apiCall('/update-goal-progress', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, goal_id: selectedGoal?.id, progress: progressValue, note: progressNote })
                });
                setShowProgressModal(false);
                setProgressValue(0);
                setProgressNote('');
                loadGoals();
            };
            
            const deleteGoal = async (goalId) => {
                if (confirm('آیا مطمئنی؟')) {
                    await apiCall('/delete-goal', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ session_id: sessionId, goal_id: goalId })
                    });
                    loadGoals();
                }
            };
            
            const completedCount = goals.filter(g => g.status === 'completed').length;
            const avgProgress = goals.length ? Math.round(goals.reduce((s, g) => s + (g.progress || 0), 0) / goals.length) : 0;
            
            return (
                <div>
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xl font-bold">🎯 اهداف SMART</h3>
                        <button onClick={() => setShowModal(true)} className="px-5 py-2 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 text-white">➕ هدف جدید</button>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-4 mb-6">
                        <div className="bg-white/10 rounded-xl p-3 text-center"><div className="text-2xl font-bold">{goals.length}</div><div className="text-sm">کل اهداف</div></div>
                        <div className="bg-white/10 rounded-xl p-3 text-center"><div className="text-2xl font-bold">{completedCount}</div><div className="text-sm">تکمیل شده</div></div>
                        <div className="bg-white/10 rounded-xl p-3 text-center"><div className="text-2xl font-bold">{avgProgress}%</div><div className="text-sm">میانگین پیشرفت</div></div>
                    </div>
                    
                    <div className="space-y-3">
                        {goals.map(g => (
                            <div key={g.id} className={`bg-white/10 rounded-xl p-4 border-r-4 ${g.priority === 'high' ? 'border-red-500' : g.priority === 'medium' ? 'border-yellow-500' : 'border-green-500'}`}>
                                <div className="flex justify-between items-start mb-2 flex-wrap gap-2">
                                    <span className="font-bold text-lg">{g.title}</span>
                                    <div className="flex gap-2">
                                        <button onClick={() => { setSelectedGoal(g); setProgressValue(g.progress || 0); setShowProgressModal(true); }} className="px-3 py-1 rounded-full bg-blue-500 text-white text-sm">📈 پیشرفت</button>
                                        <button onClick={() => deleteGoal(g.id)} className="px-3 py-1 rounded-full bg-red-500 text-white text-sm">🗑️</button>
                                    </div>
                                </div>
                                <div className="h-2 bg-white/20 rounded-full overflow-hidden mb-2"><div className="h-full bg-gradient-to-r from-purple-600 to-pink-500 rounded-full" style={{ width: `${g.progress || 0}%` }}></div></div>
                                <div className="text-sm text-white/60 flex gap-3 flex-wrap">
                                    <span>📊 پیشرفت: {g.progress || 0}%</span>
                                    <span>🏷️ اولویت: {g.priority === 'high' ? '🔴 بالا' : g.priority === 'medium' ? '🟡 متوسط' : '🟢 پایین'}</span>
                                    {g.deadline && <span>⏰ مهلت: {g.deadline}</span>}
                                </div>
                                {g.measurable && <div className="text-xs text-white/40 mt-2">📏 {g.measurable}</div>}
                            </div>
                        ))}
                        {goals.length === 0 && <div className="text-center py-8 text-white/60">هنوز هدفی تعیین نکرده‌ای. دکمه "هدف جدید" رو بزن!</div>}
                    </div>
                    
                    {showModal && (
                        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
                            <div className="bg-gray-800 rounded-2xl p-6 w-[500px] max-h-[80vh] overflow-y-auto">
                                <h3 className="text-xl font-bold mb-4">هدف SMART جدید</h3>
                                <input type="text" placeholder="عنوان هدف" value={formData.title} onChange={(e) => setFormData({...formData, title: e.target.value})} className="w-full p-2 rounded-lg bg-gray-700 text-white mb-3" />
                                <textarea placeholder="معیار اندازه‌گیری (M)" value={formData.measurable} onChange={(e) => setFormData({...formData, measurable: e.target.value})} className="w-full p-2 rounded-lg bg-gray-700 text-white mb-3" rows="2" />
                                <textarea placeholder="قابل دستیابی (A)" value={formData.achievable} onChange={(e) => setFormData({...formData, achievable: e.target.value})} className="w-full p-2 rounded-lg bg-gray-700 text-white mb-3" rows="2" />
                                <textarea placeholder="مرتبط با هدف (R)" value={formData.relevant} onChange={(e) => setFormData({...formData, relevant: e.target.value})} className="w-full p-2 rounded-lg bg-gray-700 text-white mb-3" rows="2" />
                                <input type="date" value={formData.deadline} onChange={(e) => setFormData({...formData, deadline: e.target.value})} className="w-full p-2 rounded-lg bg-gray-700 text-white mb-3" />
                                <select value={formData.priority} onChange={(e) => setFormData({...formData, priority: e.target.value})} className="w-full p-2 rounded-lg bg-gray-700 text-white mb-3">
                                    <option value="high">🔴 اولویت بالا</option><option value="medium">🟡 اولویت متوسط</option><option value="low">🟢 اولویت پایین</option>
                                </select>
                                <select value={formData.category} onChange={(e) => setFormData({...formData, category: e.target.value})} className="w-full p-2 rounded-lg bg-gray-700 text-white mb-4">
                                    <option value="تحصیلی">📚 تحصیلی</option><option value="کنکور">🎯 کنکور</option><option value="مهارتی">💡 مهارتی</option>
                                </select>
                                <div className="flex gap-3"><button onClick={createGoal} className="flex-1 py-2 rounded-full bg-purple-600 text-white">ایجاد</button><button onClick={() => setShowModal(false)} className="flex-1 py-2 rounded-full bg-gray-600 text-white">انصراف</button></div>
                            </div>
                        </div>
                    )}
                    
                    {showProgressModal && selectedGoal && (
                        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
                            <div className="bg-gray-800 rounded-2xl p-6 w-96">
                                <h3 className="text-xl font-bold mb-2">{selectedGoal.title}</h3>
                                <div className="mb-4"><label className="text-sm">پیشرفت: {progressValue}%</label><input type="range" min="0" max="100" value={progressValue} onChange={(e) => setProgressValue(e.target.value)} className="w-full" /></div>
                                <textarea placeholder="یادداشت پیشرفت" value={progressNote} onChange={(e) => setProgressNote(e.target.value)} className="w-full p-2 rounded-lg bg-gray-700 text-white mb-4" rows="3" />
                                <div className="flex gap-3"><button onClick={updateProgress} className="flex-1 py-2 rounded-full bg-purple-600 text-white">ذخیره</button><button onClick={() => setShowProgressModal(false)} className="flex-1 py-2 rounded-full bg-gray-600 text-white">انصراف</button></div>
                            </div>
                        </div>
                    )}
                </div>
            );
        };
        
        // 10. صفحه تولید سوال (جدید - React)
        const ExamPage = () => {
            const [params, setParams] = useState({ subject: 'ریاضی', grade_level: 'هفتم-نهم', difficulty: 'متوسط', question_type: 'test', count: 5 });
            const [questions, setQuestions] = useState([]);
            const [answers, setAnswers] = useState({});
            const [showResult, setShowResult] = useState(false);
            const [score, setScore] = useState(null);
            const [loading, setLoading] = useState(false);
            
            const subjects = ['ریاضی', 'علوم', 'فیزیک', 'زیست', 'شیمی', 'علوم تجربی'];
            const gradeLevels = ['ابتدایی', 'هفتم-نهم', 'دهم-دوازدهم'];
            const difficulties = ['آسان', 'متوسط', 'سخت'];
            const questionTypes = [{ value: 'test', label: 'فقط تستی' }, { value: 'descriptive', label: 'فقط تشریحی' }, { value: 'both', label: 'تستی + تشریحی' }];
            
            const generateQuestions = async () => {
                setLoading(true);
                const data = await apiCall('/generate-questions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, ...params })
                });
                setQuestions(data.questions || []);
                setAnswers({});
                setShowResult(false);
                setScore(null);
                setLoading(false);
            };
            
            const updateAnswer = (idx, value) => { setAnswers(prev => ({ ...prev, [idx]: value })); };
            
            const submitExam = () => {
                let correct = 0;
                const results = questions.map((q, idx) => {
                    const userAnswer = answers[idx] || '';
                    const isCorrect = q.type === 'test' ? userAnswer === q.answer : false;
                    if (isCorrect) correct++;
                    return { ...q, userAnswer, isCorrect };
                });
                setScore({ correct, total: questions.length, percent: Math.round((correct / questions.length) * 100), results });
                setShowResult(true);
                
                apiCall('/save-exam-result', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, subject: params.subject, grade_level: params.grade_level, questions_count: questions.length, score: Math.round((correct / questions.length) * 100), answers: results })
                });
            };
            
            return (
                <div>
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-6">
                        <select value={params.subject} onChange={(e) => setParams({...params, subject: e.target.value})} className="p-2 rounded-lg bg-white/20 text-white">{subjects.map(s => <option key={s}>{s}</option>)}</select>
                        <select value={params.grade_level} onChange={(e) => setParams({...params, grade_level: e.target.value})} className="p-2 rounded-lg bg-white/20 text-white">{gradeLevels.map(g => <option key={g}>{g}</option>)}</select>
                        <select value={params.difficulty} onChange={(e) => setParams({...params, difficulty: e.target.value})} className="p-2 rounded-lg bg-white/20 text-white">{difficulties.map(d => <option key={d}>{d}</option>)}</select>
                        <select value={params.question_type} onChange={(e) => setParams({...params, question_type: e.target.value})} className="p-2 rounded-lg bg-white/20 text-white">{questionTypes.map(q => <option key={q.value} value={q.value}>{q.label}</option>)}</select>
                        <input type="number" min="1" max="20" value={params.count} onChange={(e) => setParams({...params, count: parseInt(e.target.value)})} className="p-2 rounded-lg bg-white/20 text-white" />
                    </div>
                    <button onClick={generateQuestions} disabled={loading} className="w-full py-3 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 text-white font-bold mb-6 disabled:opacity-50">
                        {loading ? '⏳ در حال تولید...' : '🎲 تولید سوالات'}
                    </button>
                    
                    {!showResult && questions.length > 0 && (
                        <div className="space-y-4">
                            {questions.map((q, idx) => (
                                <div key={idx} className="bg-white/10 rounded-xl p-4">
                                    <p className="font-bold mb-2">{idx+1}. {q.question}</p>
                                    {q.type === 'test' && q.options && (
                                        <div className="space-y-2 mr-4">
                                            {q.options.map((opt, oidx) => (
                                                <label key={oidx} className="flex items-center gap-2"><input type="radio" name={`q${idx}`} value={opt} onChange={() => updateAnswer(idx, opt)} /> {opt}</label>
                                            ))}
                                        </div>
                                    )}
                                    {q.type === 'descriptive' && <textarea placeholder="پاسخ خود را بنویسید..." onChange={(e) => updateAnswer(idx, e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white mt-2" rows="3" />}
                                </div>
                            ))}
                            <button onClick={submitExam} className="w-full py-3 rounded-full bg-green-500 text-white font-bold">📊 ثبت پاسخ‌ها و مشاهده نمره</button>
                        </div>
                    )}
                    
                    {showResult && score && (
                        <div className="text-center">
                            <div className="text-5xl font-bold text-yellow-400 mb-4">{score.percent}%</div>
                            <p className="mb-6">از {score.total} سوال، {score.correct} سوال صحیح</p>
                            <div className="space-y-3 mb-6">
                                {score.results.map((r, idx) => (
                                    <div key={idx} className={`bg-white/10 rounded-xl p-3 text-right ${r.isCorrect ? 'border-r-4 border-green-500' : 'border-r-4 border-red-500'}`}>
                                        <p className="font-bold">{idx+1}. {r.question}</p>
                                        <p className="text-yellow-400 text-sm">پاسخ شما: {r.userAnswer || '(پاسخی داده نشده)'}</p>
                                        <p className="text-green-400 text-sm">پاسخ صحیح: {r.answer || r.answer_template}</p>
                                    </div>
                                ))}
                            </div>
                            <button onClick={() => { setQuestions([]); setShowResult(false); setScore(null); }} className="px-6 py-2 rounded-full bg-purple-600 text-white">🔄 آزمون جدید</button>
                        </div>
                    )}
                </div>
            );
        };
        
        // 11. صفحه تقویم آموزشی (جدید - React)
        const CalendarPage = () => {
            const [currentYear, setCurrentYear] = useState(1404);
            const [currentMonth, setCurrentMonth] = useState(1);
            const [calendarData, setCalendarData] = useState(null);
            const [selectedDateEvents, setSelectedDateEvents] = useState([]);
            const [eventTitle, setEventTitle] = useState('');
            const [eventDate, setEventDate] = useState('');
            const [eventDesc, setEventDesc] = useState('');
            
            const monthNames = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'];
            const weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه'];
            
            useEffect(() => { loadCalendar(); }, [currentYear, currentMonth]);
            
            const loadCalendar = async () => {
                const data = await apiCall(`/get-calendar-data?session_id=${sessionId}&year=${currentYear}&month=${currentMonth}`);
                setCalendarData(data);
            };
            
            const addEvent = async () => {
                if (!eventTitle || !eventDate) return;
                await apiCall('/add-calendar-event', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, title: eventTitle, date: eventDate.replace('/', '-'), description: eventDesc })
                });
                setEventTitle('');
                setEventDate('');
                setEventDesc('');
                loadCalendar();
            };
            
            if (!calendarData) return <div className="text-center py-8">⏳ در حال بارگذاری...</div>;
            
            const daysInMonth = calendarData.month_days || 31;
            const firstWeekday = calendarData.first_weekday || 0;
            const days = [];
            for (let i = 0; i < firstWeekday; i++) days.push(null);
            for (let i = 1; i <= daysInMonth; i++) days.push(i);
            while (days.length < 42) days.push(null);
            
            const getEventsForDay = (day) => {
                if (!day) return [];
                const dateStr = `${currentYear}-${String(currentMonth).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
                return (calendarData.events || []).filter(e => e.date === dateStr);
            };
            
            const getEventColor = (type) => {
                if (type === 'exam') return 'bg-red-500';
                if (type === 'holiday') return 'bg-green-500';
                if (type === 'study_task') return 'bg-blue-500';
                if (type === 'challenge') return 'bg-yellow-500';
                if (type === 'goal_deadline') return 'bg-purple-500';
                return 'bg-gray-500';
            };
            
            return (
                <div>
                    <div className="flex justify-between items-center mb-6">
                        <button onClick={() => { if (currentMonth === 1) { setCurrentMonth(12); setCurrentYear(currentYear-1); } else { setCurrentMonth(currentMonth-1); } }} className="px-4 py-2 rounded-full bg-white/20">◀ ماه قبل</button>
                        <h3 className="text-xl font-bold">{monthNames[currentMonth-1]} {currentYear}</h3>
                        <button onClick={() => { if (currentMonth === 12) { setCurrentMonth(1); setCurrentYear(currentYear+1); } else { setCurrentMonth(currentMonth+1); } }} className="px-4 py-2 rounded-full bg-white/20">ماه بعد ▶</button>
                    </div>
                    
                    <div className="grid grid-cols-7 gap-1 mb-2">
                        {weekdays.map(d => <div key={d} className="text-center py-2 text-white/60 text-sm">{d}</div>)}
                    </div>
                    <div className="grid grid-cols-7 gap-1">
                        {days.map((day, idx) => {
                            const events = getEventsForDay(day);
                            return (
                                <div key={idx} onClick={() => day && setSelectedDateEvents(events)} className={`min-h-[80px] p-2 rounded-xl bg-white/5 hover:bg-white/10 cursor-pointer transition ${day ? '' : 'opacity-0'}`}>
                                    {day && <div className="font-bold text-sm">{day}</div>}
                                    <div className="flex flex-wrap gap-1 mt-1">
                                        {events.slice(0, 3).map((e, eidx) => <div key={eidx} className={`w-2 h-2 rounded-full ${getEventColor(e.type)}`} title={e.title}></div>)}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                    
                    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-white/10 rounded-xl p-4">
                            <h4 className="font-bold mb-2">📋 رویدادهای انتخاب شده</h4>
                            {selectedDateEvents.length === 0 ? <p className="text-white/60 text-sm">روزی را انتخاب کنید</p> : selectedDateEvents.map((e, i) => <div key={i} className="border-b border-white/10 py-2"><strong>{e.title}</strong><br /><span className="text-xs text-white/60">{e.description}</span></div>)}
                        </div>
                        <div className="bg-white/10 rounded-xl p-4">
                            <h4 className="font-bold mb-2">➕ افزودن رویداد شخصی</h4>
                            <input type="text" placeholder="عنوان رویداد" value={eventTitle} onChange={(e) => setEventTitle(e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white mb-2" />
                            <input type="text" placeholder="تاریخ (مثال: 1404/01/15)" value={eventDate} onChange={(e) => setEventDate(e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white mb-2" />
                            <textarea placeholder="توضیحات" value={eventDesc} onChange={(e) => setEventDesc(e.target.value)} className="w-full p-2 rounded-lg bg-white/20 text-white mb-2" rows="2" />
                            <button onClick={addEvent} className="w-full py-2 rounded-full bg-purple-600 text-white">افزودن به تقویم</button>
                        </div>
                    </div>
                </div>
            );
        };
        
        // ========== کامپوننت اصلی با روتینگ ==========
        const App = () => {
            const [currentPage, setCurrentPage] = useState('home');
            const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');
            
            useEffect(() => {
                document.body.className = theme;
                localStorage.setItem('theme', theme);
            }, [theme]);
            
            const toggleTheme = () => setTheme(theme === 'dark' ? 'light' : 'dark');
            
            // جایگزین کنید (در بخش const pages = { ... })
            const pages = {
                home: HomePage, 
                chat: ChatPage, 
                pomodoro: PomodoroPage, 
                challenges: ChallengesPage,
                groups: GroupsPage, 
                track: TrackPage, 
                risk: RiskPage, 
                holland: HollandPage,
                goals: GoalsPage, 
                exam: ExamPage, 
                calendar: CalendarPage,
                pathfinder: PathFinderPage,    
                mlpredictor: MLPredictorPage   
            };
            const PageComponent = pages[currentPage] || HomePage;
            const pageTitles = { home: 'خانه', chat: 'چت بات', pomodoro: 'پومودورو', challenges: 'چالش‌ها', groups: 'گروه‌ها', track: 'انتخاب رشته', risk: 'پیش‌بینی افت', holland: 'هالند', goals: 'اهداف SMART', exam: 'تولید سوال', calendar: 'تقویم' };
            
            return (
                <AppContext.Provider value={{ currentPage, setCurrentPage, theme, toggleTheme }}>
                    <div className="min-h-screen p-4" dir="rtl">
                        <div className="max-w-6xl mx-auto">
                            <div className="flex justify-between items-center mb-6 p-4 bg-white/10 backdrop-blur-lg rounded-2xl">
                                <div className="flex items-center gap-2">
                                    <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-purple-400 bg-clip-text text-transparent">🎓 مسیرینو</h1>
                                    <span className="text-white/40 text-sm">| {pageTitles[currentPage]}</span>
                                </div>
                                <div className="flex gap-2">
                                    <button onClick={() => setCurrentPage('home')} className="px-4 py-2 rounded-full bg-purple-600 text-white hover:bg-purple-700 transition">🏠 خانه</button>
                                    <button onClick={toggleTheme} className="px-4 py-2 rounded-full bg-purple-600 text-white hover:bg-purple-700 transition">{theme === 'dark' ? '☀️' : '🌙'}</button>
                                </div>
                            </div>
                            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 min-h-[550px]">
                                <PageComponent />
                            </div>
                        </div>
                    </div>
                </AppContext.Provider>
            );
        };
        
        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
'''
# react_app.py - نسخه کاملاً بدون خطا

REACT_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - مسیرینو</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/react@18.2.0/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18.2.0/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
        * { font-family: 'Vazirmatn', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
        body { direction: rtl; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; }
        .dark { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
        .light { background: linear-gradient(135deg, #f5f7fa, #e4e8f0); }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(255,255,255,0.1); border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: #6c63ff; border-radius: 10px; }
        .animate-spin-slow { animation: spin 3s linear infinite; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel" data-presets="react">
        const { useState, useEffect, createContext, useContext } = React;
        
        // ========== Session ID ==========
        const sessionId = "{session_id}";
        
        // ========== API Helper ==========
        const apiCall = async (url, options = {}) => {
            try {
                const res = await fetch(url, options);
                return await res.json();
            } catch(e) {
                console.error('API Error:', e);
                return { error: e.message };
            }
        };
        
        // ========== صفحه مسیرشو ==========
        function PathFinderPage() {
            const [roadmaps, setRoadmaps] = useState([]);
            const [loading, setLoading] = useState(true);
            
            useEffect(() => {
                fetch('/api/path-finder?session_id=' + sessionId)
                    .then(function(res) { return res.json(); })
                    .then(function(data) {
                        setRoadmaps(data.recommended_roadmaps || []);
                        setLoading(false);
                    })
                    .catch(function() {
                        setLoading(false);
                    });
            }, []);
            
            if (loading) {
                return <div className="text-center py-8">⏳ در حال بارگذاری مسیرها...</div>;
            }
            
            if (roadmaps.length === 0) {
                return (
                    <div>
                        <h3 className="text-xl font-bold mb-4">🗺️ مسیرشو - نقشه راه شغلی</h3>
                        <p className="text-center text-white/60">ابتدا آزمون هالند را انجام دهید</p>
                    </div>
                );
            }
            
            return (
                <div>
                    <h3 className="text-xl font-bold mb-4">🗺️ مسیرشو - نقشه راه شغلی</h3>
                    {roadmaps.map(function(rm, i) {
                        var steps = rm.steps || [];
                        return (
                            <div key={i} className="bg-white/10 rounded-xl p-4 mb-3">
                                <div className="font-bold text-lg">{rm.title}</div>
                                <div className="text-sm text-white/60">📅 {rm.duration_years || "?"} سال | 💰 {rm.income_range || "نامشخص"}</div>
                                <div className="mt-2 flex flex-wrap gap-2">
                                    {steps.slice(0, 3).map(function(step, j) {
                                        return <span key={j} className="text-xs bg-purple-600/30 px-2 py-1 rounded-full">{step.title}</span>;
                                    })}
                                </div>
                            </div>
                        );
                    })}
                </div>
            );
        }
        
        // ========== صفحه پیش‌بینی ML ==========
        function MLPredictorPage() {
            const [features, setFeatures] = useState({
                study_hours: 5, study_days: 5, prev_grade: 15, sleep_hours: 7,
                stress_level: 3, test_anxiety: 3, consistency: 3, review_count: 3,
                tutor: 0, attendance: 4
            });
            const [result, setResult] = useState(null);
            const [loading, setLoading] = useState(false);
            
            const updateFeature = function(key, value) {
                var newFeatures = {};
                for (var k in features) {
                    newFeatures[k] = features[k];
                }
                newFeatures[key] = parseFloat(value);
                setFeatures(newFeatures);
            };
            
            const predict = function() {
                setLoading(true);
                fetch('/api/ml-predict-pure', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, features: features })
                })
                .then(function(res) { return res.json(); })
                .then(function(data) {
                    setResult(data);
                    setLoading(false);
                })
                .catch(function() {
                    setLoading(false);
                });
            };
            
            return (
                <div>
                    <h3 className="text-xl font-bold mb-4">🤖 پیش‌بینی نمره با هوش مصنوعی</h3>
                    <div className="grid grid-cols-2 gap-3 mb-4">
                        {Object.keys(features).map(function(key) {
                            var labelText = key.replace(/_/g, ' ');
                            return (
                                <div key={key}>
                                    <label className="text-xs text-white/60 block">{labelText}</label>
                                    <input 
                                        type="number" 
                                        value={features[key]} 
                                        onChange={function(e) { 
                                            var newFeatures = {};
                                            for (var k in features) newFeatures[k] = features[k];
                                            newFeatures[key] = parseFloat(e.target.value);
                                            setFeatures(newFeatures);
                                        }} 
                                        className="w-full p-2 rounded-lg bg-white/20 text-white" 
                                        step="0.5" 
                                    />
                                </div>
                            );
                        })}
                    </div>
                    <button 
                        onClick={predict} 
                        disabled={loading} 
                        className="w-full py-2 rounded-full bg-purple-600 text-white disabled:opacity-50"
                    >
                        {loading ? "⏳ در حال پیش‌بینی..." : "🔮 پیش‌بینی نمره"}
                    </button>
                    {result && result.status === 'success' && (
                        <div className="mt-4 p-4 bg-green-500/20 rounded-xl text-center">
                            <div className="text-3xl font-bold text-yellow-400">{result.predicted_grade}</div>
                            <div className="text-sm">نمره پیش‌بینی شده (از 20)</div>
                            <div className="text-xs text-white/60 mt-2">اطمینان: {result.confidence}%</div>
                        </div>
                    )}
                </div>
            );
        }
        
        // ========== صفحه اصلی (داشبورد) ==========
        function HomePage() {
            const { setCurrentPage } = useApp();
            
            const features = [
                { icon: "💬", title: "چت هوشمند", desc: "مشاوره تحصیلی با هوش مصنوعی", path: "chat", color: "from-purple-500 to-pink-500" },
                { icon: "🎯", title: "انتخاب رشته", desc: "تحلیل علمی 5 معیاره", path: "track", color: "from-blue-500 to-cyan-500" },
                { icon: "📉", title: "پیش‌بینی افت", desc: "بررسی 12 فاکتور خطر", path: "risk", color: "from-red-500 to-orange-500" },
                { icon: "🧠", title: "آزمون هالند", desc: "شناسایی تیپ شخصیت", path: "holland", color: "from-green-500 to-teal-500" },
                { icon: "🍅", title: "پومودورو", desc: "مدیریت زمان مطالعه", path: "pomodoro", color: "from-yellow-500 to-orange-500" },
                { icon: "🎯", title: "اهداف SMART", desc: "هدف‌گذاری هوشمند", path: "goals", color: "from-indigo-500 to-purple-500" },
                { icon: "📝", title: "تولید سوال", desc: "سوالات تستی و تشریحی", path: "exam", color: "from-pink-500 to-rose-500" },
                { icon: "🎯", title: "چالش روزانه", desc: "امتیاز و گواهی", path: "challenges", color: "from-amber-500 to-yellow-500" },
                { icon: "📅", title: "تقویم آموزشی", desc: "برنامه و رویدادها", path: "calendar", color: "from-emerald-500 to-green-500" },
                { icon: "👥", title: "گروه‌های مطالعه", desc: "یادگیری گروهی", path: "groups", color: "from-violet-500 to-purple-500" },
                { icon: "🗺️", title: "مسیرشو", desc: "نقشه راه شغلی 5 ساله", path: "pathfinder", color: "from-cyan-500 to-blue-500" },
                { icon: "🤖", title: "پیش‌بینی AI", desc: "نمره نهایی با هوش مصنوعی", path: "mlpredictor", color: "from-gray-500 to-gray-700" }
            ];
            
            return (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                    {features.map(function(f, i) {
                        return (
                            <div 
                                key={i}
                                onClick={function() { setCurrentPage(f.path); }}
                                className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 cursor-pointer transition-all duration-300 hover:scale-105 hover:bg-white/20 border border-white/10"
                            >
                                <div className={"text-5xl mb-4 bg-gradient-to-r " + f.color + " bg-clip-text text-transparent"}>
                                    {f.icon}
                                </div>
                                <h3 className="text-xl font-bold mb-2">{f.title}</h3>
                                <p className="text-white/60 text-sm">{f.desc}</p>
                            </div>
                        );
                    })}
                </div>
            );
        }
        
        // ========== صفحه چت بات ==========
        function ChatPage() {
            const [messages, setMessages] = useState([
                { text: 'سلام! 🌟 من مسیرینو هستم، مشاور تحصیلی هوشمند. چطور می‌تونم بهت کمک کنم؟', type: 'bot' }
            ]);
            const [input, setInput] = useState('');
            const [loading, setLoading] = useState(false);
            const messagesEndRef = React.useRef(null);
            
            const scrollToBottom = function() {
                if (messagesEndRef.current) {
                    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
                }
            };
            
            useEffect(function() {
                scrollToBottom();
            }, [messages]);
            
            const sendMessage = async function() {
                if (!input.trim()) return;
                var userMsg = input.trim();
                setMessages(function(prev) { return [...prev, { text: userMsg, type: 'user' }]; });
                setInput('');
                setLoading(true);
                
                var data = await apiCall('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userMsg, session_id: sessionId })
                });
                
                setMessages(function(prev) { return [...prev, { text: data.response || 'متاسفانه خطایی رخ داد', type: 'bot' }]; });
                setLoading(false);
            };
            
            return (
                <div className="flex flex-col h-[550px]">
                    <div className="flex-1 overflow-y-auto space-y-3 mb-4 p-2">
                        {messages.map(function(msg, idx) {
                            return (
                                <div key={idx} className={"flex " + (msg.type === 'user' ? 'justify-end' : 'justify-start')}>
                                    <div className={"max-w-[80%] p-3 rounded-2xl " + (msg.type === 'user' ? 'bg-gradient-to-r from-purple-600 to-pink-500 text-white' : 'bg-white/20 text-white')}>
                                        {msg.text}
                                    </div>
                                </div>
                            );
                        })}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-white/20 p-3 rounded-2xl">
                                    <div className="flex gap-1">
                                        <span className="w-2 h-2 bg-white rounded-full animate-bounce"></span>
                                        <span className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></span>
                                        <span className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={function(e) { setInput(e.target.value); }}
                            onKeyPress={function(e) { if (e.key === 'Enter') sendMessage(); }}
                            placeholder="سوال خود را بپرسید..."
                            className="flex-1 p-3 rounded-full bg-white/20 text-white placeholder-white/50 outline-none focus:ring-2 focus:ring-purple-500"
                        />
                        <button
                            onClick={sendMessage}
                            className="px-6 py-3 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 text-white hover:opacity-90 transition"
                        >
                            ارسال
                        </button>
                    </div>
                </div>
            );
        }
        
        // ========== صفحه پومودورو ==========
        function PomodoroPage() {
            const [timeLeft, setTimeLeft] = useState(25 * 60);
            const [isRunning, setIsRunning] = useState(false);
            const [isWorkMode, setIsWorkMode] = useState(true);
            const [pomodoroCount, setPomodoroCount] = useState(0);
            
            useEffect(function() {
                var interval;
                if (isRunning && timeLeft > 0) {
                    interval = setInterval(function() {
                        setTimeLeft(function(prev) { return prev - 1; });
                    }, 1000);
                } else if (timeLeft === 0) {
                    if (isWorkMode) {
                        setPomodoroCount(function(prev) { return prev + 1; });
                        setIsWorkMode(false);
                        setTimeLeft(5 * 60);
                    } else {
                        setIsWorkMode(true);
                        setTimeLeft(25 * 60);
                    }
                    setIsRunning(false);
                    alert(isWorkMode ? '🎉 پومودورو کامل شد! وقت استراحت' : '⏰ استراحت تمام شد! وقت مطالعه');
                }
                return function() { if (interval) clearInterval(interval); };
            }, [isRunning, timeLeft, isWorkMode]);
            
            var formatTime = function(seconds) {
                var mins = Math.floor(seconds / 60);
                var secs = seconds % 60;
                return (mins < 10 ? '0' + mins : mins) + ':' + (secs < 10 ? '0' + secs : secs);
            };
            
            return (
                <div className="text-center py-8">
                    <div className={"text-8xl font-mono mb-6 " + (isWorkMode ? 'text-green-400' : 'text-orange-400')}>
                        {formatTime(timeLeft)}
                    </div>
                    <div className="text-xl mb-6">{isWorkMode ? '📚 زمان مطالعه' : '☕ زمان استراحت'}</div>
                    <div className="flex gap-4 justify-center mb-8">
                        <button onClick={function() { setIsRunning(true); }} className="px-8 py-3 rounded-full bg-green-500 text-white hover:bg-green-600 transition text-lg">▶ شروع</button>
                        <button onClick={function() { setIsRunning(false); }} className="px-8 py-3 rounded-full bg-yellow-500 text-white hover:bg-yellow-600 transition text-lg">⏸ توقف</button>
                        <button onClick={function() { setIsRunning(false); setTimeLeft(25*60); setIsWorkMode(true); }} className="px-8 py-3 rounded-full bg-red-500 text-white hover:bg-red-600 transition text-lg">🔄 ریست</button>
                    </div>
                    <div className="text-white/70 text-lg">✅ پومودوروهای امروز: {pomodoroCount}</div>
                </div>
            );
        }
        
        // ========== صفحات ساده برای بقیه بخش‌ها ==========
        function TrackPage() { return <div className="text-center py-8">🎯 صفحه انتخاب رشته - در حال آماده‌سازی</div>; }
        function RiskPage() { return <div className="text-center py-8">📉 صفحه پیش‌بینی افت - در حال آماده‌سازی</div>; }
        function HollandPage() { return <div className="text-center py-8">🧠 صفحه آزمون هالند - در حال آماده‌سازی</div>; }
        function GoalsPage() { return <div className="text-center py-8">🎯 صفحه اهداف SMART - در حال آماده‌سازی</div>; }
        function ExamPage() { return <div className="text-center py-8">📝 صفحه تولید سوال - در حال آماده‌سازی</div>; }
        function CalendarPage() { return <div className="text-center py-8">📅 صفحه تقویم آموزشی - در حال آماده‌سازی</div>; }
        function ChallengesPage() { return <div className="text-center py-8">🎯 صفحه چالش‌های روزانه - در حال آماده‌سازی</div>; }
        function GroupsPage() { return <div className="text-center py-8">👥 صفحه گروه‌های مطالعه - در حال آماده‌سازی</div>; }
        
        // ========== Context ==========
        const AppContext = createContext();
        function useApp() { return useContext(AppContext); }
        
        // ========== کامپوننت اصلی ==========
        function App() {
            const [currentPage, setCurrentPage] = useState('home');
            const [theme, setTheme] = useState('dark');
            
            useEffect(function() {
                var savedTheme = localStorage.getItem('theme');
                if (savedTheme) setTheme(savedTheme);
                document.body.className = savedTheme === 'light' ? 'light' : 'dark';
            }, []);
            
            const toggleTheme = function() {
                var newTheme = theme === 'dark' ? 'light' : 'dark';
                setTheme(newTheme);
                localStorage.setItem('theme', newTheme);
                document.body.className = newTheme === 'light' ? 'light' : 'dark';
            };
            
            var pages = {
                home: HomePage, chat: ChatPage, pomodoro: PomodoroPage,
                track: TrackPage, risk: RiskPage, holland: HollandPage,
                goals: GoalsPage, exam: ExamPage, calendar: CalendarPage,
                challenges: ChallengesPage, groups: GroupsPage,
                pathfinder: PathFinderPage, mlpredictor: MLPredictorPage
            };
            
            var PageComponent = pages[currentPage] || HomePage;
            var pageTitles = {
                home: 'خانه', chat: 'چت بات', pomodoro: 'پومودورو',
                track: 'انتخاب رشته', risk: 'پیش‌بینی افت', holland: 'هالند',
                goals: 'اهداف SMART', exam: 'تولید سوال', calendar: 'تقویم',
                challenges: 'چالش‌ها', groups: 'گروه‌ها', pathfinder: 'مسیرشو', mlpredictor: 'پیش‌بینی AI'
            };
            
            return (
                <AppContext.Provider value={{ setCurrentPage: setCurrentPage }}>
                    <div className="min-h-screen p-4" dir="rtl">
                        <div className="max-w-6xl mx-auto">
                            <div className="flex justify-between items-center mb-6 p-4 bg-white/10 backdrop-blur-lg rounded-2xl">
                                <div className="flex items-center gap-2">
                                    <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-purple-400 bg-clip-text text-transparent">🎓 مسیرینو</h1>
                                    <span className="text-white/40 text-sm">| {pageTitles[currentPage]}</span>
                                </div>
                                <div className="flex gap-2">
                                    <button onClick={function() { setCurrentPage('home'); }} className="px-4 py-2 rounded-full bg-purple-600 text-white hover:bg-purple-700 transition">🏠 خانه</button>
                                    <button onClick={toggleTheme} className="px-4 py-2 rounded-full bg-purple-600 text-white hover:bg-purple-700 transition">{theme === 'dark' ? '☀️' : '🌙'}</button>
                                </div>
                            </div>
                            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 min-h-[550px]">
                                <PageComponent />
                            </div>
                        </div>
                    </div>
                </AppContext.Provider>
            );
        }
        
        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
'''