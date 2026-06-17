from html import escape
from config import THINKING_STYLES, TRACKS, SUBJECTS_BY_LEVEL, SUBJECTS_BY_TRACK
from track_risk_logic import grade_category, safe_key, color_for_percent

# اضافه کنید به ابتدای فایل html_pages.py

def render_role_select_page(session_id):
    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>انتخاب نقش - مسیرینو</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        /* ----- Font Family Fallback برای ایران بدون تحریم ----- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
        
        body, button, input, select, textarea, .role-title, .role-desc, h1, div, p, span, a {{
            font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
        }}
        
        body {{
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .role-card {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border-radius: 32px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .role-card:hover {{
            transform: translateY(-10px) scale(1.02);
            background: rgba(108,99,255,0.2);
        }}
        .role-icon {{ font-size: 5rem; margin-bottom: 20px; }}
        .role-title {{ font-size: 1.8rem; font-weight: bold; margin-bottom: 10px; letter-spacing: -0.3px; }}
        .role-desc {{ color: #c4c4f0; font-size: 0.9rem; line-height: 1.6; }}
        .container {{ max-width: 800px; margin: auto; }}
        h1 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #fff, #6c63ff);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            font-weight: 700;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>🎓 به مسیرینو خوش آمدی</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="role-card" onclick="selectRole('student')">
            <div class="role-icon">📚</div>
            <div class="role-title">دانش‌آموز / دانشجو</div>
            <div class="role-desc">مشاوره تحصیلی، برنامه ریزی، آزمون‌ها و بازی‌های آموزشی</div>
        </div>
        <div class="role-card" onclick="selectRole('counselor')">
            <div class="role-icon">👨‍🏫</div>
            <div class="role-title">مشاور تحصیلی</div>
            <div class="role-desc">مشاهده وضعیت دانش‌آموزان، آمار و گزارش‌های پیشرفت</div>
        </div>
    </div>
</div>
<script>
const sessionId = "{session_id}";
function selectRole(role) {{
    fetch('/save-role', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ session_id: sessionId, role: role }})
    }})
    .then(res => res.json())
    .then(data => {{
        if (data.status === 'ok') {{
            if (role === 'counselor') {{
                window.location.href = '/teacher-dashboard?session_id=' + sessionId;
            }} else {{
                window.location.href = '/consent-page?session_id=' + sessionId;
            }}
        }} else {{
            alert('خطا: ' + (data.message || 'مشکل در ثبت نقش'));
        }}
    }})
    .catch(err => alert('خطا در ارتباط با سرور'));
}}
</script>
</body>
</html>'''


def render_groups_page(session_id):
    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>گروه‌های مطالعه - مسیرینو</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
        body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{
            font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important;
        }}
        :root {{ --bg: linear-gradient(135deg,#0f0c29,#302b63,#24243e); --card: rgba(255,255,255,0.08); --text: #fff; --muted: #c4c4f0; }}
        [data-theme="light"] {{ --bg: linear-gradient(135deg,#f5f7fa,#e4e8f0); --card: rgba(255,255,255,0.9); --text: #1a1a2e; --muted: #666; }}
        body {{ background: var(--bg); color: var(--text); height: 100vh; overflow: hidden; }}
        .messenger-container {{ display: flex; height: 100vh; background: var(--bg); }}
        .sidebar {{ width: 320px; background: rgba(0,0,0,0.3); backdrop-filter: blur(20px); border-left: 1px solid rgba(255,255,255,0.1); display: flex; flex-direction: column; overflow-y: auto; }}
        .chat-area {{ flex: 1; display: flex; flex-direction: column; background: rgba(0,0,0,0.2); }}
        .members-panel {{ width: 280px; background: rgba(0,0,0,0.3); border-right: 1px solid rgba(255,255,255,0.1); display: flex; flex-direction: column; overflow-y: auto; }}
        .chat-header {{ padding: 20px; background: rgba(0,0,0,0.3); border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }}
        .chat-messages {{ flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }}
        .message-item {{ display: flex; max-width: 70%; animation: fadeIn 0.3s ease; }}
        .message-item.my-message {{ align-self: flex-end; }}
        .message-item.other-message {{ align-self: flex-start; }}
        .message-bubble {{ padding: 10px 15px; border-radius: 20px; background: rgba(108,99,255,0.3); word-wrap: break-word; }}
        .my-message .message-bubble {{ background: linear-gradient(135deg, #6c63ff, #ff6584); border-bottom-right-radius: 5px; }}
        .other-message .message-bubble {{ background: rgba(255,255,255,0.1); border-bottom-left-radius: 5px; }}
        .message-sender {{ font-size: 0.7rem; color: var(--muted); margin-bottom: 3px; }}
        .message-time {{ font-size: 0.65rem; color: var(--muted); margin-top: 3px; text-align: left; }}
        .chat-input-area {{ padding: 20px; background: rgba(0,0,0,0.3); border-top: 1px solid rgba(255,255,255,0.1); display: flex; gap: 12px; }}
        .chat-input {{ flex: 1; padding: 12px 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 30px; background: rgba(255,255,255,0.1); color: var(--text); outline: none; }}
        .chat-input:focus {{ border-color: #6c63ff; }}
        .send-btn {{ padding: 12px 28px; border: none; border-radius: 30px; background: linear-gradient(90deg, #6c63ff, #ff6584); color: white; font-weight: bold; cursor: pointer; }}
        .group-list-item {{ padding: 15px 20px; cursor: pointer; transition: all 0.3s; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center; gap: 12px; }}
        .group-list-item:hover {{ background: rgba(108,99,255,0.2); }}
        .group-list-item.active {{ background: rgba(108,99,255,0.3); border-right: 3px solid #6c63ff; }}
        .group-avatar {{ width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #6c63ff, #ff6584); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }}
        .group-info {{ flex: 1; }}
        .group-name {{ font-weight: bold; margin-bottom: 3px; }}
        .create-group-btn {{ margin: 15px; padding: 12px; border: none; border-radius: 30px; background: linear-gradient(90deg, #6c63ff, #ff6584); color: white; font-weight: bold; cursor: pointer; width: calc(100% - 30px); }}
        .join-group-btn {{ background: #10b981; color: white; border: none; padding: 6px 15px; border-radius: 30px; cursor: pointer; font-size: 0.8rem; }}
        .delete-group-btn {{ background: #ef4444; color: white; border: none; padding: 6px 15px; border-radius: 30px; cursor: pointer; font-size: 0.8rem; margin-right: 10px; }}
        .section-title {{ padding: 15px 20px; background: rgba(0,0,0,0.2); font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; justify-content: center; align-items: center; }}
        .modal-content {{ background: var(--card); backdrop-filter: blur(20px); border-radius: 28px; padding: 30px; max-width: 450px; width: 90%; }}
        .member-item {{ padding: 12px 20px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        .member-avatar {{ width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; }}
        .member-role {{ font-size: 0.65rem; color: #f59e0b; margin-right: auto; }}
        input, textarea, select {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 16px; color: white; outline: none; padding: 12px; width: 100%; margin-bottom: 15px; }}
        .code-display {{ background: rgba(108,99,255,0.3); padding: 10px; border-radius: 12px; text-align: center; margin: 10px 0; font-family: monospace; font-size: 1.2rem; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body>
<div class="messenger-container">
    <div class="sidebar">
        <div style="padding: 20px; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <h2 style="font-size: 1.3rem;">📱 گفتگوهای من</h2>
        </div>
        <div style="padding: 10px;">
            <button class="create-group-btn" onclick="openCreateGroupModal()">➕ ایجاد گروه جدید</button>
            <button class="create-group-btn" style="background: rgba(108,99,255,0.5); margin-top: 5px;" onclick="openJoinModal()">🔑 پیوستن با کد دعوت (خصوصی)</button>
        </div>
        <div class="section-title">📚 گروه‌های من</div>
        <div id="myGroupsList" style="flex: 0 0 auto; max-height: 40%; overflow-y: auto;"></div>
        <div class="section-title">🌍 گروه‌های عمومی</div>
        <div id="publicGroupsList" style="flex: 1; overflow-y: auto;"></div>
    </div>
    
    <div class="chat-area" id="chatArea" style="display: none;">
        <div class="chat-header">
            <div><span id="currentGroupName" style="font-size: 1.2rem; font-weight: bold;"></span><span id="currentGroupPrivacy" style="font-size: 0.8rem; color: var(--muted); margin-right: 10px;"></span></div>
            <div>
                <button onclick="copyGroupCode()" class="send-btn" style="padding: 6px 15px;">📋 کد دعوت</button>
                <button onclick="deleteCurrentGroup()" class="delete-group-btn" id="deleteGroupBtn" style="display:none;">🗑️ حذف گروه</button>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages"></div>
        <div class="chat-input-area">
            <input type="text" class="chat-input" id="messageInput" placeholder="پیام خود را بنویسید..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button class="send-btn" onclick="sendMessage()">ارسال</button>
        </div>
    </div>
    
    <div class="members-panel" id="membersPanel" style="display: none;">
        <div class="section-title">👥 اعضای گروه (<span id="memberCount">0</span>)</div>
        <div id="membersList" style="flex: 1; overflow-y: auto;"></div>
    </div>
</div>

<div id="createGroupModal" class="modal">
    <div class="modal-content">
        <h3 style="margin-bottom: 20px;">➕ ایجاد گروه جدید</h3>
        <input type="text" id="groupName" placeholder="نام گروه">
        <textarea id="groupDesc" rows="3" placeholder="توضیحات گروه"></textarea>
        <select id="groupPrivacy">
            <option value="0">🌍 عمومی - همه می‌توانند بپیوندند</option>
            <option value="1">🔒 خصوصی - فقط با کد دعوت</option>
        </select>
        <div style="display: flex; gap: 10px;">
            <button onclick="createGroup()" style="flex:1; padding:12px; border:none; border-radius:30px; background:linear-gradient(90deg,#6c63ff,#ff6584); color:white; cursor:pointer;">ایجاد</button>
            <button onclick="closeCreateModal()" style="flex:1; padding:12px; border:none; border-radius:30px; background:rgba(255,255,255,0.1); color:white; cursor:pointer;">انصراف</button>
        </div>
    </div>
</div>

<div id="joinModal" class="modal">
    <div class="modal-content">
        <h3 style="margin-bottom: 20px;">🔑 پیوستن به گروه خصوصی</h3>
        <input type="text" id="joinCode" placeholder="کد دعوت گروه را وارد کنید">
        <div style="display: flex; gap: 10px;">
            <button onclick="submitJoinCode()" style="flex:1; padding:12px; border:none; border-radius:30px; background:linear-gradient(90deg,#6c63ff,#ff6584); color:white; cursor:pointer;">پیوستن</button>
            <button onclick="closeJoinModal()" style="flex:1; padding:12px; border:none; border-radius:30px; background:rgba(255,255,255,0.1); color:white; cursor:pointer;">انصراف</button>
        </div>
    </div>
</div>

<div id="codeModal" class="modal">
    <div class="modal-content">
        <h3>🔑 کد دعوت گروه</h3>
        <div class="code-display" id="groupCodeDisplay"></div>
        <button onclick="copyCodeToClipboard()" class="send-btn" style="width:100%">📋 کپی کد</button>
        <button onclick="closeCodeModal()" style="width:100%; margin-top:10px; padding:10px; background:rgba(255,255,255,0.1); border:none; border-radius:30px; color:white; cursor:pointer;">بستن</button>
    </div>
</div>

<script>
const sessionId = "{session_id}";
let currentGroupId = null;
let currentGroupCode = null;
let currentUserRole = null;

function openCreateGroupModal() {{
    document.getElementById('createGroupModal').style.display = 'flex';
}}

function closeCreateModal() {{
    document.getElementById('createGroupModal').style.display = 'none';
    document.getElementById('groupName').value = '';
    document.getElementById('groupDesc').value = '';
}}

function openJoinModal() {{
    document.getElementById('joinModal').style.display = 'flex';
}}

function closeJoinModal() {{
    document.getElementById('joinModal').style.display = 'none';
    document.getElementById('joinCode').value = '';
}}

function openCodeModal(code) {{
    document.getElementById('groupCodeDisplay').innerText = code;
    document.getElementById('codeModal').style.display = 'flex';
}}

function closeCodeModal() {{
    document.getElementById('codeModal').style.display = 'none';
}}

function copyCodeToClipboard() {{
    const code = document.getElementById('groupCodeDisplay').innerText;
    navigator.clipboard.writeText(code);
    alert('✅ کد دعوت کپی شد: ' + code);
}}

function escapeHtml(text) {{
    if (!text) return '';
    return text.replace(/[&<>]/g, function(m) {{
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    }});
}}

async function loadGroups() {{
    const myRes = await fetch('/api/groups/my?session_id=' + sessionId);
    const myData = await myRes.json();
    const myGroups = myData.groups || [];
    
    let myHtml = '';
    for (let g of myGroups) {{
        const activeClass = (currentGroupId === g.id) ? 'active' : '';
        const privacyIcon = g.is_private ? '🔒' : '🌍';
        myHtml += '<div class="group-list-item ' + activeClass + '" onclick="selectGroup(' + g.id + ')">' +
            '<div class="group-avatar">' + privacyIcon + '</div>' +
            '<div class="group-info"><div class="group-name">' + escapeHtml(g.name) + '</div>' +
            '<div style="font-size:0.7rem;color:var(--muted)">' + (g.role === 'owner' ? '👑 مدیر' : '👤 عضو') + '</div></div>' +
        '</div>';
    }}
    document.getElementById('myGroupsList').innerHTML = myHtml || '<div style="padding:20px;text-align:center">📭 گروهی نیست</div>';
    
    const publicRes = await fetch('/api/groups/public?session_id=' + sessionId);
    const publicData = await publicRes.json();
    const myIds = myGroups.map(g => g.id);
    const available = (publicData.groups || []).filter(g => !myIds.includes(g.id));
    
    let publicHtml = '';
    for (let g of available) {{
        publicHtml += '<div class="group-list-item" style="justify-content:space-between">' +
            '<div><div class="group-name">' + escapeHtml(g.name) + '</div>' +
            '<div style="font-size:0.7rem;color:var(--muted)">👤 ' + (g.member_count || 1) + ' عضو</div></div>' +
            '<button class="join-group-btn" onclick="event.stopPropagation(); joinPublicGroup(' + g.id + ')">✨ پیوستن</button>' +
        '</div>';
    }}
    document.getElementById('publicGroupsList').innerHTML = publicHtml || '<div style="padding:20px;text-align:center">🌍 گروه عمومی دیگری نیست</div>';
}}

async function selectGroup(groupId) {{
    currentGroupId = groupId;
    const res = await fetch('/api/groups/detail?session_id=' + sessionId + '&group_id=' + groupId);
    const data = await res.json();
    
    document.getElementById('chatArea').style.display = 'flex';
    document.getElementById('membersPanel').style.display = 'flex';
    document.getElementById('currentGroupName').innerHTML = escapeHtml(data.group.name);
    
    const privacyText = data.group.is_private ? '🔒 خصوصی' : '🌍 عمومی';
    document.getElementById('currentGroupPrivacy').innerHTML = privacyText;
    currentGroupCode = data.group.group_code;
    currentUserRole = data.user_role;
    
    const deleteBtn = document.getElementById('deleteGroupBtn');
    if (currentUserRole === 'owner') {{
        deleteBtn.style.display = 'inline-block';
    }} else {{
        deleteBtn.style.display = 'none';
    }}
    
    document.getElementById('memberCount').innerText = (data.members || []).length;
    
    let membersHtml = '';
    for (let m of (data.members || [])) {{
        const isOwner = (m.role === 'owner');
        membersHtml += '<div class="member-item">' +
            '<div class="member-avatar">' + (isOwner ? '👑' : '👤') + '</div>' +
            '<div class="member-name">' + escapeHtml(m.name || m.user_id.slice(0,8)) + '</div>' +
            '<div class="member-role">' + (isOwner ? 'مدیر' : 'عضو') + '</div>' +
            '<div>⭐ ' + (m.points || 0) + '</div>' +
        '</div>';
    }}
    document.getElementById('membersList').innerHTML = membersHtml || '<div style="padding:20px;text-align:center">هیچ عضوی نیست</div>';
    
    let messagesHtml = '';
    for (let msg of (data.messages || [])) {{
        const isMe = (msg.user_id === sessionId);
        const timeStr = msg.sent_at ? new Date(msg.sent_at).toLocaleTimeString('fa-IR') : '';
        messagesHtml += '<div class="message-item ' + (isMe ? 'my-message' : 'other-message') + '">' +
            '<div><div class="message-sender">' + escapeHtml(msg.user_name || msg.user_id.slice(0,6)) + '</div>' +
            '<div class="message-bubble">' + escapeHtml(msg.message) + '</div>' +
            '<div class="message-time">' + timeStr + '</div></div>' +
        '</div>';
    }}
    document.getElementById('chatMessages').innerHTML = messagesHtml || '<div style="text-align:center;padding:40px">💬 پیامی نیست</div>';
    
    loadGroups();
}}

async function sendMessage() {{
    const input = document.getElementById('messageInput');
    const msg = input.value.trim();
    if (!msg || !currentGroupId) return;
    await fetch('/api/groups/send-message', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{session_id: sessionId, group_id: currentGroupId, message: msg}})
    }});
    input.value = '';
    selectGroup(currentGroupId);
}}

async function createGroup() {{
    const name = document.getElementById('groupName').value.trim();
    const desc = document.getElementById('groupDesc').value;
    const isPrivate = parseInt(document.getElementById('groupPrivacy').value);
    if (!name) {{ alert('نام گروه را وارد کنید'); return; }}
    
    const res = await fetch('/api/groups/create', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{session_id: sessionId, name: name, description: desc, is_private: isPrivate}})
    }});
    const data = await res.json();
    if (data.status === 'ok') {{
        if (isPrivate === 1 && data.group_code) {{
            alert('✅ گروه خصوصی ساخته شد! کد دعوت: ' + data.group_code);
            openCodeModal(data.group_code);
        }} else {{
            alert('✅ گروه عمومی ساخته شد!');
        }}
        closeCreateModal();
        loadGroups();
    }} else {{
        alert('❌ خطا: ' + (data.message || 'مشخص نیست'));
    }}
}}

async function joinPublicGroup(groupId) {{
    const res = await fetch('/api/groups/join', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{session_id: sessionId, group_id: groupId}})
    }});
    const data = await res.json();
    if (data.status === 'ok') {{
        alert('✅ به گروه پیوستید');
        loadGroups();
    }} else {{
        alert('❌ خطا: ' + (data.message || 'مشخص نیست'));
    }}
}}

async function submitJoinCode() {{
    const code = document.getElementById('joinCode').value.trim();
    if (!code) {{ alert('کد دعوت را وارد کنید'); return; }}
    const res = await fetch('/api/groups/join-by-code', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{session_id: sessionId, group_code: code}})
    }});
    const data = await res.json();
    if (data.status === 'ok') {{
        alert('✅ به گروه خصوصی پیوستید');
        closeJoinModal();
        loadGroups();
        if (data.group_id) selectGroup(data.group_id);
    }} else {{
        alert('❌ کد نامعتبر است');
    }}
}}

async function deleteCurrentGroup() {{
    if (!currentGroupId) return;
    if (!confirm('⚠️ آیا مطمئنی میخوای این گروه رو حذف کنی؟ این کار غیرقابل بازگشت است!')) return;
    
    const res = await fetch('/api/groups/delete', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{session_id: sessionId, group_id: currentGroupId}})
    }});
    const data = await res.json();
    if (data.status === 'ok') {{
        alert('✅ گروه حذف شد');
        currentGroupId = null;
        document.getElementById('chatArea').style.display = 'none';
        document.getElementById('membersPanel').style.display = 'none';
        loadGroups();
    }} else {{
        alert('❌ خطا: ' + (data.message || 'امکان حذف گروه وجود ندارد'));
    }}
}}

function copyGroupCode() {{
    if (currentGroupCode) {{
        openCodeModal(currentGroupCode);
    }} else {{
        alert('این گروه کد دعوت ندارد (عمومی)');
    }}
}}

loadGroups();
</script>
</body>
</html>'''


def render_consent_page(session_id):
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title> رضایت نامه - مسیرینو</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, div, p, h2 {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  body{{background:linear-gradient(135deg,#0f0c29,#302b63);color:white;display:flex;justify-content:center;align-items:center;min-height:100vh}}
  .box{{background:rgba(255,255,255,0.1);border-radius:30px;padding:40px;max-width:500px;text-align:center}}
  button{{padding:12px 30px;margin:10px;border:none;border-radius:30px;cursor:pointer;font-weight:bold}}
  .accept{{background:#10b981;color:white}}
  .decline{{background:#ef4444;color:white}}
  .loading{{display:none;margin-top:15px;color:#ffd700}}
</style>
</head>
<body>
<div class="box">
  <h2>🔒 رضایت‌نامه حریم خصوصی</h2>
  <p>اطلاعات شما فقط برای تحلیل آموزشی استفاده می‌شود و با کد یکتا (نه نام) ذخیره می‌گردد.</p>
  <p>✅ داده‌های شما پس از ۶ ماه حذف می‌شوند</p>
  <p>✅ شما می‌توانید درخواست حذف اطلاعات دهید</p>
  <div>
    <button class="accept" onclick="handleConsent(1)">✅ موافقم</button>
    <button class="decline" onclick="handleConsent(0)">❌ مخالفم</button>
  </div>
  <div class="loading" id="loading">در حال انتقال به صفحه اصلی...</div>
</div>
<script>
    const sessionId = "{session_id}";
    
    function handleConsent(consent) {{
        const loadingDiv = document.getElementById('loading');
        loadingDiv.style.display = 'block';
        
        fetch('/consent', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{
                session_id: sessionId,
                consent: consent
            }})
        }})
        .then(response => response.json())
        .then(data => {{
            if (data.status === 'ok') {{
                window.location.href = '/?session_id=' + sessionId;
            }} else if (data.status === 'declined') {{
                window.location.href = 'https://www.google.com';
            }} else {{
                alert('خطا در ثبت رضایت. دوباره تلاش کنید.');
                loadingDiv.style.display = 'none';
            }}
        }})
        .catch(error => {{
            console.error('Error:', error);
            alert('خطا در ارتباط با سرور. مطمئن شو سرور در حال اجراست.');
            loadingDiv.style.display = 'none';
        }});
    }}
</script>
</body></html>"""

def render_homepage(session_id):
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>مسیرینو | مشاور هوشمند تحصیلی</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* ----- فونت‌های امن و زیبا برای ایران (بدون تحریم) ----- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
        
        /* اعمال فونت روی همه المان‌ها با اولویت فونت‌های ایرانی */
        * {{
            font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
        }}
        
        /* اطمینان از اعمال فونت روی بدنه و همه اجزا */
        body, html, div, span, p, h1, h2, h3, h4, h5, h6, a, button, input, select, textarea, label, li, ul, ol, table, td, th, tr, thead, tbody, tfoot, article, section, aside, footer, header, nav, main, .glass-morphism, .card-hover, .glass-card, .track-card, .stat-card, .message, .btn, .track-name, .track-score, .role-title, .role-desc {{
            font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
        }}
        
        /* تنظیمات Tailwind برای فونت */
        .font-sans {{
            font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', system-ui, sans-serif !important;
        }}
        
        .glass-morphism {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .glass-morphism-light {{
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        .gradient-border {{
            position: relative;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            border-radius: 1.5rem;
        }}
        .gradient-border::before {{
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #6c63ff, #ff6584, #6c63ff);
            border-radius: 1.6rem;
            z-index: -1;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        .gradient-border:hover::before {{
            opacity: 1;
        }}
        .card-hover {{
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .card-hover:hover {{
            transform: translateY(-8px) scale(1.02);
        }}
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #6c63ff, #ff6584);
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, #ff6584, #6c63ff);
        }}
        .bg-grid-pattern {{
            background-image: 
                linear-gradient(rgba(108,99,255,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(108,99,255,0.05) 1px, transparent 1px);
            background-size: 50px 50px;
        }}
        
        /* انیمیشن‌ها */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-15px); }}
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        @keyframes glow {{
            0%, 100% {{ box-shadow: 0 0 5px rgba(108,99,255,0.3); }}
            50% {{ box-shadow: 0 0 20px rgba(108,99,255,0.6); }}
        }}
        @keyframes slideInLeft {{
            from {{ transform: translateX(-50px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        @keyframes slideInRight {{
            from {{ transform: translateX(50px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        .animate-fade-in-up {{
            animation: fadeInUp 0.6s ease-out forwards;
        }}
        .animate-fade-in {{
            animation: fadeIn 0.5s ease-out forwards;
        }}
        .animate-float {{
            animation: float 4s ease-in-out infinite;
        }}
        .animate-pulse-slow {{
            animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }}
        .animate-glow {{
            animation: glow 2s ease-in-out infinite;
        }}
        .animate-slide-in-left {{
            animation: slideInLeft 0.5s ease-out forwards;
        }}
        .animate-slide-in-right {{
            animation: slideInRight 0.5s ease-out forwards;
        }}
    </style>
</head>
<body class="bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] min-h-screen">
    <div class="relative min-h-screen overflow-hidden">
        <!-- پس‌زمینه متحرک -->
        <div class="absolute inset-0 bg-grid-pattern opacity-30"></div>
        <div class="absolute top-20 left-10 w-72 h-72 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
        <div class="absolute bottom-20 right-10 w-96 h-96 bg-pink-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style="animation-delay: 2s;"></div>
        <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-blue-600 rounded-full mix-blend-multiply filter blur-3xl opacity-10"></div>
        
        <!-- دکمه تم و دفترچه راهنما -->
        <div class="fixed top-6 left-6 z-50 flex gap-3">
            <button onclick="toggleTheme()" class="w-12 h-12 rounded-full glass-morphism text-white text-xl hover:scale-110 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/30">
                <span id="themeIcon">🌙</span>
            </button>
            <a href="/manual?session_id={session_id}" class="w-12 h-12 rounded-full glass-morphism text-white text-xl hover:scale-110 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/30 flex items-center justify-center">
                📘
            </a>
        </div>
        
        <!-- دکمه مدیریت -->
        <a href="/admin" class="fixed bottom-6 right-6 z-50 px-5 py-3 rounded-full glass-morphism text-white text-sm hover:scale-105 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/30 flex items-center gap-2">
            📊 داشبورد مدیریت
        </a>
        
        <!-- وضعیت اتصال آفلاین/آنلاین -->
        <div id="onlineStatus" class="fixed bottom-20 right-6 z-50 px-3 py-1 rounded-full text-xs backdrop-blur-lg" style="background: rgba(0,0,0,0.5);">
            🟢 آنلاین
        </div>
        
        <div class="relative container mx-auto px-4 py-12 max-w-7xl z-10">
            <!-- هدر -->
            <div class="text-center mb-16 animate-fade-in-up">
                <div class="inline-block mb-4">
                    <div class="text-8xl animate-float">🎓</div>
                </div>
                <h1 class="text-5xl md:text-7xl font-bold bg-gradient-to-r from-white via-purple-400 to-pink-500 bg-clip-text text-transparent mb-4">
                    مسیرینو
                </h1>
                <p class="text-gray-300 text-lg max-w-2xl mx-auto">
                    مشاور هوشمند تحصیلی | انتخاب رشته | پیش‌بینی افت | مسیرشو
                </p>
                <div class="flex justify-center gap-2 mt-4">
                    <span class="px-3 py-1 text-xs rounded-full bg-white/10 text-white/60">🎯 AI-Powered</span>
                    <span class="px-3 py-1 text-xs rounded-full bg-white/10 text-white/60">🧠 45 Test Holland</span>
                    <span class="px-3 py-1 text-xs rounded-full bg-white/10 text-white/60">📊 Real-time Analysis</span>
                    <span class="px-3 py-1 text-xs rounded-full bg-green-500/30 text-green-300">⚡ Offline Ready</span>
                </div>
            </div>
            
            <!-- گرید سرویس‌ها -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {render_modern_cards(session_id)}
            </div>
            
            <!-- فوتر -->
            <footer class="mt-20 pt-8 border-t border-white/10 text-center text-white/40 text-sm">
                <p>© 1405 مسیرینو - همه حقوق محفوظ است</p>
                <p class="mt-2">🎓 همراه شما در مسیر موفقیت تحصیلی</p>
            </footer>
        </div>
    </div>
    
    <script>
        function toggleTheme() {{
            const html = document.documentElement;
            const themeIcon = document.getElementById('themeIcon');
            if (html.classList.contains('dark')) {{
                html.classList.remove('dark');
                localStorage.setItem('theme', 'light');
                themeIcon.innerHTML = '☀️';
                document.body.className = 'bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200';
            }} else {{
                html.classList.add('dark');
                localStorage.setItem('theme', 'dark');
                themeIcon.innerHTML = '🌙';
                document.body.className = 'bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e]';
            }}
        }}
        
        // بارگذاری تم ذخیره شده
        if (localStorage.getItem('theme') === 'light') {{
            document.documentElement.classList.remove('dark');
            const themeIcon = document.getElementById('themeIcon');
            if (themeIcon) themeIcon.innerHTML = '☀️';
            document.body.className = 'bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200';
        }} else {{
            document.documentElement.classList.add('dark');
            const themeIcon = document.getElementById('themeIcon');
            if (themeIcon) themeIcon.innerHTML = '🌙';
        }}
        
        // اطمینان از اعمال فونت روی همه المان‌های داینامیک
        const observer = new MutationObserver(function(mutations) {{
            mutations.forEach(function(mutation) {{
                if (mutation.addedNodes.length) {{
                    mutation.addedNodes.forEach(function(node) {{
                        if (node.nodeType === 1 && node.style) {{
                            node.style.fontFamily = "'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', sans-serif";
                        }}
                    }});
                }}
            }});
        }});
        observer.observe(document.body, {{ childList: true, subtree: true }});
        
        // ========== ثبت Service Worker برای حالت آفلاین ==========
        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/static/sw.js')
                .then(function(registration) {{
                    console.log('✅ Service Worker registered successfully:', registration.scope);
                }})
                .catch(function(error) {{
                    console.log('❌ Service Worker registration failed:', error);
                }});
        }}
        
        // ========== نمایش وضعیت اتصال ==========
        function updateOnlineStatus() {{
            const statusDiv = document.getElementById('onlineStatus');
            if (statusDiv) {{
                if (navigator.onLine) {{
                    statusDiv.innerHTML = '🟢 آنلاین';
                    statusDiv.style.background = 'rgba(16, 185, 129, 0.2)';
                }} else {{
                    statusDiv.innerHTML = '🔴 آفلاین (حالت آفلاین فعال است)';
                    statusDiv.style.background = 'rgba(239, 68, 68, 0.2)';
                }}
            }}
        }}
        
        window.addEventListener('load', function() {{
            updateOnlineStatus();
            window.addEventListener('online', updateOnlineStatus);
            window.addEventListener('offline', updateOnlineStatus);
        }});
    </script>
</body>
</html>"""


def render_modern_cards(session_id, user_role="student"):
    """تابع کمکی برای رندر کارت‌های مدرن با توجه به نقش کاربر"""
    
    if user_role == "counselor":
        cards = [
            {"icon": "📊", "title": "داشبورد معلم", "desc": "نمودارهای لحظه‌ای و آمار دانش‌آموزان", "link": "/teacher-dashboard", "color": "from-blue-500 to-indigo-500", "badge": ""},
            {"icon": "👥", "title": "مدیریت دانش‌آموزان", "desc": "مشاهده لیست و گزارش دانش‌آموزان", "link": "/teacher-dashboard", "color": "from-purple-500 to-pink-500", "badge": ""},
            {"icon": "📈", "title": "آمار پیشرفت", "desc": "تحلیل عملکرد دانش‌آموزان", "link": "/teacher-dashboard", "color": "from-green-500 to-teal-500", "badge": ""},
            {"icon": "⚠️", "title": "هشدارهای افت", "desc": "دانش‌آموزان در معرض خطر", "link": "/teacher-dashboard", "color": "from-red-500 to-orange-500", "badge": ""},
        ]
    else:
        cards = [
            {"icon": "💬", "title": "چت هوشمند", "desc": "گفتگو با مشاور AI + تشخیص صدا", "link": "/chat-only", "color": "from-purple-500 to-pink-500", "badge": ""},
            {"icon": "🎯", "title": "انتخاب رشته", "desc": "تحلیل علمی 5 معیاره", "link": "/track-start", "color": "from-blue-500 to-cyan-500", "badge": ""},
            {"icon": "📉", "title": "پیش‌بینی افت", "desc": "بررسی 12 فاکتور خطر", "link": "/risk-start", "color": "from-red-500 to-orange-500", "badge": ""},
            {"icon": "🧠", "title": "آزمون هالند", "desc": "شناسایی تیپ شخصیت", "link": "/holland-test", "color": "from-green-500 to-teal-500", "badge": "recommended"},
            {"icon": "🍅", "title": "پومودورو", "desc": "مدیریت زمان مطالعه", "link": "/pomodoro", "color": "from-yellow-500 to-orange-500", "badge": ""},
            {"icon": "🎯", "title": "اهداف SMART", "desc": "هدف‌گذاری هوشمند", "link": "/smart-goals", "color": "from-indigo-500 to-purple-500", "badge": ""},
            {"icon": "📝", "title": "تولید سوال", "desc": "سوالات تستی و تشریحی", "link": "/exam-questions", "color": "from-pink-500 to-rose-500", "badge": ""},
            {"icon": "🎯", "title": "چالش روزانه", "desc": "امتیاز و گواهی", "link": "/daily-challenges", "color": "from-amber-500 to-yellow-500", "badge": ""},
            {"icon": "📅", "title": "تقویم آموزشی", "desc": "برنامه و رویدادها", "link": "/educational-calendar", "color": "from-emerald-500 to-green-500", "badge": ""},
            {"icon": "👥", "title": "گروه‌های مطالعه", "desc": "یادگیری گروهی", "link": "/groups", "color": "from-violet-500 to-purple-500", "badge": ""},
            {"icon": "🗺️", "title": "مسیرشو", "desc": "نقشه راه 5 ساله", "link": "/path-finder", "color": "from-cyan-500 to-blue-500", "badge": "hot"},
            {"icon": "🤖", "title": "پیش‌بینی AI", "desc": "نمره نهایی با ML", "link": "/ml-predictor", "color": "from-gray-500 to-gray-700", "badge": ""},
            {"icon": "👤", "title": "پروفایل من", "desc": "ویرایش اطلاعات شخصی", "link": "/profile", "color": "from-gray-500 to-gray-700", "badge": ""},
            {"icon": "🏆", "title": "پروفایل و افتخارات", "desc": "مشاهده سطح، مدال‌ها و لیدربرد", "link": "/gamification-profile", "color": "from-amber-500 to-orange-500", "badge": "hot"},
            {"icon": "📅", "title": "برنامه‌ریز هوشمند", "desc": "برنامه مطالعه دقیق برای امتحان", "link": "/dynamic-planner", "color": "from-cyan-500 to-blue-500", "badge": "new"},
            {"icon": "✨", "title": "خلاصه‌ساز هوشمند", "desc": "خلاصه + نکات کلیدی + فلش‌کارت", "link": "/smart-summarizer", "color": "from-purple-500 to-pink-500", "badge": "new"},
            {"icon": "🎮", "title": "بازی‌های آموزشی", "desc": "فلش‌کارت، مسابقه و بازی حافظه", "link": "/educational-games", "color": "from-green-500 to-emerald-500", "badge": "new"},
            {"icon": "📊", "title": "داشبورد تحلیلی", "desc": "نمودارهای پیشرفته و پیش‌بینی آینده", "link": "/analytics", "color": "from-cyan-500 to-blue-500", "badge": "new"},
            {"icon": "🏫", "title": "اتصال به مدرسه", "desc": "همگام‌سازی خودکار با سامانه سناد", "link": "/school-integration", "color": "from-blue-500 to-indigo-500", "badge": "new"},
        ]
    
    html = ""
    for i, card in enumerate(cards):
        delay = i * 0.05
        badge_html = ""
        if card["badge"] == "new":
            badge_html = '<span class="absolute top-3 right-3 px-2 py-0.5 text-[10px] font-bold rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white animate-pulse" style="font-family:inherit">جدید</span>'
        elif card["badge"] == "recommended":
            badge_html = '<span class="absolute top-3 right-3 px-2 py-0.5 text-[10px] font-bold rounded-full bg-green-500 text-white" style="font-family:inherit">پیشنهادی</span>'
        elif card["badge"] == "hot":
            badge_html = '<span class="absolute top-3 right-3 px-2 py-0.5 text-[10px] font-bold rounded-full bg-orange-500 text-white animate-pulse" style="font-family:inherit">🔥 داغ</span>'
        
        html += f'''
        <a href="{card["link"]}?session_id={session_id}" class="group block animate-fade-in-up" style="animation-delay: {delay}s; text-decoration: none;">
            <div class="relative overflow-hidden rounded-2xl glass-morphism p-6 card-hover" style="font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', sans-serif !important;">
                {badge_html}
                <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br {card["color"]} rounded-full blur-2xl opacity-0 group-hover:opacity-20 transition-opacity duration-500"></div>
                <div class="absolute -bottom-16 -left-16 w-32 h-32 bg-gradient-to-tr {card["color"]} rounded-full blur-2xl opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
                
                <div class="text-5xl mb-4 transition-all duration-300 group-hover:scale-110 group-hover:rotate-3 inline-block">
                    {card["icon"]}
                </div>
                <h3 class="text-xl font-bold text-white dark:text-white mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r {card["color"]} transition-all duration-300" style="font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', sans-serif !important; font-weight: bold;">
                    {card["title"]}
                </h3>
                <p class="text-gray-400 text-sm leading-relaxed" style="font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', sans-serif !important;">
                    {card["desc"]}
                </p>
                <div class="mt-4 flex items-center text-purple-400 text-sm opacity-0 group-hover:opacity-100 transition-all duration-300 group-hover:translate-x-1" style="font-family: inherit;">
                    <span>شروع کن</span>
                    <svg class="w-4 h-4 mr-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </div>
            </div>
        </a>
        '''
    return html


def render_chat_only_page(session_id):
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>چت بات مسیرینو</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0;--user:linear-gradient(135deg,#6c63ff,#ff6584);--bot:rgba(255,255,255,0.1)}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:#fff;--text:#1a1a2e;--muted:#666;--bot:#e8e8f0}}
  body{{background:var(--bg);min-height:100vh;display:flex;flex-direction:column;transition:all 0.3s}}
  .chat-container{{max-width:900px;width:100%;margin:20px auto;flex:1;display:flex;flex-direction:column;background:var(--card);backdrop-filter:blur(20px);border-radius:40px;overflow:hidden;box-shadow:0 25px 50px -12px rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.1)}}
  .chat-header{{background:rgba(0,0,0,0.3);padding:20px 25px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(255,255,255,0.1)}}
  .chat-header h3{{font-size:1.3rem;background:linear-gradient(135deg,#fff,#6c63ff);background-clip:text;-webkit-background-clip:text;color:transparent}}
  .theme-btn{{background:rgba(255,255,255,0.1);border:none;border-radius:50%;width:40px;height:40px;cursor:pointer;font-size:1.2rem}}
  .voice-controls{{display:flex;gap:10px;margin-left:10px}}
  .voice-btn{{background:rgba(108,99,255,0.3);border:none;border-radius:50%;width:40px;height:40px;cursor:pointer;font-size:1.2rem;transition:all 0.3s}}
  .voice-btn:hover{{transform:scale(1.05);background:rgba(108,99,255,0.5)}}
  .record-btn{{background:#ff6584;border:none;border-radius:50%;width:40px;height:40px;cursor:pointer;font-size:1.2rem;transition:all 0.3s}}
  .record-btn.recording{{animation:pulse 1s infinite;background:#ef4444}}
  @keyframes pulse{{0%{{transform:scale(1)}}50%{{transform:scale(1.1)}}100%{{transform:scale(1)}}}}
  .chat-messages{{flex:1;overflow-y:auto;padding:25px;display:flex;flex-direction:column;gap:15px;max-height:55vh}}
  .message{{max-width:80%;padding:12px 20px;border-radius:25px;line-height:1.5;animation:pop 0.3s ease}}
  @keyframes pop{{from{{opacity:0;transform:scale(0.9)}}to{{opacity:1;transform:scale(1)}}}}
  .message.user{{background:var(--user);color:white;align-self:flex-end;border-bottom-right-radius:5px}}
  .message.bot{{background:var(--bot);color:var(--text);align-self:flex-start;border-bottom-left-radius:5px}}
  .message.bot .confidence{{font-size:0.7rem;color:var(--muted);margin-top:5px}}
  .rating-stars{{display:flex;align-items:center;gap:5px;margin-top:10px;padding-top:5px;border-top:1px solid rgba(255,255,255,0.1)}}
  .star{{font-size:1.2rem;cursor:pointer;transition:all 0.2s;color:var(--muted)}}
  .star:hover{{transform:scale(1.2);color:#ffc107}}
  .typing{{align-self:flex-start;background:var(--bot);padding:12px 20px;border-radius:25px;display:none;gap:5px}}
  .typing.active{{display:flex}}
  .typing span{{width:8px;height:8px;background:var(--muted);border-radius:50%;animation:typing 1.4s infinite}}
  .typing span:nth-child(2){{animation-delay:0.2s}}
  .typing span:nth-child(3){{animation-delay:0.4s}}
  @keyframes typing{{0%,60%,100%{{transform:translateY(0);opacity:0.5}}30%{{transform:translateY(-8px);opacity:1}}}}
  .chat-input-area{{padding:20px;display:flex;gap:15px;border-top:1px solid rgba(255,255,255,0.1);background:rgba(0,0,0,0.2)}}
  .chat-input{{flex:1;padding:14px 20px;border:1px solid rgba(255,255,255,0.2);border-radius:30px;background:rgba(255,255,255,0.1);color:var(--text);font-size:1rem;outline:none}}
  .chat-input:focus{{border-color:#6c63ff;box-shadow:0 0 15px rgba(108,99,255,0.3)}}
  .send-btn{{background:linear-gradient(90deg,#6c63ff,#ff6584);border:none;border-radius:30px;padding:0 28px;color:white;font-weight:bold;cursor:pointer;transition:all 0.3s}}
  .send-btn:hover{{transform:scale(1.05)}}
  .back-btn{{position:fixed;bottom:20px;left:20px;background:rgba(108,99,255,0.3);backdrop-filter:blur(10px);padding:8px 20px;border-radius:30px;color:white;text-decoration:none;font-size:0.9rem;transition:all 0.3s}}
  .back-btn:hover{{background:rgba(108,99,255,0.5)}}
  .profile-panel{{background:rgba(0,0,0,0.3);padding:15px 25px;display:flex;gap:15px;align-items:center;flex-wrap:wrap}}
  .profile-panel input,.profile-panel select{{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);padding:8px 15px;border-radius:20px;color:var(--text);outline:none}}
  .profile-panel input:focus,.profile-panel select:focus{{border-color:#6c63ff}}
  .profile-panel button{{background:linear-gradient(90deg,#6c63ff,#ff6584);border:none;padding:8px 20px;border-radius:20px;color:white;cursor:pointer;transition:all 0.3s}}
  .profile-panel button:hover{{transform:scale(1.02)}}
  .recording-status{{color:#ff6584;font-size:0.8rem}}
  .profile-status{{color:#10b981;font-size:0.8rem}}
  @media(max-width:768px){{.chat-container{{margin:10px}}.message{{max-width:90%}}.profile-panel{{gap:8px}}}}
</style>
</head>
<body>
<div class="chat-container">
  <div class="chat-header">
    <h3>مسیرینو | مشاور هوشمند</h3>
    <div class="voice-controls">
      <button class="record-btn" id="recordBtn" onclick="startVoice()" title="شروع ضبط صدا">🎤</button>
      <button class="voice-btn" id="stopBtn" onclick="stopVoice()" title="توقف ضبط صدا" style="display:none">⏹️</button>
      <button class="voice-btn" onclick="speakLastMessage()" title="خواندن آخرین پیام">🔊</button>
      <button class="theme-btn" onclick="toggleTheme()">🌙</button>
    </div>
  </div>
  <div class="profile-panel">
    <span>👤 نام:</span>
    <input type="text" id="firstName" placeholder="نام" style="width:100px">
    <span>نام خانوادگی:</span>
    <input type="text" id="lastName" placeholder="نام خانوادگی" style="width:100px">
    <span>📚 پایه:</span>
    <select id="gradeLevel">
      <option value="">انتخاب کنید</option>
      <option value="ابتدایی">ابتدایی</option>
      <option value="هفتم-نهم">هفتم-نهم</option>
      <option value="دهم-دوازدهم">دهم-دوازدهم</option>
      <option value="دانشگاه">دانشگاه</option>
    </select>
    <button onclick="saveProfile()">💾 ذخیره</button>
    <span id="profileStatus" class="profile-status"></span>
    <span id="recordingStatus" class="recording-status"></span>
  </div>
  <div class="chat-messages" id="chatMessages">
    <div class="message bot">سلام! 🌟 من مسیرینو هستم، مشاور تحصیلی هوشمند. لطفاً نام و پایه خودت رو در پنل بالا وارد کن 🤗</div>
  </div>
  <div class="typing" id="typing"><span></span><span></span><span></span></div>
  <div class="chat-input-area">
    <input type="text" class="chat-input" id="chatInput" placeholder="سوال خود را بنویسید یا دکمه میکروفون را بزنید..." onkeypress="if(event.key==='Enter')sendMessage()">
    <button class="send-btn" onclick="sendMessage()">ارسال</button>
  </div>
</div>
<a href="/" class="back-btn">← بازگشت</a>
<script>
var sessionId = "{session_id}";
var currentUtterance = null;
var recognition = null;
var lastBotMessage = '';
var messageCounter = 0;

function toggleTheme() {{
    var html = document.documentElement;
    if (html.getAttribute('data-theme') === 'light') {{
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'dark');
        var btn = document.querySelector('.theme-btn');
        if (btn) btn.innerHTML = '🌙';
    }} else {{
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        var btn = document.querySelector('.theme-btn');
        if (btn) btn.innerHTML = '☀️';
    }}
}}

if (localStorage.getItem('theme') === 'light') {{
    document.documentElement.setAttribute('data-theme', 'light');
    var btn = document.querySelector('.theme-btn');
    if (btn) btn.innerHTML = '☀️';
}}

function saveProfile() {{
    var firstName = document.getElementById('firstName').value;
    var lastName = document.getElementById('lastName').value;
    var gradeLevel = document.getElementById('gradeLevel').value;
    
    fetch('/save-profile', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{
            session_id: sessionId, 
            first_name: firstName,
            last_name: lastName,
            grade_level: gradeLevel
        }})
    }})
    .then(function(res) {{ return res.json(); }})
    .then(function(data) {{
        if(data.status === 'ok') {{
            document.getElementById('profileStatus').innerText = '✅ ذخیره شد';
            setTimeout(function() {{ 
                document.getElementById('profileStatus').innerText = ''; 
            }}, 2000);
        }} else {{
            document.getElementById('profileStatus').innerText = '❌ خطا';
        }}
    }})
    .catch(function(err) {{
        console.error(err);
        document.getElementById('profileStatus').innerText = '❌ خطا';
    }});
}}

function addMessage(text, type, confidence, messageId) {{
    var div = document.getElementById('chatMessages');
    var msg = document.createElement('div');
    msg.className = 'message ' + type;
    var htmlText = text.replace(/\\n/g, '<br>');
    
    if (confidence && type === 'bot') {{
        htmlText += '<div class="confidence">🎯 دقت پاسخ: ' + confidence + '%</div>';
    }}
    
    if (type === 'bot' && messageId) {{
        htmlText += '<div class="rating-stars" data-msg-id="' + messageId + '">';
        htmlText += '<span style="font-size:0.75rem;margin-left:8px;">⭐ امتیاز بده:</span>';
        for (var r = 1; r <= 5; r++) {{
            htmlText += '<span class="star" data-rating="' + r + '" onclick="rateMessage(\\'' + messageId + '\\', ' + r + ')">☆</span>';
        }}
        htmlText += '</div>';
    }}
    
    msg.innerHTML = htmlText;
    div.appendChild(msg);
    div.scrollTop = div.scrollHeight;
    
    if (type === 'bot') {{
        speakText(text);
    }}
}}

function rateMessage(messageId, rating) {{
    var starsContainer = document.querySelector('.rating-stars[data-msg-id="' + messageId + '"]');
    if (!starsContainer) {{
        return;
    }}
    
    if (starsContainer.getAttribute('data-rated') === 'true') {{
        return;
    }}
    
    starsContainer.setAttribute('data-rated', 'true');
    
    var stars = starsContainer.querySelectorAll('.star');
    for (var i = 0; i < stars.length; i++) {{
        var star = stars[i];
        var starRating = parseInt(star.getAttribute('data-rating'), 10);
        if (starRating <= rating) {{
            star.innerHTML = '★';
            star.style.color = '#ffc107';
        }} else {{
            star.innerHTML = '☆';
            star.style.color = 'var(--muted)';
        }}
    }}
    
    fetch('/rate-message', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json'
        }},
        body: JSON.stringify({{
            session_id: sessionId,
            message_id: messageId,
            rating: rating
        }})
    }}).catch(function(e) {{
        console.error('خطا در ثبت امتیاز:', e);
    }});
}}

function showTyping() {{
    document.getElementById('typing').classList.add('active');
}}

function hideTyping() {{
    document.getElementById('typing').classList.remove('active');
}}

function sendMessage() {{
    var input = document.getElementById('chatInput');
    var msg = input.value.trim();
    if (!msg) return;
    addMessage(msg, 'user');
    input.value = '';
    showTyping();
    var currentMsgId = Date.now() + '_' + (++messageCounter);
    
    fetch('/chat', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{message: msg, session_id: sessionId, message_id: currentMsgId}})
    }})
    .then(function(res) {{ return res.json(); }})
    .then(function(data) {{
        hideTyping();
        var confidenceMatch = data.response.match(/\\(دقت پاسخ: (\\d+)%\\)/);
        var confidence = confidenceMatch ? confidenceMatch[1] : null;
        var cleanResponse = data.response;
        if (confidence) {{
            cleanResponse = cleanResponse.replace(/\\s*\\(دقت پاسخ: \\d+%\\)/, '');
        }}
        addMessage(cleanResponse, 'bot', confidence, data.message_id || currentMsgId);
        lastBotMessage = cleanResponse;
    }})
    .catch(function(e) {{
        hideTyping();
        addMessage('خطایی رخ داد. دوباره تلاش کنید.', 'bot');
    }});
}}

function startVoice() {{
    if (!('webkitSpeechRecognition' in window)) {{
        addMessage('❌ مرورگر شما از تشخیص صدا پشتیبانی نمی‌کند. لطفاً از Chrome استفاده کنید.', 'bot');
        return;
    }}
    navigator.mediaDevices.getUserMedia({{ audio: true }}).then(function(stream) {{
        stream.getTracks().forEach(function(track) {{ track.stop(); }});
        document.getElementById('recordBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'flex';
        document.getElementById('recordingStatus').innerHTML = '🎤 در حال ضبط... صحبت کنید';
        document.getElementById('recordBtn').classList.add('recording');
        recognition = new webkitSpeechRecognition();
        recognition.lang = 'fa-IR';
        recognition.interimResults = true;
        recognition.continuous = true;
        var finalTranscript = '';
        recognition.onresult = function(event) {{
            var interimTranscript = '';
            for (var i = event.resultIndex; i < event.results.length; i++) {{
                var transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {{
                    finalTranscript += transcript;
                }} else {{
                    interimTranscript += transcript;
                }}
            }}
            document.getElementById('chatInput').value = finalTranscript + interimTranscript;
        }};
        recognition.onerror = function(event) {{
            if (event.error === 'not-allowed') {{
                addMessage('❌ لطفاً به میکروفون دسترسی بدهید. روی آیکون قفل کنار آدرس کلیک کنید و Allow را بزنید.', 'bot');
            }} else {{
                addMessage('❌ خطا: ' + event.error, 'bot');
            }}
            stopVoice();
        }};
        recognition.onend = function() {{
            if (finalTranscript.trim()) {{
                sendMessage();
            }}
            stopVoice();
        }};
        recognition.start();
    }}).catch(function(err) {{
        addMessage('❌ لطفاً به میکروفون دسترسی بدهید. در مرورگر روی قفل کنار آدرس کلیک کنید و Allow را بزنید.', 'bot');
    }});
}}

function stopVoice() {{
    if (recognition) {{
        recognition.stop();
        recognition = null;
    }}
    document.getElementById('recordBtn').style.display = 'flex';
    document.getElementById('stopBtn').style.display = 'none';
    document.getElementById('recordingStatus').innerHTML = '';
    document.getElementById('recordBtn').classList.remove('recording');
}}

function speakLastMessage() {{
    if (lastBotMessage) {{
        speakText(lastBotMessage);
    }} else {{
        var lastMsg = document.querySelector('.message.bot:last-child');
        if (lastMsg) {{
            var text = lastMsg.innerText;
            text = text.replace(/🎯 دقت پاسخ: \\d+%/, '');
            speakText(text);
        }}
    }}
}}

function speakText(text) {{
    if (currentUtterance) window.speechSynthesis.cancel();
    var cleanText = text.replace(/[🩺💻📚🎯📉🤖🌟😊🌙☀️🎤⏹️✅❌⚡🔬🧠💡💪🌱🧘🎨🚀]/g, '');
    cleanText = cleanText.replace(/[#*_`~]/g, '');
    cleanText = cleanText.replace(/🎯 دقت پاسخ: \\d+%/g, '');
    var hasPersian = /[\\u0600-\\u06FF]/.test(cleanText);
    if (hasPersian) {{
        var hasPersianVoice = false;
        var voices = window.speechSynthesis.getVoices();
        for (var i = 0; i < voices.length; i++) {{
            if (voices[i].lang === 'fa-IR' || voices[i].lang === 'fa' || voices[i].name.includes('Persian') || voices[i].name.includes('فارسی')) {{
                hasPersianVoice = true;
                break;
            }}
        }}
        if (hasPersianVoice) {{
            var utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang = 'fa-IR';
            utterance.rate = 0.9;
            for (var j = 0; j < voices.length; j++) {{
                if (voices[j].lang === 'fa-IR' || voices[j].lang === 'fa') {{
                    utterance.voice = voices[j];
                    break;
                }}
            }}
            utterance.onend = function() {{ currentUtterance = null; }};
            utterance.onerror = function(e) {{ console.error('TTS error:', e); }};
            currentUtterance = utterance;
            window.speechSynthesis.speak(utterance);
        }} else if (window.location.protocol === 'https:') {{
            var url = 'https://translate.google.com/translate_tts?ie=UTF-8&q=' + encodeURIComponent(cleanText) + '&tl=fa&client=tw-ob';
            var audio = new Audio(url);
            audio.play();
            audio.onended = function() {{ currentUtterance = null; }};
            currentUtterance = audio;
        }}
    }} else {{
        var utteranceEn = new SpeechSynthesisUtterance(cleanText);
        utteranceEn.lang = 'en-US';
        utteranceEn.rate = 0.9;
        utteranceEn.onend = function() {{ currentUtterance = null; }};
        currentUtterance = utteranceEn;
        window.speechSynthesis.speak(utteranceEn);
    }}
}}

window.speechSynthesis.getVoices();
if (window.speechSynthesis.onvoiceschanged !== undefined) {{
    window.speechSynthesis.onvoiceschanged = window.speechSynthesis.getVoices;
}}

document.getElementById('chatInput').focus();

function loadUserData() {{
    fetch('/get-user-profile?session_id=' + sessionId)
        .then(function(res) {{ return res.json(); }})
        .then(function(data) {{
            if(data.status === 'ok') {{
                if(data.first_name) document.getElementById('firstName').value = data.first_name;
                if(data.last_name) document.getElementById('lastName').value = data.last_name;
                if(data.grade_level) document.getElementById('gradeLevel').value = data.grade_level;
            }}
        }})
        .catch(function(err) {{ console.error(err); }});
}}

loadUserData();
</script>
</body></html>"""


def render_track_form_page(session_id, step=1, data=None):
    data = data or {}
    grade_level = data.get("gradeLevel", "هفتم-نهم")
    category = grade_category(grade_level)
    track = data.get("track", "")
    
    if category == "basic":
        subjects = SUBJECTS_BY_LEVEL.get(grade_level, SUBJECTS_BY_LEVEL["هفتم-نهم"])
    else:
        subjects = SUBJECTS_BY_TRACK.get(track, [])
    
    progress = "33%" if step == 1 else ("66%" if step == 2 else "100%")
    
    def val(name, default=""):
        return escape(str(data.get(name, default)))
    
    think_options = "".join([f'<option value="{k}" {"selected" if data.get("dominant_think")==k else ""} style="color:{v["color"]}">{v["icon"]} {k} - {v["desc"]}</option>' for k, v in THINKING_STYLES.items()])
    
    step1 = f"""
    <div class="step-card" style="display:{'block' if step==1 else 'none'};">
      <h3>📋 مرحله ۱: اطلاعات پایه</h3>
      <div class="row"><div class="field"><label>نام (اختیاری)</label><input name="firstName" value="{val('firstName')}" placeholder="نام خود را وارد کنید"></div>
      <div class="field"><label>نام خانوادگی (اختیاری)</label><input name="lastName" value="{val('lastName')}" placeholder="نام خانوادگی"></div></div>
      <div class="row"><div class="field"><label>سن</label><input type="number" name="age" value="{val('age', 0)}" required></div>
      <div class="field"><label>پایه تحصیلی</label><select name="gradeLevel" required>
        <option value="ابتدایی" {"selected" if grade_level=="ابتدایی" else ""}>ابتدایی</option>
        <option value="هفتم-نهم" {"selected" if grade_level=="هفتم-نهم" else ""}>هفتم-نهم</option>
        <option value="دهم-دوازدهم" {"selected" if grade_level=="دهم-دوازدهم" else ""}>دهم-دوازدهم</option>
        <option value="دانشگاه" {"selected" if grade_level=="دانشگاه" else ""}>دانشگاه</option>
      </select></div></div>
      <div class="row"><div class="field"><label>🎯 سبک فکری غالب</label><select name="dominant_think" required>{think_options}</select></div>
      <div class="field"><label>📊 معدل تقریبی (از 20)</label><input type="number" step="0.1" min="0" max="20" name="average_grade" value="{val('average_grade', 15)}" required></div></div>
      <div class="hint">💡 سبک فکری به تحلیل دقیق‌تر رشته و شغل کمک می‌کند | معدل تقریبی خود را وارد کنید</div>
    </div>"""
    
    track_select = ""
    if category == "advanced" and step == 1:
        track_select = f"""<div class="step-card"><h3>🎓 رشته تحصیلی فعلی</h3><select name="track" required>
          <option value="ریاضی فیزیک">⚡ ریاضی فیزیک</option>
          <option value="علوم تجربی">🔬 علوم تجربی</option>
          <option value="علوم انسانی">📖 علوم انسانی</option>
          <option value="هنر">🎨 هنر</option>
        </select><div class="hint">رشته فعلی خود را انتخاب کنید</div></div>"""
    
    subjects_html = ""
    if step == 2:
        for subj in subjects:
            k = safe_key(subj)
            subjects_html += f"""
            <div class="subject-item">
              <h4>{subj}</h4>
              <div class="row">
                <div class="field"><label>📖 فهم و درک (1-5)</label><input type="number" min="1" max="5" name="{k}__understanding" value="3" required></div>
                <div class="field"><label>📝 عملکرد در آزمون (1-5)</label><input type="number" min="1" max="5" name="{k}__performance" value="3" required></div>
              </div>
              <div class="field"><label>❤️ علاقه به درس (1-5)</label><input type="number" min="1" max="5" name="{k}__interest" value="3" required></div>
              <div class="hint">1=خیلی کم، 5=خیلی زیاد</div>
            </div>"""
    
    next_text = "بعدی ➡️" if step < 2 else "مشاهده نتایج پیشرفته 🎯"
    
    return f"""<!doctype html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>انتخاب رشته مسیرینو</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .wrap{{max-width:800px;margin:auto}}
  .progress{{height:8px;background:rgba(255,255,255,0.1);border-radius:10px;margin-bottom:30px}}
  .bar{{height:100%;width:{progress};background:linear-gradient(90deg,#6c63ff,#ff6584);border-radius:10px}}
  .step-card,.subject-item{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;margin-bottom:20px;border:1px solid rgba(255,255,255,0.1)}}
  .row{{display:grid;grid-template-columns:1fr 1fr;gap:15px}}
  .field label{{display:block;margin-bottom:8px;color:var(--muted)}}
  input,select{{width:100%;padding:12px;border-radius:16px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.2);color:var(--text);outline:none}}
  input:focus,select:focus{{border-color:#6c63ff}}
  button{{width:100%;padding:14px;border:none;border-radius:30px;background:linear-gradient(90deg,#6c63ff,#ff6584);color:white;font-weight:bold;cursor:pointer;transition:all 0.3s}}
  button:hover{{transform:translateY(-2px)}}
  .hint{{font-size:12px;color:var(--muted);margin-top:10px}}
  .back-home{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  @media(max-width:768px){{.row{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="wrap"><div class="progress"><div class="bar"></div></div>
<form method="POST" action="/track-submit"><input type="hidden" name="session_id" value="{escape(session_id)}"><input type="hidden" name="step" value="{step}">
{step1}{track_select}<div style="display:{'block' if step==2 else 'none'}">{subjects_html}</div>
<button type="submit">{next_text}</button></form>
<a href="/" class="back-home">← بازگشت به صفحه اصلی</a></div>
<script>if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light');</script>
</body></html>"""


def render_track_result_page(data):
    if not data:
        return "<html><body>نتیجه‌ای یافت نشد</body></html>"
    
    all_tracks = data.get("all_tracks", [])
    strengths_weaknesses = data.get("strengths_weaknesses", {})
    subject_interests = data.get("subject_interests", {})
    career_by_track = data.get("career_by_track", {})
    user_code = data.get("user_code", "کاربر مهمان")
    grade_level = data.get("gradeLevel", "")
    
    tracks_html = ""
    for t in all_tracks:
        tracks_html += f"""
        <div class="track-card" style="border-right:4px solid {t['color']}">
          <div class="track-header"><span class="track-icon">{t.get('icon', '📚')}</span><span class="track-name">{t['track']}</span><span class="track-score" style="color:{t['color']}">{t['score']}%</span></div>
          <div class="track-details"><span>🎯 توانایی {t['ability_score']}%</span><span>❤️ علاقه {t['interest_score']}%</span><span>🧠 سبک {t['think_score']}%</span><span>📈 آینده {t['future_score']}%</span><span>📊 معدل {t.get('grade_score', 0)}%</span></div>
          <div class="meter"><div class="fill" style="width:{t['score']}%;background:linear-gradient(90deg,{t['color']},#ff6584)"></div></div>
          <div class="track-level">📍 {t['level']}</div>
          <div class="track-desc" style="font-size:0.85rem;color:var(--muted);margin-top:12px;line-height:1.5">{t.get('description', '')}</div>
        </div>"""
    
    sw_html = ""
    for track, sw in strengths_weaknesses.items():
        strengths_list = ", ".join([s['subject'] for s in sw.get('strengths', [])]) or "—"
        weaknesses_list = ", ".join([w['subject'] for w in sw.get('weaknesses', [])]) or "—"
        sw_html += f"""
        <div class="sw-card">
          <h4><span class="track-icon">{'🔬' if track=='علوم تجربی' else '⚡' if track=='ریاضی فیزیک' else '📖' if track=='علوم انسانی' else '🎨'}</span> {track}</h4>
          <div class="strengths">✅ نقاط قوت: {strengths_list}</div>
          <div class="weaknesses">⚠️ نقاط ضعف: {weaknesses_list}</div>
        </div>"""
    
    careers_html = ""
    for track, careers in career_by_track.items():
        if careers:
            track_icon = '🔬' if track=='علوم تجربی' else '⚡' if track=='ریاضی فیزیک' else '📖' if track=='علوم انسانی' else '🎨'
            careers_html += f"""
            <div class="career-card">
              <h4>{track_icon} شغل‌های مناسب برای {track}</h4>
              <div class="career-list">
                {''.join([f'<div class="career-item" style="border-right:3px solid {c.get("rec_color", "#6c63ff")}"><span class="career-icon">{c["icon"]}</span><div><div class="career-name">{c["job"]}</div><div class="career-hint">{c["hint"]}</div><div class="career-details"><span>⏱️ {c.get("study_time", "4 سال")}</span><span>💰 {c.get("avg_income", "نامشخص")}</span></div></div><div class="career-percent" style="color:{c.get("rec_color", "#6c63ff")}">{c["percent"]}%</div><div class="career-badge" style="background:{c.get("rec_color", "#6c63ff")}">{c["recommendation"]}</div></div>' for c in careers[:5]])}
              </div>
            </div>"""
    
    interest_bars = ""
    for subj, val in sorted(subject_interests.items(), key=lambda x: x[1], reverse=True)[:12]:
        pct = (val / 5.0) * 100
        col = color_for_percent(pct)
        interest_bars += f"""
        <div class="interest-bar"><div class="interest-label">{subj} — {val}/5</div><div class="meter"><div class="fill" style="width:{pct}%;background:linear-gradient(90deg,{col},#ff6584)"></div></div></div>"""
    
    return f"""<!doctype html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>نتیجه انتخاب رشته</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .wrap{{max-width:1000px;margin:auto}}
  .card,.track-card,.sw-card,.career-card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;margin-bottom:20px}}
  .track-card{{margin-bottom:15px}}
  .track-header{{display:flex;align-items:center;gap:12px;margin-bottom:10px}}
  .track-icon{{font-size:1.5rem}}
  .track-name{{font-size:1.3rem;font-weight:bold;flex:1}}
  .track-score{{font-size:1.8rem;font-weight:bold}}
  .track-details{{display:flex;gap:15px;margin-bottom:10px;font-size:0.8rem;color:var(--muted);flex-wrap:wrap}}
  .meter{{height:8px;background:rgba(255,255,255,0.1);border-radius:10px;overflow:hidden;margin:10px 0}}
  .fill{{height:100%;border-radius:10px}}
  .track-level{{font-size:0.85rem;color:var(--muted);margin-top:8px}}
  .sw-card h4{{margin-bottom:8px;display:flex;align-items:center;gap:8px}}
  .strengths{{color:#10b981;margin:5px 0}}
  .weaknesses{{color:#f59e0b;margin:5px 0}}
  .career-item{{display:flex;align-items:center;gap:12px;padding:12px;background:rgba(0,0,0,0.2);border-radius:16px;margin-bottom:8px}}
  .career-icon{{font-size:1.8rem}}
  .career-name{{font-weight:bold;font-size:1rem}}
  .career-hint{{font-size:0.7rem;color:var(--muted)}}
  .career-details{{display:flex;gap:12px;margin-top:4px;font-size:0.65rem;color:var(--muted)}}
  .career-percent{{margin-right:auto;font-weight:bold;font-size:1.1rem}}
  .career-badge{{padding:2px 8px;border-radius:20px;font-size:0.7rem;color:white}}
  .interest-bar{{margin:12px 0}}
  .interest-label{{font-weight:bold;margin-bottom:4px}}
  .report-buttons{{display:flex;gap:15px;justify-content:center;margin:20px 0;flex-wrap:wrap}}
  .report-btn{{padding:12px 25px;border:none;border-radius:30px;font-weight:bold;cursor:pointer;transition:all 0.3s}}
  .report-btn.html{{background:#10b981;color:white}}
  .report-btn.pdf{{background:#ef4444;color:white}}
  .report-btn:hover{{transform:translateY(-3px);box-shadow:0 5px 15px rgba(0,0,0,0.3)}}
  .back{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
</style>
</head>
<body>
<div class="wrap">
  <div class="report-buttons">
    <button class="report-btn html" onclick="downloadHTML()">📄 دانلود گزارش HTML</button>
    <button class="report-btn pdf" onclick="downloadPDF()">📑 دانلود گزارش PDF</button>
  </div>
  <div id="report-content">
    <div class="card"><h2>🎯 نتیجه تحلیل رشته تحصیلی</h2><div><span class="badge">کد: {data.get('user_code', 'کاربر مهمان')}</span><span class="badge">پایه: {data['gradeLevel']}</span><span class="badge">سبک فکری: {data.get('dominant_think', 'تحلیلی')}</span></div>
      <div class="hint" style="margin-top:10px;font-size:13px;">📊 درصدها بر اساس: 30% توانایی + 25% علاقه + 20% سبک فکری + 15% آینده شغلی + 10% معدل</div></div>
      <div class="card"><h3>✅ امتیاز رشته‌های تحصیلی</h3>{tracks_html}</div>
      <div class="card"><h3>📊 نقاط قوت و ضعف هر رشته</h3>{sw_html}</div>
      <div class="card"><h3>📊 میزان علاقه به درس‌ها (اولویت‌بندی شده)</h3>{interest_bars}</div>
      <div class="card"><h3>💼 شغل‌های مناسب بر اساس رشته</h3>{careers_html}</div>
  </div>
  <a href="/" class="back">← بازگشت به صفحه اصلی</a>
</div>
<script>
function downloadHTML() {{
    const content = document.getElementById('report-content').innerHTML;
    const style = document.querySelector('style').innerHTML;
    const fullHtml = `<!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head><meta charset="UTF-8"><title>گزارش انتخاب رشته</title><style>${{style}} body{{padding:20px;background:white;color:black}} .report-buttons{{display:none}} .back{{display:none}}</style></head>
    <body><div class="wrap">${{content}}</div></body></html>`;
    const blob = new Blob([fullHtml], {{type: 'text/html'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'holland_track_report_{user_code}_{grade_level}.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}}
function downloadPDF() {{
    const element = document.getElementById('report-content');
    const opt = {{
        margin: [0.5, 0.5, 0.5, 0.5],
        filename: 'holland_track_report_{user_code}_{grade_level}.pdf',
        image: {{ type: 'jpeg', quality: 0.98 }},
        html2canvas: {{ scale: 2, useCORS: true, letterRendering: true }},
        jsPDF: {{ unit: 'in', format: 'a4', orientation: 'portrait' }}
    }};
    html2pdf().set(opt).from(element).save();
}}
</script>
<script>if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light');</script>
</body></html>"""


def render_risk_form_page(session_id, data=None):
    data = data or {}
    def val(name, default=""): return escape(str(data.get(name, default)))
    
    return f"""<!doctype html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>پیش‌بینی افت نمره</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .wrap{{max-width:800px;margin:auto}}
  .glass-card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;margin-bottom:20px}}
  .row{{display:grid;grid-template-columns:1fr 1fr;gap:15px}}
  .field label{{display:block;margin-bottom:8px;color:var(--muted)}}
  input,select{{width:100%;padding:12px;border-radius:16px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.2);color:var(--text);outline:none}}
  input:focus,select:focus{{border-color:#6c63ff}}
  button{{width:100%;padding:14px;border:none;border-radius:30px;background:linear-gradient(90deg,#6c63ff,#ff6584);color:white;font-weight:bold;cursor:pointer;transition:all 0.3s}}
  button:hover{{transform:translateY(-2px)}}
  .back-home{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  .hint{{font-size:12px;color:var(--muted);margin-top:5px}}
  @media(max-width:768px){{.row{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="wrap">
<form method="POST" action="/risk-submit"><input type="hidden" name="session_id" value="{escape(session_id)}">
<div class="glass-card"><h3>📋 اطلاعات اولیه</h3><div class="row"><div class="field"><label>نام (اختیاری)</label><input name="firstName" value="{val('firstName')}" placeholder="نام خود را وارد کنید"></div><div class="field"><label>نام خانوادگی (اختیاری)</label><input name="lastName" value="{val('lastName')}" placeholder="نام خانوادگی"></div></div>
<div class="row"><div class="field"><label>سن</label><input name="age" value="{val('age',0)}" type="number"></div><div class="field"><label>پایه تحصیلی</label><select name="gradeLevel"><option>هفتم-نهم</option><option>دهم-دوازدهم</option><option>دانشگاه</option></select></div></div></div>
<div class="glass-card"><h3>📚 عادات مطالعه</h3><div class="row"><div class="field"><label>ساعت مطالعه روزانه (1-5)</label><input name="study_hours_rating" value="3" type="number" min="1" max="5"><div class="hint">1=کمتر از 1 ساعت، 5=بیش از 5 ساعت</div></div><div class="field"><label>روزهای مطالعه در هفته (1-7)</label><input name="study_days_week_rating" value="3" type="number" min="1" max="7"></div></div>
<div class="row"><div class="field"><label>شیوه مطالعه</label><select name="study_mode"><option>منظم</option><option>نیمه‌منظم</option><option>ضربتی</option></select></div><div class="field"><label>حواس‌پرتی (1-5)</label><input name="distract_rating" value="3" type="number" min="1" max="5"><div class="hint">1=کمترین، 5=بیشترین</div></div></div>
<div class="row"><div class="field"><label>مرور بعد از یادگیری</label><select name="has_review"><option>دارم (منظم)</option><option>بعضی وقت‌ها</option><option>تقریباً نه</option></select></div><div class="field"><label>شروع مطالعه قبل از امتحان</label><select name="start_days_before_exam"><option>30+</option><option>10–20</option><option>3–7</option><option>از روز امتحان!</option></select></div></div>
<div class="row"><div class="field"><label>کیفیت خواب</label><select name="sleep_status"><option>خوب</option><option>متوسط</option><option>کم</option></select></div><div class="field"><label>استرس قبل امتحان (1-5)</label><input name="stress_rating" value="3" type="number" min="1" max="5"></div></div>
<div class="row"><div class="field"><label>ناحیه ضعف اصلی</label><select name="main_weakness_area"><option>محاسباتی / تمرین</option><option>مفهومی (درک)</option><option>تشریحی / نگارش</option><option>زمان کم می‌آورم</option><option>بی‌دقتی</option></select></div><div class="field"><label>اجرای برنامه (1-5)</label><input name="can_execute_plan" value="3" type="number" min="1" max="5"></div></div>
<div class="row"><div class="field"><label>معلم خصوصی</label><select name="has_tutor"><option>ندارم</option><option>تا حدی</option><option>دارم (کلاس/معلم خصوصی)</option></select></div><div class="field"><label>جلسات پشتیبان در هفته</label><input name="tutor_sessions_week" value="0" type="number" min="0" max="7"></div></div>
<div class="row"><div class="field"><label>حمایت خانواده</label><select name="family_support"><option>خوب</option><option>متوسط</option><option>ضعیف</option></select></div><div class="field"><label>سابقه افت نمره</label><select name="previous_fail"><option>ندارم</option><option>دارم</option></select></div></div>
<div class="row"><div class="field"><label>اضطراب امتحان (1-5)</label><input name="test_anxiety" value="3" type="number" min="1" max="5"><div class="hint">1=بدون اضطراب، 5=اضطراب شدید</div></div></div></div>
<button type="submit">محاسبه دقیق ریسک افت نمره 📊</button></form>
<a href="/" class="back-home">← بازگشت</a></div>
<script>if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light');</script>
</body></html>"""


def render_risk_result_page(data):
    if not data:
        return "<html><body>نتیجه‌ای یافت نشد</body></html>"
    
    risk_fall = data.get("risk_fall", {})
    risk_data = risk_fall.get("risk_data", {})
    breakdown = risk_fall.get("breakdown", {})
    risky_subjects = risk_fall.get("risky_subjects", [])
    plan = risk_fall.get("plan", {})
    resources = risk_fall.get("resources", {})
    tips = risk_fall.get("tips", [])
    user_code = data.get("user_code", "کاربر مهمان")
    grade_level = data.get("gradeLevel", "")
    
    risk_percent = risk_data.get("risk_percent", 0)
    level_text = risk_data.get("level_text", "کم")
    level_color = risk_data.get("level_color", "#10b981")
    advice = risk_data.get("advice", "")
    recommendation = risk_data.get("recommendation", "")
    
    breakdown_html = "".join([f'<div class="break-item"><span class="break-label">{k}</span><div class="break-bar"><div style="width:{v}%;background:{color_for_percent(v)}"></div></div><span class="break-value">{v}%</span></div>' for k, v in breakdown.items()])
    
    risky_html = "".join([f'<li class="risk-item" style="border-right-color:{r.get("color", "#f59e0b")}"><strong>{r["subject"]}</strong><div class="risk-bar"><div style="width:{r["risk_percent"]}%;background:{r.get("color", "#f59e0b")}"></div></div><span>{r["risk_percent"]}%</span><div class="risk-reason">{r["reason"]}</div></li>' for r in risky_subjects]) if risky_subjects else "<li class=\"risk-item\">✅ درسی در معرض خطر جدی شناسایی نشد - عالی کار می‌کنی!</li>"
    
    plan_days = plan.get("days", [])
    plan_html = "".join([f'<div class="plan-day"><span class="day-icon">{d["icon"]}</span><span class="day-name">{d["day"]}</span><span class="day-task">{d["task"]}</span><span class="day-time">⏱️ {d["time"]}</span><span class="day-priority" style="color:{"#ef4444" if d["priority"]=="بسیار مهم" else "#f59e0b" if d["priority"]=="مهم" else "#10b981"}">{d["priority"]}</span></div>' for d in plan_days])
    
    resources_html = "".join([f'<div class="resource-item"><div class="resource-icon">📚</div><div><strong>{subj}</strong><div class="resource-links">{", ".join(res)}</div></div></div>' for subj, res in resources.items()]) if resources else "<div class=\"resource-item\">منابع پیشنهادی با توجه به دروس شما ارائه خواهد شد</div>"
    
    tips_html = "".join([f"<li class='tip-item'>{tip}</li>" for tip in tips])
    
    return f"""<!doctype html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>نتیجه پیش‌بینی افت</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .wrap{{max-width:950px;margin:auto}}
  .card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;margin-bottom:20px}}
  .risk-box{{text-align:center;padding:30px}}
  .risk-percent{{font-size:4rem;font-weight:bold;color:{level_color}}}
  .risk-level{{font-size:1.3rem;margin:10px 0}}
  .advice{{color:var(--muted);margin-top:10px}}
  .recommendation{{background:rgba(108,99,255,0.2);padding:12px;border-radius:16px;margin-top:15px;font-size:1rem}}
  .break-item{{display:flex;align-items:center;gap:12px;margin:10px 0}}
  .break-label{{width:110px;font-size:0.85rem}}
  .break-bar{{flex:1;height:10px;background:rgba(255,255,255,0.1);border-radius:10px;overflow:hidden}}
  .break-bar div{{height:100%;border-radius:10px}}
  .break-value{{width:45px;font-size:0.85rem;text-align:right}}
  .risk-item{{list-style:none;background:rgba(0,0,0,0.2);border-radius:16px;padding:12px;margin:10px 0;border-right:4px solid}}
  .risk-bar{{height:6px;background:rgba(255,255,255,0.1);border-radius:10px;overflow:hidden;margin:8px 0}}
  .risk-bar div{{height:100%}}
  .risk-reason{{font-size:0.7rem;color:var(--muted);margin-top:5px}}
  .plan-day{{display:flex;align-items:center;gap:12px;padding:12px;background:rgba(0,0,0,0.2);border-radius:16px;margin:8px 0;flex-wrap:wrap}}
  .day-icon{{font-size:1.2rem}}
  .day-name{{font-weight:bold;width:70px}}
  .day-task{{flex:2;font-size:0.9rem}}
  .day-time{{width:80px;font-size:0.8rem;color:var(--muted)}}
  .day-priority{{width:70px;font-size:0.75rem;font-weight:bold}}
  .resource-item{{display:flex;gap:12px;padding:12px;background:rgba(0,0,0,0.2);border-radius:16px;margin:8px 0}}
  .resource-icon{{font-size:1.5rem}}
  .resource-links{{font-size:0.8rem;color:var(--muted);margin-top:5px}}
  .tip-item{{margin:8px 0;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)}}
  .report-buttons{{display:flex;gap:15px;justify-content:center;margin:20px 0;flex-wrap:wrap}}
  .report-btn{{padding:12px 25px;border:none;border-radius:30px;font-weight:bold;cursor:pointer;transition:all 0.3s}}
  .report-btn.html{{background:#10b981;color:white}}
  .report-btn.pdf{{background:#ef4444;color:white}}
  .report-btn:hover{{transform:translateY(-3px);box-shadow:0 5px 15px rgba(0,0,0,0.3)}}
  .back{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
</style>
</head>
<body>
<div class="wrap">
  <div class="report-buttons">
    <button class="report-btn html" onclick="downloadHTML()">📄 دانلود گزارش HTML</button>
    <button class="report-btn pdf" onclick="downloadPDF()">📑 دانلود گزارش PDF</button>
  </div>
  <div id="report-content">
    <div class="card"><h2>📉 نتیجه پیش‌بینی افت نمره</h2><div>کد: {data.get('user_code', 'کاربر مهمان')} | پایه: {data['gradeLevel']}</div></div>
    <div class="card risk-box"><div class="risk-percent">{risk_percent}%</div><div class="risk-level">سطح ریسک: {level_text}</div><div class="advice">{advice}</div><div class="recommendation">💡 توصیه اصلی: {recommendation}</div></div>
    <div class="card"><h3>📊 تحلیل فاکتورهای ریسک</h3>{breakdown_html}</div>
    <div class="card"><h3>📚 درس‌های در معرض خطر</h3><ul style="list-style:none">{risky_html}</ul></div>
    <div class="card"><h3>📅 برنامه ۷ روزه ضد افت</h3><div class="plan-intensity">⚡ شدت: {plan.get('intensity', 'متوسط')} | ⏱️ مجموع ساعات: {plan.get('total_hours', 0)} ساعت | 📊 آزمون هفتگی: {plan.get('weekly_tests', 0)}</div>{plan_html}<div class="hint" style="margin-top:12px">💡 {plan.get('recommendation', '')}</div></div>
    <div class="card"><h3>📚 منابع پیشنهادی</h3>{resources_html}</div>
    <div class="card"><h3>💡 توصیه‌های کلی</h3><ul style="list-style:none">{tips_html}</ul></div>
  </div>
  <a href="/" class="back">← بازگشت به صفحه اصلی</a>
</div>
<script>
function downloadHTML() {{
    const content = document.getElementById('report-content').innerHTML;
    const style = document.querySelector('style').innerHTML;
    const fullHtml = `<!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head><meta charset="UTF-8"><title>گزارش پیش‌بینی افت</title><style>${{style}} body{{padding:20px;background:white;color:black}} .report-buttons{{display:none}} .back{{display:none}}</style></head>
    <body><div class="wrap">${{content}}</div></body></html>`;
    const blob = new Blob([fullHtml], {{type: 'text/html'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'risk_fall_report_{user_code}_{grade_level}.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}}
function downloadPDF() {{
    const element = document.getElementById('report-content');
    const opt = {{
        margin: [0.5, 0.5, 0.5, 0.5],
        filename: 'risk_fall_report_{user_code}_{grade_level}.pdf',
        image: {{ type: 'jpeg', quality: 0.98 }},
        html2canvas: {{ scale: 2, useCORS: true, letterRendering: true }},
        jsPDF: {{ unit: 'in', format: 'a4', orientation: 'portrait' }}
    }};
    html2pdf().set(opt).from(element).save();
}}
</script>
<script>if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light');</script>
</body></html>"""


def render_admin_dashboard():
    from database import get_dashboard_stats
    stats = get_dashboard_stats("admin")
    
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>داشبورد مدیریت مسیرینو</title><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .wrap{{max-width:1200px;margin:auto}}
  .stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-bottom:30px}}
  .stat-card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;text-align:center}}
  .stat-number{{font-size:2.5rem;font-weight:bold;color:#6c63ff}}
  .stat-label{{color:var(--muted);margin-top:10px}}
  .card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;margin-bottom:20px}}
  h2{{margin-bottom:20px}}
  .back{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  .refresh-btn{{background:linear-gradient(90deg,#6c63ff,#ff6584);border:none;padding:10px 20px;border-radius:30px;color:white;cursor:pointer;margin-bottom:20px}}
</style>
</head>
<body>
<div class="wrap">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
    <h1>📊 داشبورد مدیریت مسیرینو</h1>
    <button class="refresh-btn" onclick="location.reload()">🔄 به‌روزرسانی</button>
  </div>
  
  <div class="stats-grid">
    <div class="stat-card"><div class="stat-number">{stats.get('total_users', 0)}</div><div class="stat-label">👥 کاربران فعال</div></div>
    <div class="stat-card"><div class="stat-number">{stats.get('total_conversations', 0)}</div><div class="stat-label">💬 گفتگوها</div></div>
    <div class="stat-card"><div class="stat-number">{stats.get('avg_confidence', 0)}%</div><div class="stat-label">⭐ دقت متوسط پاسخ‌ها</div></div>
    <div class="stat-card"><div class="stat-number">{stats.get('avg_satisfaction', 0)}</div><div class="stat-label">😊 رضایت کاربران</div></div>
    <div class="stat-card"><div class="stat-number">{stats.get('wrong_recommendations', 0)}</div><div class="stat-label">📝 بازخوردهای منفی</div></div>
  </div>
  
  <div class="card"><h2>⚙️ وضعیت سیستم (کامل)</h2>
    <p>✅ سرور فعال است</p>
    <p>✅ جستجوی آنلاین (ویکی‌پدیا + DuckDuckGo) فعال</p>
    <p>✅ دیتابیس SQLite با 10 جدول فعال</p>
    <p>✅ تشخیص احساسات پیشرفته (شادی/ناراحتی/استرس/انگیزه)</p>
    <p>✅ پشتیبانی از ورودی و خروجی صدا (ضبط + خواندن پیام)</p>
    <p>✅ تشخیص خودکار زبان (فارسی/انگلیسی) با ترجمه خودکار</p>
    <p>✅ سلام شخصی‌سازی شده با کد کاربر</p>
    <p>✅ API عمومی در /api/v1/ask و /api/v1/feedback</p>
    <p>✅ تحلیل پیشرفته افت نمره با 12 فاکتور + هشدار خودکار</p>
    <p>✅ انتخاب رشته با 5 معیار (توانایی، علاقه، سبک فکری، آینده، معدل)</p>
    <p>✅ سیستم امتیاز اعتماد (Confidence Score) مبتنی بر بازخورد</p>
    <p>✅ کش برای محاسبات سنگین (LRU Cache)</p>
    <p>✅ پشتیبان‌گیری خودکار از دیتابیس (zip + حذف قدیمی‌ها)</p>
    <p>✅ لاگینگ حرفه‌ای (فایل + کنسول)</p>
    <p>✅ رضایت‌نامه حریم خصوصی (ذخیره کد به جای نام)</p>
    <p>✅ پاکسازی خودکار اطلاعات قدیمی (بیش از ۶ ماه)</p>
    <p>✅ یادگیری از بازخورد منفی کاربران</p>
    <p>✅ مقایسه با کاربران مشابه (API /api/v1/compare)</p>
    <p>✅ تولید گزارش JSON/HTML/TXT</p>
    <p>✅ طراحی واکنش‌گرا با حالت شب/روز</p>
    <p>✅ آزمون شخصیت هالند (45 سوال استاندارد)</p>
    <p>✅ تایمر پومودورو با لیست کارها</p>
    <p>✅ امتیازدهی ستاره‌ای به پاسخ‌های چت بات</p>
  </div>
      html += '''
    <div class="card">
        <h2>🔌 یکپارچگی با سامانه‌های آموزشی (School API Integration)</h2>
        <p>✅ <strong>وضعیت:</strong> حالت شبیه‌سازی (Sandbox Mode)</p>
        <p>🔐 <strong>روش احراز هویت:</strong> OAuth 2.0 / Bearer Token</p>
        <p>📚 <strong>قابلیت‌ها:</strong></p>
        <ul>
            <li>دریافت خودکار اطلاعات دانش‌آموز (نام، مدرسه، پایه، رشته)</li>
            <li>دریافت خودکار نمرات و معدل</li>
            <li>دریافت برنامه هفتگی مدرسه</li>
            <li>همگام‌سازی یکپارچه با دیتابیس مسیرینو</li>
        </ul>
        <p>⚠️ <strong>توجه:</strong> این قابلیت در حالت شبیه‌سازی قرار دارد. برای استفاده واقعی نیاز به مجوز رسمی از وزارت آموزش و پرورش و دریافت API Key معتبر است.</p>
        <p>📖 <strong>مستندات API:</strong> <code>/api/school/documentation</code></p>
    </div>
    '''
    
    return html
  
  <a href="/" class="back">← بازگشت به صفحه اصلی</a>
</div>
<script>if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light');</script>
</body></html>"""


def render_holland_test_page(session_id):
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>آزمون شخصیت شغلی هالند - مسیرینو</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .container{{max-width:800px;margin:auto}}
  .progress-bar{{height:8px;background:rgba(255,255,255,0.2);border-radius:10px;margin-bottom:30px;overflow:hidden}}
  .progress-fill{{height:100%;background:linear-gradient(90deg,#6c63ff,#ff6584);width:0%;transition:width 0.3s}}
  .question-card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:30px;margin-bottom:20px}}
  .question-text{{font-size:1.2rem;margin-bottom:25px}}
  .options{{display:flex;gap:15px;flex-wrap:wrap}}
  .option-btn{{flex:1;padding:12px;border:none;border-radius:20px;cursor:pointer;transition:all 0.3s;font-weight:bold}}
  .option-btn:hover{{transform:translateY(-3px)}}
  .opt-1{{background:#10b981;color:white}} .opt-2{{background:#3b82f6;color:white}} .opt-3{{background:#f59e0b;color:white}} .opt-4{{background:#ef4444;color:white}} .opt-5{{background:#8b5cf6;color:white}}
  .nav-buttons{{display:flex;gap:15px;margin-top:20px}}
  .nav-btn{{padding:12px 25px;border:none;border-radius:30px;cursor:pointer;background:linear-gradient(90deg,#6c63ff,#ff6584);color:white;font-weight:bold}}
  .nav-btn:disabled{{opacity:0.5;cursor:not-allowed}}
  .result-card{{background:var(--card);border-radius:28px;padding:30px;margin-top:20px;text-align:center}}
  .result-score{{font-size:3rem;font-weight:bold;margin:20px 0}}
  .type-desc{{margin:15px 0;line-height:1.6}}
  .back-home{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  .question-counter{{text-align:center;margin-bottom:15px;color:var(--muted)}}
  @media(max-width:768px){{.options{{flex-direction:column}}}}
</style>
</head>
<body>
<div class="container">
  <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
  <div class="question-counter" id="counter">سوال 1 از 45</div>
  <div class="question-card" id="questionCard">
    <div class="question-text" id="questionText"></div>
    <div class="options" id="options"></div>
    <div class="nav-buttons">
      <button class="nav-btn" id="prevBtn" onclick="prevQuestion()" disabled>قبلی</button>
      <button class="nav-btn" id="nextBtn" onclick="nextQuestion()">بعدی</button>
    </div>
  </div>
  <div id="resultContainer" style="display:none"></div>
  <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>
<script>
let sessionId = "{session_id}";
let currentQuestion = 0;
let answers = new Array(45).fill(null);
let testCompleted = false;

const questions = [
  "من کار با ابزار و ماشین‌آلات را دوست دارم.",
  "من فردی عملی و واقع‌گرا هستم.",
  "من تعمیر وسایل برقی و مکانیکی را بلدم.",
  "من از کارهای فیزیکی و بیرون از دفتر لذت می‌برم.",
  "من رانندگی و کار با ماشین‌آلات را دوست دارم.",
  "من به طبیعت و حیوانات علاقه دارم.",
  "من از کارهای علمی و تحقیقاتی لذت می‌برم.",
  "من حل مسائل ریاضی و علمی را دوست دارم.",
  "من به کشف و یادگیری چیزهای جدید علاقه دارم.",
  "من فردی تحلیلی و منطقی هستم.",
  "من کار در آزمایشگاه را دوست دارم.",
  "من به مطالعه کتاب‌های علمی و تخصصی علاقه دارم.",
  "من هنرمند و خلاق هستم.",
  "من طراحی و نقاشی را دوست دارم.",
  "من موسیقی یا تئاتر را دوست دارم.",
  "من نوشتن داستان یا شعر را دوست دارم.",
  "من از کارهای هنری و خلاقانه لذت می‌برم.",
  "من ایده‌های جدید و نوآورانه دارم.",
  "من به کمک به دیگران علاقه دارم.",
  "من تدریس و آموزش را دوست دارم.",
  "من مشاوره و راهنمایی دیگران را دوست دارم.",
  "من کار در حوزه سلامت و پزشکی را دوست دارم.",
  "من از ارتباط با مردم لذت می‌برم.",
  "من کار تیمی و گروهی را ترجیح می‌دهم.",
  "من رهبری و مدیریت تیم را دوست دارم.",
  "من فروش و مذاکره را دوست دارم.",
  "من به کسب‌وکار و کارآفرینی علاقه دارم.",
  "من سخنرانی در جمع را دوست دارم.",
  "من متقاعد کردن دیگران را بلدم.",
  "من ریسک‌پذیر و جسور هستم.",
  "من سازماندهی و برنامه‌ریزی را دوست دارم.",
  "من کار با کامپیوتر و نرم‌افزار را دوست دارم.",
  "من به امور مالی و حسابداری علاقه دارم.",
  "من جزئیات را دقیق رعایت می‌کنم.",
  "من بایگانی و نظم‌دهی اطلاعات را دوست دارم.",
  "من از کارهای دفتری و اداری لذت می‌برم.",
  "من کار در بانک یا موسسه مالی را دوست دارم.",
  "من قوانین و مقررات را دقیق رعایت می‌کنم.",
  "من تحقیق و جستجوی اطلاعات را دوست دارم.",
  "من سفر و ماجراجویی را دوست دارم.",
  "من ورزش و فعالیت بدنی را دوست دارم.",
  "من یادگیری زبان خارجی را دوست دارم.",
  "من کارآفرینی و راه‌اندازی کسب‌وکار را دوست دارم.",
  "من به سیاست و مسائل اجتماعی علاقه دارم.",
  "من برنامه‌نویسی و کدنویسی را دوست دارم."
];

const types = [
  {{name:"واقع‌گرا (Realistic)", icon:"🔧", desc:"عملی، فنی، مکانیکی، ورزشی - مناسب برای مهندسی، تعمیرات، کشاورزی"}},
  {{name:"پژوهشی (Investigative)", icon:"🔬", desc:"تحلیلی، علمی، پژوهشی - مناسب برای پزشکی، داروسازی، تحقیق، فناوری"}},
  {{name:"هنری (Artistic)", icon:"🎨", desc:"خلاق، ایده‌پرداز، احساسی - مناسب برای هنر، طراحی، موسیقی، ادبیات"}},
  {{name:"اجتماعی (Social)", icon:"🤝", desc:"یاری‌رسان، آموزشی، مشاور - مناسب برای معلمی، روانشناسی، مددکاری"}},
  {{name:"متهور (Enterprising)", icon:"🚀", desc:"رهبر، فروشنده، مدیر - مناسب برای مدیریت، حقوق، فروش، سیاست"}},
  {{name:"سازمانی (Conventional)", icon:"📊", desc:"سازمان‌یافته، دقیق، اداری - مناسب برای حسابداری، امور مالی، مدیریت"}}
];

function updateProgress() {{
  const percent = ((currentQuestion + 1) / 45) * 100;
  document.getElementById('progressFill').style.width = percent + '%';
  document.getElementById('counter').innerText = "سوال " + (currentQuestion + 1) + " از 45";
}}

function renderQuestion() {{
  if (testCompleted) return;
  const q = questions[currentQuestion];
  const saved = answers[currentQuestion];
  document.getElementById('questionText').innerText = q;
  const optionsDiv = document.getElementById('options');
  optionsDiv.innerHTML = '';
  for(let i = 1; i <= 5; i++) {{
    const labels = ["خیلی کم", "کم", "متوسط", "زیاد", "خیلی زیاد"];
    const btn = document.createElement('button');
    btn.className = "option-btn opt-" + i;
    btn.innerText = i + " - " + labels[i-1];
    btn.onclick = (function(idx) {{
      return function() {{
        answers[currentQuestion] = idx;
        const btns = document.querySelectorAll('.option-btn');
        for(let b of btns) b.style.opacity = '0.6';
        this.style.opacity = '1';
        setTimeout(() => nextQuestion(), 200);
      }};
    }})(i);
    if(saved === i) {{
      btn.style.opacity = '1';
      btn.style.border = '3px solid white';
    }} else {{
      btn.style.opacity = '0.6';
    }}
    optionsDiv.appendChild(btn);
  }}
  document.getElementById('prevBtn').disabled = currentQuestion === 0;
  updateProgress();
}}

function nextQuestion() {{
  if(answers[currentQuestion] === null) {{
    alert('لطفاً یک گزینه را انتخاب کنید');
    return;
  }}
  if(currentQuestion < 44) {{
    currentQuestion++;
    renderQuestion();
  }} else {{
    calculateResults();
  }}
}}

function prevQuestion() {{
  if(currentQuestion > 0) {{
    currentQuestion--;
    renderQuestion();
  }}
}}

function calculateResults() {{
  const scores = [0,0,0,0,0,0];
  const typeRanges = [[0,7], [8,14], [15,21], [22,28], [29,35], [36,44]];
  for(let i = 0; i < 45; i++) {{
    for(let t = 0; t < 6; t++) {{
      if(i >= typeRanges[t][0] && i <= typeRanges[t][1]) {{
        scores[t] += (answers[i] || 3);
        break;
      }}
    }}
  }}
  const maxScore = Math.max(...scores);
  const primaryIndex = scores.indexOf(maxScore);
  const primaryType = types[primaryIndex];
  const percentages = scores.map(function(s) {{ return Math.round((s / 45) * 100); }});
  
  let recommendations = "";
  if(primaryIndex === 0) recommendations = "🔧 مهندسی مکانیک، برق، عمران، معماری، تعمیرات، کشاورزی، ورزش";
  else if(primaryIndex === 1) recommendations = "🔬 پزشکی، دندانپزشکی، داروسازی، بیوتکنولوژی، پژوهش، داده‌کاوی";
  else if(primaryIndex === 2) recommendations = "🎨 گرافیک، انیمیشن، طراحی داخلی، موسیقی، عکاسی، نویسندگی";
  else if(primaryIndex === 3) recommendations = "🤝 روانشناسی، مشاوره، مددکاری، معلمی، پرستاری، مدیریت منابع انسانی";
  else if(primaryIndex === 4) recommendations = "🚀 مدیریت بازرگانی، حقوق، فروش، کارآفرینی، بازاریابی، سیاست";
  else recommendations = "📊 حسابداری، امور مالی، مدیریت اداری، امور بانکی، برنامه‌ریزی";
  
  let typesHtml = "";
  for(let idx = 0; idx < types.length; idx++) {{
    const t = types[idx];
    const percent = percentages[idx];
    typesHtml += '<div style="margin:8px 0"><span style="display:inline-block;width:140px">' + t.icon + ' ' + t.name + '</span> <div style="display:inline-block;width:200px;height:20px;background:rgba(255,255,255,0.2);border-radius:10px;overflow:hidden;vertical-align:middle"><div style="width:' + percent + '%;height:100%;background:linear-gradient(90deg,#6c63ff,#ff6584)"></div></div> <span style="margin-left:10px">' + percent + '%</span></div>';
  }}
  
  const resultHTML = '<div class="result-card">' +
    '<h2>📊 نتیجه آزمون هالند</h2>' +
    '<div class="result-score">' + primaryType.icon + ' ' + primaryType.name + '</div>' +
    '<div class="type-desc">' + primaryType.desc + '</div>' +
    '<div style="margin:20px 0"><strong>💼 پیشنهاد شغلی:</strong> ' + recommendations + '</div>' +
    '<div style="margin:15px 0"><strong>📈 امتیازات شما در هر تیپ:</strong></div>' +
    typesHtml +
    '<button class="nav-btn" onclick="location.reload()" style="margin-top:20px">🔄 شروع مجدد آزمون</button>' +
    '</div>';
  
  document.getElementById('questionCard').style.display = 'none';
  document.getElementById('resultContainer').style.display = 'block';
  document.getElementById('resultContainer').innerHTML = resultHTML;
  testCompleted = true;
  
  fetch('/save-holland-test', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{session_id: sessionId, scores: scores, primary_type: primaryType.name, percentages: percentages}})
  }});
}}

renderQuestion();
if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light');
</script>
</body></html>"""


def render_pomodoro_page(session_id):
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>تایمر پومودورو - مسیرینو</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);min-height:100vh;display:flex;justify-content:center;align-items:center}}
  .pomodoro-container{{background:var(--card);backdrop-filter:blur(20px);border-radius:60px;padding:50px;text-align:center;max-width:500px;width:90%}}
  .timer{{font-size:6rem;font-weight:bold;font-family:monospace;margin:30px 0;letter-spacing:5px}}
  .mode{{font-size:1.3rem;margin-bottom:15px;color:var(--muted)}}
  .controls{{display:flex;gap:15px;justify-content:center;margin:25px 0;flex-wrap:wrap}}
  .ctrl-btn{{padding:12px 25px;border:none;border-radius:40px;font-weight:bold;cursor:pointer;transition:all 0.3s}}
  .ctrl-btn:hover{{transform:scale(1.05)}}
  .start{{background:#10b981;color:white}}
  .pause{{background:#f59e0b;color:white}}
  .reset{{background:#ef4444;color:white}}
  .session-count{{margin-top:25px;font-size:1rem}}
  .task-input{{margin:20px 0;display:flex;gap:10px}}
  .task-input input{{flex:1;padding:12px;border-radius:30px;border:none;background:rgba(255,255,255,0.2);color:var(--text);outline:none}}
  .task-input button{{padding:12px 20px;border-radius:30px;border:none;background:linear-gradient(90deg,#6c63ff,#ff6584);color:white;cursor:pointer}}
  .task-list{{margin-top:20px;text-align:right}}
  .task-item{{display:flex;justify-content:space-between;align-items:center;padding:10px;background:rgba(0,0,0,0.2);border-radius:20px;margin:8px 0}}
  .task-item.completed{{opacity:0.6;text-decoration:line-through}}
  .delete-task{{background:none;border:none;color:#ef4444;cursor:pointer;font-size:1.2rem}}
  .back-home{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  @media(max-width:500px){{.timer{{font-size:3.5rem}}.pomodoro-container{{padding:25px}}}}
</style>
</head>
<body>
<div class="pomodoro-container">
  <h2>🍅 تایمر پومودورو</h2>
  <div class="mode" id="modeLabel">⏰ زمان مطالعه</div>
  <div class="timer" id="timer">25:00</div>
  <div class="controls">
    <button class="ctrl-btn start" onclick="startTimer()">▶ شروع</button>
    <button class="ctrl-btn pause" onclick="pauseTimer()">⏸ توقف</button>
    <button class="ctrl-btn reset" onclick="resetTimer()">🔄 ریست</button>
  </div>
  <div class="session-count" id="sessionCount">✅ پومودوروهای امروز: 0</div>
  
  <div class="task-input">
    <input type="text" id="taskInput" placeholder="مثال: ریاضی فصل ۱">
    <button onclick="addTask()">➕ افزودن کار</button>
  </div>
  <div class="task-list" id="taskList"></div>
  
  <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>
<script>
let sessionId = "{session_id}";
let timeLeft = 25 * 60;
let timerId = null;
let isWorkMode = true;
let pomodoroCount = 0;
let tasks = JSON.parse(localStorage.getItem("pomodoro_tasks_" + sessionId) || '[]');

function updateDisplay() {{
  const mins = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  document.getElementById('timer').innerText = (mins.toString().padStart(2,'0')) + ":" + (secs.toString().padStart(2,'0'));
  document.title = (isWorkMode ? '🍅 مطالعه' : '☕ استراحت') + " " + mins + ":" + (secs.toString().padStart(2,'0'));
}}

function updateModeLabel() {{
  const label = document.getElementById('modeLabel');
  if(isWorkMode) {{
    label.innerHTML = '📚 زمان مطالعه (۲۵ دقیقه)';
    label.style.color = '#10b981';
  }} else {{
    label.innerHTML = '☕ زمان استراحت (۵ دقیقه)';
    label.style.color = '#f59e0b';
  }}
}}

function startTimer() {{
  if(timerId) return;
  timerId = setInterval(() => {{
    if(timeLeft <= 0) {{
      clearInterval(timerId);
      timerId = null;
      if(isWorkMode) {{
        pomodoroCount++;
        document.getElementById('sessionCount').innerHTML = "✅ پومودوروهای امروز: " + pomodoroCount;
        try {{
          const audio = new Audio('data:audio/wav;base64,U3RlYWx0aCBiZWxs');
          audio.play();
        }} catch(e) {{}}
        alert('🎉 تبریک! یک پومودورو کامل شد. وقت استراحت ۵ دقیقه‌ای!');
        fetch('/save-pomodoro', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{session_id: sessionId, completed_sessions: 1}})
        }});
        isWorkMode = false;
        timeLeft = 5 * 60;
      }} else {{
        alert('⏰ استراحت تمام شد! وقت مطالعه است.');
        isWorkMode = true;
        timeLeft = 25 * 60;
      }}
      updateModeLabel();
      updateDisplay();
      startTimer();
    }} else {{
      timeLeft--;
      updateDisplay();
    }}
  }}, 1000);
}}

function pauseTimer() {{
  if(timerId) {{
    clearInterval(timerId);
    timerId = null;
  }}
}}

function resetTimer() {{
  pauseTimer();
  isWorkMode = true;
  timeLeft = 25 * 60;
  updateModeLabel();
  updateDisplay();
}}

function addTask() {{
  const input = document.getElementById('taskInput');
  const taskName = input.value.trim();
  if(!taskName) return;
  tasks.push({{name: taskName, completed: false, createdAt: new Date().toISOString()}});
  saveTasks();
  input.value = '';
  renderTasks();
}}

function toggleTask(index) {{
  tasks[index].completed = !tasks[index].completed;
  saveTasks();
  renderTasks();
}}

function deleteTask(index) {{
  tasks.splice(index, 1);
  saveTasks();
  renderTasks();
}}

function saveTasks() {{
  localStorage.setItem("pomodoro_tasks_" + sessionId, JSON.stringify(tasks));
  fetch('/save-tasks', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{session_id: sessionId, tasks: tasks}})
  }});
}}

function renderTasks() {{
  const container = document.getElementById('taskList');
  if(tasks.length === 0) {{
    container.innerHTML = '<div style="color:var(--muted);text-align:center">📝 هنوز کاری اضافه نکرده‌اید</div>';
    return;
  }}
  let html = "";
  for(let i = 0; i < tasks.length; i++) {{
    const task = tasks[i];
    html += '<div class="task-item ' + (task.completed ? 'completed' : '') + '">';
    html += '<span onclick="toggleTask(' + i + ')" style="flex:1;cursor:pointer">' + (task.completed ? '✅' : '⬜') + ' ' + escapeHtml(task.name) + '</span>';
    html += '<button class="delete-task" onclick="deleteTask(' + i + ')">🗑️</button>';
    html += '</div>';
  }}
  container.innerHTML = html;
}}

function escapeHtml(text) {{
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}}

renderTasks();
updateDisplay();
updateModeLabel();

if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light');
</script>
</body></html>"""


def render_smart_goals_page(session_id):
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>اهداف SMART - مسیرینو</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .container{{max-width:1000px;margin:auto}}
  .glass-card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;margin-bottom:20px}}
  .smart-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px}}
  .smart-title{{font-size:1.8rem;background:linear-gradient(135deg,#fff,#6c63ff);background-clip:text;-webkit-background-clip:text;color:transparent}}
  .btn{{padding:10px 20px;border:none;border-radius:30px;cursor:pointer;font-weight:bold;transition:all 0.3s}}
  .btn-primary{{background:linear-gradient(90deg,#6c63ff,#ff6584);color:white}}
  .btn-success{{background:#10b981;color:white}}
  .btn-warning{{background:#f59e0b;color:white}}
  .btn-danger{{background:#ef4444;color:white}}
  .btn-sm{{padding:5px 12px;font-size:0.8rem}}
  .form-group{{margin-bottom:15px}}
  .form-group label{{display:block;margin-bottom:8px;color:var(--muted);font-weight:bold}}
  .form-group input,.form-group textarea,.form-group select{{width:100%;padding:12px;border-radius:16px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.2);color:var(--text);outline:none}}
  .form-group input:focus{{border-color:#6c63ff}}
  .row{{display:grid;grid-template-columns:1fr 1fr;gap:15px}}
  .goal-card{{background:rgba(0,0,0,0.2);border-radius:20px;padding:20px;margin-bottom:15px;transition:all 0.3s}}
  .goal-card:hover{{transform:translateY(-3px);background:rgba(0,0,0,0.3)}}
  .goal-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap}}
  .goal-title{{font-size:1.2rem;font-weight:bold}}
  .goal-status{{padding:4px 12px;border-radius:20px;font-size:0.7rem}}
  .status-active{{background:#10b981;color:white}}
  .status-completed{{background:#6c63ff;color:white}}
  .status-archived{{background:#6c757d;color:white}}
  .priority-high{{border-right:4px solid #ef4444}}
  .priority-medium{{border-right:4px solid #f59e0b}}
  .priority-low{{border-right:4px solid #10b981}}
  .progress-bar{{height:8px;background:rgba(255,255,255,0.1);border-radius:10px;overflow:hidden;margin:10px 0}}
  .progress-fill{{height:100%;background:linear-gradient(90deg,#6c63ff,#ff6584);border-radius:10px;transition:width 0.3s}}
  .goal-details{{font-size:0.8rem;color:var(--muted);margin:10px 0}}
  .goal-details span{{display:inline-block;margin-left:15px}}
  .deadline-warning{{color:#ef4444;font-weight:bold}}
  .modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:1000;justify-content:center;align-items:center}}
  .modal-content{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:30px;max-width:600px;width:90%;max-height:80vh;overflow-y:auto}}
  .modal-header{{display:flex;justify-content:space-between;margin-bottom:20px}}
  .close{{cursor:pointer;font-size:1.5rem}}
  .stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin-bottom:20px}}
  .stat-card{{text-align:center;padding:15px;background:rgba(0,0,0,0.2);border-radius:20px}}
  .stat-number{{font-size:1.8rem;font-weight:bold;color:#6c63ff}}
  .stat-label{{font-size:0.7rem;color:var(--muted)}}
  .filter-buttons{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px}}
  .filter-btn{{padding:6px 15px;border-radius:20px;background:rgba(255,255,255,0.1);cursor:pointer;transition:all 0.3s}}
  .filter-btn.active{{background:linear-gradient(90deg,#6c63ff,#ff6584)}}
  .back-home{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  @media(max-width:768px){{.row{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="container">
  <div class="glass-card">
    <div class="smart-header">
      <h1 class="smart-title">🎯 سیستم اهداف SMART</h1>
      <button class="btn btn-primary" onclick="openNewGoalModal()">➕ هدف جدید</button>
    </div>
    
    <div class="stats-grid" id="statsGrid"></div>
    
    <div class="filter-buttons">
      <button class="filter-btn active" onclick="filterGoals('all')">همه</button>
      <button class="filter-btn" onclick="filterGoals('active')">فعال</button>
      <button class="filter-btn" onclick="filterGoals('completed')">تکمیل شده</button>
      <button class="filter-btn" onclick="filterGoals('high')">اولویت بالا</button>
      <button class="filter-btn" onclick="filterGoals('medium')">اولویت متوسط</button>
      <button class="filter-btn" onclick="filterGoals('low')">اولویت پایین</button>
    </div>
    
    <div id="goalsList"></div>
  </div>
  <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<div id="goalModal" class="modal">
  <div class="modal-content">
    <div class="modal-header">
      <h3>🎯 هدف SMART جدید</h3>
      <span class="close" onclick="closeModal()">&times;</span>
    </div>
    <form id="goalForm">
      <div class="form-group">
        <label>📝 عنوان هدف (S - Specific)</label>
        <input type="text" id="goalTitle" required placeholder="مثال: یادگیری کامل فصل 1 ریاضی دهم">
      </div>
      <div class="form-group">
        <label>📏 معیار اندازه‌گیری (M - Measurable)</label>
        <textarea id="goalMeasurable" rows="2" placeholder="مثال: حل 100 تست با نمره 80%"></textarea>
      </div>
      <div class="form-group">
        <label>🎯 آیا قابل دستیابی است؟ (A - Achievable)</label>
        <textarea id="goalAchievable" rows="2" placeholder="چرا این هدف قابل دستیابی است؟"></textarea>
      </div>
      <div class="form-group">
        <label>🔗 چرا این هدف برای تو مهم است؟ (R - Relevant)</label>
        <textarea id="goalRelevant" rows="2" placeholder="این هدف چطور به موفقیت تو کمک می‌کند؟"></textarea>
      </div>
      <div class="row">
        <div class="form-group">
          <label>⏰ ضرب‌الاجل (T - Time-bound)</label>
          <input type="date" id="goalDeadline">
        </div>
        <div class="form-group">
          <label>🏷️ اولویت</label>
          <select id="goalPriority">
            <option value="high">🔴 بالا</option>
            <option value="medium" selected>🟡 متوسط</option>
            <option value="low">🟢 پایین</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label>📂 دسته‌بندی</label>
        <select id="goalCategory">
          <option value="تحصیلی">📚 تحصیلی</option>
          <option value="کنکور">🎯 کنکور</option>
          <option value="مهارتی">💡 مهارتی</option>
          <option value="زبانی">🌍 زبان</option>
          <option value="شخصی">🧘 شخصی</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary" style="width:100%">ایجاد هدف 🚀</button>
    </form>
  </div>
</div>

<div id="progressModal" class="modal">
  <div class="modal-content">
    <div class="modal-header">
      <h3>📈 به‌روزرسانی پیشرفت</h3>
      <span class="close" onclick="closeProgressModal()">&times;</span>
    </div>
    <div id="progressGoalTitle"></div>
    <div class="form-group">
      <label>پیشرفت فعلی (0-100%)</label>
      <input type="range" id="progressValue" min="0" max="100" step="5" value="0" oninput="updateProgressPercent(this.value)">
      <div style="text-align:center;margin-top:10px"><span id="progressPercent">0</span>%</div>
    </div>
    <div class="form-group">
      <label>یادداشت پیشرفت</label>
      <textarea id="progressNote" rows="3" placeholder="چه کارهایی انجام دادی؟"></textarea>
    </div>
    <button class="btn btn-primary" style="width:100%" onclick="updateGoalProgress()">ذخیره پیشرفت</button>
  </div>
</div>

<script>
let sessionId = "{session_id}";
let currentFilter = "all";
let goals = [];

function toggleTheme() {{
    const html = document.documentElement;
    if (html.getAttribute('data-theme') === 'light') {{
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'dark');
    }} else {{
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }}
}}
if (localStorage.getItem('theme') === 'light') {{
    document.documentElement.setAttribute('data-theme', 'light');
}}

async function loadGoals() {{
    const res = await fetch('/get-goals?session_id=' + sessionId);
    const data = await res.json();
    goals = data.goals || [];
    renderStats();
    renderGoals();
}}

function renderStats() {{
    const total = goals.length;
    const completed = goals.filter(g => g.status === 'completed').length;
    const active = goals.filter(g => g.status === 'active').length;
    const avgProgress = goals.length > 0 ? Math.round(goals.reduce((sum, g) => sum + (g.progress || 0), 0) / goals.length) : 0;
    const expired = goals.filter(g => g.deadline && new Date(g.deadline) < new Date() && g.status !== 'completed').length;
    
    document.getElementById('statsGrid').innerHTML = `
        <div class="stat-card"><div class="stat-number">${{total}}</div><div class="stat-label">کل اهداف</div></div>
        <div class="stat-card"><div class="stat-number">${{active}}</div><div class="stat-label">در حال انجام</div></div>
        <div class="stat-card"><div class="stat-number">${{completed}}</div><div class="stat-label">تکمیل شده</div></div>
        <div class="stat-card"><div class="stat-number">${{avgProgress}}%</div><div class="stat-label">میانگین پیشرفت</div></div>
        ${{expired > 0 ? `<div class="stat-card"><div class="stat-number" style="color:#ef4444">${{expired}}</div><div class="stat-label">⏰ مهلت گذشته</div></div>` : ''}}
    `;
}}

function renderGoals() {{
    let filtered = [...goals];
    if (currentFilter === 'active') filtered = filtered.filter(g => g.status === 'active');
    else if (currentFilter === 'completed') filtered = filtered.filter(g => g.status === 'completed');
    else if (currentFilter === 'high') filtered = filtered.filter(g => g.priority === 'high');
    else if (currentFilter === 'medium') filtered = filtered.filter(g => g.priority === 'medium');
    else if (currentFilter === 'low') filtered = filtered.filter(g => g.priority === 'low');
    
    if (filtered.length === 0) {{
        document.getElementById('goalsList').innerHTML = '<div style="text-align:center;padding:40px">🎯 هنوز هدفی تعیین نکرده‌ای. دکمه "هدف جدید" رو بزن و شروع کن!</div>';
        return;
    }}
    
    document.getElementById('goalsList').innerHTML = filtered.map(goal => {{
        const isExpired = goal.deadline && new Date(goal.deadline) < new Date() && goal.status !== 'completed';
        const daysLeft = goal.deadline ? Math.ceil((new Date(goal.deadline) - new Date()) / (1000 * 60 * 60 * 24)) : null;
        return `
            <div class="goal-card priority-${{goal.priority}}">
                <div class="goal-header">
                    <span class="goal-title">🎯 ${{escapeHtml(goal.title)}}</span>
                    <div>
                        <span class="goal-status status-${{goal.status === 'completed' ? 'completed' : 'active'}}">${{goal.status === 'completed' ? '✅ تکمیل شده' : '🟢 در حال انجام'}}</span>
                        <button class="btn btn-sm btn-primary" onclick="openProgressModal(${{goal.id}}, '${{escapeHtml(goal.title)}}', ${{goal.progress || 0}})">📈 به‌روزرسانی</button>
                        <button class="btn btn-sm btn-warning" onclick="editGoal(${{goal.id}})">✏️</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteGoal(${{goal.id}})">🗑️</button>
                    </div>
                </div>
                <div class="progress-bar"><div class="progress-fill" style="width:${{goal.progress || 0}}%"></div></div>
                <div class="goal-details">
                    <span>📊 پیشرفت: ${{goal.progress || 0}}%</span>
                    <span>🏷️ اولویت: ${{goal.priority === 'high' ? '🔴 بالا' : goal.priority === 'medium' ? '🟡 متوسط' : '🟢 پایین'}}</span>
                    <span>📂 دسته: ${{goal.category || 'عمومی'}}</span>
                    ${{daysLeft !== null ? `<span>⏰ ${{daysLeft >= 0 ? daysLeft + ' روز مونده' : '<span class="deadline-warning">⏰ مهلت گذشته!</span>'}}</span>` : ''}}
                </div>
                <div class="goal-details">
                    <strong>📏 معیار:</strong> ${{escapeHtml(goal.measurable || '-')}}<br>
                    <strong>🎯 قابل دستیابی:</strong> ${{escapeHtml(goal.achievable || '-')}}<br>
                    <strong>🔗 مرتبط با:</strong> ${{escapeHtml(goal.relevant || '-')}}
                </div>
            </div>
        `;
    }}).join('');
}}

function escapeHtml(text) {{
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}}

function filterGoals(filter) {{
    currentFilter = filter;
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    renderGoals();
}}

function openNewGoalModal() {{
    document.getElementById('goalForm').reset();
    document.getElementById('goalModal').style.display = 'flex';
}}

function closeModal() {{
    document.getElementById('goalModal').style.display = 'none';
}}

function openProgressModal(goalId, title, currentProgress) {{
    document.getElementById('progressModal').style.display = 'flex';
    document.getElementById('progressGoalTitle').innerHTML = `<h4>${{escapeHtml(title)}}</h4>`;
    document.getElementById('progressValue').value = currentProgress;
    document.getElementById('progressPercent').innerText = currentProgress;
    window.currentGoalId = goalId;
}}

function closeProgressModal() {{
    document.getElementById('progressModal').style.display = 'none';
}}

function updateProgressPercent(val) {{
    document.getElementById('progressPercent').innerText = val;
}}

async function updateGoalProgress() {{
    const progress = parseInt(document.getElementById('progressValue').value);
    const note = document.getElementById('progressNote').value;
    
    const res = await fetch('/update-goal-progress', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{session_id: sessionId, goal_id: window.currentGoalId, progress: progress, note: note}})
    }});
    const data = await res.json();
    if (data.status === 'ok') {{
        closeProgressModal();
        loadGoals();
        document.getElementById('progressNote').value = '';
    }}
}}

async function deleteGoal(goalId) {{
    if (confirm('آیا مطمئنی می‌خوای این هدف رو حذف کنی؟')) {{
        const res = await fetch('/delete-goal', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{session_id: sessionId, goal_id: goalId}})
        }});
        if (res.ok) loadGoals();
    }}
}}

async function editGoal(goalId) {{
    const goal = goals.find(g => g.id === goalId);
    if (!goal) return;
    
    document.getElementById('goalTitle').value = goal.title;
    document.getElementById('goalMeasurable').value = goal.measurable || '';
    document.getElementById('goalAchievable').value = goal.achievable || '';
    document.getElementById('goalRelevant').value = goal.relevant || '';
    document.getElementById('goalDeadline').value = goal.deadline || '';
    document.getElementById('goalPriority').value = goal.priority || 'medium';
    document.getElementById('goalCategory').value = goal.category || 'تحصیلی';
    window.editGoalId = goalId;
    document.getElementById('goalModal').style.display = 'flex';
}}

document.getElementById('goalForm').addEventListener('submit', async (e) => {{
    e.preventDefault();
    const goalData = {{
        session_id: sessionId,
        title: document.getElementById('goalTitle').value,
        measurable: document.getElementById('goalMeasurable').value,
        achievable: document.getElementById('goalAchievable').value,
        relevant: document.getElementById('goalRelevant').value,
        deadline: document.getElementById('goalDeadline').value,
        priority: document.getElementById('goalPriority').value,
        category: document.getElementById('goalCategory').value
    }};
    if (window.editGoalId) {{
        goalData.goal_id = window.editGoalId;
        await fetch('/update-goal', {{method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: JSON.stringify(goalData)}});
        delete window.editGoalId;
    }} else {{
        await fetch('/create-goal', {{method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: JSON.stringify(goalData)}});
    }}
    closeModal();
    loadGoals();
}});

loadGoals();
</script>
</body></html>"""


def render_exam_questions_page(session_id):
    # ساخت CSS به صورت تکه تکه برای جلوگیری از تشخیص Pylance
    css_part1 = "body{font-family:Tahoma;padding:30px;direction:rtl}"
    css_part2 = "h1{color:#6c63ff;text-align:center}"
    css_part3 = ".info-box{background:#f0f0f0;padding:15px;border-radius:10px;margin:20px 0;text-align:center}"
    css_part4 = ".question-item{margin-bottom:30px;padding:15px;border-bottom:1px solid #eee}"
    css_part5 = ".question-text{font-weight:bold}"
    css_part6 = ".options{margin-right:25px;margin-top:8px}"
    css_part7 = ".option{margin:5px 0}"
    css_part8 = ".answer-line{margin-top:12px;padding:10px;background:#f9f9f9;border-radius:8px;border:1px dashed #ccc}"
    css_part9 = ".footer{text-align:center;margin-top:40px;padding:15px;border-top:1px solid #ddd;font-size:11px;color:#999}"
    pdf_css = css_part1 + css_part2 + css_part3 + css_part4 + css_part5 + css_part6 + css_part7 + css_part8 + css_part9
    
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>تولید سوال امتحانی - مسیرینو</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .container{{max-width:1000px;margin:auto}}
  .glass-card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;margin-bottom:20px}}
  .row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:15px}}
  .form-group{{margin-bottom:15px}}
  .form-group label{{display:block;margin-bottom:8px;color:var(--muted);font-weight:bold}}
  select,input{{width:100%;padding:12px;border-radius:16px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.2);color:var(--text);outline:none}}
  .btn{{padding:12px 25px;border:none;border-radius:30px;cursor:pointer;font-weight:bold;transition:all 0.3s}}
  .btn-primary{{background:linear-gradient(90deg,#6c63ff,#ff6584);color:white}}
  .btn-success{{background:#10b981;color:white}}
  .btn-warning{{background:#f59e0b;color:white}}
  .question-item{{background:rgba(0,0,0,0.2);border-radius:20px;padding:20px;margin-bottom:15px}}
  .question-text{{font-size:1.1rem;margin-bottom:12px}}
  .options{{margin:10px 0;padding-right:20px}}
  .option{{margin:8px 0;display:flex;align-items:center;gap:10px}}
  .option input{{width:auto;margin-left:10px}}
  .answer-input{{width:100%;padding:10px;border-radius:16px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.2);color:var(--text);margin-top:10px}}
  .show-answer{{background:rgba(108,99,255,0.3);padding:10px;border-radius:16px;margin-top:10px;display:none}}
  .score-box{{text-align:center;padding:20px;background:rgba(0,0,0,0.3);border-radius:20px;margin:20px 0}}
  .score-value{{font-size:2.5rem;font-weight:bold;color:#6c63ff}}
  .back-home{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  @media(max-width:600px){{.row{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="container">
  <div class="glass-card">
    <h2>📝 تولید سوال امتحانی هوشمند</h2>
    <p style="margin-bottom:20px;color:var(--muted)">بر اساس درس، مقطع و سطح دشواری، سوالات تستی و تشریحی تولید کنید</p>
    
    <div class="row">
      <div class="form-group">
        <label>📚 درس</label>
        <select id="subject">
          <option value="ریاضی">ریاضی</option>
          <option value="علوم">علوم</option>
          <option value="فیزیک">فیزیک</option>
          <option value="زیست">زیست</option>
          <option value="شیمی">شیمی</option>
          <option value="علوم تجربی">علوم تجربی</option>
        </select>
      </div>
      <div class="form-group">
        <label>🎓 مقطع</label>
        <select id="gradeLevel">
          <option value="ابتدایی">ابتدایی</option>
          <option value="هفتم-نهم">هفتم-نهم</option>
          <option value="دهم-دوازدهم">دهم-دوازدهم</option>
        </select>
      </div>
      <div class="form-group">
        <label>⚡ سطح دشواری</label>
        <select id="difficulty">
          <option value="آسان">آسان</option>
          <option value="متوسط">متوسط</option>
          <option value="سخت">سخت</option>
        </select>
      </div>
      <div class="form-group">
        <label>📋 نوع سوال</label>
        <select id="questionType">
          <option value="test">فقط تستی</option>
          <option value="descriptive">فقط تشریحی</option>
          <option value="both">تستی + تشریحی</option>
        </select>
      </div>
      <div class="form-group">
        <label>🔢 تعداد سوالات</label>
        <input type="number" id="count" min="1" max="20" value="5">
      </div>
    </div>
    
    <button class="btn btn-primary" onclick="generateQuestions()" style="width:100%;margin-top:10px">🎲 تولید سوالات</button>
  </div>
  
  <div id="questionsContainer"></div>
  <div id="resultContainer" style="display:none" class="glass-card"></div>
  
  <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<script>
let sessionId = "{session_id}";
let currentQuestions = [];
const pdfCss = `{pdf_css}`;

function toggleTheme() {{
    const html = document.documentElement;
    if (html.getAttribute('data-theme') === 'light') {{
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'dark');
    }} else {{
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }}
}}
if (localStorage.getItem('theme') === 'light') {{
    document.documentElement.setAttribute('data-theme', 'light');
}}

async function generateQuestions() {{
    const subject = document.getElementById('subject').value;
    const gradeLevel = document.getElementById('gradeLevel').value;
    const difficulty = document.getElementById('difficulty').value;
    const questionType = document.getElementById('questionType').value;
    const count = parseInt(document.getElementById('count').value);
    
    document.getElementById('questionsContainer').innerHTML = '<div class="glass-card" style="text-align:center;padding:40px">⏳ در حال تولید سوالات...</div>';
    document.getElementById('resultContainer').style.display = 'none';
    
    const res = await fetch('/generate-questions', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{
            session_id: sessionId,
            subject: subject,
            grade_level: gradeLevel,
            difficulty: difficulty,
            question_type: questionType,
            count: count
        }})
    }});
    const data = await res.json();
    currentQuestions = data.questions;
    renderQuestions(currentQuestions);
}}

function renderQuestions(questions) {{
    if (!questions || questions.length === 0) {{
        document.getElementById('questionsContainer').innerHTML = '<div class="glass-card" style="text-align:center">❌ سوالی تولید نشد. پارامترها را تغییر دهید.</div>';
        return;
    }}
    
    let html = '<div class="glass-card" id="printArea"><h3>📋 سوالات تولید شده</h3>';
    
    for (let idx = 0; idx < questions.length; idx++) {{
        const q = questions[idx];
        html += '<div class="question-item" id="q-' + idx + '">';
        html += '<div class="question-text"><strong>' + (idx+1) + '.</strong> ' + escapeHtml(q.question) + '</div>';
        
        if (q.type === 'test' && q.options) {{
            html += '<div class="options">';
            for (let opt of q.options) {{
                html += '<label class="option"><input type="radio" name="q' + idx + '" value="' + escapeHtml(opt) + '"> ' + escapeHtml(opt) + '</label>';
            }}
            html += '</div>';
            html += '<button class="btn btn-warning" style="padding:8px 16px;font-size:0.8rem" onclick="checkAnswer(' + idx + ')">✅ بررسی پاسخ</button>';
            html += '<div class="show-answer" id="answer-' + idx + '"><strong>پاسخ صحیح:</strong> ' + escapeHtml(q.answer) + '<br><strong>توضیح:</strong> ' + escapeHtml(q.explanation || '-') + '</div>';
        }} else if (q.type === 'descriptive') {{
            html += '<textarea class="answer-input" id="descAnswer' + idx + '" rows="3" placeholder="پاسخ خود را بنویسید..."></textarea>';
            html += '<button class="btn btn-warning" style="padding:8px 16px;font-size:0.8rem" onclick="checkDescriptiveAnswer(' + idx + ')">✅ دیدن پاسخ پیشنهادی</button>';
            html += '<div class="show-answer" id="answer-' + idx + '"><strong>پاسخ پیشنهادی:</strong><br>' + escapeHtml(q.answer_template || 'پاسخی برای این سوال ثبت نشده است') + '</div>';
        }}
        
        html += '</div>';
    }}
    
    html += '<div style="display:flex;gap:15px;margin-top:20px;flex-wrap:wrap">';
    html += '<button class="btn btn-success" onclick="submitExam()">📊 ثبت پاسخ‌ها و مشاهده نمره</button>';
    html += '</div></div>';
    
    document.getElementById('questionsContainer').innerHTML = html;
}}

function escapeHtml(str) {{
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {{
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    }});
}}

function checkAnswer(idx) {{
    const div = document.getElementById('answer-' + idx);
    if (div.style.display === 'none' || div.style.display === '') {{
        div.style.display = 'block';
    }} else {{
        div.style.display = 'none';
    }}
}}

function checkDescriptiveAnswer(idx) {{
    const div = document.getElementById('answer-' + idx);
    if (div.style.display === 'none' || div.style.display === '') {{
        div.style.display = 'block';
    }} else {{
        div.style.display = 'none';
    }}
}}

async function submitExam() {{
    let score = 0;
    let total = currentQuestions.length;
    let answers = [];
    
    for (let i = 0; i < currentQuestions.length; i++) {{
        const q = currentQuestions[i];
        let userAnswer = '';
        let isCorrect = false;
        
        if (q.type === 'test') {{
            const selected = document.querySelector('input[name="q' + i + '"]:checked');
            userAnswer = selected ? selected.value : '(پاسخی انتخاب نشده)';
            isCorrect = (userAnswer === q.answer);
        }} else {{
            userAnswer = document.getElementById('descAnswer' + i).value || '(پاسخی نوشته نشده)';
            isCorrect = false;
        }}
        
        if (isCorrect) score++;
        answers.push({{
            question: q.question,
            userAnswer: userAnswer,
            correctAnswer: q.answer || q.answer_template,
            isCorrect: isCorrect
        }});
    }}
    
    const finalScore = Math.round((score / total) * 100);
    
    let resultHtml = '<div class="score-box"><div class="score-value">' + finalScore + '%</div>';
    resultHtml += '<div>از ' + total + ' سوال، ' + score + ' سوال صحیح</div></div>';
    resultHtml += '<div><h4>📊 جزئیات پاسخ‌ها:</h4>';
    
    for (let i = 0; i < answers.length; i++) {{
        const a = answers[i];
        resultHtml += '<div class="question-item"><strong>' + (i+1) + '.</strong> ' + escapeHtml(a.question) + '<br>';
        resultHtml += '<span style="color:#f59e0b">پاسخ شما:</span> ' + escapeHtml(a.userAnswer) + '<br>';
        resultHtml += '<span style="color:#10b981">پاسخ صحیح:</span> ' + escapeHtml(a.correctAnswer) + '<br>';
        resultHtml += '<span style="color:' + (a.isCorrect ? '#10b981' : '#ef4444') + '">' + (a.isCorrect ? '✓ صحیح' : '✗ نادرست') + '</span></div>';
    }}
    
    resultHtml += '</div><button class="btn btn-primary" onclick="location.reload()">🔄 آزمون جدید</button>';
    
    document.getElementById('resultContainer').style.display = 'block';
    document.getElementById('resultContainer').innerHTML = resultHtml;
    document.getElementById('questionsContainer').style.display = 'none';
    
    fetch('/save-exam-result', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{
            session_id: sessionId,
            subject: document.getElementById('subject').value,
            grade_level: document.getElementById('gradeLevel').value,
            questions_count: total,
            score: finalScore,
            answers: answers
        }})
    }});
}}

</script>
</body></html>"""


def render_daily_challenges_page(session_id):
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>چالش‌های روزانه - مسیرینو</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .container{{max-width:900px;margin:auto}}
  .glass-card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;margin-bottom:20px}}
  .header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:15px}}
  .title{{font-size:1.5rem;background:linear-gradient(135deg,#fff,#6c63ff);background-clip:text;-webkit-background-clip:text;color:transparent}}
  .level-selector{{display:flex;gap:10px}}
  .level-btn{{padding:8px 20px;border:none;border-radius:30px;cursor:pointer;background:rgba(255,255,255,0.1);transition:all 0.3s}}
  .level-btn.active{{background:linear-gradient(90deg,#6c63ff,#ff6584);color:white}}
  .points-summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin-bottom:25px}}
  .point-card{{background:rgba(0,0,0,0.2);border-radius:20px;padding:15px;text-align:center}}
  .point-value{{font-size:1.8rem;font-weight:bold;color:#ffc107}}
  .challenge-item{{background:rgba(0,0,0,0.2);border-radius:20px;padding:20px;margin-bottom:15px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}}
  .challenge-item.completed{{opacity:0.6}}
  .challenge-title{{font-size:1.1rem;font-weight:bold}}
  .challenge-points{{color:#ffc107}}
  .btn-complete{{background:#10b981;color:white;border:none;padding:10px 25px;border-radius:30px;cursor:pointer}}
  .btn-complete:disabled{{opacity:0.5}}
  .streak-box{{text-align:center;padding:15px;background:linear-gradient(90deg,#6c63ff,#ff6584);border-radius:20px;margin-top:20px}}
  .certificate-btn{{background:#8b5cf6;color:white;border:none;padding:12px 30px;border-radius:30px;cursor:pointer;margin-top:15px;width:100%}}
  .back-home{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  .new-badge{{background:#ff6584;padding:2px 8px;border-radius:20px;font-size:0.65rem;margin-right:10px}}
</style>
</head>
<body>
<div class="container">
  <div class="glass-card">
    <div class="header">
      <h1 class="title">🎯 چالش‌های روزانه</h1>
      <div class="level-selector">
        <button class="level-btn active" onclick="changeLevel('آسان')">😊 آسان</button>
        <button class="level-btn" onclick="changeLevel('متوسط')">🤔 متوسط</button>
        <button class="level-btn" onclick="changeLevel('سخت')">💪 سخت</button>
      </div>
    </div>
    
    <div class="points-summary">
      <div class="point-card"><div class="point-value" id="totalPoints">0</div><div>⭐ امتیاز کل</div></div>
      <div class="point-card"><div class="point-value" id="weeklyPoints">0</div><div>📅 این هفته</div></div>
      <div class="point-card"><div class="point-value" id="challengesCompleted">0</div><div>✅ انجام شده</div></div>
    </div>
    
    <div id="challengesList"></div>
    
    <div class="streak-box"><div>🔥 رکورد حضور روزانه</div><div class="point-value" id="streakDays">0 روز</div></div>
    
    <button class="certificate-btn" id="certificateBtn" onclick="getWeeklyCertificate()" style="display:none">🎓 دریافت گواهی تلاش هفتگی</button>
  </div>
  <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<script>
let sessionId = "{session_id}";
let currentLevel = "آسان";

async function loadChallenges() {{
    const res = await fetch('/get-challenges?session_id=' + sessionId + '&level=' + currentLevel);
    const data = await res.json();
    
    document.getElementById('totalPoints').innerText = data.total_points || 0;
    document.getElementById('weeklyPoints').innerText = data.weekly_points || 0;
    document.getElementById('challengesCompleted').innerText = data.completed_count || 0;
    document.getElementById('streakDays').innerText = (data.streak_days || 0) + ' روز';
    
    if (data.weekly_points >= 100) {{
        document.getElementById('certificateBtn').style.display = 'block';
    }} else {{
        document.getElementById('certificateBtn').style.display = 'none';
    }}
    
    let html = '';
    for (let i = 0; i < (data.challenges || []).length; i++) {{
        const ch = data.challenges[i];
        const completedClass = (ch.status === 'completed') ? 'completed' : '';
        const disabledAttr = (ch.status === 'completed') ? 'disabled' : '';
        const btnText = (ch.status === 'completed') ? '✅ انجام شد' : '✨ انجام دادم';
        const newBadge = ch.is_new ? '<span class=\"new-badge\">جدید</span>' : '';
        
        html += '<div class=\"challenge-item ' + completedClass + '\" id=\"challenge-' + ch.challenge_id + '\">';
        html += '<div><div class=\"challenge-title\">' + (ch.icon || '🎯') + ' ' + this.escapeHtml(ch.title) + newBadge + '</div>';
        html += '<div style=\"font-size:0.8rem;color:var(--muted)\">' + this.escapeHtml(ch.description) + '</div>';
        html += '<div style=\"font-size:0.7rem;color:var(--muted)\">📂 ' + (ch.category || 'عمومی') + ' | ⭐ ' + ch.points + ' امتیاز</div></div>';
        html += '<button class=\"btn-complete\" onclick=\"completeChallenge(\\'' + ch.challenge_id + '\\')\" ' + disabledAttr + '>' + btnText + '</button>';
        html += '</div>';
    }}
    
    if ((data.challenges || []).length === 0) {{
        html = '<div style=\"text-align:center;padding:40px\">✨ امروز همه چالش‌ها رو انجام دادی! فردا دوباره بیا ✨</div>';
    }}
    
    document.getElementById('challengesList').innerHTML = html;
}}

function escapeHtml(str) {{
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {{
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    }});
}}

async function completeChallenge(challengeId) {{
    const res = await fetch('/complete-challenge', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{
            session_id: sessionId,
            challenge_id: challengeId,
            level: currentLevel
        }})
    }});
    const data = await res.json();
    if (data.status === 'ok') {{
        alert('🎉 تبریک! ' + data.points + ' امتیاز گرفتی');
        loadChallenges();
    }} else {{
        alert('❌ خطا در ثبت انجام چالش');
    }}
}}

async function changeLevel(level) {{
    currentLevel = level;
    const btns = document.querySelectorAll('.level-btn');
    for (let i = 0; i < btns.length; i++) {{
        btns[i].classList.remove('active');
    }}
    event.target.classList.add('active');
    loadChallenges();
}}

async function getWeeklyCertificate() {{
    try {{
        const res = await fetch('/get-certificate', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{
                session_id: sessionId
            }})
        }});
        const data = await res.json();
        console.log('پاسخ سرور:', data);
        if (data.status === 'ok' && data.url) {{
            window.open(data.url, '_blank');
        }} else {{
            alert('❌ ' + (data.message || 'خطا در دریافت گواهی'));
        }}
    }} catch(e) {{
        console.error('Error:', e);
        alert('❌ خطا: ' + e.message);
    }}
}}

function toggleTheme() {{
    const html = document.documentElement;
    if (html.getAttribute('data-theme') === 'light') {{
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'dark');
    }} else {{
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }}
}}
if (localStorage.getItem('theme') === 'light') {{
    document.documentElement.setAttribute('data-theme', 'light');
}}

loadChallenges();
</script>
</body></html>"""


def render_educational_calendar_page(session_id):
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>تقویم آموزشی - مسیرینو</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:20px}}
  .container{{max-width:1200px;margin:auto}}
  .calendar-header{{background:var(--card);border-radius:28px;padding:20px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}}
  .month-nav{{display:flex;gap:15px;align-items:center}}
  .nav-btn{{background:rgba(108,99,255,0.3);border:none;padding:10px 20px;border-radius:30px;color:white;cursor:pointer}}
  .current-month{{font-size:1.5rem;font-weight:bold}}
  .calendar-grid{{background:var(--card);border-radius:28px;padding:20px;overflow-x:auto}}
  .weekdays{{display:grid;grid-template-columns:repeat(7,1fr);text-align:center;margin-bottom:10px}}
  .weekday{{padding:10px;font-weight:bold;color:var(--muted)}}
  .days-grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}}
  .day-cell{{background:rgba(0,0,0,0.2);border-radius:16px;padding:10px;min-height:100px;cursor:pointer;transition:all 0.3s}}
  .day-cell:hover{{transform:translateY(-2px);background:rgba(108,99,255,0.2)}}
  .day-cell.today{{border:2px solid #6c63ff}}
  .day-number{{font-weight:bold;margin-bottom:8px;font-size:1.1rem}}
  .event-indicator{{display:inline-block;width:8px;height:8px;border-radius:50%;margin:0 2px}}
  .event-indicator.exam{{background:#ef4444}}
  .event-indicator.holiday{{background:#10b981}}
  .event-indicator.study{{background:#3b82f6}}
  .event-indicator.challenge{{background:#f59e0b}}
  .event-indicator.goal{{background:#8b5cf6}}
  .sidebar{{margin-top:20px;display:grid;grid-template-columns:1fr 1fr;gap:20px}}
  .event-list{{background:var(--card);border-radius:28px;padding:20px}}
  .event-item{{padding:12px;border-bottom:1px solid rgba(255,255,255,0.1);display:flex;gap:10px;align-items:center}}
  .add-event-form{{background:var(--card);border-radius:28px;padding:20px}}
  .form-group{{margin-bottom:15px}}
  .form-group input,.form-group textarea{{width:100%;padding:10px;border-radius:16px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.2);color:var(--text)}}
  .btn{{padding:10px 20px;border:none;border-radius:30px;cursor:pointer;background:linear-gradient(90deg,#6c63ff,#ff6584);color:white}}
  .back-home{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  .stats{{display:flex;gap:15px;flex-wrap:wrap;margin-bottom:20px}}
  .stat-card{{background:rgba(0,0,0,0.2);padding:12px;border-radius:20px;flex:1;text-align:center}}
  @media(max-width:768px){{.sidebar{{grid-template-columns:1fr}}.days-grid{{gap:4px}}.day-cell{{min-height:70px;padding:5px}}}}
</style>
</head>
<body>
<div class="container">
  <div class="calendar-header">
    <button class="nav-btn" id="prevMonthBtn">◀ ماه قبل</button>
    <div class="current-month" id="currentMonth">در حال بارگذاری...</div>
    <button class="nav-btn" id="nextMonthBtn">ماه بعد ▶</button>
  </div>
  
  <div class="stats" id="stats"></div>
  
  <div class="calendar-grid">
    <div class="weekdays" id="weekdays"></div>
    <div class="days-grid" id="daysGrid"></div>
  </div>
  
  <div class="sidebar">
    <div class="event-list">
      <h3>📋 رویدادهای انتخاب شده</h3>
      <div id="selectedDateEvents">روزی را انتخاب کنید</div>
    </div>
    <div class="add-event-form">
      <h3>➕ افزودن رویداد شخصی</h3>
      <div class="form-group">
        <input type="text" id="eventTitle" placeholder="عنوان رویداد">
      </div>
      <div class="form-group">
        <input type="text" id="eventDate" placeholder="مثال: 1404/01/15">
      </div>
      <div class="form-group">
        <textarea id="eventDesc" rows="3" placeholder="توضیحات (اختیاری)"></textarea>
      </div>
      <button class="btn" id="addEventBtn">افزودن به تقویم</button>
    </div>
  </div>
  
  <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<script>
let sessionId = "{session_id}";
let currentYear = 1404;
let currentMonth = 1;
let currentEvents = [];
let weekdaysList = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"];
let monthNamesList = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"];

function toggleTheme() {{
    const html = document.documentElement;
    if (html.getAttribute('data-theme') === 'light') {{
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'dark');
    }} else {{
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }}
}}
if (localStorage.getItem('theme') === 'light') {{
    document.documentElement.setAttribute('data-theme', 'light');
}}

async function loadCalendar() {{
    try {{
        const res = await fetch('/get-calendar-data?session_id=' + sessionId + '&year=' + currentYear + '&month=' + currentMonth);
        const data = await res.json();
        currentEvents = data.events || [];
        
        document.getElementById('currentMonth').innerText = (data.month_name || monthNamesList[currentMonth-1]) + ' ' + data.year;
        
        // نمایش روزهای هفته
        let weekdaysHtml = '';
        for (let i = 0; i < weekdaysList.length; i++) {{
            weekdaysHtml += '<div class="weekday">' + weekdaysList[i] + '</div>';
        }}
        document.getElementById('weekdays').innerHTML = weekdaysHtml;
        
        const stats = data.summary || {{}};
        document.getElementById('stats').innerHTML = 
            '<div class="stat-card">📅 کل رویدادها: ' + (stats.total_events || 0) + '</div>' +
            '<div class="stat-card">📝 امتحانات: ' + (stats.exam_count || 0) + '</div>' +
            '<div class="stat-card">🎉 تعطیلات: ' + (stats.holiday_count || 0) + '</div>' +
            '<div class="stat-card">📖 برنامه مطالعه: ' + (stats.study_count || 0) + '</div>' +
            '<div class="stat-card">🏆 چالش‌ها: ' + (stats.challenge_count || 0) + '</div>' +
            '<div class="stat-card">🎯 اهداف: ' + (stats.goal_count || 0) + '</div>';
        
        renderCalendar(data);
    }} catch(e) {{
        console.error('خطا در بارگذاری:', e);
        document.getElementById('daysGrid').innerHTML = '<div style="text-align:center;padding:50px">❌ خطا در بارگذاری تقویم</div>';
    }}
}}

function renderCalendar(data) {{
    const firstWeekday = data.first_weekday || 0;
    const daysInMonth = data.month_days || 31;
    const today = data.current || {{}};
    
    let html = '';
    let dayCounter = 1;
    let totalCells = 42;
    
    for (let i = 0; i < totalCells; i++) {{
        if (i < firstWeekday || dayCounter > daysInMonth) {{
            html += '<div class="day-cell"></div>';
            continue;
        }}
        
        const dateStr = data.year + '-' + String(data.month).padStart(2,'0') + '-' + String(dayCounter).padStart(2,'0');
        const dayEvents = currentEvents.filter(function(e) {{ return e.date === dateStr; }});
        const isToday = (today.year === data.year && today.month === data.month && today.day === dayCounter);
        
        let eventIndicators = '';
        for (let j = 0; j < dayEvents.length; j++) {{
            const ev = dayEvents[j];
            let indicatorClass = '';
            if (ev.type === 'exam') indicatorClass = 'exam';
            else if (ev.type === 'holiday') indicatorClass = 'holiday';
            else if (ev.type === 'study_task') indicatorClass = 'study';
            else if (ev.type === 'challenge') indicatorClass = 'challenge';
            else if (ev.type === 'goal_deadline') indicatorClass = 'goal';
            if (indicatorClass) {{
                eventIndicators += '<span class="event-indicator ' + indicatorClass + '"></span>';
            }}
        }}
        
        let todayClass = isToday ? ' today' : '';
        html += '<div class="day-cell' + todayClass + '" data-date="' + dateStr + '" data-day="' + dayCounter + '">';
        html += '<div class="day-number">' + dayCounter + '</div>';
        html += '<div>' + eventIndicators + '</div>';
        html += '</div>';
        
        dayCounter++;
    }}
    
    document.getElementById('daysGrid').innerHTML = html;
    
    // اضافه کردن رویداد کلیک به خانه‌ها
    const cells = document.querySelectorAll('.day-cell');
    for (let i = 0; i < cells.length; i++) {{
        const cell = cells[i];
        const dateAttr = cell.getAttribute('data-date');
        if (dateAttr) {{
            cell.onclick = (function(date) {{
                return function() {{ showDayEvents(date); }};
            }})(dateAttr);
        }}
    }}
}}

function showDayEvents(dateStr) {{
    const dayEvents = currentEvents.filter(function(e) {{ return e.date === dateStr; }});
    let html = '<div style="padding:10px"><strong>📅 ' + dateStr + '</strong></div>';
    
    if (dayEvents.length === 0) {{
        html += '<div style="padding:10px;color:var(--muted)">هیچ رویدادی برای این روز وجود ندارد</div>';
    }} else {{
        for (let i = 0; i < dayEvents.length; i++) {{
            const ev = dayEvents[i];
            let color = '#6c63ff';
            if (ev.type === 'exam') color = '#ef4444';
            else if (ev.type === 'holiday') color = '#10b981';
            else if (ev.type === 'study_task') color = '#3b82f6';
            else if (ev.type === 'challenge') color = '#f59e0b';
            else if (ev.type === 'goal_deadline') color = '#8b5cf6';
            
            html += '<div class="event-item" style="border-right:3px solid ' + color + '">';
            html += '<div style="flex:1"><strong>' + ev.title + '</strong>';
            if (ev.description) html += '<div style="font-size:0.75rem;color:var(--muted)">' + ev.description + '</div>';
            html += '</div></div>';
        }}
    }}
    
    document.getElementById('selectedDateEvents').innerHTML = html;
}}

// دکمه‌های ناوبری
document.getElementById('prevMonthBtn').onclick = function() {{
    currentMonth--;
    if (currentMonth < 1) {{
        currentMonth = 12;
        currentYear--;
    }}
    loadCalendar();
}};

document.getElementById('nextMonthBtn').onclick = function() {{
    currentMonth++;
    if (currentMonth > 12) {{
        currentMonth = 1;
        currentYear++;
    }}
    loadCalendar();
}};

// دکمه افزودن رویداد
document.getElementById('addEventBtn').onclick = async function() {{
    const title = document.getElementById('eventTitle').value;
    const date = document.getElementById('eventDate').value;
    const desc = document.getElementById('eventDesc').value;
    
    if (!title || !date) {{
        alert('لطفاً عنوان و تاریخ رویداد را وارد کنید');
        return;
    }}
    
    let formattedDate = date.replace(/\\//g, '-');
    
    try {{
        const res = await fetch('/add-calendar-event', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{
                session_id: sessionId,
                title: title,
                date: formattedDate,
                description: desc
            }})
        }});
        const data = await res.json();
        if (data.status === 'ok') {{
            alert('✅ رویداد با موفقیت اضافه شد');
            document.getElementById('eventTitle').value = '';
            document.getElementById('eventDate').value = '';
            document.getElementById('eventDesc').value = '';
            loadCalendar();
        }} else {{
            alert('❌ خطا در افزودن رویداد');
        }}
    }} catch(e) {{
        alert('❌ خطا در ارتباط با سرور');
    }}
}};

// بارگذاری اولیه
loadCalendar();
</script>
</body></html>"""


def render_counselor_dashboard(session_id):
    """داشبورد مشاور - نمایش آمار و نمودارهای پیشرفته"""
    return f"""
<!doctype html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>داشبورد مشاور - مسیرینو</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
        body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
        :root {{ --bg: linear-gradient(135deg,#0f0c29,#302b63,#24243e); --card: rgba(255,255,255,0.08); --text: #fff; --muted: #c4c4f0; }}
        [data-theme="light"] {{ --bg: linear-gradient(135deg,#f5f7fa,#e4e8f0); --card: rgba(255,255,255,0.9); --text: #1a1a2e; --muted: #666; }}
        body {{ background: var(--bg); color: var(--text); padding: 30px; }}
        .container {{ max-width: 1400px; margin: auto; }}
        .glass-card {{ background: var(--card); backdrop-filter: blur(20px); border-radius: 28px; padding: 25px; margin-bottom: 20px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: rgba(0,0,0,0.2); border-radius: 20px; padding: 20px; text-align: center; }}
        .stat-number {{ font-size: 2rem; font-weight: bold; color: #6c63ff; }}
        .stat-label {{ font-size: 0.8rem; color: var(--muted); margin-top: 8px; }}
        .charts-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .chart-container {{ background: rgba(0,0,0,0.2); border-radius: 20px; padding: 20px; }}
        canvas {{ max-height: 300px; }}
        .students-table {{ overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: right; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ color: #6c63ff; }}
        .alert-item {{ padding: 12px; background: rgba(239,68,68,0.2); border-radius: 16px; margin: 8px 0; border-right: 3px solid #ef4444; }}
        .alert-warning {{ background: rgba(245,158,11,0.2); border-right-color: #f59e0b; }}
        .btn {{ padding: 8px 16px; border: none; border-radius: 20px; cursor: pointer; background: linear-gradient(90deg,#6c63ff,#ff6584); color: white; font-size: 0.8rem; }}
        .back-home {{ display: inline-block; margin-top: 20px; color: #6c63ff; text-decoration: none; }}
        .tab-buttons {{ display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
        .tab-btn {{ padding: 10px 20px; background: rgba(255,255,255,0.1); border: none; border-radius: 30px; cursor: pointer; }}
        .tab-btn.active {{ background: linear-gradient(90deg,#6c63ff,#ff6584); }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .risk-high {{ color: #ef4444; }}
        .risk-medium {{ color: #f59e0b; }}
        .risk-low {{ color: #10b981; }}
    </style>
</head>
<body>
<div class="container">
    <div class="glass-card">
        <h2>📊 داشبورد مشاور</h2>
        <p style="color:var(--muted); margin-bottom:20px">نمایش پیشرفت دانش‌آموزان، تحلیل ریسک و توصیه‌های هوشمند</p>
        
        <div class="tab-buttons">
            <button class="tab-btn active" onclick="showTab('overview')">📈 نمای کلی</button>
            <button class="tab-btn" onclick="showTab('students')">👥 دانش‌آموزان</button>
            <button class="tab-btn" onclick="showTab('alerts')">⚠️ هشدارها</button>
            <button class="tab-btn" onclick="showTab('recommendations')">💡 توصیه‌ها</button>
        </div>
        
        <div id="tab-overview" class="tab-content active">
            <div class="stats-grid" id="statsGrid"></div>
            <div class="charts-grid">
                <div class="chart-container">
                    <h4>📊 توزیع رشته‌های تحصیلی</h4>
                    <canvas id="trackChart"></canvas>
                </div>
                <div class="chart-container">
                    <h4>⚠️ سطح ریسک دانش‌آموزان</h4>
                    <canvas id="riskChart"></canvas>
                </div>
                <div class="chart-container">
                    <h4>📈 روند پیشرفت هفتگی</h4>
                    <canvas id="progressChart"></canvas>
                </div>
                <div class="chart-container">
                    <h4>🏆 امتیازات گروهی</h4>
                    <canvas id="pointsChart"></canvas>
                </div>
            </div>
        </div>
        
        <div id="tab-students" class="tab-content">
            <div class="students-table" id="studentsTable"></div>
        </div>
        
        <div id="tab-alerts" class="tab-content">
            <div id="alertsList"></div>
        </div>
        
        <div id="tab-recommendations" class="tab-content">
            <div id="recommendationsList"></div>
            <button class="btn" onclick="generateReport()" style="margin-top:20px">📥 خروجی گزارش (Excel/PDF)</button>
        </div>
    </div>
    <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<script>
var sessionId = "{session_id}";
var trackChart = null;
var riskChart = null;
var progressChart = null;
var pointsChart = null;

function toggleTheme() {{
    var html = document.documentElement;
    if (html.getAttribute('data-theme') === 'light') {{
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'dark');
    }} else {{
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }}
}}
if (localStorage.getItem('theme') === 'light') {{
    document.documentElement.setAttribute('data-theme', 'light');
}}

function showTab(tabName) {{
    var tabs = ['overview', 'students', 'alerts', 'recommendations'];
    for (var i = 0; i < tabs.length; i++) {{
        document.getElementById('tab-' + tabs[i]).classList.remove('active');
    }}
    document.getElementById('tab-' + tabName).classList.add('active');
    
    var btns = document.querySelectorAll('.tab-btn');
    for (var j = 0; j < btns.length; j++) {{
        btns[j].classList.remove('active');
    }}
    event.target.classList.add('active');
}}

function loadDashboard() {{
    fetch('/api/counselor/stats?session_id=' + sessionId)
        .then(function(res) {{ return res.json(); }})
        .then(function(data) {{
            // آمارها
            var statsHtml = '';
            var stats = [
                {{ label: '👥 کل دانش‌آموزان', value: data.total_students || 0 }},
                {{ label: '⚠️ در معرض خطر', value: data.high_risk_count || 0 }},
                {{ label: '📊 میانگین پیشرفت', value: (data.avg_progress || 0) + '%' }},
                {{ label: '🏆 گروه‌های فعال', value: data.active_groups || 0 }},
                {{ label: '✅ چالش‌های انجام شده', value: data.total_challenges || 0 }},
                {{ label: '⭐ میانگین امتیاز', value: data.avg_points || 0 }}
            ];
            for (var i = 0; i < stats.length; i++) {{
                statsHtml += '<div class="stat-card"><div class="stat-number">' + stats[i].value + '</div><div class="stat-label">' + stats[i].label + '</div></div>';
            }}
            document.getElementById('statsGrid').innerHTML = statsHtml;
            
            // نمودار رشته‌ها
            if (trackChart) trackChart.destroy();
            trackChart = new Chart(document.getElementById('trackChart'), {{
                type: 'pie',
                data: {{ labels: data.track_labels || [], datasets: [{{ data: data.track_data || [], backgroundColor: ['#6c63ff', '#ff6584', '#10b981', '#f59e0b'] }}] }},
                options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom', labels: {{ color: getComputedStyle(document.documentElement).getPropertyValue('--text') }} }} }} }}
            }});
            
            // نمودار ریسک
            if (riskChart) riskChart.destroy();
            riskChart = new Chart(document.getElementById('riskChart'), {{
                type: 'doughnut',
                data: {{ labels: ['ریسک بالا', 'ریسک متوسط', 'ریسک کم'], datasets: [{{ data: [data.high_risk || 0, data.medium_risk || 0, data.low_risk || 0], backgroundColor: ['#ef4444', '#f59e0b', '#10b981'] }}] }},
                options: {{ responsive: true }}
            }});
            
            // نمودار پیشرفت
            if (progressChart) progressChart.destroy();
            progressChart = new Chart(document.getElementById('progressChart'), {{
                type: 'line',
                data: {{ labels: data.progress_labels || ['هفته 1', 'هفته 2', 'هفته 3', 'هفته 4'], datasets: [{{ label: 'پیشرفت متوسط', data: data.progress_data || [0,0,0,0], borderColor: '#6c63ff', tension: 0.3 }}] }},
                options: {{ responsive: true }}
            }});
            
            // نمودار امتیازات گروهی
            if (pointsChart) pointsChart.destroy();
            pointsChart = new Chart(document.getElementById('pointsChart'), {{
                type: 'bar',
                data: {{ labels: data.group_names || [], datasets: [{{ label: 'امتیاز', data: data.group_points || [], backgroundColor: '#ff6584' }}] }},
                options: {{ responsive: true }}
            }});
        }})["catch"](function(err) {{ console.error(err); }});
    
    loadStudents();
    loadAlerts();
    loadRecommendations();
}}

function loadStudents() {{
    fetch('/api/counselor/students?session_id=' + sessionId)
        .then(function(res) {{ return res.json(); }})
        .then(function(data) {{
            var html = '<table><thead><tr><th>نام</th><th>پایه</th><th>رشته</th><th>پیشرفت</th><th>ریسک</th><th>امتیاز</th><th>عملیات</th></tr></thead><tbody>';
            for (var i = 0; i < (data.students || []).length; i++) {{
                var s = data.students[i];
                var riskClass = s.risk_level === 'high' ? 'risk-high' : (s.risk_level === 'medium' ? 'risk-medium' : 'risk-low');
                html += '<tr>' +
                    '<td>' + escapeHtml(s.name || s.user_code) + '</td>' +
                    '<td>' + (s.grade_level || '-') + '</td>' +
                    '<td>' + (s.track || '-') + '</td>' +
                    '<td><div style="background:rgba(255,255,255,0.2);border-radius:10px;width:100px"><div style="width:' + (s.progress || 0) + '%;background:#6c63ff;border-radius:10px;height:6px"></div></div> ' + (s.progress || 0) + '%</td>' +
                    '<td class="' + riskClass + '">' + (s.risk_percent || 0) + '%</td>' +
                    '<td>⭐ ' + (s.points || 0) + '</td>' +
                    '<td><button class="btn" onclick="viewStudent(\'' + s.user_id + '\')">مشاهده</button></td>' +
                '</tr>';
            }}
            html += '</tbody></table>';
            document.getElementById('studentsTable').innerHTML = html || '<p style="text-align:center;padding:40px">هنوز دانش‌آموزی ثبت نشده</p>';
        }})["catch"](function(err) {{ console.error(err); }});
}}

function loadAlerts() {{
    fetch('/api/counselor/alerts?session_id=' + sessionId)
        .then(function(res) {{ return res.json(); }})
        .then(function(data) {{
            var html = '';
            for (var i = 0; i < (data.alerts || []).length; i++) {{
                var a = data.alerts[i];
                var cls = a.level === 'danger' ? '' : 'alert-warning';
                html += '<div class="alert-item ' + cls + '"><strong>⚠️ ' + escapeHtml(a.title) + '</strong><br>' + escapeHtml(a.message) + '<br><small>' + a.date + '</small></div>';
            }}
            document.getElementById('alertsList').innerHTML = html || '<p style="text-align:center;padding:40px">هیچ هشداری وجود ندارد</p>';
        }})["catch"](function(err) {{ console.error(err); }});
}}

function loadRecommendations() {{
    fetch('/api/counselor/recommendations?session_id=' + sessionId)
        .then(function(res) {{ return res.json(); }})
        .then(function(data) {{
            var html = '<ul style="list-style:none">';
            for (var i = 0; i < (data.recommendations || []).length; i++) {{
                var r = data.recommendations[i];
                html += '<li style="padding:12px;background:rgba(0,0,0,0.2);border-radius:16px;margin:8px 0">💡 ' + escapeHtml(r) + '</li>';
            }}
            html += '</ul>';
            document.getElementById('recommendationsList').innerHTML = html || '<p style="text-align:center;padding:40px">توصیه‌ای موجود نیست</p>';
        }})["catch"](function(err) {{ console.error(err); }});
}}

function viewStudent(userId) {{
    window.location.href = '/student-report?session_id=' + sessionId + '&user_id=' + userId;
}}

function generateReport() {{
    fetch('/api/counselor/export-report?session_id=' + sessionId)
        .then(function(res) {{ return res.json(); }})
        .then(function(data) {{
            if (data.url) {{
                window.open(data.url, '_blank');
            }} else {{
                alert('گزارش در حال آماده‌سازی است...');
            }}
        }})["catch"](function(err) {{ console.error(err); }});
}}

function escapeHtml(text) {{
    if (!text) return '';
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}}

loadDashboard();
</script>
</body></html>
"""


def render_profile_page(session_id):
    from database import get_user_from_db
    user = get_user_from_db(session_id)
    user_code = user.get("user_code", session_id[:8]) if user else session_id[:8]
    first_name = user.get("name", "") if user else ""
    last_name = user.get("lastname", "") if user else ""
    grade_level = user.get("grade_level", "") if user else ""
    email = user.get("email", "") if user else ""
    
    # تعیین selected برای گزینه‌ها
    selected_basic = 'selected' if grade_level == "ابتدایی" else ''
    selected_seventh = 'selected' if grade_level == "هفتم-نهم" else ''
    selected_tenth = 'selected' if grade_level == "دهم-دوازدهم" else ''
    selected_univ = 'selected' if grade_level == "دانشگاه" else ''
    
    return f"""<!doctype html>
<html lang="fa" dir="rtl">
<head><meta charset="utf-8"><title>پروفایل من - مسیرینو</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
  body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{ font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important; }}
  :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
  [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
  body{{background:var(--bg);color:var(--text);padding:30px}}
  .container{{max-width:500px;margin:auto}}
  .glass-card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:30px}}
  .field{{margin-bottom:20px}}
  label{{display:block;margin-bottom:8px;color:var(--muted)}}
  input,select{{width:100%;padding:12px;border-radius:16px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.2);color:var(--text);outline:none}}
  button{{width:100%;padding:14px;border:none;border-radius:30px;background:linear-gradient(90deg,#6c63ff,#ff6584);color:white;font-weight:bold;cursor:pointer;transition:all 0.3s}}
  button:hover{{transform:translateY(-2px)}}
  .code-box{{background:rgba(108,99,255,0.2);padding:15px;border-radius:16px;text-align:center;margin-bottom:20px}}
  .back-home{{display:inline-block;margin-top:20px;color:#6c63ff;text-decoration:none}}
  .success-msg{{background:#10b981;padding:10px;border-radius:12px;margin-top:15px;text-align:center;display:none}}
  .info-box{{background:rgba(16,185,129,0.2);padding:12px;border-radius:16px;margin-bottom:20px;font-size:0.8rem;text-align:center}}
</style>
</head>
<body>
<div class="container">
  <div class="glass-card">
    <h2 style="text-align:center;margin-bottom:20px">👤 پروفایل من</h2>
    <div class="code-box">
      <span style="font-size:0.8rem">🆔 کد یکتا شما:</span><br>
      <strong style="font-size:1.2rem">{user_code}</strong>
      <button onclick="copyCode()" style="width:auto;padding:5px 15px;margin-top:10px;font-size:0.8rem">📋 کپی کد</button>
    </div>
    
    <div class="info-box">
      ✉️ با وارد کردن ایمیل، یادآوری برنامه مطالعه و اطلاع‌رسانی‌های مهم را دریافت خواهید کرد.
    </div>
    
    <div class="field">
      <label>نام</label>
      <input type="text" id="firstName" value="{first_name}" placeholder="نام خود را وارد کنید">
    </div>
    <div class="field">
      <label>نام خانوادگی</label>
      <input type="text" id="lastName" value="{last_name}" placeholder="نام خانوادگی">
    </div>
    <div class="field">
      <label>پایه تحصیلی</label>
      <select id="gradeLevel">
        <option value="">انتخاب کنید</option>
        <option value="ابتدایی" {selected_basic}>ابتدایی</option>
        <option value="هفتم-نهم" {selected_seventh}>هفتم-نهم</option>
        <option value="دهم-دوازدهم" {selected_tenth}>دهم-دوازدهم</option>
        <option value="دانشگاه" {selected_univ}>دانشگاه</option>
      </select>
    </div>
    <div class="field">
      <label>📧 ایمیل (برای دریافت اطلاع‌رسانی)</label>
      <input type="email" id="email" value="{email}" placeholder="example@gmail.com">
      <p style="font-size:0.7rem;color:#c4c4f0;margin-top:5px">ایمیل شما فقط برای ارسال یادآوری مطالعه استفاده می‌شود</p>
    </div>
    <button onclick="saveProfile()">💾 ذخیره تغییرات</button>
    <div id="status" class="success-msg"></div>
  </div>
  <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>
<script>
const sessionId = "{session_id}";
function saveProfile() {{
  const firstName = document.getElementById('firstName').value;
  const lastName = document.getElementById('lastName').value;
  const gradeLevel = document.getElementById('gradeLevel').value;
  const email = document.getElementById('email').value;
  
  fetch('/save-profile', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{
      session_id: sessionId,
      first_name: firstName,
      last_name: lastName,
      grade_level: gradeLevel,
      email: email
    }})
  }})
  .then(res => res.json())
  .then(data => {{
    if(data.status === 'ok') {{
      const statusDiv = document.getElementById('status');
      statusDiv.innerText = '✅ اطلاعات با موفقیت ذخیره شد';
      statusDiv.style.display = 'block';
      setTimeout(() => statusDiv.style.display = 'none', 3000);
    }} else {{
      alert('❌ خطا در ذخیره اطلاعات');
    }}
  }})
  .catch(err => {{
    alert('❌ خطا در ارتباط با سرور');
  }});
}}
function copyCode() {{
  navigator.clipboard.writeText("{user_code}");
  alert('✅ کد یکتا کپی شد: ' + "{user_code}");
}}
</script>
</body></html>"""