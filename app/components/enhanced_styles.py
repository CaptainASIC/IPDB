"""
Enhanced CSS styling for IP Address Tracker
Advanced dark mode theme with orange accents and micro-interactions
"""

def get_enhanced_css():
    """Return enhanced CSS with animations and micro-interactions"""
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Variables for consistent theming */
    :root {
        --primary-color: #FF6B35;
        --primary-hover: #FF8C42;
        --primary-light: #FFA500;
        --primary-dark: #E55A2B;
        --secondary-color: #FF8C42;
        --accent-color: #FFA500;
        --background-dark: #0F0F0F;
        --background-medium: #1A1A1A;
        --background-light: #2D2D2D;
        --background-card: #252525;
        --text-primary: #FFFFFF;
        --text-secondary: #CCCCCC;
        --text-muted: #999999;
        --border-color: #404040;
        --success-color: #00D084;
        --warning-color: #FFB800;
        --error-color: #FF4757;
        --shadow-light: rgba(255, 107, 53, 0.1);
        --shadow-medium: rgba(255, 107, 53, 0.2);
        --shadow-heavy: rgba(0, 0, 0, 0.3);
        --border-radius: 12px;
        --border-radius-small: 8px;
        --transition-fast: 0.2s ease;
        --transition-medium: 0.3s ease;
        --transition-slow: 0.5s ease;
    }
    
    /* Global Styles */
    * {
        box-sizing: border-box;
    }
    
    /* Hide Streamlit's default navigation menu */
    .css-1d391kg .css-1v0mbdj {
        display: none;
    }
    
    .css-1d391kg .css-1v0mbdj.e1fqkh3o1 {
        display: none;
    }
    
    /* Hide default page navigation */
    section[data-testid="stSidebar"] > div:first-child > div:first-child {
        display: none;
    }
    
    /* Alternative selectors for hiding default navigation */
    .css-1d391kg .css-1v0mbdj,
    .css-1d391kg .css-1v0mbdj.e1fqkh3o1,
    .css-1d391kg .css-1v0mbdj.e1fqkh3o2,
    .css-1d391kg .css-1v0mbdj.e1fqkh3o3 {
        display: none !important;
    }
    
    /* Hide any navigation list in sidebar */
    .css-1d391kg ul[role="listbox"],
    .css-1d391kg .css-1v0mbdj ul,
    .css-1d391kg nav,
    .css-1d391kg .css-1v0mbdj nav {
        display: none !important;
    }
    
    /* Hide Streamlit's automatic page navigation */
    .css-1d391kg .css-1v0mbdj.e1fqkh3o0 {
        display: none !important;
    }
    
    /* More robust selectors for hiding default navigation */
    [data-testid="stSidebar"] > div > div > div > div > ul,
    [data-testid="stSidebar"] > div > div > div > ul,
    [data-testid="stSidebar"] ul[role="listbox"],
    [data-testid="stSidebar"] nav,
    .css-1d391kg > div:first-child > div:first-child,
    .css-1d391kg > div:first-child > div:first-child > div,
    .css-1d391kg > div:first-child > div:first-child > div > div {
        display: none !important;
    }
    
    /* Hide any element that looks like default navigation */
    .css-1d391kg > div:first-child > div:first-child > div:first-child {
        display: none !important;
    }
    
    /* Target specific Streamlit navigation elements found in inspection */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavSeparator"] {
        display: none !important;
    }
    
    /* Hide the navigation list and links */
    ul[data-testid="stSidebarNavItems"],
    div[data-testid="stSidebarNavSeparator"],
    a[data-testid="stSidebarNavLink"] {
        display: none !important;
    }
    
    /* Additional selectors for the navigation container */
    .st-emotion-cache-1oe5cao,
    .eczjsme9,
    .st-emotion-cache-t2bj6i,
    .eczjsme8 {
        display: none !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--background-dark) 0%, var(--background-medium) 100%);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        line-height: 1.6;
    }
    
    /* Enhanced Header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 50%, var(--primary-light) 100%);
        padding: 2rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px var(--shadow-medium);
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.6s ease-out;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        margin: 1rem 0 0 0;
        font-size: 1.2rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced Cards and Containers */
    .metric-container {
        background: linear-gradient(135deg, var(--background-card) 0%, var(--background-light) 100%);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--primary-color);
        margin: 0.5rem 0;
        transition: all var(--transition-medium);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 16px var(--shadow-light);
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 107, 53, 0.1), transparent);
        transition: left var(--transition-slow);
    }
    
    .metric-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px var(--shadow-medium);
        border-left-color: var(--primary-hover);
    }
    
    .metric-container:hover::before {
        left: 100%;
    }
    
    .search-container, .nav-container {
        background: linear-gradient(135deg, var(--background-card) 0%, var(--background-light) 100%);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        transition: all var(--transition-medium);
        box-shadow: 0 2px 8px var(--shadow-light);
    }
    
    .search-container:hover, .nav-container:hover {
        border-color: var(--primary-color);
        box-shadow: 0 4px 16px var(--shadow-medium);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
        color: white;
        border: none;
        border-radius: var(--border-radius-small);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all var(--transition-fast);
        box-shadow: 0 4px 12px var(--shadow-light);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left var(--transition-medium);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-hover) 0%, var(--primary-light) 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px var(--shadow-medium);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px var(--shadow-light);
    }
    
    /* Enhanced Form Elements */
    .stSelectbox > div > div {
        background: var(--background-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-small);
        transition: all var(--transition-fast);
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px var(--shadow-light);
    }
    
    .stTextInput > div > div > input {
        background: var(--background-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-small);
        padding: 0.75rem;
        transition: all var(--transition-fast);
        font-size: 0.95rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px var(--shadow-light);
        outline: none;
    }
    
    .stTextArea > div > div > textarea {
        background: var(--background-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-small);
        transition: all var(--transition-fast);
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px var(--shadow-light);
        outline: none;
    }
    
    /* Enhanced Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--background-medium) 0%, var(--background-dark) 100%);
        border-right: 1px solid var(--border-color);
    }
    
    .css-1d391kg .stRadio > div {
        background: var(--background-card);
        border-radius: var(--border-radius-small);
        padding: 0.5rem;
        margin: 0.25rem 0;
        transition: all var(--transition-fast);
    }
    
    .css-1d391kg .stRadio > div:hover {
        background: var(--background-light);
        transform: translateX(4px);
    }
    
    /* Enhanced Tables */
    .dataframe {
        background: var(--background-card);
        color: var(--text-primary);
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: 0 4px 16px var(--shadow-light);
        border: 1px solid var(--border-color);
    }
    
    .dataframe thead th {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
        color: white;
        font-weight: 600;
        padding: 1rem;
        border: none;
    }
    
    .dataframe tbody tr {
        transition: all var(--transition-fast);
        border-bottom: 1px solid var(--border-color);
    }
    
    .dataframe tbody tr:hover {
        background: var(--background-light);
        transform: scale(1.01);
    }
    
    .dataframe tbody td {
        padding: 0.75rem 1rem;
        border: none;
    }
    
    /* Enhanced Status Indicators */
    .status-active {
        color: var(--success-color);
        font-weight: 600;
        position: relative;
    }
    
    .status-active::before {
        content: '●';
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    .status-inactive {
        color: var(--error-color);
        font-weight: 600;
    }
    
    .status-reserved {
        color: var(--warning-color);
        font-weight: 600;
    }
    
    /* Enhanced Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 208, 132, 0.1) 0%, rgba(0, 208, 132, 0.05) 100%);
        border: 1px solid var(--success-color);
        border-radius: var(--border-radius);
        color: var(--success-color);
        animation: slideInRight 0.4s ease-out;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 71, 87, 0.05) 100%);
        border: 1px solid var(--error-color);
        border-radius: var(--border-radius);
        color: var(--error-color);
        animation: shake 0.5s ease-in-out;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(255, 107, 53, 0.05) 100%);
        border: 1px solid var(--primary-color);
        border-radius: var(--border-radius);
        color: var(--primary-color);
        animation: slideInLeft 0.4s ease-out;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 184, 0, 0.1) 0%, rgba(255, 184, 0, 0.05) 100%);
        border: 1px solid var(--warning-color);
        border-radius: var(--border-radius);
        color: var(--warning-color);
        animation: bounce 0.6s ease-out;
    }
    
    /* Enhanced Expanders */
    .streamlit-expanderHeader {
        background: var(--background-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-small);
        transition: all var(--transition-fast);
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--background-light);
        border-color: var(--primary-color);
        transform: translateY(-1px);
    }
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--background-card);
        border-radius: var(--border-radius-small);
        padding: 0.25rem;
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: var(--border-radius-small);
        color: var(--text-secondary);
        transition: all var(--transition-fast);
        margin: 0 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--background-light);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
        color: white;
    }
    
    /* Loading Animations */
    .stSpinner > div {
        border-color: var(--primary-color) transparent var(--primary-color) transparent;
    }
    
    /* Custom Animations */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes shimmer {
        0% {
            transform: translateX(-100%);
        }
        100% {
            transform: translateX(100%);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    @keyframes shake {
        0%, 100% {
            transform: translateX(0);
        }
        25% {
            transform: translateX(-5px);
        }
        75% {
            transform: translateX(5px);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .metric-container {
            padding: 1rem;
        }
        
        .search-container, .nav-container {
            padding: 1rem;
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-medium);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--primary-hover) 0%, var(--primary-light) 100%);
    }
    
    /* Focus Indicators for Accessibility */
    *:focus {
        outline: 2px solid var(--primary-color);
        outline-offset: 2px;
    }
    
    /* Print Styles */
    @media print {
        .main-header {
            background: white;
            color: black;
        }
        
        .metric-container {
            border: 1px solid #ccc;
            background: white;
        }
    }
    </style>
    """

