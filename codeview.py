import streamlit as st

# Set wide layout
st.set_page_config(layout="wide", page_title="HTML Previewer")

# Sidebar
st.sidebar.title("Editor Options")
st.sidebar.markdown("Customize your layout or add controls here.")

# Page title
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-family: sans-serif;'>Live HTML Preview</h1>
""", unsafe_allow_html=True)

# Sample HTML content
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

# Two-column layout
left_col, right_col = st.columns(2, gap="large")

# Left: HTML Output
with left_col:
    st.markdown(
        """
        <div style="
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 20px;
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        ">
            <h3 style="color: #333;">HTML Output</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.components.v1.html(html_content, height=350, scrolling=True)

# Right: Code View with Syntax Highlighting
with right_col:
    st.markdown(
        """
        <div style="
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 20px;
            background-color: #1e1e1e;
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        ">
            <h3 style="color: #90ee90;">HTML Code</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code(html_content, language='html')

# Optional Footer
st.markdown("""
    <hr style="margin-top: 50px;">
    <p style="text-align:center; color: gray; font-size: 14px;">Created with Streamlit - Styled like W3Schools Preview</p>
""", unsafe_allow_html=True)
