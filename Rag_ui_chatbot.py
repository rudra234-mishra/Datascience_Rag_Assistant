import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataScience RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Reset & root ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(99,102,241,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 90%, rgba(16,185,129,0.08) 0%, transparent 55%);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid rgba(99,102,241,0.25);
}
section[data-testid="stSidebar"] * { color: #c4c4d4 !important; }

/* ── Header block ── */
.rag-header {
    padding: 2rem 0 1.5rem;
    text-align: center;
}
.rag-header h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    background: linear-gradient(135deg, #818cf8 0%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -0.5px;
}
.rag-header p {
    color: #6b7280;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    margin-top: 0.4rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Chat container ── */
.chat-wrap {
    max-width: 780px;
    margin: 0 auto;
}

/* ── Message bubbles ── */
.msg-user, .msg-bot {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
    align-items: flex-start;
    animation: fadeUp 0.3s ease;
}
.msg-user { flex-direction: row-reverse; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.avatar-user { background: rgba(99,102,241,0.25); border: 1px solid rgba(99,102,241,0.5); }
.avatar-bot  { background: rgba(52,211,153,0.18); border: 1px solid rgba(52,211,153,0.4); }

.bubble {
    padding: 0.85rem 1.1rem;
    border-radius: 14px;
    font-size: 0.93rem;
    line-height: 1.65;
    max-width: 82%;
}
.bubble-user {
    background: rgba(99,102,241,0.18);
    border: 1px solid rgba(99,102,241,0.3);
    color: #e2e2f0;
    border-top-right-radius: 3px;
}
.bubble-bot {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    color: #d1d5db;
    border-top-left-radius: 3px;
}

/* ── Source chips ── */
.sources-wrap {
    margin-top: 0.6rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
}
.source-chip {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    padding: 2px 8px;
    border-radius: 20px;
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.3);
    color: #34d399;
    letter-spacing: 0.5px;
}

/* ── Status badge ── */
.status-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #34d399;
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    letter-spacing: 0.5px;
}
.dot { width: 6px; height: 6px; background: #34d399; border-radius: 50%;
       animation: pulse 2s infinite; }
@keyframes pulse {
    0%,100% { opacity:1; } 50% { opacity:0.3; }
}

/* ── Metric cards ── */
.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.metric-val {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #818cf8;
    line-height: 1;
}
.metric-label {
    font-size: 0.7rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.3rem;
}

/* ── Input override ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    border-radius: 10px !important;
    color: #e2e2f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.7) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pipeline_ready" not in st.session_state:
    st.session_state.pipeline_ready = False
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None
if "model" not in st.session_state:
    st.session_state.model = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "chunks_count" not in st.session_state:
    st.session_state.chunks_count = 0


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload Knowledge File",
        type=["txt", "md"],
        help="Upload a .txt or .md file to use as the knowledge base."
    )

    st.markdown("### Retrieval Settings")
    top_k = st.slider("Top-K Documents", min_value=1, max_value=10, value=5)
    search_type = st.selectbox("Search Strategy", ["mmr", "similarity", "similarity_score_threshold"])
    chunk_size = st.slider("Chunk Size", min_value=100, max_value=1000, value=250, step=50)
    chunk_overlap = st.slider("Chunk Overlap", min_value=0, max_value=100, value=10, step=5)

    st.markdown("---")
    init_btn = st.button("🚀 Initialize Pipeline", use_container_width=True)

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='font-family: Space Mono, monospace; font-size: 0.65rem; color: #4b5563; line-height: 1.8;'>
    STACK<br>
    · Azure OpenAI GPT<br>
    · Azure Embeddings<br>
    · ChromaDB VectorStore<br>
    · LangChain RAG Pipeline
    </div>
    """, unsafe_allow_html=True)


# ── Pipeline init logic ───────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def build_pipeline(file_bytes: bytes, file_name: str, _chunk_size: int, _chunk_overlap: int):
    import tempfile
    from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_chroma import Chroma

    # Write uploaded bytes to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file_name}") as f:
        f.write(file_bytes)
        tmp_path = f.name

    model = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("api_version"),
        azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    emd_model = AzureOpenAIEmbeddings(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("api_version"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    loader = TextLoader(tmp_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=_chunk_size, chunk_overlap=_chunk_overlap)
    chunks = splitter.split_documents(docs)
    vector_db = Chroma.from_documents(documents=chunks, embedding=emd_model, persist_directory="chroma.db")
    return model, vector_db, len(chunks)


if init_btn:
    if uploaded_file is None:
        st.sidebar.error("Please upload a knowledge file first.")
    else:
        with st.spinner("Building RAG pipeline…"):
            try:
                model, vector_db, n_chunks = build_pipeline(
                    uploaded_file.read(), uploaded_file.name, chunk_size, chunk_overlap
                )
                st.session_state.model = model
                st.session_state.vector_db = vector_db
                st.session_state.chunks_count = n_chunks
                st.session_state.retriever = vector_db.as_retriever(
                    search_type=search_type,
                    search_kwargs={"k": top_k}
                )
                st.session_state.pipeline_ready = True
                st.sidebar.success(f"Pipeline ready · {n_chunks} chunks indexed")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rag-header">
    <h1>🧠 DataScience RAG Assistant</h1>
    <p>Retrieval-Augmented Generation · Azure OpenAI · ChromaDB</p>
</div>
""", unsafe_allow_html=True)

# Status row
col1, col2, col3, col4 = st.columns(4)
with col1:
    status_html = (
        '<span class="status-badge"><span class="dot"></span>Pipeline Active</span>'
        if st.session_state.pipeline_ready
        else '<span class="status-badge" style="color:#6b7280;border-color:rgba(107,114,128,0.3);background:rgba(107,114,128,0.05);">⬤ Not Initialized</span>'
    )
    st.markdown(status_html, unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-val">{st.session_state.chunks_count}</div><div class="metric-label">Chunks</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-val">{st.session_state.total_queries}</div><div class="metric-label">Queries</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-val">{len(st.session_state.messages)}</div><div class="metric-label">Messages</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align:center; padding: 3rem 0; color: #374151;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>💬</div>
            <div style='font-family: Space Mono, monospace; font-size: 0.8rem; letter-spacing: 1px; text-transform: uppercase;'>
                Initialize the pipeline and start asking questions
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-user">
                    <div class="avatar avatar-user">👤</div>
                    <div class="bubble bubble-user">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)
            else:
                sources_html = ""
                if msg.get("sources"):
                    chips = "".join(
                        f'<span class="source-chip">CHUNK {i+1}</span>'
                        for i in range(len(msg["sources"]))
                    )
                    sources_html = f'<div class="sources-wrap">{chips}</div>'
                st.markdown(f"""
                <div class="msg-bot">
                    <div class="avatar avatar-bot">🤖</div>
                    <div>
                        <div class="bubble bubble-bot">{msg["content"]}</div>
                        {sources_html}
                    </div>
                </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Input row ─────────────────────────────────────────────────────────────────
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate(
    template="""You are a helpful assistant.
Give me the answer based on the following context.
If the context is insufficient, just say "I don't know".

Context: {context}

Question: {query}""",
    input_variables=["context", "query"]
)

input_col, btn_col = st.columns([6, 1])
with input_col:
    user_query = st.text_input(
        label="query",
        placeholder="Ask anything about your document…",
        label_visibility="collapsed",
        key="user_input"
    )
with btn_col:
    send = st.button("Send →", use_container_width=True)

if send and user_query:
    if not st.session_state.pipeline_ready:
        st.error("⚠️ Please initialize the pipeline first using the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.session_state.total_queries += 1

        with st.spinner("Retrieving & generating…"):
            try:
                ret_docs = st.session_state.retriever.invoke(user_query)
                context = "\n\n".join(d.page_content for d in ret_docs)
                final_prompt = prompt_template.invoke({"context": context, "query": user_query})
                answer = st.session_state.model.invoke(final_prompt).content
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": ret_docs
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ Error: {e}",
                    "sources": []
                })

        st.rerun()