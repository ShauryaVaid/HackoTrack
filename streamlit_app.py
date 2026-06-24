import streamlit as st
import requests
import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="HackoTrack",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    /* Global Background and Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', monospace; /* coding vibe */
    }
    
    /* Coding Vibe Matrix Grid Background */
    .stApp {
        background-color: #0a0e17;
        background-image: linear-gradient(rgba(110, 58, 255, 0.1) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(110, 58, 255, 0.1) 1px, transparent 1px);
        background-size: 30px 30px;
        background-position: center center;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Top Navigation Area */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF, #A0A0A0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .brand-subtitle {
        color: #A0A0A0;
        font-size: 1rem;
        font-weight: 400;
        margin-top: 0.2rem;
    }
    
    /* Glassmorphism Buttons */
    div[data-testid="stPopover"] > button, .stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stPopover"] > button:hover, .stButton > button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        color: #fff !important;
    }
    
    /* Primary Button override */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6E3AFF, #3B82F6) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(110, 58, 255, 0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7C4DFF, #4B90F6) !important;
        box-shadow: 0 6px 20px rgba(110, 58, 255, 0.4) !important;
    }
    
    /* Hackathon Cards */
    .card-container {
        background: rgba(20, 20, 20, 0.6);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        backdrop-filter: blur(12px);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .card-container:hover {
        transform: translateY(-5px);
        border-color: rgba(110, 58, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(110, 58, 255, 0.1);
    }
    
    /* Expanded Card */
    .card-expanded {
        background: rgba(30, 30, 30, 0.8);
        border: 1px solid rgba(110, 58, 255, 0.6);
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        transform: scale(1.02);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 16px;
    }
    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        line-height: 1.3;
    }
    .card-badge {
        background: rgba(110, 58, 255, 0.2);
        color: #B490FF;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(110, 58, 255, 0.3);
        white-space: nowrap;
    }
    
    .card-meta-list {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 16px;
    }
    .card-meta-item {
        display: flex;
        align-items: center;
        font-size: 0.85rem;
        color: #A0A0A0;
    }
    .card-meta-icon {
        margin-right: 6px;
        font-size: 1rem;
    }
    
    .card-desc {
        color: #D0D0D0;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 20px;
        flex-grow: 1;
    }
    
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 16px;
    }
    .tag {
        background: rgba(255, 255, 255, 0.05);
        color: #C0C0C0;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Expanded specifics */
    .expanded-section {
        margin-top: 24px;
        padding-top: 24px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    .expanded-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 12px;
    }
    .expanded-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 20px;
    }
    .expanded-kv {
        background: rgba(0,0,0,0.2);
        padding: 12px;
        border-radius: 8px;
    }
    .kv-label {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .kv-value {
        font-size: 0.95rem;
        color: #E0E0E0;
        font-weight: 500;
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stDateInput > div > div > input {
        background-color: rgba(20, 20, 20, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px !important;
        transition: all 0.3s !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #6E3AFF !important;
        box-shadow: 0 0 0 2px rgba(110, 58, 255, 0.2) !important;
    }
    
    /* Search Bar Specific */
    .search-container {
        position: sticky;
        top: 0;
        z-index: 100;
        background: rgba(14, 17, 23, 0.8);
        backdrop-filter: blur(12px);
        padding: 10px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

ADMIN_PASS = os.getenv("ADMIN_PASS", "HCKTRK26")

# State management
if 'expanded_card_id' not in st.session_state:
    st.session_state.expanded_card_id = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'trigger_confetti' not in st.session_state:
    st.session_state.trigger_confetti = False

def toggle_card(eid):
    if st.session_state.expanded_card_id == eid:
        st.session_state.expanded_card_id = None
    else:
        st.session_state.expanded_card_id = eid

# Fetch functions
@st.cache_data(ttl=5) # Cache data for 5 seconds
def load_all_hackathons():
    try:
        response = requests.get(f"{API_BASE_URL}/hackathons")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
        return []

def post_hackathon(data):
    try:
        response = requests.post(f"{API_BASE_URL}/hackathons", json=data)
        if response.status_code == 200:
            return True, response.json()
        return False, response.json()
    except Exception as e:
        return False, str(e)

def delete_hackathon(entry_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/hackathons/{entry_id}", headers={"X-Admin-Key": ADMIN_PASS})
        return response.status_code == 200
    except:
        return False

def update_hackathon(entry_id, data):
    try:
        response = requests.put(f"{API_BASE_URL}/hackathons/{entry_id}", json=data, headers={"X-Admin-Key": ADMIN_PASS})
        return response.status_code == 200
    except:
        return False

# --- HEADER SECTION ---
st.markdown("""
<div class="top-nav">
    <div>
        <h1 class="brand-title">HackoTrack</h1>
        <div class="brand-subtitle">Discover the next big build.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Layout Header Controls
col0, col1, col2 = st.columns([1, 7, 2])
with col0:
    with st.popover("⚙️ Admin"):
        if st.session_state.is_admin:
            st.success("Active")
            if st.button("Logout"):
                st.session_state.is_admin = False
                st.rerun()
        else:
            pwd = st.text_input("Key", type="password")
            if st.button("Login"):
                if pwd == ADMIN_PASS:
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Invalid")

with col1:
    search_query = st.text_input("🔍 Search Hackathons...", placeholder="Type to search by name, tech stack, location, tags...", label_visibility="collapsed")
    
with col2:
    with st.popover("✨ Post Hackathon", use_container_width=True):
        st.markdown("### Create New Post")
        with st.form("post_hackathon_form", border=False, clear_on_submit=True):
            h_name = st.text_input("Hackathon Name *")
            u_name = st.text_input("Your Name *")
            u_email = st.text_input("Your Email *")
            app_date = st.date_input("Application Deadline *", datetime.date.today())
            
            with st.expander("📝 Event Details"):
                desc = st.text_area("Description")
                org_comm = st.text_input("Organizer / Community")
                location = st.text_input("Location (City or Online)")
                venue_details = st.text_input("Venue Details")
                prize_pool = st.text_input("Prize Pool")
                team_size = st.text_input("Team Size")
                rules = st.text_area("Rules / Guidelines")
            
            with st.expander("🛠️ Tech & Timeline"):
                tags = st.text_input("Tags (comma separated)")
                tech_stack = st.text_input("Tech Stack (comma separated)")
                rough_start = st.text_input("Rough Start Month")
                tentative_date = st.date_input("Tentative Start Date", datetime.date.today())
                
            with st.expander("🔗 Social Links"):
                reg_link = st.text_input("Registration Link (URL)")
                l_url = st.text_input("LinkedIn URL")
                g_url = st.text_input("GitHub URL")
            
            submitted = st.form_submit_button("Launch 🚀", use_container_width=True, type="primary")
            
            if submitted:
                if not h_name or not u_name or not u_email:
                    st.error("Please fill in all required fields!")
                else:
                    payload = {
                        "hackathon_name": h_name,
                        "user_name": u_name,
                        "user_email": u_email,
                        "application_date": str(app_date),
                        "organizing_community": org_comm if org_comm else None,
                        "description": desc if desc else None,
                        "location": location if location else None,
                        "venue_details": venue_details if venue_details else None,
                        "prize_pool": prize_pool if prize_pool else None,
                        "team_size": team_size if team_size else None,
                        "rules": rules if rules else None,
                        "registration_link": reg_link if reg_link else None,
                        "tags": tags if tags else None,
                        "tech_stack": tech_stack if tech_stack else None,
                        "linkedin_url": l_url if l_url else None,
                        "github_url": g_url if g_url else None,
                        "rough_start_month": rough_start if rough_start else None,
                        "tentative_start_date": str(tentative_date) if tentative_date else None,
                        "created_at": str(datetime.datetime.now().isoformat())
                    }
                    with st.spinner("Publishing..."):
                        success, res = post_hackathon(payload)
                    if success:
                        st.toast("Hackathon posted successfully! 🚀", icon="✅")
                        st.session_state.trigger_confetti = True
                        st.cache_data.clear()
                    else:
                        st.error(f"Failed to post: {res}")


# --- DATA FETCHING & FILTERING ---
all_hackathons = load_all_hackathons()

filtered_hackathons = []
sq = search_query.lower()

if not all_hackathons:
    st.info("No hackathons found in the database. Be the first to post one!")
else:
    for h in all_hackathons:
        searchable_text = " ".join([
            str(h.get('hackathon_name') or ''),
            str(h.get('user_name') or ''),
            str(h.get('organizing_community') or ''),
            str(h.get('description') or ''),
            str(h.get('location') or ''),
            str(h.get('tags') or ''),
            str(h.get('tech_stack') or '')
        ]).lower()
        
        if sq in searchable_text:
            filtered_hackathons.append(h)

# --- RENDERING ---
if sq and not filtered_hackathons:
    st.warning("No results found for your search. Try different keywords.")
else:
    st.markdown(f"<p style='color: #888; font-size: 0.9rem; margin-bottom: 20px;'>Showing {len(filtered_hackathons)} hackathons</p>", unsafe_allow_html=True)
    
    # Sort newest first
    filtered_hackathons.reverse()
    
    # Grid layout: 2 columns
    for i in range(0, len(filtered_hackathons), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(filtered_hackathons):
                h = filtered_hackathons[i + j]
                eid = h.get('entry_id')
                is_expanded = st.session_state.expanded_card_id == eid
                
                with cols[j]:
                    card_class = "card-container card-expanded" if is_expanded else "card-container"
                    
                    # Safe gets to avoid NoneType issues
                    title = h.get('hackathon_name') or 'Unnamed Hackathon'
                    org = h.get('organizing_community') or h.get('user_name') or 'Unknown'
                    app_date = h.get('application_date') or 'TBA'
                    loc = h.get('location') or 'Online / TBA'
                    desc = h.get('description') or "Join this amazing hackathon and build something incredible!"
                    short_desc = desc[:120] + "..." if len(desc) > 120 else desc
                    
                    tags_html = ""
                    tags_raw = h.get('tags')
                    if tags_raw:
                        tag_list = [t.strip() for t in str(tags_raw).split(',')]
                        tags_html = "<div class='tag-container'>" + "".join([f"<span class='tag'>{t}</span>" for t in tag_list[:3]]) + "</div>"

                    # Construct HTML string without empty lines to prevent markdown paragraph breaks
                    html_content = f'<div class="{card_class}">'
                    html_content += f'<div class="card-header"><h3 class="card-title">{title}</h3><span class="card-badge">Ends {app_date}</span></div>'
                    html_content += f'<div class="card-meta-list"><div class="card-meta-item"><span class="card-meta-icon">🏢</span> {org}</div><div class="card-meta-item"><span class="card-meta-icon">📍</span> {loc}</div></div>'
                    html_content += tags_html
                    html_content += f'<div class="card-desc">{short_desc}</div>'
                    
                    if is_expanded:
                        # Full expanded view
                        prize = h.get('prize_pool') or 'TBA'
                        team = h.get('team_size') or 'TBA'
                        tech = h.get('tech_stack') or 'Open'
                        rules = h.get('rules') or 'See registration page'
                        venue = h.get('venue_details') or 'TBA'
                        start = h.get('tentative_start_date') or 'TBA'
                        link = h.get('registration_link') or '#'
                        l_url = h.get('linkedin_url') or ''
                        g_url = h.get('github_url') or ''
                        
                        rules_display = rules[:50] + ('...' if len(rules)>50 else '')
                        
                        html_content += '<div class="expanded-section">'
                        html_content += '<div class="expanded-title">Event Details</div>'
                        html_content += f'<p style="color: #ccc; font-size: 0.9rem; margin-bottom: 20px;">{desc}</p>'
                        html_content += '<div class="expanded-grid">'
                        html_content += f'<div class="expanded-kv"><div class="kv-label">Prize Pool</div><div class="kv-value">{prize}</div></div>'
                        html_content += f'<div class="expanded-kv"><div class="kv-label">Team Size</div><div class="kv-value">{team}</div></div>'
                        html_content += f'<div class="expanded-kv"><div class="kv-label">Tech Stack</div><div class="kv-value">{tech}</div></div>'
                        html_content += f'<div class="expanded-kv"><div class="kv-label">Start Date</div><div class="kv-value">{start}</div></div>'
                        html_content += '</div>'
                        html_content += '<div class="expanded-title">Logistics & Rules</div>'
                        html_content += '<div class="expanded-grid">'
                        html_content += f'<div class="expanded-kv"><div class="kv-label">Venue Details</div><div class="kv-value">{venue}</div></div>'
                        html_content += f'<div class="expanded-kv"><div class="kv-label">Rules</div><div class="kv-value">{rules_display}</div></div>'
                        html_content += '</div>'
                        html_content += '<div style="margin-top: 20px; display: flex; gap: 10px;">'
                        if link != '#':
                            html_content += f'<a href="{link}" target="_blank" style="background: #6E3AFF; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem;">Register Now</a>'
                        if l_url:
                            html_content += f'<a href="{l_url}" target="_blank" style="background: rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem;">LinkedIn</a>'
                        if g_url:
                            html_content += f'<a href="{g_url}" target="_blank" style="background: rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem;">GitHub</a>'
                        html_content += '</div></div>'
                    
                    html_content += "</div>"
                    st.markdown(html_content, unsafe_allow_html=True)
                    
                    # Admin Controls (visible immediately for Admins)
                    if st.session_state.is_admin:
                        st.markdown("<hr style='margin: 10px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
                        c_edit, c_del = st.columns(2)
                        with c_edit:
                            with st.popover("✏️ Edit", use_container_width=True):
                                with st.form(f"admin_form_{eid}"):
                                    st.markdown("#### Edit Details")
                                    edit_name = st.text_input("Name", value=h.get('hackathon_name') or '')
                                    edit_desc = st.text_area("Description", value=h.get('description') or '')
                                    edit_loc = st.text_input("Location", value=h.get('location') or '')
                                    edit_tags = st.text_input("Tags", value=h.get('tags') or '')
                                    
                                    if st.form_submit_button("💾 Save", type="primary", use_container_width=True):
                                        payload = {"hackathon_name": edit_name, "description": edit_desc, "location": edit_loc, "tags": edit_tags}
                                        if update_hackathon(eid, payload):
                                            st.toast("Updated Event!", icon="✅")
                                            st.cache_data.clear()
                                            st.rerun()
                                        else:
                                            st.error("Update Failed")
                        with c_del:
                            if st.button("🗑️ Delete", key=f"del_btn_{eid}", use_container_width=True):
                                if delete_hackathon(eid):
                                    st.toast("Deleted Event!", icon="🗑️")
                                    st.session_state.expanded_card_id = None
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error("Delete Failed")
                    
                    # Toggle button via callback
                    if is_expanded:
                        st.button("Close Details ▲", key=f"btn_close_{eid}", use_container_width=True, on_click=toggle_card, args=(eid,))
                    else:
                        st.button("View Details ▼", key=f"btn_open_{eid}", use_container_width=True, on_click=toggle_card, args=(eid,))

# --- DELIGHT & COMPANION SYSTEM ---
import streamlit.components.v1 as components

# Trigger confetti if needed
if st.session_state.trigger_confetti:
    components.html("""
    <script>
        const parentDoc = window.parent.document;
        if (parentDoc.window && parentDoc.window.triggerConfetti) {
            parentDoc.window.triggerConfetti();
        }
    </script>
    """, height=0, width=0)
    st.session_state.trigger_confetti = False

# Core engine injection
components.html("""
<script>
    const parentDoc = window.parent.document;
    
    // --- 1. MILESTONE DELIGHT SYSTEM (CONFETTI) ---
    if (!parentDoc.window) parentDoc.window = {};
    parentDoc.window.triggerConfetti = function() {
        if (!parentDoc.getElementById('confetti-script')) {
            const s = parentDoc.createElement('script');
            s.id = 'confetti-script';
            s.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js';
            s.onload = fireConfetti;
            parentDoc.head.appendChild(s);
        } else {
            fireConfetti();
        }
        
        function fireConfetti() {
            if (!window.confetti && !parentDoc.window.confetti) return;
            const conf = window.confetti || parentDoc.window.confetti;
            const duration = 3000;
            const end = Date.now() + duration;
            
            (function frame() {
                conf({ particleCount: 5, angle: 60, spread: 55, origin: { x: 0 }, colors: ['#6E3AFF', '#3B82F6', '#FFFFFF'], zIndex: 9998 });
                conf({ particleCount: 5, angle: 120, spread: 55, origin: { x: 1 }, colors: ['#6E3AFF', '#3B82F6', '#FFFFFF'], zIndex: 9998 });
                if (Date.now() < end) {
                    requestAnimationFrame(frame);
                }
            }());
        }
    };
</script>
""", height=0, width=0)
