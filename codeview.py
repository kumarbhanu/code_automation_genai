import streamlit as st

# Set wide layout
st.set_page_config(layout="wide", page_title="HTML Previewer")

# Sidebar
st.sidebar.title("Sidebar")
st.sidebar.markdown("Customize controls here...")

# Page title
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-family: sans-serif; margin-bottom: 2rem;'>
        Live HTML Output & Code Preview
    </h1>
""", unsafe_allow_html=True)

# Toggle to show/hide code
show_code = st.toggle("Show Code", value=True)

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

# If code is shown, use two columns
if show_code:
    col1, col2 = st.columns(2, gap="large")

    # Left: Output
    with col1:
        st.markdown("""
            <div style="
                background-color: #ffffff;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                border: 1px solid #e2e2e2;
                margin-bottom: 20px;
            ">
                <h3 style="margin-top: 0; color: #333; font-family: sans-serif;">HTML Output</h3>
        """, unsafe_allow_html=True)
        st.components.v1.html(html_content, height=350, scrolling=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Right: Code
    with col2:
        st.markdown("""
            <div style="
                background-color: #1e1e1e;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                border: 1px solid #333;
                margin-bottom: 20px;
            ">
                <h3 style="margin-top: 0; color: #90ee90; font-family: sans-serif;">HTML Code</h3>
        """, unsafe_allow_html=True)
        st.code(html_content, language='html')
        st.markdown("</div>", unsafe_allow_html=True)

# If code is hidden, output takes full width
else:
    st.markdown("""
        <div style="
            background-color: #ffffff;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 1px solid #e2e2e2;
            margin-bottom: 20px;
        ">
            <h3 style="margin-top: 0; color: #333; font-family: sans-serif;">HTML Output</h3>
    """, unsafe_allow_html=True)
    st.components.v1.html(html_content, height=400, scrolling=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr style="margin-top: 50px;">
    <p style="text-align:center; color: gray; font-size: 14px;">
        Built with Streamlit • Inspired by W3Schools & CodePen
    </p>
""", unsafe_allow_html=True)
