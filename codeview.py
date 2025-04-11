import streamlit as st

# Set page config
st.set_page_config(layout="wide", page_title="HTML Previewer")

# Sidebar
st.sidebar.title("Sidebar")
st.sidebar.markdown("Customize your view")

# Heading (with less bottom margin)
st.markdown("""
    <h2 style='text-align: center; color: #333; font-family: sans-serif; margin-bottom: 1rem;'>
        HTML Output & Code Preview
    </h2>
""", unsafe_allow_html=True)

# Toggle for Show/Hide Code
show_code = st.toggle("Show Code", value=True)

# HTML Content
html_content = """
<div style="padding: 20px; font-family: Arial;">
    <h1 style="color: teal;">Hello, World!</h1>
    <p>This is a beautiful HTML preview area. The styles are clean and modern.</p>
    <button style="padding: 10px 20px; background-color: teal; color: white; border: none; border-radius: 5px;">Click Me</button>
    <p style="margin-top: 20px;">Here is a long line of code to test horizontal scrolling:
    &lt;div style='display:flex; justify-content:space-between; width:100%'&gt;&lt;p&gt;Left&lt;/p&gt;&lt;p&gt;Right&lt;/p&gt;&lt;/div&gt;
    </p>
</div>
"""

# Layout with or without code
if show_code:
    col1, col2 = st.columns(2, gap="medium")

    # Output Card
    with col1:
        st.markdown("""
            <div style="
                background-color: #f0f8ff;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border: 1px solid #d0e4f7;
            ">
                <h4 style="margin-top: 0; font-family: sans-serif; color: #0a4d6b;">HTML Output</h4>
        """, unsafe_allow_html=True)
        st.components.v1.html(html_content, height=350, scrolling=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Code Card
    with col2:
        st.markdown("""
            <div style="
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                border: 1px solid #444;
            ">
                <h4 style="margin-top: 0; font-family: sans-serif; color: #90ee90;">HTML Code</h4>
        """, unsafe_allow_html=True)
        st.code(html_content, language="html")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid #d0e4f7;
        ">
            <h4 style="margin-top: 0; font-family: sans-serif; color: #0a4d6b;">HTML Output</h4>
    """, unsafe_allow_html=True)
    st.components.v1.html(html_content, height=400, scrolling=True)
    st.markdown("</div>", unsafe_allow_html=True)
